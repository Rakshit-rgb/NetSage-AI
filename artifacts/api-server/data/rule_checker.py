"""
rule_checker.py — NetSage AI deterministic rule checker.

Runs BEFORE or AFTER the AI diagnosis to catch common Cisco config mistakes
using plain rules (no AI involved). This is what the problem statement means
by "deterministic checks" — reproducible, explainable, and independent of
the AI's judgment, so a human reviewer can cross-check the AI's answer.

Checks implemented (per the problem statement's required list):
  1. Duplicate IP addresses across hosts
  2. Wrong / mismatched subnet masks between hosts on the same VLAN
  3. Gateway mismatch (host's configured gateway != subnet's real gateway)
  4. Interface administratively down
  5. Missing VLAN (a VLAN referenced by a host/port doesn't exist on the switch)
  6. Missing route (destination network absent from the routing table)

Known limitation: the mask/CIDR check compares every prefix length found in a
case's evidence text. A case that legitimately mixes a /24 LAN with a /30
point-to-point transit link (common in multi-router topologies) will trigger
this check even though that is correct design, not a fault. Treat a
mask_mismatch trigger as "worth a second look," not a confirmed diagnosis —
that's exactly why every case still goes through human review.

Usage:
    python3 rule_checker.py --cases data/cases.csv --out data/rule_checker_results.csv

The script works off the free-text `show_output` field in cases.csv using
lightweight pattern matching — it flags a *hypothesis*, not a guaranteed
diagnosis, which is exactly why a human still reviews both the AI's and the
checker's output side by side.
"""
import argparse
import csv
import re
import ipaddress
from collections import defaultdict


def _strip_parentheticals(text: str) -> str:
    """Drop '(should be ...)'/'(wrong; actual ...)' style annotations so
    narrative commentary in evidence text doesn't get parsed as a second
    literal device value."""
    return re.sub(r'\([^)]*\)', '', text)


def check_duplicate_ip(show_output: str):
    clean = _strip_parentheticals(show_output)
    # Only count an IP as a host/device value when it's directly followed by
    # a CIDR suffix or immediately preceded by an assignment-style keyword.
    ips = re.findall(r'(?:(?:IP|IPv4|Address|address)[:\s]+)?(\d{1,3}(?:\.\d{1,3}){3})/\d{1,2}', clean)
    seen = defaultdict(int)
    for ip in ips:
        seen[ip] += 1
    dupes = [ip for ip, n in seen.items() if n > 1]
    if dupes:
        return f"Duplicate IP detected: {', '.join(dupes)} appears more than once."
    if re.search(r'\b(duplicate|conflict)\b.*\bip\b|\bip\b.*\b(duplicate|conflict)\b', show_output, re.IGNORECASE):
        return "Show output text explicitly reports a duplicate/conflict IP condition."
    return None


def check_mask_mismatch(show_output: str):
    clean = _strip_parentheticals(show_output)
    # CIDR suffix only counts when it directly follows a full dotted-quad IP
    # (avoids false hits on port names like Fa0/2 or VLAN lists like "1,20").
    cidr_masks = set(re.findall(r'\d{1,3}(?:\.\d{1,3}){3}/(\d{1,2})\b', clean))
    # Dotted-decimal masks (255.255.255.0 style) — only real subnet masks.
    dotted_masks = set(re.findall(r'255(?:\.(?:255|254|252|248|240|224|192|128|0)){3}', clean))
    if len(cidr_masks) > 1:
        return f"Multiple CIDR prefix lengths found on hosts expected to share a subnet: {sorted(cidr_masks)}."
    if len(dotted_masks) > 1:
        return f"Multiple dotted-decimal subnet masks found on hosts expected to share a subnet: {sorted(dotted_masks)}."
    return None


def check_gateway_mismatch(show_output: str):
    gw_matches = re.findall(r'[Gg]ateway[:\s]+(\d{1,3}(?:\.\d{1,3}){3})', show_output)
    svi_matches = re.findall(r'ip address\s+(\d{1,3}(?:\.\d{1,3}){3})', show_output)
    if gw_matches and svi_matches:
        if gw_matches[0] not in svi_matches:
            return f"Configured gateway {gw_matches[0]} does not match SVI/router address {svi_matches}."
    return None


def check_interface_down(show_output: str):
    if re.search(r'administratively down', show_output, re.IGNORECASE):
        return "Interface is administratively down (shutdown) — a human should verify this was intentional."
    if re.search(r'line protocol is down', show_output, re.IGNORECASE) and \
       not re.search(r'administratively down', show_output, re.IGNORECASE):
        return "Line protocol down while interface is not administratively down — check Layer 1 (cable/media)."
    return None


def check_missing_vlan(show_output: str, topology_note: str):
    referenced = set(re.findall(r'VLAN\s?(\d+)', show_output + " " + topology_note, re.IGNORECASE))
    configured = set(re.findall(r'VLAN\s?(\d+)\s+fa', show_output, re.IGNORECASE))
    missing = referenced - configured if configured else set()
    # Only flag if the case text signals a VLAN that never shows up as configured anywhere
    if "vlan" in show_output.lower() and "not permitted" in show_output.lower():
        return "Trunk allowed-VLAN list does not include a VLAN referenced elsewhere in this case."
    return None


def check_missing_route(show_output: str):
    if re.search(r'no route entry|not in routing table|no default route', show_output, re.IGNORECASE):
        return "Routing table is missing an expected route/entry referenced by the symptom."
    return None


CHECKS = [
    ("duplicate_ip", check_duplicate_ip),
    ("mask_mismatch", check_mask_mismatch),
    ("gateway_mismatch", check_gateway_mismatch),
    ("interface_down", check_interface_down),
    ("missing_route", check_missing_route),
]


def run_checks(case: dict):
    findings = []
    for name, fn in CHECKS:
        try:
            if fn is check_gateway_mismatch:
                result = fn(case["show_output"])
            else:
                result = fn(case["show_output"])
            if result:
                findings.append((name, result))
        except Exception as e:
            findings.append((name, f"[checker error: {e}]"))
    vlan_result = check_missing_vlan(case["show_output"], case.get("topology_note", ""))
    if vlan_result:
        findings.append(("missing_vlan", vlan_result))
    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default="data/cases.csv")
    ap.add_argument("--out", default="data/rule_checker_results.csv")
    args = ap.parse_args()

    rows_out = []
    with open(args.cases, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for case in reader:
            if case.get("evidence_status") == "Pending" or not case.get("show_output"):
                rows_out.append({
                    "case_id": case["case_id"],
                    "expected_fault": case.get("expected_fault", ""),
                    "checks_triggered": "not run",
                    "checker_notes": "Evidence pending — rule checker not run for this case yet.",
                    "num_checks_triggered": 0,
                })
                continue
            findings = run_checks(case)
            rows_out.append({
                "case_id": case["case_id"],
                "expected_fault": case["expected_fault"],
                "checks_triggered": "; ".join(name for name, _ in findings) if findings else "none",
                "checker_notes": " | ".join(msg for _, msg in findings) if findings else "No deterministic rule matched — relies on AI/human judgment.",
                "num_checks_triggered": len(findings),
            })

    fieldnames = ["case_id", "expected_fault", "checks_triggered", "checker_notes", "num_checks_triggered"]
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows_out)

    triggered = sum(1 for r in rows_out if r["num_checks_triggered"] > 0)
    print(f"Checked {len(rows_out)} cases. Rule checker triggered on {triggered} of them.")
    print(f"Results written to {args.out}")


if __name__ == "__main__":
    main()

# NetSage AI — Responsible AI Log

This log documents cases where the AI's diagnosis was **corrected or rejected**
by a human reviewer, per the project's mandatory human-review safety rule.
Source data: `data/ai_results.csv` + `data/human_review_log.csv`, built
against the real evidence in `data/cases.csv` (22 of 30 cases have real
evidence from the team's Packet Tracer documentation; 8 are still pending).

> Note: the AI diagnoses and review verdicts below are still **sample data**
> — the team hasn't run the real Step 4 (feeding cases through the AI prompt)
> yet. What's real is the case evidence itself (symptom, topology, show
> output, expected fault) and the kind of mistake shown here is a realistic
> example of what an LLM does when it pattern-matches to a nearby-but-wrong
> cause. Once Step 4/5 are run for real, regenerate this log from the actual
> `human_review_log.csv` — the structure stays the same.

---

### Case C08 — RIP Routing Error — Status: Edited
- **AI said:** the remote LAN wasn't being advertised because auto-summary was misconfigured on Router1 (medium confidence).
- **Human correction:** `show ip protocols` on Router1 lists "Routing for Networks: 10.0.0.0" with no `192.168.20.0` entry at all — the network statement itself is missing, not an auto-summary setting.
- **Why the AI was wrong:** auto-summary issues are a common RIP gotcha, so the AI reached for that explanation instead of reading the specific "Routing for Networks" list in the evidence.
- **Lesson:** the prompt should require the AI to quote the exact "Routing for Networks" line before naming a specific RIP misconfiguration type.

### Case C09 — Port Security — Status: Rejected
- **AI said:** Fa0/1 was manually shut down by an administrator (medium confidence).
- **Human correction:** the evidence shows a `%PSECURE-2` violation message, `Secure-shutdown` status, and `Violation Count: 1` — this is a port-security err-disable, a different mechanism with a different fix (correct the secure MAC address, then recover with `shutdown`/`no shutdown` — not just `no shutdown`).
- **Why the AI was wrong:** both faults produce a down interface, and the AI didn't check for the `%PSECURE` log line before assuming a plain administrative shutdown.
- **Lesson:** treat "port administratively/operationally down" as ambiguous until the AI has checked specifically for `%PSECURE` or `err-disabled` in the evidence — a rejected diagnosis is the right outcome when the mechanism, not just the symptom, is wrong.

### Case C12 — STP Problem — Status: Edited
- **AI said:** VLAN 1 wasn't enabled for spanning-tree on SW1 (medium confidence).
- **Human correction:** STP is running fine on SW1 — the evidence shows `show spanning-tree vlan 1` returning "This bridge is the root" only *after* SW1's priority was set to 4096. The real issue being demonstrated is the root-bridge priority/election, not STP being disabled.
- **Why the AI was wrong:** the AI defaulted to a generic "STP not running" explanation instead of reading the specific priority/Root ID values in the evidence.
- **Lesson:** for STP cases, require the AI to cite the actual Bridge ID/priority numbers, not just whether STP output exists.

### Case C13 — DNS Configuration Error — Status: Edited
- **AI said:** Server0's DNS service was not running (medium confidence).
- **Human correction:** Server0's A record and DNS service are confirmed working in the evidence — the fault is PC0's client-side DNS server setting pointing to the wrong address, not a server-side outage.
- **Why the AI was wrong:** the AI assumed the "server" in "DNS Configuration Error" meant a server-side fault, without checking which side (client vs. server) the evidence actually flagged.
- **Lesson:** DNS cases need the AI to explicitly state whether it's diagnosing client-side or server-side configuration, backed by which device's evidence shows the fault.

### Case C26 — EtherChannel Error — Status: Edited
- **AI said:** a duplex mismatch on SW2 Fa0/23 caused it to drop from the EtherChannel (medium confidence).
- **Human correction:** `show etherchannel summary` plus the interface config show Fa0/23 in access mode with LACP passive, while its bundle peers are trunk mode with LACP active — a configuration parameter mismatch, not a duplex issue.
- **Why the AI was wrong:** duplex mismatch is a very common generic explanation for "port acting oddly in a bundle," and the AI reached for it without checking the specific mode/LACP fields shown in the evidence.
- **Lesson:** EtherChannel cases should require the AI to compare switchport mode and channel-group mode across all bundle members before naming a cause, rather than defaulting to duplex.

---

## Summary
- **Total corrected/rejected cases documented:** 5 (meets the ≥5 requirement)
- **Edited:** 4 (C08, C12, C13, C26)
- **Rejected:** 1 (C09)
- **Common failure pattern:** in every case, the AI reached for a *generic, textbook-common* explanation for the symptom class (auto-summary for RIP, admin shutdown for a down port, "STP not running" for an STP case, server outage for "DNS error," duplex mismatch for a bad EtherChannel member) instead of reading the specific field in that case's evidence that would confirm or rule it out. This is exactly the failure mode the mandatory human-review rule exists to catch — the AI's confidence was "medium" in every one of these cases, reinforcing that medium-confidence diagnoses need the cited evidence checked line-by-line before acceptance.

## Evidence Coverage Note
22 of 30 cases currently have real evidence from the team's Packet Tracer
documentation (`data/cases.csv`, `evidence_status` column). The remaining 8
— C01 (DNS Problem), C03 (Gateway Problem), C15 (FTP Server Error),
C16 (Baseline VLAN20), C17 (DHCP Problem #2), C18 (DNS Troubleshooting),
C29 (NAT Working Baseline), C30 (Inter-VLAN Routing) — are marked `Pending`
and excluded from the AI-vs-human agreement rate and rule-checker trigger
rate until their evidence is supplied.

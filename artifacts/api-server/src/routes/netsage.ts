import { Router, type IRouter } from "express";
import { readFile } from "node:fs/promises";
import { resolve } from "node:path";

type CsvRecord = Record<string, string>;

const dataDir = resolve(import.meta.dirname, "../data");
let cachedCases: ReturnType<typeof buildCases> | undefined;

function parseCsv(text: string): CsvRecord[] {
  const rows: string[][] = [];
  let row: string[] = [];
  let cell = "";
  let quoted = false;

  for (let i = 0; i < text.length; i += 1) {
    const character = text[i];
    const next = text[i + 1];
    if (character === '"' && quoted && next === '"') {
      cell += '"';
      i += 1;
    } else if (character === '"') {
      quoted = !quoted;
    } else if (character === "," && !quoted) {
      row.push(cell);
      cell = "";
    } else if ((character === "\n" || character === "\r") && !quoted) {
      if (character === "\r" && next === "\n") i += 1;
      row.push(cell);
      if (row.some((value) => value.length > 0)) rows.push(row);
      row = [];
      cell = "";
    } else {
      cell += character;
    }
  }
  if (cell.length > 0 || row.length > 0) {
    row.push(cell);
    rows.push(row);
  }

  const headers = rows.shift() ?? [];
  return rows.map((values) =>
    headers.reduce<CsvRecord>((record, header, index) => {
      record[header] = values[index] ?? "";
      return record;
    }, {}),
  );
}

async function loadCsv(name: string) {
  return parseCsv(await readFile(resolve(dataDir, name), "utf8"));
}

function buildCases(
  sourceCases: CsvRecord[],
  aiResults: CsvRecord[],
  humanReviews: CsvRecord[],
  checkerResults: CsvRecord[],
) {
  const aiById = new Map(aiResults.map((row) => [row.case_id, row]));
  const reviewById = new Map(humanReviews.map((row) => [row.case_id, row]));
  const checkerById = new Map(checkerResults.map((row) => [row.case_id, row]));

  return sourceCases.map((row) => {
    const ai = aiById.get(row.case_id) ?? {};
    const review = reviewById.get(row.case_id) ?? {};
    const checker = checkerById.get(row.case_id) ?? {};
    return {
      caseId: row.case_id,
      pktFile: row.pkt_file,
      evidenceFile: row.evidence_file,
      evidenceStatus: row.evidence_status,
      symptom: row.symptom,
      topologyNote: row.topology_note,
      showOutput: row.show_output,
      expectedFault: row.expected_fault,
      osiLayer: row.osi_layer,
      conceptTag: row.concept_tag,
      severity: row.severity,
      aiRootCause: ai.ai_root_cause ?? "",
      aiConfidence: ai.ai_confidence ?? "",
      aiMatchesExpected: ai.ai_matches_expected ?? "",
      reviewStatus: review.review_status ?? "",
      reviewerNotes: review.reviewer_notes ?? "",
      checksTriggered: checker.checks_triggered ?? "",
      checkerNotes: checker.checker_notes ?? "",
      numChecksTriggered: Number(checker.num_checks_triggered ?? 0),
    };
  });
}

async function getCases() {
  if (cachedCases) return cachedCases;
  const [sourceCases, aiResults, humanReviews, checkerResults] =
    await Promise.all([
      loadCsv("cases.csv"),
      loadCsv("ai_results.csv"),
      loadCsv("human_review_log.csv"),
      loadCsv("rule_checker_results.csv"),
    ]);
  cachedCases = buildCases(
    sourceCases,
    aiResults,
    humanReviews,
    checkerResults,
  );
  return cachedCases;
}

function countsBy(cases: Awaited<ReturnType<typeof getCases>>, key: keyof (typeof cases)[number]) {
  const counts = new Map<string, number>();
  cases.forEach((item) => {
    const label = String(item[key] || "Unclassified");
    counts.set(label, (counts.get(label) ?? 0) + 1);
  });
  return [...counts.entries()]
    .map(([label, count]) => ({ label, count }))
    .sort((a, b) => b.count - a.count || a.label.localeCompare(b.label));
}

const router: IRouter = Router();

router.get("/netsage/cases", async (req, res, next) => {
  try {
    res.json(await getCases());
  } catch (error) {
    next(error);
  }
});

router.get("/netsage/cases/:caseId", async (req, res, next) => {
  try {
    const item = (await getCases()).find((row) => row.caseId === req.params.caseId);
    if (!item) {
      res.status(404).json({ message: "Case not found" });
      return;
    }
    res.json(item);
  } catch (error) {
    next(error);
  }
});

router.get("/netsage/overview", async (_req, res, next) => {
  try {
    const cases = await getCases();
    const reviewed = cases.filter((item) => item.aiMatchesExpected !== "pending");
    const agreements = reviewed.filter((item) => item.aiMatchesExpected === "yes");
    const checkerHits = cases.filter(
      (item) => item.numChecksTriggered > 0,
    ).length;

    res.json({
      totalCases: cases.length,
      evidenceComplete: cases.filter((item) => item.evidenceStatus === "Complete").length,
      pendingEvidence: cases.filter((item) => item.evidenceStatus === "Pending").length,
      highSeverity: cases.filter((item) => item.severity === "High").length,
      mediumSeverity: cases.filter((item) => item.severity === "Medium").length,
      aiReviewed: reviewed.length,
      agreementRate: reviewed.length ? (agreements.length / reviewed.length) * 100 : 0,
      accepted: cases.filter((item) => item.reviewStatus === "Accepted").length,
      edited: cases.filter((item) => item.reviewStatus === "Edited").length,
      rejected: cases.filter((item) => item.reviewStatus === "Rejected").length,
      ruleHits: checkerHits,
      conceptBreakdown: countsBy(cases, "conceptTag"),
      severityBreakdown: countsBy(cases, "severity"),
      reviewBreakdown: countsBy(cases, "reviewStatus"),
      checkerBreakdown: countsBy(
        cases.filter((item) => item.checksTriggered !== "not run"),
        "checksTriggered",
      ),
    });
  } catch (error) {
    next(error);
  }
});

export default router;
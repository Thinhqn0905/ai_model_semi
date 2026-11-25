# R4_CLAIMS — claim records for every number promoted to reports/final and NeedtoDo (evidence-integrity rule 4)
Account: .codex-B. Effort: medium.
Owner files: runs/claims.jsonl, reports/run4/claims_index.md
Read: AGENTS.md, .claude/rules/evidence-integrity.md, reports/final/report_run4.md, Instruction/NeedtoDo.md, reports/run3/*.md, reports/run4/*.md.
Contract: one JSON line per headline number in report_run4.md with fields claim_id, metric, value, unit, boundary, baseline, runs (Drive or
local path as written in the source report), profile, command (if stated), script, limitations. Do not recompute; copy from the reports.
claims_index.md: a table of claim_id -> report section. Flag numbers in report_run4.md that have no source in reports/ as NOT_VERIFIED.
Gate: jsonl loads; every claim has a boundary; index lists all claims.

# W8_TRACE — Mentor/reviewer traceability matrix + final report and slide skeleton   [M01-M16, deliverables XI]
Account: default. Effort: medium.
Owner files: docs/traceability.md, reports/final/report_draft.md, reports/final/slides_outline.md
Read: AGENTS.md, Instruction/Mentor_Feedback.md, Instruction/Project_Profile.md, docs/decisions.md, docs/ai_plan.md,
  docs/system_spec.md, and the report files under reports/ (data, audit, safety, economics, electrical, benchmark, ai, sensitivity,
  figures, product). Read result CSV headers only when a number is needed; every number cites its file and boundary label.
Contract:
- docs/traceability.md: table M01..M16 (mentor requirements as listed in Instruction/Mentor_Feedback.md, plus the user's WP list) ->
  work package -> evidence file(s) -> status (DONE / PARTIAL / OPEN) -> boundary label -> remaining gap. Include the reviewer
  "What to avoid" list with how each is avoided.
- reports/final/report_draft.md: structure = context, gap, D001 physics finding (why converter burn-in gives no shared-DC gain;
  storage/bidirectional cycling does), method (ledger, exact MILP oracle, rolling + AI, twin, replay), data (DS01-DS05 roles),
  results (oracle Go/No-Go, ladder, AI P vs P0 incl. negative results, sensitivity, failure injection, business case), limitations,
  roadmap (shadow -> pilot), water as separate workstream. Placeholders `[[PENDING: <file>]]` where results are still running —
  never invent numbers.
- reports/final/slides_outline.md: 12-15 slides mapped to figures F01-F15 (docs/figures.md) and the mentor pitch wording.
Gate: files exist; every numeric claim in them has a (file, boundary) citation; a `grep -c PENDING` count is reported in the final message.

## Run 2 (lead)
New evidence since run 1: docs/decisions.md D003; reports/ai/branch_C_ds05.md (+ results/ai_ds05_branchC); reports/economics/business_case_v1.md (alpha=1 base); reports/electrical/grounding.md; reports/safety/failure_injection.md. DS06 ladder (AI-EXP12) still running: keep [[PENDING: results/v2_ladder]]. Finish the citation review and set STATUS from the gate.

## Run 3 (lead)
Add D004 and reports/ai/ai_exp12_ds06.md (AI-EXP12 result: kill test passed on measured cycles, AI variants not better than P0 -> optimisation-only recommendation for energy; peak test pending results/v2_peak). Update traceability (M12, M14), report draft and slides outline accordingly.

## Run 3 (lead)
Add D005 + peak-aware + CQR + bus stability KPI to traceability (M06, M11, M12, M14) and report draft; replace the remaining PENDING markers where the evidence now exists.

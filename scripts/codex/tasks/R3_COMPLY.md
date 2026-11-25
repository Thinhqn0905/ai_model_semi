# R3_COMPLY — Run 3 mentor compliance audit M01-M16 (draft now, final after the lead's last campaigns)
Account: .codex-B. Effort: medium.
Owner files: reports/run3/mentor_compliance_audit.md, runs/run3/comply/**
Read: AGENTS.md, Instruction/Mentor_Feedback.md (authoritative mentor text), docs/traceability.md, docs/decisions.md, docs/run3_plan.md,
  reports/run3/*.md (root_cause_analysis, metric_audit_v3, economics_v3, cross_dataset_benchmark, electrical_feasibility,
  failure_injection_v2, demonstrator), reports/ai/*.md, reports/safety/*.md, reports/economics/*.md, reports/benchmark/*.md.
  Do not edit any other file. Do not run campaigns or training.
Contract:
1. One section per requirement M01..M16 with: original mentor quotation (exact words from Instruction/Mentor_Feedback.md with its
   section/line), implemented module (file path), supporting experiment, evidence file (path), result (number + boundary label),
   remaining limitation, status PASS / PARTIAL / FAIL / BLOCKED.
2. Rules: an experiment that ran is not a PASS by itself; PASS only when the evidence answers the requirement at the stated
   boundary. Distinguish CONCEPT-LEVEL (simulation/benchmark) from SITE validation; nothing is site-validated (no shadow-mode
   data) -> say so for M05/M08. M12 must follow the AI-necessity rule (AI adopted only if P beats P0 with a paired CI excluding 0).
   Evidence still pending (Colab runs in progress: PQ/PQ*, E1 limits) -> status BLOCKED or PARTIAL with "pending: <file>".
3. Summary table + counts per status recalculated from the evidence (do not inherit the earlier 8/4/4).
4. A short list of the 5 most important open items with the owner (lead / user / mentor) and what evidence would close them.
Gate: the file has 16 requirement sections, every PASS cites an existing evidence file (check the paths exist and write the check
output to runs/run3/comply/path_check.txt), and a counts table.

## Run 2 (lead) — use THESE requirement IDs (user's Run 3 plan; internal decomposition, not the competition rubric)
M01 position as intelligent energy coordination, not an AI scheduler. M02 one compatible high-power long-duration test cell.
M03 scheduling flexibility + incremental grid kWh = first Go/No-Go gate. M04 converter losses + consistent energy accounting.
M05 offline simulation -> read-only shadow -> Go/No-Go -> protected pilot. M06 bus stability, independent protection, FMEA,
vendor compatibility. M07 synthetic profiles grounded in datasheets/vendor specs/measured data. M08 data priority: time-aligned
station power, movable start windows, efficiency curves, cell AC import/export, quality records. M09 strong baselines + perfect
Oracle. M10 incremental grid kWh vs existing regeneration = primary KPI. M11 FPY/throughput/test integrity hard constraints.
M12 AI incremental benefit over matched non-AI optimisation. M13 sensitivity + paired statistics. M14 AI predicts power/duration/
uncertainty; constrained optimizer decides. M15 electricity first; water needs separate evidence. M16 savings must justify
investment/payback. Map each to the closest mentor quotation in Instruction/Mentor_Feedback.md (quote + location); if your
draft used another numbering, renumber it. Note: the NaN fallback FAIL is fixed by the lead (ai_engine.py non-finite -> recipe);
check reports/run3/failure_injection_v2.md for the rerun result before grading.

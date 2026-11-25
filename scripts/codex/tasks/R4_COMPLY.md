# R4_COMPLY — Run 4 mentor compliance audit M01-M16 (draft now; lead triggers the final pass)
Account: default. Effort: medium.
Owner files: reports/run4/mentor_compliance_run4.md, runs/run4/comply/**
Read: AGENTS.md, Instruction/Mentor_Feedback.md, scripts/codex/tasks/R3_COMPLY.md (M01-M16 definitions), docs/decisions.md (D001-D017),
  reports/run3/mentor_compliance_audit.md, reports/run3/*.md, reports/run4/*.md, reports/final/report_run4.md.
Contract: same format as the Run 3 audit (quote + location, module, experiment, evidence path, result + boundary, limitation, status),
recalculated from Run 4 evidence; distinguish concept-level vs site validation; gates G01-G12 table; counts per status; 5 key open items.
Mark items depending on running Colab jobs (P0-BILL, AI-BILL, multi-cell FIN-B, sizing, TCN) as PENDING with the expected file.
Gate: 16 sections + G01-G12 table; every PASS cites an existing file (path check in runs/run4/comply/path_check.txt).

## Run 2 (lead)
Refresh now with: verified TNB tariffs (data/tariffs, reports/run4/tariff_registry.md), factory-clustered CIs and multi-cell results (reports/run4/facility_billing.md), FIN-B break-even verdict (reports/run4/economics_run4.md), AFE sizing + default engine n=100 (reports/run3/e1_electrical_constraints.md), TCN (reports/run4/ai_eta.md), D017. P0-BILL extension and AI-BILL remain PENDING (reports/run4/facility_billing.md). Return ALL_PASS when the gate passes.

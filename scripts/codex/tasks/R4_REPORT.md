# R4_REPORT — Run 4 integrated technical report (md) + traceability + system spec update (no slides)
Account: default. Effort: medium.
Owner files: reports/final/report_run4.md, docs/traceability.md, docs/system_spec.md (append a "Run 4" section only), Instruction/NeedtoDo.md
Read: AGENTS.md, docs/decisions.md (D001-D016), docs/run3_plan.md, reports/run3/*.md, reports/run4/*.md, reports/final/qa_backup_run4.md.
Do not change numbers; copy them with their boundary label and source file. Do not edit other files.
Contract:
1. report_run4.md: executive summary (what is proven at which boundary, what is not), reference cell (D007), physics/kill test, P0-E1-Peak
   engine, information-value decomposition, AI results (ETA PASS as accuracy; WP-C downstream FAIL; energy AI FAIL), electrical feasibility
   (E1 + twin), facility-level billing (DS07, TNB peak-period rule), economics (DS06 FIN-A/B/C; facility-level pending), contribution
   decomposition (D016), gates G01-G12 table with PASS/PARTIAL/FAIL/BLOCKED and evidence path, open items and data requests.
2. traceability.md: add Run 3/Run 4 evidence rows for M01-M16 (file paths), keep existing rows.
3. system_spec.md: append "Run 4" section: P0-BILL billing level, E1 parameters, facility simulation boundary, tariff registry, AI paths A/B/C.
4. NeedtoDo.md: rewrite the open list from the reports (keep "Done" history short).
Gate: files exist; every number in report_run4.md has a source path; a gates table with 12 rows.

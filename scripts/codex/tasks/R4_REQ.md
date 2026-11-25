# R4_REQ — Run 4 mentor data-request matrix + contribution decomposition (D016) + Q&A update (md only, no slides)
Account: default. Effort: medium.
Owner files: reports/run4/mentor_data_request.md, reports/run4/contribution_decomposition.md, reports/final/qa_backup_run4.md
Read: AGENTS.md, Instruction/Mentor_Feedback.md, docs/decisions.md (D006-D016), reports/run3/*.md, reports/run4/*.md,
  reports/final/qa_backup.md. Do not run campaigns; do not edit other files. Do not send anything externally.
Contract:
1. mentor_data_request.md: matrix of what public data cannot replace (target-cell topology, synchronised station + facility meters,
   movable start windows, converter curves of the actual equipment, site tariff + contract, integration/requalification cost, vendor
   API permissions, FPY/quality records, shadow-mode access): item, why needed (which gate G01-G12 / M-ID), minimum format/resolution,
   duration, who owns it, what decision it unblocks.
2. contribution_decomposition.md (D016): table hardware (B0->B1), topology (B1p-OPT->B2, B1p-OPT->B3), conventional scheduling
   (B2->B3), rolling (B3->P0), peak/E1 (P0->P0-E1-Peak), AI energy (P0->best AI), AI production (TT), facility billing (B2->P0-E1-Peak
   MD increment) with values + CIs + boundary copied from the reports (cite file); state explicitly that the 11.6 % shared-link figure
   is topology + optimisation, not AI or software-only.
3. qa_backup_run4.md: 20 hardest judge questions with evidence-based answers (Vietnamese + English), including "why is AI not in the
   loop", "is this just battery testing", "what does Chroma already do", "why only 2 kW of billed demand", "payback".
Gate: three files exist; every number cites a report file path; no number without a boundary label.

## Run 2 (lead)
Use the numbers that already have CIs in reports/run3/root_cause_analysis.md, ai_run3.md, e1_electrical_constraints.md, reports/ai/ai_exp12_ds06.md (Run 2 ladder table: B0->B1 57.49 [55.61,59.41], B1->B2 2.84 [2.73,2.95], B2->B3 0.218 [0.189,0.248], B3->P0 0.018 [0.009,0.028], B1p-OPT->ORACLE 1.094 [1.037,1.148]), reports/run4/facility_billing.md (TNB section), reports/run4/ai_production_planning.md. Mark NOT_VERIFIED only what truly has no CI in those files. Complete all three files now; return ALL_PASS when the gate passes.

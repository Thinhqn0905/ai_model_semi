# NeedtoDo (living list — updated 2026-11-25 morning by lead)

## Done overnight (evidence in reports/, decisions D001-D005)
- Kill test explained (D001) and passed for the right cell type: S3 storage / bidirectional cycling. DS06 measured cycles:
  ORACLE -11.6 % vs optimised in-rack (n=100), -13.3 % at full flexibility; peak -20 % (P0) / -23 % (P0 + peak level).
- Converter burn-in (S1/S2): shared DC == in-rack exactly -> NO-GO for that cell type (sensitivity: 0 in every sweep).
- AI: forecasters beat the recipe baseline on measured DS05 (skill 0.3-0.7, duration MAE 87 vs 261 min, CQR coverage 0.79-0.86)
  but do NOT improve grid kWh or peak downstream (AI-EXP12, n=100/50) -> P0 + peak-aware optimizer recommended (D005).
- Business case (alpha=1 behind the meter): energy alone does not pay back; needs a demand charge (peak) -> FIN-B best case.
- Twin: AFE 20 kW / link 80 A of the old deck are undersized for an 8-station cell; coordinated plans pass more often.
- Deliverables: reports/final/ReGenATE_final.pptx (19 slides), qa_backup.md, report_draft.md, docs/traceability.md, figures,
  dashboard (streamlit run app/dashboard.py), README + docs/runbook.md, GitHub ai_model_semi.

## Open (needs the user)
- [ ] Confirm target cell = storage / bidirectional power-module cycling (D001/D003). Converter burn-in is a NO-GO for shared DC.
- [ ] Review the deck wording and the honest AI result (slides 10-13) before sending to the mentor.
- [ ] Colab GH_TOKEN is read-only for ai_model_semi (push 403); results reach the repo via local push.
- [ ] Site data request list for the mentor (per-station traces, start windows, converter curves, tariff with demand charge).
- [ ] Optional: larger n at flex 1.0 (stopped at 26), cycle_scale=2 sweep point (generator limit), F01/F02/F11 need DS05 prediction rows.

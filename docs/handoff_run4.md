# Run 4 hand-off (lead, 2026-11-25) — what is still running and how to integrate it

## Running autonomously on Colab (results land on Google Drive `MyDrive/semiexpo/ai_runs/`)
| Runtime | Job | Output when done |
|---|---|---|
| 1 (8 CPU + T4, notebook semiexpo_ai.ipynb cells 83, 86) | facility-load forecaster training (`forecasting/facility_load.py`) -> AI-BILL vs P0-BILL(hist/oracle) on test months 2019-08/09, 6 factories, 1 cell, ToU rule -> figure generator | `run4_final_summary.md` (tables with factory-clustered CIs + forecaster metrics + figure log), `run4/fac_aibill_*`, `run4/facility_load/`, `run4/figures/` |
| 3 (2 CPU) | twin screening of the AFE sizing schedules (15/32 and 20/16 still running; 10/32, 30/32 done) | `run4_rt3/screen_sizing_summary.csv` |
| 2 | idle (done: 100-pool grids, holiday sensitivity) | `run4_rt2/` |
Decision rule for AI-BILL (D017.1): adopt only if P0-BILL:ai beats P0-BILL:hist AND P0-E1-Peak with a factory-clustered CI excluding 0. Note
that P0-BILL:oracle did not beat P0-E1-Peak (reports/run4/facility_billing.md), so a positive AI-BILL outcome is not expected.

## How to integrate (whoever continues)
1. Download `run4_final_summary.md` and `run4_rt3/screen_sizing_summary.csv` from Drive into `runs/run4/` (gitignored).
2. Add the AI-BILL table to reports/run4/facility_billing.md (section "AI-BILL") and the approval-by-AFE table to
   reports/run3/e1_electrical_constraints.md (section "sizing twin screening"); partial result already known: AFE 10 kW -> B2 10 %,
   P0 66.7 %, ORACLE 100 % approved; AFE 30 kW -> all 100 %.
3. Copy figures from Drive `run4/figures/` to `reports/run4/figures/` and update reports/run4/figures/INDEX.md.
4. Re-run the compliance audit (scripts/codex/tasks/R4_COMPLY.md) and report update (R4_REPORT2.md).

## Status of the evidence (see reports/run4/*.md)
Done: verified TNB tariffs (PDF p.2), factory-clustered CIs, multi-cell 1/3/5/10, FIN-B break-even verdict, default engine n=100, AFE sizing
(MILP), TCN (not justified), WP-C/monitoring FAIL (stopped per D017), P0-BILL (no gain), holiday sensitivity, 100-pool robustness.

# NeedtoDo (living list — updated 2026-11-25 by lead, Run 3 in progress; md deliverables only, no slides)

Run 3 plan: `docs/run3_plan.md`. Heavy compute runs on Colab only (user machine is weak): `semiexpo_ai.ipynb` cells 26-39,
outputs Drive `MyDrive/semiexpo/ai_runs/run3/`.

## Run 3 findings so far (evidence in reports/run3/)
- Reproducibility: local DS05 rebuild = Colab (14,755 cycles, 2 errors); DS06 P0/B1p-OPT/ORACLE/B1 reproduce Run 2 to 3 decimals;
  all 200 one-shot MILPs optimal, gap 0.
- Root cause of the AI failure (`root_cause_analysis.md`): rolling oracle TR_ALL == one-shot ORACLE (P0 -> ORACLE gap is pure
  information, 0.094 kWh = 1.1 %); queued-job information = 52 % of it, running-job = 26 %; the Run 2 integration fed PERFECT
  forecasts captures 0 % or loses (P1*..P4*) -> integration failure, not model failure.
- P5/P5s phase-aligned recipe: no gain (P5 worse, CI excludes 0). AI14: recipe already predicts most transitions exactly.
- Cycle-level queued-job model with AI18 gate: duration skill +0.60 on held-out test; downstream PQ/PQ5 pending (partial: no gain).
- E1: AFE/bus/step limits are hard MILP constraints (brute-force tested); DS06 run with limits queued on Colab.
- AI-G10 bug found by R3_FAIL (NaN accepted when engine claims valid) -> fixed in ai_engine.py.

## Open
- [ ] PQ/PQ5/PQ* final, E1 limits campaign, Branch C retrain reproducibility (Colab queue).
- [ ] Twin v2 post-collapse screening + sizing (R3_TWIN), demonstrator bench v2 check (R3_DEMO), audit DS06 rows (R3_AUDIT),
      economics rerun on DS06 (R3_ECON --results), final mentor compliance audit (R3_COMPLY).
- [ ] USER: confirm target cell (storage / bidirectional power-module cycling vs converter burn-in NO-GO).
- [ ] USER/MENTOR: site data request (station traces, start windows, converter curves, tariff with demand charge).

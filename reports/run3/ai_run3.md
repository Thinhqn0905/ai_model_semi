# Run 3 WP-B — AI experiments AI14, AI15a, AI18, AI19-lite (queued-job forecasting) and downstream tests

Mentor references: M07, M08, M12, M13, M14. Decision rule (mentor): AI is adopted only if a P variant beats P0 on the SAME
instances with a paired 95 % CI excluding 0; otherwise recommend the optimisation-only solution.
Data: DS05 measured cycles (Loughborough, CC BY 4.0), split per module chronological 70/15/15; selection on **val**, final numbers
on **test**; DS06 downstream on test-split cycles (SIM_DATA_PROFILE). Root cause of the Run 2 failure: `root_cause_analysis.md`.

## AI14 — phase-transition timing (forecasting, LOCAL_RUN on MEASURED data)
Code `src/regenate/forecasting/phase.py`, `phase_bench.py`; outputs `runs/run3/ai14/ai14_{val,test}_summary.csv`.
Next-transition timing error (minutes), decision points every 15 min from minute 60, phase-structured cycles:
| Use case | val MAE recipe | val MAE phase-aligned | test MAE recipe | test MAE phase-aligned | test skill |
|---|---|---|---|---|---|
| Day Ahead | 1.4 | 1.4 | 1.8 | 1.6 | +0.15 |
| EFR | 226.9 | 166.8 | 193.5 | 130.1 | +0.33 |
| FFR (flickers every bin) | 1.9 | 33.0 | 1.1 | 34.0 | -28.9 |
| PV | 2.0 | 1.7 | 19.4 | 28.2 | -0.46 |
| PV-TOU | 5.5 | 4.4 | 2.2 | 2.2 | +0.02 |
| TOU | 13.3 | 20.2 | 10.3 | 14.6 | -0.41 |
Finding: the time-indexed recipe already predicts most transitions exactly (median error 0-1 min in 5 of 6 use cases), because
DS05 cycles follow programmed schedules. The hypothesis "regression smooths important phase transitions" is true for the Run 2
3-horizon integration (see root cause), but there is little transition-timing error left for a forecaster to remove, except EFR.
The val-selected use cases (EFR, PV, PV-TOU) do not all hold on test (PV reverses): AI14 phase alignment is **INCONCLUSIVE**.

## AI15a / AI18 — phase-aligned recipe for running jobs (P5, P5s), DS06 n = 100, paired vs P0
| Variant | kWh vs P0 (+ = better) | equal-TT kWh | peak kW vs P0 | status |
|---|---|---|---|---|
| P5 (all use cases) | -0.022 [-0.034, -0.010] | -0.023 [-0.036, -0.011] (n=95) | -0.54 [-1.08, -0.00] | FAIL |
| P5s (val-selected use cases) | -0.004 [-0.010, +0.004] | same (n=100, TT identical) | -0.20 [-0.52, +0.09] | FAIL (no gain) |
Source `MyDrive/semiexpo/ai_runs/run3/v2_p5/results.csv` (P0 identical to the diag run, max |diff| 1e-15 kWh).

## AI19-lite / AI18 — cycle-level queued-job forecaster (forecasting, LOCAL_RUN on MEASURED data)
Code `src/regenate/forecasting/cycle_model.py`: LightGBM on lagged cycles of the same module only (no same-cycle information),
target = log ratio to the previous cycle; AI18 gate: per (target, use case) threshold on |predicted log ratio| chosen on val.
Outputs `MyDrive/semiexpo/ai_runs/run3/cycle_model/{cycle_metrics,gates,selection}.csv`.
| Target (test, all use cases) | AI00 recipe MAE | AI10 LGBM skill | AI18 gated skill | median APE recipe / gated |
|---|---|---|---|---|
| cycle duration (h) | 4.84 | +0.49 | **+0.60** | 0.0005 / 0.0005 |
| charge energy (kWh/module) | 0.0236 | +0.01 | +0.06 | 0.0013 / 0.0038 |
| discharge energy | 0.0195 | -0.14 | +0.11 | 0.0013 / 0.0019 |
The ungated model degrades typical cycles (median APE 0.05 vs 0.0005); the gate keeps the recipe for them and corrects the
outliers. Forecasting gain is real on held-out test data.

## Downstream: PQ / PQ5 (queued-job AI) — DS06 n = 100, paired vs P0 (+ = better than P0)
Sources `MyDrive/semiexpo/ai_runs/run3/v2_{pq_gated,pq_ungated,pqstar}/results.csv` (P0 identical across runs).
| Variant | kWh vs P0 | equal-TT kWh | peak kW vs P0 | TT saved (h) | status |
|---|---|---|---|---|---|
| PQ, AI18 gated | -0.019 [-0.036, -0.006] | -0.016 [-0.030, -0.003] (n=98) | -0.39 [-0.86, +0.06] | -0.005 | FAIL |
| PQ5 (PQ + P5), gated | -0.034 [-0.052, -0.018] | -0.031 [-0.048, -0.014] (n=91) | -0.86 [-1.56, -0.19] | +0.007 | FAIL |
| PQ, ungated | -0.045 [-0.066, -0.026] | -0.043 [-0.061, -0.025] (n=94) | -0.99 [-1.55, -0.41] | -0.001 | FAIL |
| PQ* (PERFECT cycle ratios, same integration) | +0.008 [-0.007, +0.022] | +0.011 [-0.004, +0.025] (n=90) | +0.04 [-0.48, +0.54] | +0.048 | ceiling, n.s. |
| TR_Q (PERFECT queued profiles) | +0.049 [+0.035, +0.064] | +0.050 [+0.035, +0.066] (n=90) | +0.82 [+0.31, +1.36] | +0.048 | ceiling |

Reading: perfect cycle-level information (duration + energies) recovers ALL of the tardiness value of queued-job information
(0.048 h) but only ~16 % of its energy value, not significant. The energy value lies in the intra-cycle shape (when source and
sink phases occur), which neither the recipe warp nor a cycle-level model provides. Real forecasts then add errors on top: the
AI18 gate halves the damage of the ungated model but cannot make it positive.

## Verdict (AI-G08/G09, M12/M14)
- No AI variant tested in Run 2 or Run 3 (P1-P5, P5s, PQ, PQ5) beats P0 on energy or peak with a CI excluding 0; several are
  significantly worse. **AI is not adopted for scheduling decisions** (mentor rule; decision D006).
- Forecasting itself has measured value as information: remaining duration (Branch C, skill ~0.7), next-cycle duration
  (AI18, skill 0.60 on test, recipe-exact typical cycles preserved). Recommended use: engineer-facing station-availability /
  ETA display and anomaly flag (cycle far from recipe), behind the AI-G10 fallback, without any energy or peak claim.
- What would be needed for AI to matter (not done, stated as future work): a within-cycle phase-level trajectory forecaster
  for queued jobs whose errors are smaller than the recipe's, and a site where recipes deviate more than DS05's programmed
  cycles. Upper bound of the prize on DS06: 0.094 kWh/instance (1.1 % of P0) energy, 1.1 kW peak.

# Branch C — DS05 measured battery cycling: Model A (power) and Model B (remaining duration)

Boundary: **LOCAL_RUN on MEASURED data** (DS05, Loughborough second-life battery sweat test, Chroma 17020, CC BY 4.0,
doi:10.17028/rd.lboro.28732490.v2), run on Colab T4 runtime (CPU models). Source files: `results/ai_ds05_branchC/*`,
code `src/regenate/forecasting/ds05_bench.py`, data processing `src/regenate/data/ds05.py`.

Data: 14,755 valid cycles (2 unreadable, recorded), 6 modules (one per use case: TOU, PV, PV-TOU, EFR, FFR, Day Ahead),
60-s bins. Time unit check: `Cumulative_Time` x 10 s = wall clock (verified on 3 use cases). Split per module,
chronological 70/15/15 by cycle order; test cycles never seen in training. Decision points every 15 min from minute 60
of a cycle; features use only the past of the running cycle and the previous cycle of the same module.
166,301 samples; 118,808 train (capped at 250k), 22,178 test.

Baseline AI00 = the previous cycle of the same module at the same elapsed time (the "recipe" a planner has).
Skill = 1 - MAE(model) / MAE(AI00).

| Target (module kW / minutes) | AI01 persistence | AI03 ridge | AI04 RF | AI05 XGBoost | AI10 quantile LGBM (P50) | AI10 coverage P10-P90 |
|---|---|---|---|---|---|---|
| sink power, slot +1 (15 min) | -0.92 | -0.42 | 0.43 | 0.44 | **0.47** | 0.82 |
| sink power, slot +4 (1 h) | -2.61 | -0.92 | 0.20 | **0.31** | 0.21 | 0.77 |
| sink power, slot +16 (4 h) | -4.43 | -1.69 | 0.30 | **0.37** | 0.29 | 0.78 |
| source power, slot +1 | -0.93 | -0.44 | 0.32 | 0.35 | **0.36** | 0.80 |
| source power, slot +4 | -2.51 | -1.06 | 0.03 | **0.17** | 0.12 | 0.75 |
| source power, slot +16 | -3.96 | -1.41 | -0.08 | **0.19** | 0.19 | 0.77 |
| remaining duration (min) | n/a | -0.10 | 0.71 | **0.72** (MAE 73 min) | 0.67 (MAE 87 vs 261 min) | 0.72 |

Findings
- Tree ensembles clearly beat the recipe-from-history baseline on measured data; the largest gain is remaining duration
  (Model B, skill ~0.7). Persistence and linear models are worse than the recipe baseline at every horizon.
- XGBoost point forecasts are best at 1-4 h; quantile LightGBM is close and provides intervals. Intervals are slightly
  narrow (coverage 0.72-0.82 vs nominal 0.80): calibrate (split-conformal on validation) before using P90 in scheduling.
- Not established here: whether this accuracy yields grid-kWh savings. That is AI-EXP12, tested on DS06 (bench v2) with the
  same rolling MILP: `results/v2_ladder/*` (P0 vs P1..P4).
- Domain limit: DS05 modules are ~0.24 kW second-life EV modules on a cycler, not semiconductor DUTs; they are used because
  they are measured bidirectional source/sink cycles (the S3 cell type selected by D001/D003).

## AI-G04 calibration: split-conformal quantile regression (CQR) on the validation split
Source: Drive `MyDrive/semiexpo/ai_runs/ds05_cqr2/model_metrics.csv` (same data/split/seed; P50 unchanged).
| Target | coverage80 before | after CQR |
|---|---|---|
| sink +1 / +4 / +16 slots | 0.815 / 0.774 / 0.780 | 0.858 / 0.823 / 0.828 |
| source +1 / +4 / +16 slots | 0.804 / 0.754 / 0.773 | 0.842 / 0.792 / 0.797 |
| remaining duration | 0.720 | 0.755 |
Power intervals now meet the nominal 80 % within ~2 points; remaining-duration intervals stay under-covered (val->test drift in
time-ordered cycles), so P90 duration must not be used as a guaranteed bound — AI-G04 PARTIAL for Model B.

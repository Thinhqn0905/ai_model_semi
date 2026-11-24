# W5_AIFW — Unified AI benchmark framework + Branch A (DS02) and Branch B (DS04)   [AI plan s3, s4, s9, s10 AI-EXP01..03]
Account: default. Effort: medium.
Owner files: src/regenate/forecasting/framework.py, src/regenate/forecasting/models.py, src/regenate/forecasting/tcn.py,
  src/regenate/forecasting/bench_ds02.py, src/regenate/forecasting/bench_ds04v2.py, tests/test_ai_framework.py,
  runs/ai/ds02/**, runs/ai/ds04/**, reports/ai/branch_A_ds02.md, reports/ai/branch_B_ds04.md
Read: AGENTS.md, docs/system_spec.md (2, 8), src/regenate/forecasting/{baselines,metrics,ds04_bench}.py (reuse metrics and
  baselines; do not edit them), reports/data/ds02_report.md, reports/data/ds04_report.md.

## Contract (framework is shared by all branches; the lead builds Branch C/D on it)
- framework.py: `WindowSpec(lookback_steps, horizon_steps, step_s)`, causal window generation from a long table with
  group key (asset/dataset/run) without materialising all windows in RAM (index-based generator), split by the stored
  chronological split or by group; `run_benchmark(task, models, out_dir)` writing the standard files:
  forecast_predictions.parquet (dataset, task, model, group, t, horizon_step, y, p10, p50, p90), model_metrics.csv
  (dataset, task, model, horizon, mae, rmse, nmae, skill_vs_persistence, pinball10/50/90, coverage80, n_test),
  horizon_metrics.csv, quantile_calibration.csv (nominal 0.1..0.9 vs empirical), training_log.csv, runtime_metrics.csv
  (fit_s, predict_ms_per_sample, model_size_kb). NMAE normalised by the dataset's rated/p99 |y| (state which).
- models.py registry with the same fit/predict(p10,p50,p90) API: M0 persistence, M1 linear, M2 random forest, M3 XGBoost,
  M4 LightGBM, M5 quantile LightGBM, M6 TCN (tcn.py, PyTorch, CUDA if available, pinball loss for 3 quantiles, early stop
  on val, seed fixed). Equal tuning budget per model (small grid on val only), documented.
- Branch A (DS02 SHIFT2DC): task = multi-step forecast of bus/infeed power (p_kw or infeed_p_kw per dataset) at the native
  ~1 s cadence resampled to 10 s, horizons 1/6/30 steps; per-dataset chronological split 70/15/15.
- Branch B (DS04): reuse ds04_bench task definition, add M3, M6 and skill score; cap rows as before.
- Reports: tables of NMAE / skill / coverage per model and horizon, label LOCAL_RUN, domain-limit statement.
Gate: `python -m pytest -q tests/test_ai_framework.py` (window causality: every feature timestamp < every target timestamp;
split disjointness; metrics on hand example; TCN overfits a tiny sine to low loss) and both runs/ai/ds02/model_metrics.csv
and runs/ai/ds04/model_metrics.csv exist. Keep total runtime < 40 min.

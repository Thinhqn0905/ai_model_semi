# R4_ETA — Run 4 WP-B AI ETA and station availability: code + tests (lead runs it on Colab; D010; mentor M08, M12, M14)
Account: .codex-A. Effort: medium.
Owner files: src/regenate/forecasting/eta.py, tests/test_eta.py, reports/run4/ai_eta.md (method + placeholders PENDING_COLAB)
Read: AGENTS.md, src/regenate/forecasting/cycle_model.py (Run 3 gated next-cycle model, reuse its build_table/fit/gates; do not edit),
  src/regenate/forecasting/ds05_bench.py (remaining-duration samples: make_samples, features_at; do not edit), reports/run3/ai_run3.md,
  reports/ai/branch_C_ds05.md. No training on this machine (weak): tests use small synthetic data only.
Contract — eta.py with a CLI `python -m regenate.forecasting.eta --proc DIR --out DIR`:
1. Task T1 total duration before start (cycle level): baselines recipe/previous cycle, median of last 5, rolling EWMA (alpha chosen on
   val), ridge, RF, XGBoost, LightGBM, quantile LightGBM (P10/P50/P90) and the Run 3 AI18 gated model; CQR calibration of P10/P90 on
   val; metrics on test: MAE, RMSE, skill vs previous cycle, pinball, coverage80, width80, median APE, normal vs abnormal cycles
   (abnormal = |log(dur/dur_prev)| > log 1.5 in the TRUE data, reported separately), per use case, inference latency per prediction.
2. Task T2 remaining duration during a cycle (decision points every 15 min from minute 60, features from features_at only):
   same model list (where meaningful), CQR, metrics as above plus error by cycle progress bins (0-25/25-50/50-75/75-100 % of TRUE
   duration; the bin uses truth only for reporting, never as a feature).
3. Leakage guards (asserted in tests): no same-cycle totals in T1 features; T2 features use only bins < b; split from cyc.split
   (chronological per module, unchanged Run 2/3 split); model selection on val only.
4. Outputs: metrics_T1.csv, metrics_T2.csv, predictions (cycle_file, q10, q50, q90, true) parquet, eta_models.joblib, manifest.json.
5. Report skeleton: protocol, tables to be filled from the CSVs, claims rules (forecast accuracy is not a production improvement).
Gate: `python -m pytest -q -p no:cacheprovider --basetemp runs/tmp_pytest_eta tests/test_eta.py` passes (synthetic: CQR coverage
improves on a miscalibrated model; leakage assertions; abnormal split; CLI writes the files).

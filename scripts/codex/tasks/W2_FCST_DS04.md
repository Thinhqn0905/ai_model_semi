# W2_FCST_DS04 — External forecasting benchmark on DS04 (E10)   [WP06, mentor M12 M14]
Account: .codex-C. Effort: medium.
Owner files: src/regenate/forecasting/baselines.py, src/regenate/forecasting/metrics.py,
  src/regenate/forecasting/ds04_bench.py, tests/test_forecasting.py, reports/forecast/ds04_bench.md,
  runs/forecast_ds04/**
Read: AGENTS.md, docs/system_spec.md (2, 8), reports/data/ds04_report.md, src/regenate/data/ds04.py (interface).

## Contract
- metrics.py: mae, rmse, nmae (by mean |y|), pinball(q), interval_coverage(lo, hi), all numpy, tested.
- baselines.py (model-agnostic API `fit(X, y)`, `predict(X) -> dict(p10, p50, p90)`):
  F01 persistence / per-asset rolling mean, F02 linear regression (+ residual quantiles for P10/P90),
  F03 random forest, F04 LightGBM point, F05 LightGBM quantile (alpha 0.1/0.5/0.9, monotone fix p10<=p50<=p90).
- ds04_bench.py: task = next-slot power per asset at a fixed cadence (resample Company A to 5 min mean,
  Company B to 1 min; state the rule), horizons 1, 6, 12 steps. Features: lags, rolling mean/std,
  status one-hot, hour-of-day, asset id. Use the stored chronological split only; features computed
  causally (no future). Seeds fixed. Cap training rows (e.g. 300k per company, stated) to stay < 10 min CPU.
- Output runs/forecast_ds04/results.csv: company, horizon, model, mae, rmse, nmae, pinball10/50/90,
  coverage80, fit_s, predict_ms; report table with label LOCAL_RUN and the domain-limit statement
  (DS04 is not a semiconductor test cell; this only benchmarks the forecasting code path).
Gate: `python -m pytest -q tests/test_forecasting.py` passes (metrics hand examples, quantile monotonic,
no-leakage check that every feature row uses only past timestamps) and
`python -m regenate.forecasting.ds04_bench` writes results.csv.

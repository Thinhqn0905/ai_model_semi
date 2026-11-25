# R4_TCN — Run 4 WP-B optional temporal deep learning: TCN for remaining duration (T2) on Colab GPU (lead runs it)
Account: .codex-B. Effort: medium.
Owner files: src/regenate/forecasting/eta_tcn.py, tests/test_eta_tcn.py, reports/run4/ai_eta_tcn.md (method + PENDING_COLAB)
Read: AGENTS.md, src/regenate/forecasting/eta.py (T2 sample construction, split, metrics; reuse its functions, do not edit),
  src/regenate/forecasting/ds05_bench.py (features_at, SLOT), src/regenate/forecasting/tcn.py (existing Net/TCN; reuse or extend in your
  own file), reports/run4/ai_eta.md (RF baseline: MAE 62.0 min, skill 0.60). No training on this machine: tests on tiny synthetic data, CPU.
Contract — CLI `python -m regenate.forecasting.eta_tcn --proc DIR --out DIR [--device cuda] [--lookback 240] [--epochs 30]`:
1. Same decision points, same test samples and same val/test split as eta.py T2 (assert identical sample keys); input = last
   `lookback` 1-min bins (zero-padded at cycle start) of charge kW, discharge kW, voltage, ambient temperature, plus the static
   features of eta.py T2 (elapsed, previous-cycle stats, use case one-hot). Past bins only (assert). Target: log remaining minutes
   (report in minutes); quantile heads q10/q50/q90 with pinball loss; CQR on val.
2. Training with early stopping on val loss, fixed seed, mixed precision when cuda; record GPU name, epochs, train time, inference
   ms/sample (GPU and CPU).
3. Outputs: metrics_tcn.csv in the SAME schema as eta.py metrics_T2.csv (model names AI11_tcn, AI11_tcn_cqr; progress bins and
   normal/abnormal subsets), predictions parquet, manifest.json; the report compares against RF and QLGBM rows from metrics_T2.csv.
Gate: `python -m pytest -q -p no:cacheprovider --basetemp runs/tmp_pytest_tcn tests/test_eta_tcn.py` (synthetic: past-only window
assertion, identical sample keys, CPU 1-epoch run writes the files).

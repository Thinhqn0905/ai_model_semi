# W5_FIGS — Automatic figure pipeline F01-F15   [WP11 reporting, user figure list 2026-11-25]
Account: .codex-A. Effort: medium.
Owner files: src/regenate/visualization/** , tests/test_figures.py, reports/figures/** , docs/figures.md
Read: AGENTS.md, docs/system_spec.md (7, 10), docs/decisions.md, runs/oracle_v1/results.csv + schedules.parquet (schema
  only), data/processed/efficiency_points.parquet, runs/twin_v1/*, runs/forecast_ds04/results.csv.

## Contract
- One module per figure family: plot_forecasting.py (F01 probabilistic forecast: plot + fill_between(step="mid"), F02
  actual-vs-pred scatter with y=x, MAE/RMSE/R2, F03 error vs horizon, F11 error distribution box/violin, F12 quantile
  calibration nominal vs empirical coverage), plot_cross_dataset.py (F04 heatmap of NMAE or forecast skill
  1 - MAE/MAE_persistence; never mix metric types in one heatmap), plot_efficiency.py (F05 from efficiency_points),
  plot_energy_matching.py (F06 source/sink/matched with np.minimum incl. link cap), plot_bus_transients.py (F07 with
  axhline limits), plot_scheduling.py (F13 broken_barh Gantt original vs proposed), plot_ablation.py (F08 baseline barh
  with paired-CI error bars, F09 ablation bars), plot_sensitivity.py (F10 heatmap flexibility x efficiency), plot_pareto.py
  (F15 accuracy-latency), plot_sankey.py (F14 plotly Sankey from ledger totals), generate_all_figures.py (CLI:
  `python -m regenate.visualization.generate_all_figures --campaign runs/oracle_v1 --out reports/figures`).
- Input = the standard output files (forecast_predictions.parquet, model_metrics.csv, horizon_metrics.csv,
  quantile_calibration.csv, benchmark/results.csv, ablation_results.csv, sensitivity_results.csv, runtime_metrics.csv,
  schedules.parquet, bus_transients.csv). Document each file's columns in docs/figures.md; a figure whose input file is
  missing is skipped with a printed note (never filled with invented numbers).
- Style: serif font, no top/right spines, PDF + PNG 300 dpi; every figure carries its boundary label (from the data's
  `boundary` column) in a corner caption.
Gate: `python -m pytest -q tests/test_figures.py` (each plot function on a tiny synthetic frame labelled MOCK writes a file;
missing-input skip) and generate_all_figures runs on runs/oracle_v1 producing at least F05, F06, F08, F13.

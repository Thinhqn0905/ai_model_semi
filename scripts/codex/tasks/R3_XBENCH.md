# R3_XBENCH — Run 3 WP-C cross-dataset benchmark standardisation (mentor M07, M12, M13, M14)
Account: .codex-A. Effort: medium.
Owner files: src/regenate/forecasting/xbench.py, tests/test_xbench.py, src/regenate/visualization/plot_cross_dataset.py,
  reports/run3/cross_dataset_benchmark.md, reports/run3/figures/F04_v3.*, runs/run3/xbench/**
Read: AGENTS.md, docs/ai_plan.md, docs/run3_plan.md, reports/ai/branch_{A_ds02,B_ds04,C_ds05}.md, reports/forecast/ds04_bench.md,
  results/ai_ds05_branchC/model_metrics.csv, runs/ai/**, runs/forecast_ds04/**, src/regenate/forecasting/{framework,models,metrics,
  bench_ds02,bench_ds04v2,ds05_bench}.py, the existing plot_cross_dataset.py (keep its old entry point working for test_figures).
Contract:
1. One model-ID table used everywhere: AI00 domain baseline (previous cycle / recipe / seasonal), AI01 persistence, AI02 seasonal
   naive (if defined), AI03 ridge, AI04 RF, AI05 XGBoost, AI06 LightGBM, AI10 quantile LGBM (P50), AI11 TCN. Map every legacy
   name (M5, etc.) to this ID in a mapping table.
2. xbench.py: collect existing metric CSVs into one long table (dataset, task, target, horizon_min in real minutes, model_id,
   MAE, RMSE, NMAE, skill_vs_persistence, skill_vs_domain_baseline, coverage80, width80, latency_ms when present, source file).
   Compute a skill only when that baseline exists on the same split; otherwise NaN with the reason.
   No retraining unless a metric is missing AND the bench script runs in < 10 min on CPU; record any rerun command.
3. F04_v3: annotated heatmap (rows dataset/target/horizon, cols model_id), panel 1 skill_vs_persistence, panel 2
   skill_vs_domain_baseline; NaN cells hatched; PNG 300 dpi + PDF + SVG; provenance json next to it.
4. Report: protocol table per dataset (split, horizons, baseline), the heatmap, and an explicit statement that these are
   independently trained within-dataset benchmarks, NOT cross-dataset transfer. Never compare classification accuracy with NMAE.
   No superiority claim over published work.
Gate: `python -m pytest -q -p no:cacheprovider --basetemp runs/tmp_pytest_xbench tests/test_xbench.py tests/test_figures.py`
(skill formula hand check, NaN when baseline missing, ID mapping total) and the three figure files exist.

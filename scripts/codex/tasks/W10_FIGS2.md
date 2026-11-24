# W10_FIGS2 — Regenerate the full figure set from real results (F01-F15)
Account: .codex-A. Effort: medium.
Owner files: src/regenate/visualization/**, reports/figures/**, docs/figures.md, tests/test_figures.py
Read: AGENTS.md, docs/figures.md, docs/decisions.md (D001-D004), reports/ai/branch_C_ds05.md, reports/ai/ai_exp12_ds06.md,
  results/ai_ds05_branchC/*.csv, runs/oracle_v1, runs/rolling_v1 (ladder.csv, timeseries.parquet, schedules.parquet), runs/biz_v1,
  runs/twin_v1, runs/ai/ds02, runs/ai/ds04, data/processed/efficiency_points.parquet, runs/sens_v1 (if present).
Contract: produce PDF+PNG for F03 (horizon error from results/ai_ds05_branchC model_metrics: skill vs horizon per model), F04 (cross-dataset
skill heatmap DS02/DS04/DS05 — skill vs each dataset's own baseline, say which baseline in the caption), F05, F06 (S3 ORACLE vs B1p-OPT),
F07 (twin controls), F08 (ladder S3 with paired CI bars from rolling_v1/ladder.csv), F09 (AI ablation: build the input CSV from the
tables in reports/ai/ai_exp12_ds06.md — copy the numbers exactly into reports/figures/ai_exp12_table.csv with boundary SIM_DATA_PROFILE),
F10 (sensitivity heatmap if runs/sens_v1/sensitivity_results.csv exists, else skip with note), F12 (coverage nominal vs empirical from
results/ai_ds05_branchC), F13, F14 (html), F15 (accuracy vs predict_ms from runtime_metrics). Every figure carries its boundary label.
Gate: `python -m pytest -q -p no:cacheprovider --basetemp runs/tmp_pytest_figs2 tests/test_figures.py` and reports/figures/INDEX.md listing
each figure, its input file and boundary.

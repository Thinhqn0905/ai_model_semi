# W9_DASH2 — Dashboard on real campaign results (WP11, mentor M01 M05 M14 M16)
Account: .codex-E. Effort: medium.
Owner files: app/**, tests/test_dashboard_data.py, reports/product/dashboard_v2.md
Read: AGENTS.md, docs/system_spec.md (7, 10), docs/decisions.md (D001-D003), app/ (current code), runs/rolling_v1/ladder.csv,
  runs/rolling_v1/timeseries.parquet, runs/oracle_v1/schedules.parquet, runs/biz_v1/business_case.csv, results/ai_ds05_branchC/model_metrics.csv,
  reports/ai/branch_C_ds05.md.
Contract:
- Campaign selector lists runs/*/ folders that contain results.csv or ladder.csv (ladder.csv preferred); boundary banner from data.
- New page "AI forecasting": table/heatmap of skill_vs_prev_cycle per target x model from results/ai_ds05_branchC/model_metrics.csv,
  coverage vs nominal 0.8, with the note that forecast accuracy is not the energy claim (AI-EXP12 is separate).
- Finance page: read runs/biz_v1/business_case.csv (alpha, capex factor, demand toggles as filters), show payback/NPV, never compute
  new numbers beyond what the CSV holds.
- Engineer approval page keeps the decision log; Overview tiles computed from the selected ladder (S3 default).
- AppTest: every page runs without exception on runs/rolling_v1 and on a mock campaign.
Gate: `python -m pytest -q -p no:cacheprovider --basetemp runs/tmp_pytest_dash2 tests/test_dashboard_data.py` passes.

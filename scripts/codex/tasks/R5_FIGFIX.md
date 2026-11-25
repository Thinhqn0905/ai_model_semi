# R5_FIGFIX — make run4_figs accept the REAL result schemas (lead reruns on Colab)
Account: .codex-A. Effort: medium.
Owner files: src/regenate/visualization/run4_figs.py, tests/test_run4_figs.py, scripts/colab_collect_run4.py
Real schemas (from Colab, 2026-11-25):
- run4/eta/predictions_T1.parquet: cycle_file, use_case, true, model, q10, q50, q90  (F17: pick model 'quantile_lightgbm_cqr' or first q-model; sample cycles)
- run4/eta/predictions_T2.parquet: cycle_file, use_case, true, elapsed_min, model, q10, q50, q90
- run4/eta/metrics_T2.csv: use_case, subset, progress ('ALL','0-25','25-50','50-75','75-100'), model, n, mae, rmse, skill_vs_previous, median_ape,
  pinball, coverage80, width80, predict_ms, boundary  (F18: rows use_case=='ALL', subset=='ALL', progress != 'ALL'; y = mae)
- run3/screen_e1.csv: run, instance_id, method, afe_kw, link_a, approved, v_min, v_max, i_peak, kinds, peak_sink_kw, peak_src_kw, max_step_kw
  (F22: approval by run (v2_diag = E0, v2_e1 = E1) and method; boundary label constant 'SIM_DATA_PROFILE' if column absent); also add
  run4_rt3/screen_sizing_summary.csv (afe_kw, bus_kw, method, n, approved, kinds) as a second F22 panel when present.
- run3/fin_v3_ds06.csv: ... annual_net_usd, break_even_capex_usd, payback_years, option, method, set, dc_usd_kw_month (F25/F32: use annual_net_usd
  and break_even_capex_usd; also run4/fin_fac_{gen,tou}_fx0.21/clustered_summary.csv with option, n_cells, annual_net_usd, ceiling_3y, ceiling_5y,
  ceiling_10y_discounted, tariff for the multi-cell FIN-B panel).
- facility_md.csv: facility, month, method, md_window, n_cells, block_h, n_blocks, md_bg_kw, md_kw, md_increment_kw, md_time, bg_md_time, cell_kwh,
  cell_peak_kw, coverage, boundary. P0-BILL files contain methods 'P0-BILL:<kind>@etol0.02' AND 'P0@v2_e1_peak' present in several files for the same
  facility-month: de-duplicate by (facility, month, method) keeping the first and log it (F30 = P0-E1-Peak vs P0-BILL:hist/ai/oracle vs ORACLE,
  include run4/fac_aibill_*).
- campaign manifests differ in their `methods` list by design: F16/F19 must only require equal seeds/flex/split/n_jobs/n_stations/time_limit/prm/peak.
- F26: build the DS07 monthly summary from run4/fac_grid*/facility_md.csv (md_bg_kw per facility-month) when ds07/facility_monthly_summary.csv is absent.
- F01-F15: list in INDEX.md with the existing files under reports/figures/ (Run 2) as PASS where present, else MISSING.
Gate: `python -m pytest -q -p no:cacheprovider --basetemp runs/tmp_pytest_f5 tests/test_run4_figs.py` with fixtures using exactly these columns.

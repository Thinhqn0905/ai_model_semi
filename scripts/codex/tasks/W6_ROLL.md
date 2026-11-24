# W6_ROLL — Rolling P0 / P campaign on bench_v1 (WP08 E12/E13)   [mentor M09 M10 M12]
Account: .codex-E. Effort: medium.
Owner files: src/regenate/evaluation/rolling_campaign.py, tests/test_rolling_campaign.py, runs/rolling_v1/**, reports/benchmark/rolling_v1.md
Read: AGENTS.md, docs/system_spec.md (6, 7, 10), docs/decisions.md (D002), src/regenate/optimization/rolling.py (Replanner),
  src/regenate/simulation/replay.py (Replay), src/regenate/evaluation/oracle_campaign.py (load, score, run_instance, CLI),
  src/regenate/evaluation/stats.py. Do not edit those modules.
Contract:
- For each bench_v1 instance (n=10, seeds 0 1, scenarios S1 S3, flex 0.25): initial plan = FIFO (generator.fifo_schedule);
  run Replay with Replanner(mode="P0") and Replanner(mode="P"), period 0.25 h, time_limit 10, max_solve_s 60; score with
  oracle_campaign.score(..., topology "DC"). Write rows with method P0 / P into runs/rolling_v1/results.csv (section-10 schema +
  n_replans, n_rejected, flex), schedules.parquet and timeseries.parquet (per-step p_import/p_export/direct from the ledger).
- Merge with runs/oracle_v1/results.csv (flex 0.25 rows) into runs/rolling_v1/ladder.csv and compute ladder_table (equal TT and
  all-instance versions). Parallelise over instances with ProcessPoolExecutor(8).
- Report: full ladder B0..ORACLE incl. P0, P, paired CIs, dE_AI = P0 - P, oracle gap; label SIM_ASSUMED_PROFILE and the D002
  caveat (bench_v1 uncertainty is i.i.d., so P - P0 is a control, not the AI claim).
Gate: `python -m pytest -q -p no:cacheprovider --basetemp runs/tmp_pytest_roll tests/test_rolling_campaign.py` (1 tiny instance end-to-end,
schema) and runs/rolling_v1/ladder.csv exists.

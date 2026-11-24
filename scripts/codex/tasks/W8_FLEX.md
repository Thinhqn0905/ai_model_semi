# W8_FLEX — Rolling P0 across flexibility on bench_v1 S3 (E06/E13 extension, mentor M03)
Account: .codex-C. Effort: medium.
Owner files: runs/rolling_flex/**, reports/benchmark/rolling_flex.md
Read: AGENTS.md, src/regenate/evaluation/rolling_campaign.py (CLI/functions), runs/oracle_v1/results.csv, src/regenate/evaluation/stats.py.
  Do not edit src/.
Contract: run the rolling campaign (P0 only, S3, n=10 seeds 0 1) at flex 0, 0.1, 0.5, 1.0 (0.25 exists in runs/rolling_v1) into
runs/rolling_flex/f<flex>/; merge with runs/oracle_v1 rows of the same flex; table + paired CI per flex of: B1p-OPT - P0, P0 - ORACLE,
B2 - P0, peak P0 vs B1p-OPT. State how much of the shared-DC gain needs scheduling flexibility (flex 0 = topology only).
Label SIM_ASSUMED_PROFILE. Keep workers <= 6.
Gate: report exists; every flex point has 18 instances or the failure is listed.

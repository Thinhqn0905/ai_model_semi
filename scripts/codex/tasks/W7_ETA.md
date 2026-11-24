# W7_ETA — Ground the electrical model in DS03 efficiency curves (WP03 M04/M07)
Account: .codex-A. Effort: medium.
Owner files: src/regenate/electrical/grounded.py, tests/test_grounded.py, configs/elec_grounded.yaml, reports/electrical/grounding.md,
  runs/oracle_grounded/**
Read: AGENTS.md, docs/system_spec.md (4, 5), docs/decisions.md (D001), src/regenate/electrical/ledger.py (ElecParams, dc_gain_bound),
  src/regenate/data/ds03.py (eta_curve), data/processed/efficiency_points.parquet, reports/data/ds03_report.md,
  src/regenate/evaluation/oracle_campaign.py (CLI --prm). Do not edit ledger.py or oracle_campaign.py.
Contract:
- grounded.py: `grounded_params(load_frac=0.5) -> (ElecParams, provenance dict)` mapping each ElecParams efficiency to a DS03
  device/direction at a stated load fraction: eta_sup_dc / eta_rl_dc <- TIDA-010938 battery buck/boost curves, eta_afe_imp /
  eta_afe_exp <- TIDA-010938 DC-AC curves (and Chroma 62000D/63700 rated 94 % as a cross-check), eta_sup_ac <- product of the
  relevant stages, eta_link <- keep ASSUMED 0.99 with a cable-loss estimate note. Also a load-dependent variant
  `eta_at(param, load_frac)`. Every value carries provenance (DATASHEET/DERIVED/ASSUMED + file/page).
- configs/elec_grounded.yaml with the chosen values; reports/electrical/grounding.md: table assumed vs grounded, dc_gain_bound
  for both, and the effect on D001 (gain per kWh of residual source).
- Rerun the oracle with grounded values: `python -m regenate.evaluation.oracle_campaign --out runs/oracle_grounded --n 10
  --seeds 0 1 --flex 0.25 --time_limit 30 --workers 6 --prm '<json from yaml>'` and report ORACLE vs B1p-OPT / B1-OPT for S1/S3
  with paired CI (regenate.evaluation.stats.ladder_table), label SIM_ASSUMED_PROFILE + DATASHEET efficiencies.
Gate: `python -m pytest -q -p no:cacheprovider --basetemp runs/tmp_pytest_eta tests/test_grounded.py` (values in (0,1], provenance
present for every efficiency, eta_at monotone-or-documented within valid range) and runs/oracle_grounded/results.csv exists.

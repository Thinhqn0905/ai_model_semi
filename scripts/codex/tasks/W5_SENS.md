# W5_SENS — Sensitivity / Go-No-Go map (WP09.1, SENS-01..12 subset)   [mentor M03 M13]
Account: .codex-B. Effort: medium.
Owner files: src/regenate/evaluation/sensitivity.py, configs/sens/*.yaml, data/generated/sens_*/** , runs/sens_v1/**,
  reports/sensitivity/sens_v1.md, tests/test_sensitivity.py
Read: AGENTS.md, docs/system_spec.md (5-7), docs/decisions.md, src/regenate/evaluation/oracle_campaign.py (CLI: --bench,
  --prm JSON overrides of ElecParams, --flex, --scenarios), src/regenate/data/generator.py (config keys),
  configs/bench_v1.yaml. Do NOT edit those modules: call them (CLI or functions).

## Contract
- Base = bench_v1 config, n=10, seeds 0 1, flex 1.0, time_limit 30, workers 8. One-at-a-time sweeps, scenarios S3 and
  S1 (S1 = negative control, expect ORACLE == B1p-OPT):
  SENS-01 flex {0, 0.1, 0.25, 0.5, 1}; SENS-02 eta_afe_imp=eta_afe_exp {0.94, 0.96, 0.98}; eta_link {0.97, 0.99, 1.0};
  SENS-03 P_link_max {5, 10, 20, inf}; SENS-04 n_stations {4, 8, 16} (new bench via generator config -> data/generated/sens_n*);
  SENS-08 allow_export {true, false}; SENS-10 cycle_scale {0.5, 1, 2}; unit_h {0.5, 1, 2}.
  Plus the 2-D Go/No-Go grid flex {0, 0.25, 1} x eta_link {0.97, 0.99, 1.0} for S3.
- Each point writes runs/sens_v1/<sweep>_<value>/results.csv via oracle_campaign. sensitivity.py aggregates to
  runs/sens_v1/sensitivity_results.csv: sweep, value, scenario, n, mean/CI of (B1p-OPT - ORACLE) kWh and %, (B1-OPT - ORACLE),
  peak diff, R_match of ORACLE, share of instances with gain > 0, max mip_gap. Use regenate.evaluation.stats.paired_ci.
- Report: tables + the statement of where the shared-DC gain is > 0 with CI excluding 0; label SIM_ASSUMED_PROFILE.
Gate: `python -m pytest -q tests/test_sensitivity.py` (aggregation on a hand-made results.csv) and sensitivity_results.csv exists
with every sweep point; points that failed list the error, no silent drop.

# W2_ECON — Economics module: tariff, CAPEX/OPEX, payback, FIN-A/B/C   [WP10.1, mentor M16]
Account: .codex-A. Effort: medium.
Owner files: src/regenate/economics/model.py, configs/economics_v1.yaml, tests/test_economics.py,
  reports/economics/economics_method.md
Read: AGENTS.md, docs/system_spec.md (5, 7), Instruction/Project_Profile.md (Feasibility section),
  Instruction/Mentor_Feedback.md (Required KPIs, financial). Use web search only for the current Vietnam
  EVN production tariff structure (peak/normal/off-peak hours, VND/kWh, demand charge existence) and cite URL.

## Contract
- Inputs: per-step p_import / p_export arrays (kW) from regenate.electrical.ledger, dt_h, timestamps or
  hour-of-day, tariff config (TOU import price per band, export credit factor alpha_ex in {0, 0.5, 1}
  or export price, optional demand charge per kW-month), CAPEX items, OPEX items, horizon, discount rate.
- Functions: `energy_cost(...)`, `annualise(run_cost, run_hours, operating_hours_per_year)`,
  `incremental_case(base_run, new_run, capex_add, opex_add, cfg) -> dict(annual_saving, simple_payback_y,
  npv, irr or None)`; peak saving counted ONLY if the tariff has a demand charge; cooling saving only
  from an explicit input (never derived from electricity here).
- FIN-A software-only on regen-to-AC, FIN-B optimisation on existing shared DC, FIN-C full retrofit:
  CAPEX lists as config with provenance (slide 16 estimates = ASSUMED estimate; any quote = SOURCE).
- Sensitivity helper: grid over price low/base/high ($0.046/0.078/0.132 from slide 16, ASSUMED until
  the EVN source is cited), alpha_ex, capex x {0.5, 1, 2}; returns a tidy DataFrame.
- reports/economics/economics_method.md: formulas, tariff source, what is assumed, and the rule that
  payback is reported as "not reached" when annual saving <= 0.
Gate: `python -m pytest -q tests/test_economics.py` (hand-computed 2-step example, TOU band split, zero or
negative saving -> payback None, demand charge only applied when configured).

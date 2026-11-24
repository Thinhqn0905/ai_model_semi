# W4_WATER — Cooling-water workstream method (no quantitative claim)   [WP10.2, mentor M15]
Account: .codex-C. Effort: medium.
Owner files: src/regenate/economics/thermal.py, tests/test_thermal.py, reports/economics/water_method.md
Read: AGENTS.md, Instruction/Mentor_Feedback.md (Water), docs/system_spec.md (5), src/regenate/electrical/ledger.py
  (outputs hvac_kwh, dump_kwh, loss_kwh). Web search allowed for published chiller / cooling-tower water-use
  relations (cite URL; label SOURCE_REPORTED).

## Contract
- thermal.py: `heat_rejected_kwh(ledger_out)` = conversion losses + dump + DUT loss inside the cell (all from the
  ledger, no new physics); `cooling_load(heat_kwh, dt_h)`; `q_dot(m_dot_kg_s, cp, t_in, t_out)`;
  `water_estimate(heat_kwh, wue_l_per_kwh_th)` that REQUIRES an explicit, cited coefficient and returns
  label NOT_VERIFIED unless `metered=True`.
- water_method.md: the required measurements (cooling-loop flow, dT, heat load per station, chiller/tower
  make-up water meters), how a reduced heat load would map to water only with a metered baseline, why no % water
  saving is claimed now, and which ledger quantities change between B0/B1/B1p/DC (heat goes down mainly B0->B1).
Gate: `python -m pytest -q tests/test_thermal.py` (energy-consistency on a hand ledger example; water_estimate
refuses without coefficient; label NOT_VERIFIED unless metered).

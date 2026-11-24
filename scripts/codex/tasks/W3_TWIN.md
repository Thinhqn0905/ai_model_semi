# W3_TWIN — Dynamic DC-bus twin + plan checker   [WP09.2, mentor M06 M11]
Account: .codex-C. Effort: medium.
Owner files: src/regenate/simulation/bus_twin.py, tests/test_bus_twin.py, reports/safety/bus_twin.md,
  runs/twin_v1/**
Read: AGENTS.md, docs/system_spec.md (3, 4, 5), DS01_Quanh/code/bus_twin_check.py (legacy logic, read-only),
  reports/data/ds02_report.md (what DS02 can / cannot calibrate), src/regenate/electrical/ledger.py (interface).

## Contract
- Model (two time scales, plan IX/9.2): scheduler power per slot -> fine-step trajectory with ramp limits
  (ramp_kw_per_s per station, ASSUMED) at dt_s = 1 ms; bus energy d/dt(0.5 C V^2) = P_src - P_sink - P_afe - P_chop
  - P_loss; AFE droop P_afe = clip(K_droop (V_nom - V), -P_afe_max, P_afe_max) with first-order lag tau_afe
  (ASSUMED 80 ms, slide 11; DS02 cannot identify it — say so); chopper above V_chop (415 V) up to P_chop_max
  (15 kW); limits V 380-420 V, |I_link| <= 80 A, P_direct <= P_link_max. Defaults = slide 12 values, ASSUMED.
- `check_plan(p_src_kw, p_sink_kw, slot_s, params) -> dict(approved, v_min, v_max, i_peak, p_chop_kwh,
  violations=[(t_s, kind, value)])`; the window simulated = each slot boundary +/- 2 s (where steps happen), not
  the whole day; state carried across.
- Negative controls (tests): (a) synchronous burst of all stations reversing at once at max power -> rejected;
  (b) smooth plan with ramps -> approved; (c) AFE saturation (net demand > P_afe_max) -> undervoltage -> rejected;
  (d) energy check: with P_src = P_sink and no AFE action V stays at V_nom within 1e-6 V.
  Reproduce the legacy example values (393.5-400.4 V approved, 440.2 V / 86.5 A rejected) only if the same inputs
  are reconstructable from bus_twin_check.py; otherwise state that they are not reproduced.
- reports/safety/bus_twin.md: equations, parameters + provenance, negative-control results with label
  SIM_ASSUMED_PROFILE, and the statement that this proves simulation logic only, not hardware safety.
Gate: `python -m pytest -q tests/test_bus_twin.py` passes.

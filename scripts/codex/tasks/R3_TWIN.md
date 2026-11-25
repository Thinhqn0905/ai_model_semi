# R3_TWIN — Run 3 WP-E twin v2: all-violation screening, conservation tests, transient model (mentor M04, M06, M11)
Account: .codex-C. Effort: medium.
Owner files: src/regenate/simulation/bus_twin.py, src/regenate/simulation/transient.py, tests/test_bus_twin.py,
  tests/test_transient.py, runs/run3/twin/**, reports/run3/electrical_feasibility.md, reports/run3/figures/F07_v3.*
Read: AGENTS.md, docs/run3_plan.md, docs/system_spec.md, src/regenate/electrical/{ledger,grounded}.py, configs/elec_grounded.yaml,
  reports/safety/bus_stability_kpi.md, reports/electrical/grounding.md, runs/twin_v1/**, runs/twin_check/**,
  DS02_SHIFT2DC/README.md and its processed data (measured LVDC behaviour). Do not edit milp.py / rolling.py (lead owns them).
Contract:
1. bus_twin.check_plan keeps its signature and default behaviour for existing callers/tests; add `all_violations=True` that does
   not stop at the first undervoltage and returns per-type counts, durations and first time (UV, OV, link over-current,
   AFE import/export over-limit, ramp over-limit).
2. transient.py: lumped DC-bus model (bus capacitance C, link R/L, AFE as current-limited source with droop and bandwidth,
   stations as constant-power loads/sources) integrated with scipy solve_ivp at ms scale for: job start step, source->sink
   phase flip, AFE trip, link trip. Parameters from configs/elec_grounded.yaml or DS02 where measured, else ASSUMED and listed.
   ngspice is not installed; the scipy model is the deliverable (state this).
3. Tests: energy conservation (sources = loads + losses + capacitor energy change, 1e-6 relative), no negative losses, negative
   control (zero-power plan -> no violation), overload control (step above AFE limit -> detected), constant-power instability
   control (very small C -> detected).
4. Rerun the Run 2 screening plans of runs/twin_v1 with all_violations=True; violation mix per method and the AFE/link sizing that
   removes each type. F07_v3: voltage/current transient with limit lines (PNG 300 dpi + PDF + SVG).
5. Report: simulation-only boundary; independent hardware protection mandatory; what the twin cannot show.
Gate: `python -m pytest -q -p no:cacheprovider --basetemp runs/tmp_pytest_twin tests/test_bus_twin.py tests/test_transient.py`
passes and runs/run3/twin/violations.csv exists.

## Run 2 (lead)
The failing test expects an undervoltage for a 50 kW step with default TwinParams; first check by hand whether the model really must undervolt (AFE 20 kW + droop + chopper). If physics says no UV, change the test to a case that must undervolt by construction (e.g. sink far above p_afe_max for longer than C can bridge: 0.5*C*(v_nom^2-v_min^2) / excess power) and assert that. Never weaken a test to pass without that justification in a comment. Then complete contract items 2-5 (transient.py, tests, rerun twin_v1 plans, violations.csv, F07_v3, report).

## Run 3 (lead)
Post-collapse: once v < 0.5*v_min (or energy clamp hits), stop integrating THAT plan, record "collapse" with time and the violation counts up to that point, and do not report currents after it (they are nonphysical). That is a valid screening outcome (REJECT). Then rerun the plans, write violations.csv, and the sizing table: per method the smallest AFE kW (grid 20,30,40,60,80) and link A (80,120,160,240) that gives zero violations, or "none in grid". Finish the report.

## Run 4 (lead)
Machine is weak: single process, no multiprocessing. Reduce the sizing grid to AFE {20, 40, 80} kW x link {80, 160} A and only the methods B2, B1p-OPT, P0, ORACLE, burst. Run the screening in the foreground to completion (it is allowed to take long), write violations.csv + sizing table, finish the report, run the gate.

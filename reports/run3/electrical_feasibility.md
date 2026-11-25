# Electrical feasibility — Run 3

Boundary: **SIM_ASSUMED_PROFILE**. This is a numerical screening of synthetic S3 schedules, not a hardware validation or site measurement. Independent hardware protection is mandatory. The models cannot establish fault interruption, protection coordination, converter stability, electromagnetic compatibility, isolation, cable heating or test integrity.

The screening replay uses the saved Run 2 instances and schedules with the reduced Run 4 AFE/link grid (20, 40, 80 kW and 80, 160 A); see `runs/run3/twin/screen.py`, `screen_run4.log`, `results.json`, `violations.csv` and `sizing.csv` for actual progress, errors and per-method violation mix. Integration covers windows around schedule boundaries only; gaps are skipped while states are carried forward. Consequently durations are simulated-window durations, not whole-plan durations. A plan is rejected and integration stops when voltage drops below half the minimum voltage or the energy clamp is reached; currents after that point are not reported. Violation durations and counts stop at collapse. The ramp flag measures unmet station power requests under a ramp limiter, not a measured converter slew rate. The AFE flags measure requested droop power exceeding its rating, not actual power exceeding the limiter. B1p-OPT is a hypothetical shared-bus screening, not its actual separate-bus topology. Oracle schedules may be time-limited incumbents. The completed grid establishes only simulated screening outcomes; hardware sizing remains **NOT_VERIFIED**. The selected size must approve every screened instance for that method; a ramp or other violation can remain regardless of rating.

The SciPy `solve_ivp` lumped transient model is the deliverable; ngspice is not installed. Figure F07_v3 shows assumed job start, source-to-sink flip, AFE trip and link trip, and voltage and current screening limits. It is not a switching model or a validated protection study. Default assumptions (not fitted to DS02): nominal 400 V, voltage limits 380–420 V, C 0.04 F, link R 0.1 ohm and L 0.01 H, AFE limit 50 A, droop 0.5 A/V, response time 0.08 s, and link limit 80 A. The grounded electrical configuration supplies efficiency proxies, not these dynamic parameters. The DS02 processed 700 V dataset is a different system; it does not establish the millisecond parameters for this model. The current-controlled RL approximation and abrupt trips are assumptions; no protection device or post-trip inductive energy dissipation is represented. The solver terminates near voltage collapse because constant-power behavior is singular there. Trip traces therefore do not validate fault behavior.

Reproduce the controls with `python -m pytest -q -p no:cacheprovider --basetemp runs/tmp_pytest_twin tests/test_bus_twin.py tests/test_transient.py`; see `runs/run3/twin/pytest_run4.log`. Transient figure generation: `python runs/run3/twin/plot.py`; see `runs/run3/twin/plot_run3.log`.

## Completed grid results

Boundary: **SIM_ASSUMED_PROFILE**; counts are violation episodes accumulated across simulated windows and truncated at collapse. Each size must eliminate the stated violation and avoid collapse in every screened instance. The first zero-violation pair in ascending AFE then link order is shown; this ordering is not a cost optimum.

| Method | Default-grid violation episodes by type | Smallest AFE kW / link A with zero violations |
|---|---|---|
| B2 | undervoltage: 18, overvoltage: 0, overcurrent: 22, direct_power: 0, afe_import: 33, afe_export: 0, ramp: 77, collapse: 18 | none in grid / none in grid |
| B1p-OPT | undervoltage: 20, overvoltage: 0, overcurrent: 23, direct_power: 0, afe_import: 44, afe_export: 2, ramp: 192, collapse: 18 | none in grid / none in grid |
| P0 | undervoltage: 19, overvoltage: 0, overcurrent: 18, direct_power: 0, afe_import: 20, afe_export: 0, ramp: 225, collapse: 18 | none in grid / none in grid |
| ORACLE | undervoltage: 18, overvoltage: 0, overcurrent: 18, direct_power: 0, afe_import: 21, afe_export: 0, ramp: 229, collapse: 18 | none in grid / none in grid |
| uncoordinated burst | undervoltage: 0, overvoltage: 18, overcurrent: 18, direct_power: 0, afe_import: 0, afe_export: 18, ramp: 18, collapse: 0 | none in grid / none in grid |

| Method | Violation type | Smallest AFE kW / link A eliminating type |
|---|---|---|
| B2 | undervoltage | none in grid |
| B2 | overvoltage | 80 / 80 |
| B2 | overcurrent | 80 / 160 |
| B2 | direct_power | 80 / 80 |
| B2 | afe_import | 80 / 80 |
| B2 | afe_export | 80 / 80 |
| B2 | ramp | none in grid |
| B2 | collapse | 80 / 80 |
| B1p-OPT | undervoltage | none in grid |
| B1p-OPT | overvoltage | 80 / 80 |
| B1p-OPT | overcurrent | 80 / 160 |
| B1p-OPT | direct_power | 80 / 80 |
| B1p-OPT | afe_import | 80 / 80 |
| B1p-OPT | afe_export | 80 / 80 |
| B1p-OPT | ramp | none in grid |
| B1p-OPT | collapse | 80 / 80 |
| P0 | undervoltage | none in grid |
| P0 | overvoltage | 80 / 80 |
| P0 | overcurrent | 80 / 160 |
| P0 | direct_power | 80 / 80 |
| P0 | afe_import | 80 / 80 |
| P0 | afe_export | 80 / 80 |
| P0 | ramp | none in grid |
| P0 | collapse | 80 / 80 |
| ORACLE | undervoltage | none in grid |
| ORACLE | overvoltage | 40 / 80 |
| ORACLE | overcurrent | 40 / 160 |
| ORACLE | direct_power | 40 / 80 |
| ORACLE | afe_import | 80 / 80 |
| ORACLE | afe_export | 40 / 80 |
| ORACLE | ramp | none in grid |
| ORACLE | collapse | 40 / 80 |
| uncoordinated burst | undervoltage | 20 / 80 |
| uncoordinated burst | overvoltage | 40 / 80 |
| uncoordinated burst | overcurrent | 20 / 160 |
| uncoordinated burst | direct_power | 20 / 80 |
| uncoordinated burst | afe_import | 20 / 80 |
| uncoordinated burst | afe_export | 40 / 80 |
| uncoordinated burst | ramp | none in grid |
| uncoordinated burst | collapse | 20 / 80 |

Absence of a later type after collapse is not evidence that it would be absent in a non-collapsing replay; use the zero-violation column for a complete screening approval. Command: `python -u runs/run3/twin/screen.py`; outputs: `runs/run3/twin/screen_run4.log`, `results.json`, `violations.csv`, and `sizing.csv`.

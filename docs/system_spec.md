# ReGenATE system specification v1 (contract for all workers)

Owner: lead. Changes only by the lead. Version 1, 2026-11-24.

## 1. Scope
One long-duration test cell (mentor M02). N similar stations (4–32), each =
station supply -> DUT -> regenerative load. Decision = start time (and station among
eligible ones) inside an allowed window. Recipe, stress level, duration, protection are fixed
inputs (C04–C06). Speed changes from the CMC model are NOT a ReGenATE decision.

## 2. Time and units
- Internal step `dt_h` (hours, float, from config; default 1/60 h = 1 min for energy; scheduler
  slot `slot_min` default 15 min). Power kW, energy kWh, voltage V, current A, time in hours
  unless the column name says `_min` or `_s`.
- Sign: all power columns are >= 0 magnitudes; direction is in the column name
  (`p_import_kw`, `p_export_kw`). Never encode direction by sign in parquet files.

## 3. Measurement points (standardised, replaces slide 10/11 naming)
| ID | Location | Quantities |
|---|---|---|
| M0 | AC boundary of the test cell | import kW, export kW, kWh, peak kW |
| M1 | shared DC link | V_bus, I_bus, P_bus |
| M2a | DUT input per station | V, I, P_in |
| M2b | DUT output / regen-load input per station | V, I, P_rec |
| M3 | thermal / auxiliary loads (chamber, HVAC) | T, P_aux |
| M4 | MES/ATE interface | recipe, state, start/end events (no electrical sensor) |

## 4. Station power model (per station s, step k)
- `p_in`  : power the station supply delivers to the DUT (M2a).
- `p_rec` : DUT output absorbed by the regen load (M2b). Physical rule: for a converter DUT
  `p_rec <= eta_dut * p_in` at every step (never more out than in). For an energy-storage DUT
  (battery/supercap, DS03 EDC / DS05) `p_rec > 0` only in discharge phases where `p_in = 0`.
- `p_aux` : chamber/fans/controls drawn from AC (M3).
- Converter efficiencies (curves vs load fraction, DS03/datasheet, else ASSUMED constants):
  `eta_sup` supply (bus/AC -> DUT), `eta_rl` regen load (DUT output -> its output bus),
  `eta_afe_exp` DC->AC, `eta_afe_imp` AC->DC, `eta_link` DC path between stations.

## 5. Topologies (energy ledger, implemented only in `regenate.electrical.ledger`)
At each step, all terms are brought to the same boundary before netting.
- **B0 no recovery**: regen energy dumped as heat. AC load = sum(p_in/eta_sup_ac + p_aux)
  + HVAC = heat/COP (COP ASSUMED). import = load, export = 0.
- **B1 regen-to-AC**: each regen load returns `p_rec*eta_rl_ac` to the cell AC bus. Netting
  behind M0 is physical and 1:1: L = sum(p_in/eta_sup_ac + p_aux) - sum(p_rec*eta_rl_ac);
  import = max(L,0), export = max(-L,0). (Legacy code treated all return as export x alpha:
  wrong when the cell is net importing.)
- **B1p in-rack reuse**: station's own recovered power feeds its own supply first:
  m_s = min(p_rec*eta_self, p_in/eta_sup_dc); the remainder of both sides goes through AC as in B1.
- **DC shared link**: supplies and regen loads of all stations on one DC bus.
  direct = min(sum p_rec*eta_rl_dc, sum p_in/eta_sup_dc, P_link_max) (one conversion, `eta_link`);
  shortfall imported via AFE (`/eta_afe_imp`), surplus exported via AFE (`*eta_afe_exp`) or dumped
  when export is not allowed / AFE limit reached (chopper, reported as `dump_kwh`).
- Optional `in_rack_first` flag for DC: in-rack reuse before link sharing (realistic hybrid).
- Outputs per run: `import_kwh, export_kwh, net_kwh = import-export, peak_import_kw,
  direct_reuse_kwh, recoverable_kwh, loss_kwh, dump_kwh, hvac_kwh`. Export credit `alpha_ex` and
  tariffs are applied ONLY in `regenate.economics`, never inside the ledger.

### Ledger invariants (tests ELEC-01..09, `tests/test_ledger.py`)
01 energy balance per step: inputs = outputs + losses (|err| < 1e-9 relative);
02 losses >= 0; 03 no energy without source; 04 idle/zero load -> only aux/idle;
05 AFE import/export <= P_afe_max (excess -> dump or violation flag); 06 direct <= P_link_max;
07 in-rack reuse <= own demand; 08 no double counting (direct + exported + dumped + lost =
recoverable); 09 equal efficiencies & no cap => DC shared == B1p when every station's
own demand >= own recovery at every step (theory).

## 6. Baseline ladder (IDs used in every CSV)
| ID | Topology | Schedule | Forecast |
|---|---|---|---|
| B0 | none | FIFO | - |
| B1 | AC | FIFO | - |
| B1-OPT | AC | optimized (same optimizer, AC ledger) | true |
| B1p | in-rack | FIFO | - |
| B1p-OPT | in-rack | optimized | true |
| B2 | DC | FIFO | - |
| B3 | DC | static one-shot, nominal profile | nominal |
| P0 | DC | rolling, nominal/statistical forecast | F00/F01 |
| P | DC | rolling, learned forecast | F05/F06 |
| ORACLE | DC | perfect foresight (exact on small n, else gap reported) | true |
Same instance, realised traces, constraints, horizon and compute budget for P and P0.

## 7. KPIs (`regenate.evaluation.metrics`)
S_B1 = (E_B1 - E_P)/E_B1 (only if E_B1 > 0, else absolute kWh); dE_AI = E_P0 - E_P;
dE_oracle = E_P - E_ORACLE; gap_closed = (E_P0 - E_P)/(E_P0 - E_ORACLE) when denominator > 0;
R_match = direct_reuse / recoverable; peak kW; TT, makespan, completed jobs, violations,
solve time. Comparisons are paired by instance; report mean, median, std, paired diff with
95 % CI (bootstrap over instances, 10 000 resamples, seed 0). Statistical unit = instance/run.
kWh comparisons only at equal TT (lexicographic), or report TT alongside.

## 8. Data products (parquet unless noted; every file has a provenance column or sidecar)
| File | Key columns |
|---|---|
| data/processed/ds01_jobs.parquet | instance_id, job_id, release_h, due_h, size, p_stage{1..4}_*, provenance |
| data/processed/ds01_stations.parquet | instance_id, stage, machine_id, capacity, p_run_kw, p_idle_kw |
| data/processed/efficiency_points.parquet | device, direction, v_dc, load_frac, p_out_kw, eta, source_file, page, provenance |
| data/processed/ds02_bus.parquet | dataset, ts, v_bus, i_bus, p_kw, state, provenance |
| data/processed/ds04_machines.parquet | company, asset, ts, status, power_kw, cycle_time_s, split |
| data/processed/ds05_cycles.parquet | cell_id, ts, step, phase(charge/discharge/rest), v, i, p_kw |
| data/generated/<bench>/... | generator output (WP04, spec later) |
| data/processed/provenance.json | per file: source path, url, license, units, transforms, label |
Provenance labels: MEASURED, DATASHEET, DERIVED, SYNTHETIC, ASSUMED.
Evidence labels for results: `.claude/rules/evidence-integrity.md`.

## 9. Layout and ownership
`src/regenate/<pkg>` modules; `tests/test_<module>.py`; reports in `reports/<area>/`.
Raw data folders (DS01..DS05, predict_ai_electrics, doc/ref) are read-only. DS01_Quanh/code is
the frozen legacy reference (import it read-only via sys.path, never edit).
Run everything from repo root with `python -m pytest` (pytest.ini sets pythonpath=src).

## 10. Result files (written by regenate.evaluation.runner, read by app/ and reports)
`runs/<campaign>/results.csv` one row per (instance_id, method):
instance_id, scenario, n_jobs, n_stations, seed, split, method, topology, TT_h, makespan_h,
completed_jobs, violations, import_kwh, export_kwh, net_kwh, peak_import_kw, direct_reuse_kwh,
self_use_kwh, recoverable_kwh, dump_kwh, loss_kwh, solve_s, mip_gap, boundary.
`runs/<campaign>/schedules.parquet`: instance_id, method, job_id, station, start_h, end_h, shift_h.
`runs/<campaign>/timeseries.parquet`: instance_id, method, t_h, p_import_kw, p_export_kw,
direct_kw, self_use_kw, recoverable_kw, dump_kw.
`runs/<campaign>/manifest.json`: config, git-free code hash (sha256 of src/), command, timestamps.


## Run 4

P0-BILL extends the lexicographic P0 engine with facility-plus-cell billed demand as the final level after tardiness and energy tolerance; background information may be persistence, historical profile or oracle. The causal evaluation is pending; perfect-background headroom is not deployable performance. Source: `reports/run4/p0_architecture.md`, `reports/run4/facility_billing.md`.

E1 assumes AFE import 20 kW, bus throughput 32 kW and slot step 10 kW; the dynamic twin is an assumed-parameter screen, not protection qualification. Boundary SIM_DATA_PROFILE, hardware NOT_VERIFIED. Source: `reports/run3/e1_electrical_constraints.md`, `reports/run3/electrical_feasibility.md`.

Facility billing adds a simulated DS06 cell to measured DS07 facility load without synchronization. Tariffs are geographic counterfactuals; the registry distinguishes TNB ToU peak eligibility from the unverified general-tariff rule and records missing interval, export and adjustment details. Source: `reports/run4/facility_billing.md`, `reports/run4/tariff_registry.md`.

AI path A provides advisory cycle ETA and availability; path B provides advisory deviation monitoring; path C tests production planning with forecast durations. ETA accuracy does not establish downstream value; monitoring and WP-C acceptance failed, so automatic scheduling remains optimization-only. Source: `reports/run4/ai_eta.md`, `reports/run4/ai_monitoring.md`, `reports/run4/ai_production_planning.md`.

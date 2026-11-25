# Run 4 WP-A — P0 architecture and value of information (mentor M09, M10, M12, M14)

## P0 as implemented (code is the source of truth)
| Element | Implementation | File |
|---|---|---|
| Decision variables | binary start slot per not-yet-started job (one start in its window); per-slot LP energy flows of the shared DC topology: direct link transfer, AFE import, AFE export, dump; tardiness per job; peak / billed-demand variable in the third level | `src/regenate/optimization/milp.py::solve` |
| Information | nominal recipe = previous cycle of the same module (`bench_v2.job_profile(..., "nominal")`) for every queued and running job; observed elapsed time and station of running jobs; no learned forecast (`ai_engine.make_profile_fn(variant="P0")` returns the recipe) | `forecasting/ai_engine.py`, `optimization/rolling.py` |
| Re-planning | every 15-min period and at events (job release/start/end) via SimPy `Replay`; cache key = (queued set, running profiles) -> unchanged information = no re-solve | `simulation/replay.py`, `rolling.py::Replanner.__call__` |
| Freeze / commitment | running and finished jobs are fixed (start = 0 in the sub-problem, remaining recipe profile); only not-started jobs are re-planned; engineer gate can reject a plan (previous plan kept) | `replay.py`, `rolling.py` |
| Objective hierarchy | (1) total tardiness, (2) net grid energy at M0 within TT <= TT* , (3) optional peak import (P0-Peak) or billed demand of facility + cell (P0-BILL) within energy <= E*(1+e_tol) | `milp.py` |
| Production constraints | release, latest start (deadline - duration, flexibility share of the max shift), station capacity per slot (interval-graph colouring), hard deadlines via window; due dates enter tardiness | `milp.py`, `v2_campaign.milp_jobs` |
| Electrical constraints (E1) | AFE import cap `P_afe_max`, link cap `P_link_max`, bus throughput `P_bus_max` (residual sink and source totals), slot-step cap `dP_step_max`; brute-force tested | `milp.py`, `tests/test_milp.py` |
| Solver | SciPy `milp` (HiGHS), 20 s per stage in campaigns; fallback widens windows to deadlines; infeasible -> keep previous plan | `milp.py`, `rolling.py` |
| Forecast integration | `profile_fn(jid, run_obs)` replaces the recipe profile of a job; the MILP is unchanged | `rolling.py`, `ai_engine.py` |

## Policy ladder (same instances, same ledger; DS06, SIM_DATA_PROFILE)
| Policy | net kWh / instance | peak kW | source |
|---|---|---|---|
| B3 static nominal optimisation | 8.55 | 11.60 | reports/ai/ai_exp12_ds06.md (n=100) |
| P0 event-driven rolling | 8.446 | 11.34 | run3 v2_diag (n=100) |
| P0-Peak | energy n.s. different, peak -3.9 % vs P0 | | reports/ai/ai_exp12_ds06.md (n=50) |
| P0-E1 | 8.890 (n=50 subset) | 10.96 | run3 v2_e1 |
| P0-E1-Peak (D006 default) | energy n.s. vs P0-E1; peak -3.67 kW vs B1p-OPT (-25.6 %) | | run3 v2_e1_peak |
| Rolling perfect information (TR_ALL) | = ORACLE exactly on 100/100 | | run3 v2_diag |
| One-shot ORACLE | 8.352 | 10.19 | run3 v2_diag |

## Value of information (queued jobs carry most of it), paired vs P0, n = 100
| Information given to the same rolling MILP | kWh saved vs P0 | TT saved h | what it contains |
|---|---|---|---|
| everything (TR_ALL) | +0.094 [+0.077, +0.112] | +0.048 | full true profiles of all jobs |
| queued jobs, full true profile (TR_Q) | +0.049 [+0.035, +0.064] | +0.048 | duration + energy + phase timing + within-cycle trajectory |
| queued jobs, true duration + true charge/discharge energy (PQ*) | +0.008 [-0.007, +0.022] n.s. | +0.048 | aggregates only, recipe shape time-warped |
| queued jobs, true duration only (PQd*) | -0.002 [-0.015, +0.012] n.s. | +0.048 [+0.017, +0.087] | length only, recipe energy |
| running jobs, full true profile (TR_RUN) | +0.024 [+0.013, +0.037] | +0.013 | remaining trajectory |
Decomposition of the queued-job value: duration -> all of the tardiness value, ~0 energy; + total energies -> ~16 % of the energy
value (n.s.); the remaining ~84 % needs the phase timing / within-cycle power trajectory (TR_Q - PQ*). Why aggregates are not enough:
the shared-DC gain comes from overlapping one station's residual SOURCE phase with another's SINK phase; a uniformly warped recipe
with the right total length and energy still puts the phases at the wrong slots, so the overlap it plans is not the one that happens.

## Forecast-integration audit
Run 2 defect (3-horizon interpolation + elapsed-indexed tail; perfect inputs captured 0 % or less): reproduced and documented in
reports/run3/root_cause_analysis.md. Run 3/4 integrations (P5 phase-aligned, PQ/PQ5 warped cycle forecasts, PQd duration-only) are
exact in the PERFECT case where they should be (PQ*/PQd* reproduce the full tardiness value of TR_Q), so the remaining loss is the
learned forecast error, not the plumbing. Leakage audit: profiles of queued jobs use only the previous cycle (nominal) or a
cycle-level model on lagged features (`cycle_model.py`, tests forbid same-cycle features); running-job AI uses only bins < elapsed.
P0 has not been weakened in any comparison (same MILP, period, time limit, constraints).

## Status
P0 architecture documented; information headroom verified (0.094 kWh energy, 0.048 h tardiness per instance on DS06).

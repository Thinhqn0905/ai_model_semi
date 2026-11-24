# Benchmark generator report

Boundary: SIM_ASSUMED_PROFILE. DS01 abstract stage-3 duration and due dates mapped using ASSUMED unit_h; synthetic station power, phase power, station availability and events. DS03 EDC timing and observed sequence energy ratio are DERIVED; endpoints may differ in SOC, so ratio is not a closed-cycle efficiency. The DS03 transformer-side ratio is used as an assumed DUT-level proxy, not a measured DUT efficiency.

FIFO residual-source share = (r - u)/r, where r = p_rec * eta_rl_dc and u = min(p_in / eta_sup_dc, r), summed over stations and steps. Ledger self_use supplies u. Phase lengths use constrained largest-remainder rounding to max(ceil(duration / dt), number of nonzero phases) steps, with at least one step per nonzero phase (short jobs are extended to make this feasible); starts are on the step grid. Scheduler slots use nominal whole-slot duration and report mixed charge/discharge slots.

| Scenario | Runs | Mean share |
|---|---:|---:|
| S1 | 90 | 0.000000 |
| S2 | 90 | -0.000000 |
| S3 | 90 | 1.000000 |

Command: python -m regenate.data.generator --config configs/bench_v1.yaml
Output: data/generated/bench_v1/manifest.json
Recipe phase durations are synthetic rescaling of the first DS03 EDC sequence; the zero-duration rest is assumed because no rest was observed.
`nGate: 5 passed; data/generated/bench_v1/pytest_run2.txt (SIM_ASSUMED_PROFILE, software checks only). Short jobs are extended when fewer grid steps than active phases; strict duration preservation is infeasible for these jobs.

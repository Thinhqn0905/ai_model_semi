# Run 4 verification

## Production constraints

Boundary: SIM_DATA_PROFILE, DS06 instances using measured DS05 cycle profiles; sources: [campaign](../../src/regenate/evaluation/v2_campaign.py), [MILP](../../src/regenate/optimization/milp.py), and [raw binding manifest](../../docs/raw_binding_manifest.md). The one-shot MILP starts each job once within its release/latest window, limits concurrent jobs by station capacity, and first minimises total tardiness against a soft due date. The latest start is initially the minimum of deadline minus planned duration and the release plus permitted shift. However, `milp_jobs()` then raises it to at least the release and FIFO start; thus the deadline window is not unconditionally hard. Fixed rolling starts also bypass window construction. Predicted and true durations may differ. Identical interchangeable stations are assumed; station-specific eligibility is not represented.

The campaign uses the same instance, FIFO seed schedule, scoring path and electrical parameters across methods; one-shot methods call the same `milp_jobs()` and `solve()`, while FIFO uses `fifo()` and rolling uses `Replanner`/`Replay`, not the same MILP path. Thus identical enforcement and equal realised tardiness across every method are NOT_VERIFIED. The manifest explicitly reports higher rolling tardiness than one-shot; comparisons must use matched production or state this limitation.

Deadline counts per manifest file: **NOT_VERIFIED separately** wherever the manifest gives a combined or unspecified violation count. The following files have zero reported violations, hence zero reported deadline violations within that manifest accounting: `v2_flex025_n100.csv`, `v2_flex1/results.csv`, `v2_peak/results.csv`, `run3/v2_diag/results.csv`, the `run3/v2_p5`, `v2_pq_gated`, `v2_pq_ungated`, `v2_pqd`, `v2_pqstar` files, and `run4_rt3/v2_size_afe20_bus16`, `v2_size_afe20_bus24`, `v2_size_afe30_bus32`. For `run3/v2_e1`, `run3/v2_e1_peak`, `run4_rt2/v2_e1_peak_b`, `run4_rt2/v2_e1_peak100`, `run4/v2_wpc_gated`, `run4/v2_wpc_ungated`, `run4_rt3/v2_size_afe10_bus32`, `v2_size_afe15_bus32` and `v2_size_afe15_bus24`, deadline-only counts are not broken out; reported AFE shortfalls must not be relabelled deadline misses. Source: [manifest](../../docs/raw_binding_manifest.md), DS06 campaign table. These are manifest-reported counts, not independently inspected raw files.

## Multi-cell feasibility

Boundary: SIM_DATA_PROFILE cells plus unsynchronised MEASURED DS07 facility loads; [facility report](facility_billing.md) and [facility code](../../src/regenate/evaluation/facility.py). Each cell uses separately scheduled DS06 instances; E1 feasibility is per instance and is not universal for every policy or sizing, as the manifest records violations and infeasibilities. Facility simulation places successive workload blocks per cell and sums cell traces at the meter. The default block length covers the longest saved trace; `place()` itself does not enforce overlap despite its docstring, and custom block lengths and billing-generated traces are not proven non-overlapping. Different cells may run simultaneously. Cross-cell electrical coupling is not modelled; separate AFEs per cell are assumed. Billing-aware sequential multi-cell scheduling was only tested in the P0-BILL five-cell cases, not a joint centralised multi-cell MILP; it performed worse in those cases ([facility report](facility_billing.md), extended P0-BILL section). Site feasibility is NOT_VERIFIED.

## Solver scalability

Boundary: SIM_DATA_PROFILE DS06; lead-reported Colab timings, 2026-11-25, for `ai_runs/run4_rt2/v2_e1_peak100/results.csv` and `ai_runs/run3/v2_diag/results.csv` (raw files bound in [manifest](../../docs/raw_binding_manifest.md)); the timing aggregation itself is NOT_VERIFIED locally. These are elapsed seconds per instance; P0 includes all replans. Instance size: 10 jobs, 8 stations, 15-minute slots; 200 rows across the two datasets. Source: lead's R6 task measurement.

| Method | Mean s | Median s | Max s |
|---|---:|---:|---:|
| ORACLE | 3.52 | 1.98 | 29.18 |
| B1p-OPT | 0.06 | 0.05 | 0.17 |
| P0 | 9.61 | 5.44 | 131.91 |
| TR_ALL | 2.68 | 2.50 | 7.44 |

The manifest records one-shot optimal gap zero except flex 1.0 (ORACLE 17/26 and B3 18/26 time-limit incumbents), B3 one infeasible in the flex 0.25 ladder, and AFE-10 ORACLE 3/30 infeasible. Source: [manifest](../../docs/raw_binding_manifest.md); SIM_DATA_PROFILE. Larger job or station counts have not been tested here; these timings do not establish production-scale runtime or feasibility.

## FIN-B cost sensitivity

Boundary: SIM_DATA_PROFILE cells + unsynchronised MEASURED DS07, assumed annualisation and FX; site costs and tariff applicability NOT_VERIFIED. The [missing-cost sensitivity table](economics_run4.md#missing-cost-sensitivity--derived) specifies payback and discounted NPV for additional upfront cost, excluding recurring support. Its displayed rounded annual net and known site CAPEX of USD 4,220 produce the following additional-upfront-cost ceilings, derived as `years × annual net − 4,220` (negative means the target is already unmet at zero extra cost). These are not site investment approvals; unquantified support reduces the ceilings.

| MV tariff; cells | 3-year ceiling USD | 5-year ceiling USD |
|---|---:|---:|
| General; 1 | -2,768 | -1,800 |
| General; 3 | -1,076 | 1,020 |
| General; 5 | -56 | 2,720 |
| General; 10 | 6,226 | 13,190 |
| ToU; 1 | -2,930 | -2,070 |
| ToU; 3 | -1,706 | -30 |
| ToU; 5 | -356 | 2,220 |
| ToU; 10 | 4,993 | 11,135 |

Source: [FIN-B results and sensitivity](economics_run4.md), derived from displayed rounded annual values; thresholds may differ slightly from calculations on underlying unrounded results. HV values by cell count are not supplied in the displayed table; their additional-cost ceilings remain NOT_VERIFIED.

## Acceptance boundary

Simulation acceptance concerns only the reported DS06 model and its recorded exceptions; it does not certify every schedule or electrical configuration. Site acceptance is NOT_VERIFIED: actual production constraints, hardware protection, cross-cell electrical design, synchronised facility load, tariffs and missing installation, requalification and support costs require site evidence. Sources: [E1 report](../run3/e1_electrical_constraints.md), [facility report](facility_billing.md), [economics](economics_run4.md), [manifest](../../docs/raw_binding_manifest.md).

Gate check: PASS — report exists and four required sections present; boundary DOCUMENT_STRUCTURE. Command: PowerShell Test-Path and section membership; output: reports/run4/verification_run4.md (this line).

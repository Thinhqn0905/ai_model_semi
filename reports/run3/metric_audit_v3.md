# Run 3 metric audit v3

Boundary: SIM_ASSUMED_PROFILE for bench_v1 computations; LOCAL_RUN on MEASURED DS05 for Branch C; remote DS06 is NOT_VERIFIED locally. This is an incomplete audit; do not promote its numbers as validated site results.

## 1. Manifest and provenance

OK — `runs/run3/manifest_run2.json` inventories the task-named campaign directories, their CSV hashes, available seeds, instance counts, methods, embedded arguments and recorded boundaries. Infinities in old manifests are represented as strings for strict JSON. `runs/run3/audit/run.log` records the generation run.

NOT_VERIFIED — Commands and claim-level report bindings are frequently absent in original manifests. The manifest explicitly records these gaps. It does not claim a repository-wide inventory; only directories named by this task were searched. DS06 inputs are REMOTE, recomputed by lead on Colab, not locally re-verifiable; CQR inputs remain remote.

## 2. Report number reconciliation

Comparison uses the raw `runs/rolling_v1/ladder.csv`, instance-paired bootstrap, and equal tardiness where specified. Full computed comparison table: `runs/run3/audit/rolling_recomputed.csv`; boundary SIM_ASSUMED_PROFILE.

| Claim | Report value | Recomputed value | Match |
|---|---:|---:|---|
| `reports/benchmark/rolling_v1.md` equal-TT B1 vs B0 | 242.9 kWh [214, 271.2] | 242.8873 [214.0137, 271.2275] | yes, rounding |
| `reports/benchmark/rolling_v1.md` equal-TT P0 minus P | -0.4260 kWh [-0.6032, -0.2575] | -0.4260 [-0.6032, -0.2575] | yes, rounding |
| `reports/benchmark/rolling_v1.md` equal-TT P minus ORACLE | 0.5596 kWh [0.3605, 0.7716] | 0.5596 [0.3605, 0.7716] | yes, rounding |

NOT_VERIFIED — All other headline figures across AI, benchmark and economics reports have not yet been individually reconciled. In particular, the DS02/DS04 forecast tables and `reports/benchmark/p_vs_p0_diagnosis.md` cite sources outside the explicitly named data paths; DS06 and CQR are remote. Branch C local metric CSV and business-case local CSV exist, but their claim-by-claim recomputation is outstanding. No match is inferred merely from a report citing a CSV.

## 3. Units, signs and pairing

OK — `src/regenate/electrical/ledger.py:52` rejects negative power; `:82` treats recovered power as source, `:109` integrates kW by hours into kWh, and `:111` computes net import minus export. `:83-92` removes in-rack reuse before shared transfer and subtracts direct transfer from both residuals, avoiding the indicated double count in the code path. Slot sizes must be converted to hours (`src/regenate/evaluation/oracle_campaign.py:38-44`). This is source review, not a new physical validation.

ISSUE — `src/regenate/evaluation/stats.py:19` pivots by instance alone using `aggfunc="first"`; repeated instance/method rows from different flex, profile or seeds can silently collapse. Filter and assert uniqueness on the complete experiment key before pivoting. In the inspected rolling_v1 ladder, `runs/run3/audit/pairing.json` records zero duplicate keys and 36 paired IDs for each of the nine comparisons; this does not prove matched bus settings or identical realized tardiness. Equal-TT filtering is implemented at `src/regenate/evaluation/stats.py:43`.

## 4. Oracle fairness

ISSUE — `src/regenate/evaluation/oracle_campaign.py:108` uses one-shot optimization with truth profiles and capacity; `src/regenate/optimization/rolling.py:94` replans with rolling profiles and fixed running jobs. ORACLE versus P0 is NOT an information-only matched pair. Objective is lexicographic TT then energy, with optional peak third (`src/regenate/optimization/milp.py:164-194`); a time-limited first stage can make the following stages conditional on an incumbent. Rolling windows, downtime treatment and solve budgets differ as documented in `reports/benchmark/rolling_v1.md:167` and `reports/benchmark/rolling_flex.md:19`. Recommend matched rolling truth, running-only truth, and queued-only truth with identical constraints and budget.

NOT_VERIFIED — Per-comparison equality of all workloads, profile versions, electrical limits and production constraints has not been established. `stats.COMPARISONS` pairs instance identifiers but does not enforce these attributes (`src/regenate/evaluation/stats.py:35-50`). P0 versus P is an information comparison only if those other controls are demonstrably identical. Other ladder comparisons also change topology, scheduling or both.

## 5. Solver outcomes

OK — Per-file, per-method status counts, explicit time-limit messages, nonmissing gap counts and positive-gap shares are in `runs/run3/audit/solver_counts.json` (SIM_ASSUMED_PROFILE where recorded). A time-limited solution is an incumbent. For `runs/oracle_v1/results.csv`, ORACLE has 134 reported optimal statuses and 28 explicit time limits; 35/162 recorded gaps are positive. B3 has 111 optimal, 29 time limits and 22 infeasible TT-stage statuses; 34/140 recorded gaps are positive. These are rows across flex settings, not 162 independent instance IDs.

ISSUE — `src/regenate/optimization/milp.py:169-199` returns the energy-stage status and gap; first-stage status and optional peak-stage gap are not propagated as overall optimality. It also replaces missing gaps with zero. Record all stage statuses and gaps and never use missing as zero. Rolling rows without status/gap cannot establish optimality or count all time-limit hits; non-solver FIFO zero gaps are not solver proof.

## 6. Disposition and recommendations

ISSUE — `reports/ai/ai_exp12_ds06.md:27` labels ORACLE minus P0 as perfect-forecast headroom although one-shot versus rolling changes the planning setup too. Relabel descriptive ceiling and execute matched rolling truth experiments.

NOT_VERIFIED — Complete the report-by-report raw-CSV reconciliation, including all local headline figures and the business case; provide precise claim-to-source bindings and complete per-comparison fairness analysis. Fetch the remote DS06/CQR inputs or retain remote status. Verify bus excursions separately: these CSV checks do not validate hardware, site performance, or safety.

### Additional local reconciliation (Run 2 continuation)

OK — `runs/run3/audit/claim_reconciliation.csv` contains the reported Branch C model skill and coverage cells, independently recomputed from local model MAEs and coverage, plus the business-case equal-TT sample counts, means and t intervals recomputed from individual `runs/rolling_v1/ladder.csv` rows. Boundary: LOCAL_RUN on MEASURED DS05 for forecast metrics; SIM_ASSUMED_PROFILE for economics. The generated CSV identifies the claim, reported value, recomputed value, and match. `runs/run3/audit/reconciliation.log` records the run. These matches do not validate the underlying measured data, model split, or financial assumptions.

NOT_VERIFIED — The task requires all headline figures; this table does not yet cover every local headline in the benchmark and economics reports, nor DS02/DS04 or diagnostic source CSVs. Several cited sources fall outside the task-named input paths. DS06 results are REMOTE, recomputed by lead on Colab; no remote values are treated as locally verified. CQR inputs remain remote. Branch C sample counts and the 73/87/261-minute MAEs remain unreconciled. Monetary columns have not been independently recalculated. The listed output is a partial audit, not a completed gate.

### Comparison-specific fairness matrix

Source review: `src/regenate/evaluation/stats.py:23`, `src/regenate/evaluation/oracle_campaign.py:108`, `src/regenate/evaluation/rolling_campaign.py:26`, `src/regenate/evaluation/v2_campaign.py:19`, `src/regenate/optimization/rolling.py:94`, and `src/regenate/optimization/milp.py:60`. FIFO has no optimization objective; optimized methods use TT then energy, with optional peak third. All use the simulation ledger, but matching instance IDs alone does not establish identical solver constraints, realized tardiness or electrical limits.

| Comparison | Topology, scheduling and information differences | Fairness finding |
|---|---|---|
| B0 vs B1 | FIFO, same workload; no recovery vs AC recovery | NOT_VERIFIED: instance pairing checked, complete configuration binding unproven. |
| B1 vs B2 | FIFO; AC vs shared DC | NOT_VERIFIED: same limitations, topology changes. |
| B2 vs B3 | shared DC; FIFO vs one-shot nominal MILP | NOT_VERIFIED: scheduling and information change; TT must be matched. |
| B3 vs P0 | DC; one-shot nominal vs rolling recipe | ISSUE: `src/regenate/optimization/rolling.py:94` replanning and constraints differ; not an information-only comparison. |
| P0 vs P | DC rolling recipe vs rolling learned estimator | NOT_VERIFIED: same code path intended; instance pairing alone cannot establish all settings and TT. |
| B1-OPT vs P | AC one-shot truth vs DC rolling learned | ISSUE: `src/regenate/evaluation/oracle_campaign.py:108` topology, planning, information and budget differ. |
| B1p-OPT vs P | in-rack one-shot truth vs DC rolling learned | ISSUE: `src/regenate/evaluation/oracle_campaign.py:108` topology, planning, information and budget differ. |
| P vs ORACLE | DC rolling learned vs DC one-shot truth | ISSUE: `src/regenate/evaluation/oracle_campaign.py:108` and `src/regenate/optimization/rolling.py:94`; not information-only. |
| B1p-OPT vs ORACLE | in-rack vs DC; both one-shot truth | NOT_VERIFIED: objective and workload intended matched, solver incumbents and physical constraints require review. |
| P0 vs ORACLE | DC rolling recipe vs one-shot truth | ISSUE: `src/regenate/evaluation/v2_campaign.py:19` and `:61`; NOT an information-only matched pair. |
| P0 vs P1 | common rolling configuration, P1 power forecast | NOT_VERIFIED: DS06 CSVs remote; paired instance and equal-TT checks pending. |
| P0 vs P2 | common rolling configuration, P2 duration forecast | NOT_VERIFIED: DS06 CSVs remote; paired instance and equal-TT checks pending. |
| P0 vs P3 | common rolling configuration, P3 joint forecast | NOT_VERIFIED: DS06 CSVs remote; paired instance and equal-TT checks pending. |
| P0 vs P4 | common rolling configuration, P4 joint P90 duration | NOT_VERIFIED: DS06 CSVs remote; paired instance and equal-TT checks pending. |

ISSUE — `src/regenate/optimization/milp.py:11` models downtime as aggregate capacity, while `src/regenate/optimization/rolling.py:94` does not supply the same capacity constraint; electrical bus caps are not established as hard scheduling constraints. Recommend identically constrained rolling truth and recipe experiments and independently verify solver stages, time budgets and realized TT before causal attribution.

### Run 3 continuation: reproducibility and cross-report checks

OK — `runs/ds05_local_build.log:7` records 14,755 cycles and 2 errors (local rebuild; MEASURED DS05). The lead reports the matching Colab build in `reports/run3/root_cause_analysis.md:16`; its remote output is NOT_VERIFIED locally.

NOT_VERIFIED — The lead reports Branch C retraining identical for 55/55 metrics and DS06 P0/B1p-OPT/ORACLE/B1 reproducing Run 2 to three decimals; the underlying remote retraining and Run 2 precision are not locally available for independent verification. `reports/run3/root_cause_analysis.md:31` gives the four Run 3 means and only two-decimal Run 2 values. The lead reports all 200 one-shot MILPs optimal at gap 0 (`reports/run3/root_cause_analysis.md:32`); REMOTE, recomputed by lead on Colab, SIM_DATA_PROFILE, not locally re-verifiable. This statement does not apply to rolling solvers or other campaigns.

OK — The locally available Branch C remaining-duration MAEs were checked against model_metrics.csv; see `runs/run3/audit/branch_c_mae_check.csv` and `runs/run3/audit/run3_check.log` (LOCAL_RUN on MEASURED DS05).

OK — Shared DS06 claims reviewed: P0 versus rolling truth 0.094 kWh and the 0.188 versus 0.140 h tardiness figures agree between `reports/run3/root_cause_analysis.md:38` and `reports/run3/ai_run3.md:66` and `:69`; `reports/run3/mentor_compliance_audit.md:127` agrees for 0.094 kWh. The E1 50-instance and economics equal-TT subsets differ from the 100-instance diagnostic; their values must not be treated as the same claim. These are report-consistency checks, not independent remote recomputation.

ISSUE — `reports/run3/economics_v3.md:15` says DS06 rows are pending while the same file reports completed DS06 results at `reports/run3/economics_v3.md:27`. Recommend removing or qualifying the stale pending statement.

NOT_VERIFIED — A complete cross-report audit of every DS06 numeric claim and complete raw-CSV reconciliation across all requested local report headlines remain outstanding; the partial matches above do not establish full coverage.

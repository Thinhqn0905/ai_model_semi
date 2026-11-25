## 13 Industrial applicability

Simulation acceptance is limited to the stated evidence and gates; industrial site acceptance has not been performed.

D018 fixes the reference as a Chroma 17020-type regenerative battery module cycling cell, rated 48 kW/cell; DS06 assumes 8 stations, 25 modules/station at 0.24 kW/module, 20 kW AFE, 32 kW link and 10 kW step. These are ASSUMED simulation settings, not vendor specifications; baseline and CI not applicable, n not applicable (`docs/decisions.md`, D007/D018; `reports/final/report_run4.md`; raw configuration binding NOT_VERIFIED). Chroma documents independent charge/discharge channels, reuse to charging channels or mains, recipes and protection (VENDOR_REPORTED; `reports/run4/vendor_reference.md`). Internal bus topology, external access and scheduling rights are NOT_VERIFIED.

Bidirectional DC-DC, battery-emulator, power-module cycling, storage and EV power-conversion testing are conditional transfer candidates. Each needs independently timed residual source and sink at the station boundary after local reuse; a bidirectional DUT alone is insufficient. Converter burn-in has no residual under the D001 assumptions (`reports/run4/industrial_use_case_matrix.md`; `docs/decisions.md`). Site validation needs synchronized signed station and facility metering, movable start windows, converter curves, vendor interface rights, quality records, tariffs, protection study and costs (`reports/run4/mentor_data_request.md`). Semiconductor applicability and site acceptance remain NOT_VERIFIED.


| Candidate | Eligibility and missing evidence |
|---|---|
| Battery module cycling | Reference; site residual phases, reuse, windows and mentor acceptance NOT_VERIFIED. |
| Bidirectional DC-DC validation | Conditional; net station traces after local reuse and independent windows needed. |
| Battery-emulator power electronics | Conditional; meter both net phases and document setup and starts. |
| Power-module cycling | Conditional; DUT topology, residual traces and independent starts needed. |
| Energy-storage module testing | Conditional; boundary traces, actual equipment and reuse needed. |
| EV power conversion | Conditional; net phases, topology and test constraints needed. |
| Converter burn-in | Ineligible under D001 assumptions; measured exceptions require review. |

Source and boundary: `reports/run4/industrial_use_case_matrix.md`, `docs/target_cell_spec.md`; site NOT_VERIFIED; vendor descriptions VENDOR_REPORTED.

## 14 Product readiness

Simulation acceptance is limited to the stated evidence and gates; industrial site acceptance has not been performed.

The software-first deployment paths are FIN-A existing regen-to-AC, FIN-B existing compatible shared-energy infrastructure, and FIN-C full retrofit; FIN-B is preferred subject to site evidence (`docs/decisions.md`, D009/D018). The default is P0-E1-Peak with independent protection and twin screening; forecasting is advisory (`docs/decisions.md`, D006/D010/D012). Ledger, scheduler and simulation are documented in `src/regenate/electrical/ledger.py`, `src/regenate/optimization/milp.py`, `src/regenate/optimization/rolling.py`, and `src/regenate/simulation/replay.py` (`reports/run3/metric_audit_v3.md`). The file-backed dashboard provides facility load, tariff inputs, monthly charge estimates, FIN comparison and Markdown export; no live integration is established (`reports/run4/demonstrator_v2.md`). Dashboard screenshots are reported at `reports/run4/screenshots/` (final figure status in part 1); independent local inspection NOT_VERIFIED.

Offline demonstration: pipeline versus B1, n=1, net grid 10.086 versus 13.972 kWh, peak 13.429 versus 13.977 kW, equal tardiness 0 h, 10 completed jobs each and zero reported violations; CI unavailable, SIM_DATA_PROFILE. The source report has no exact raw-result path, so raw binding is NOT_VERIFIED (`reports/run3/demonstrator.md`). Failure injection reports invalid forecasts fall back to nominal and rejection executes FIFO; its test output is `runs/run3/fail/pytest_fail2_run2.log`, SIM_ASSUMED_PROFILE (`reports/run3/failure_injection_v2.md`). Solver stage status and missing gaps, matching, and dynamic protection remain unresolved (`reports/run3/metric_audit_v3.md`, `reports/final/report_run4.md`).


| Failure scenario | Simulation behavior and raw evidence |
|---|---|
| Solver timeout | Accepted plan retained; `runs/run3/fail/solver_timeout.json`. |
| Invalid AI / exception | Nominal fallback matched P0; `runs/run3/fail/ai_invalid.json`. |
| Nonfinite AI power | Finite nominal fallback; `runs/run3/fail/ai_nan.json`. |
| Engineer rejects | Initial FIFO executed; `runs/run3/fail/engineer_reject_all.json`. |

Boundary SIM_ASSUMED_PROFILE; `reports/run3/failure_injection_v2.md`. These checks do not establish physical safety.

## 15 Scientific evidence

Simulation acceptance is limited to the stated evidence and gates; industrial site acceptance has not been performed.

Reconciliation (SIM_DATA_PROFILE): baselines are matched by instance within each file; P0 rows match across the diagnostic and Run 3 forecast files. In the Run 2 ladder B3 has one infeasible tardiness-stage instance (99/100 optimal); flex 1.0 has time-limit incumbents for ORACLE 17/26 and B3 18/26, so the reported oracle saving is a lower bound, not a certified optimum: MyDrive/semiexpo/ai_runs/v2_flex1/results.csv (sha256 43b3f53afd3a6284). Rolling P0 has higher mean tardiness than one-shot methods (0.18?0.25 h versus 0.105?0.174 h); energy comparisons are not equal-production unless an equal-tardiness subset is stated. In the merged E1 run B2 has 13/100 violations, P0 1/100, and optimized one-shot 0; PQd has 2/100: MyDrive/semiexpo/ai_runs/run4/v2_wpc_gated (sha256 f346ca242945923d), MyDrive/semiexpo/ai_runs/run4_rt2/v2_e1_peak100/results.csv (sha256 57cd90452ba6e187).

DS06 replays measured DS05 battery cycles with assumed scaling and timing: SIM_DATA_PROFILE, not semiconductor-site data. The diagnostic uses seeds 0–99, n=100, paired bootstrap 95% intervals and Drive raw results `MyDrive/semiexpo/ai_runs/run3/v2_diag/results.csv`; manifest binding MyDrive/semiexpo/ai_runs/run3/v2_diag/results.csv (sha256 4a8d6b74b0c8a154) (`reports/run3/root_cause_analysis.md`, `reports/run3/metric_audit_v3.md`). Facility studies use factory-clustered paired bootstrap intervals on unsynchronized MEASURED DS07 and SIM_DATA_PROFILE cells; exact campaign paths `ai_runs/run4/fac_{gen,tou}_{3,5,10}cells` and `MyDrive/semiexpo/ai_runs/run4/fac_grid_tnb/` (`reports/final/report_run4.md`).

Negative evidence includes station AI energy and production failures, monitoring failure, no stable P0-BILL gain and withdrawn larger-pool effects; AI-BILL is NO-GO (section 5, D020; raw `MyDrive/semiexpo/ai_runs/run4_final_summary.md`) (`reports/final/report_run4.md`, `docs/handoff_run4.md`). The metric audit identifies incomplete raw reconciliation, possible pairing collapse, unequal tardiness and planning constraints, incomplete solver status and one-shot versus rolling oracle differences; no site savings, safety, FPY or water outcome is established (`reports/run3/metric_audit_v3.md`).


| Diagnostic method | Result versus P0, kWh saved [paired 95% CI] | Evidence |
|---|---|---|
| TR_ALL / ORACLE | 0.094 [0.077, 0.112] | `MyDrive/semiexpo/ai_runs/run3/v2_diag/results.csv` |
| TR_Q | 0.049 [0.035, 0.064] | same raw file |
| TR_RUN | 0.024 [0.013, 0.037] | same raw file |
| P1* | -0.005 [-0.017, 0.007] | same raw file |
| P2* | 0.000 [-0.009, 0.009] | same raw file |
| P3* / P4* | -0.009 [-0.022, 0.003] | same raw file |

All rows: n=100, SIM_DATA_PROFILE; perfect-information diagnostics are not deployable. Tardiness differs between methods; causal matching is NOT_VERIFIED (`reports/run3/root_cause_analysis.md`, `reports/run3/metric_audit_v3.md`).

| Learned / information method | Energy saved versus P0, kWh [paired 95% CI] | Result |
|---|---|---|
| P5 | -0.022 [-0.034, -0.010] | FAIL |
| P5s | -0.004 [-0.010, 0.004] | FAIL, interval includes zero |
| PQ gated | -0.019 [-0.036, -0.006] | FAIL |
| PQ5 gated | -0.034 [-0.052, -0.018] | FAIL |
| PQ ungated | -0.045 [-0.066, -0.026] | FAIL |
| PQ* perfect cycle ratios | 0.008 [-0.007, 0.022] | not significant |
| TR_Q perfect queued profiles | 0.049 [0.035, 0.064] | diagnostic ceiling |

All rows: n=100, SIM_DATA_PROFILE, `reports/run3/ai_run3.md`; raw MyDrive/semiexpo/ai_runs/run3/v2_p5 (sha256 08e1bf44), MyDrive/semiexpo/ai_runs/run3/v2_pq_gated (sha256 9a345636), MyDrive/semiexpo/ai_runs/run3/v2_pq_ungated (sha256 17331443), MyDrive/semiexpo/ai_runs/run3/v2_pqd (sha256 42be5793), MyDrive/semiexpo/ai_runs/run3/v2_pqstar (sha256 0b3e7234). Production AI and automated monitoring also failed their downstream gates (`reports/run4/ai_production_planning.md`, `reports/run4/ai_monitoring.md`; raw monitoring `MyDrive/semiexpo/ai_runs/run4/monitor/`).

## 17 Mentor compliance

Simulation acceptance is limited to the stated evidence and gates; industrial site acceptance has not been performed.

Statuses below are inherited concept-level assessments, not fresh passes; each evidence source and gap is documented in `reports/run4/mentor_compliance_run4.md`. PASS is a documentation/decision assessment, with raw-run path NOT_VERIFIED except where identified below; it does not authorize deployment.

| ID | Requirement | Status | Remaining gap |
|---|---|---|---|
| M01 | Coordination | PASS | Presentation review; SOURCE_REPORTED  Evidence: `docs/traceability.md`. |
| M02 | Compatible cell | BLOCKED | Semiconductor transfer and site access NOT_VERIFIED  Evidence: `reports/run4/industrial_use_case_matrix.md`. |
| M03 | Flexibility and energy | PARTIAL | Matched baseline and site flexibility NOT_VERIFIED  Evidence: `reports/run4/contribution_decomposition.md`. |
| M04 | Loss ledger | PARTIAL | Site curves and configuration binding NOT_VERIFIED  Evidence: `reports/run3/metric_audit_v3.md`. |
| M05 | Shadow and pilot | BLOCKED | Site and engineer acceptance missing  Evidence: `reports/run4/demonstrator_v2.md`. |
| M06 | Protection and compatibility | PARTIAL | Hardware study and vendor approval missing  Evidence: `reports/run3/electrical_feasibility.md`. |
| M07 | Grounded profiles | PARTIAL | Battery proxy is not semiconductor data  Evidence: `docs/target_cell_spec.md`. |
| M08 | Site data | BLOCKED | Synchronized site records missing  Evidence: `reports/run4/mentor_data_request.md`. |
| M09 | Baselines and oracle | PARTIAL | Fairness and solver certificates incomplete  Evidence: `reports/run4/p0_architecture.md`. |
| M10 | Incremental M0 versus B1 | PARTIAL | Matched site evidence missing  Evidence: `reports/run3/e1_electrical_constraints.md`. |
| M11 | Quality and throughput | PARTIAL | Site FPY and integrity missing  Evidence: `reports/run3/failure_injection_v2.md`. |
| M12 | AI incremental value | FAIL | Evaluation completed; matched AI scheduling benefit not demonstrated; SIM_DATA_PROFILE, `MyDrive/semiexpo/ai_runs/run3/v2_diag/results.csv`  Evidence: `reports/run3/ai_run3.md`. |
| M13 | Statistics and sensitivity | PARTIAL | Complete raw reconciliation missing  Evidence: `reports/run4/facility_billing.md`. |
| M14 | Forecast and constrained optimizer | PARTIAL | Calibration and deployment validation missing  Evidence: `reports/run4/ai_eta.md`. |
| M15 | Electricity before water | PASS | Water metering missing; SOURCE_REPORTED, raw path NOT_VERIFIED  Evidence: `docs/traceability.md`. |
| M16 | Investment case | BLOCKED | Real costs and site contract missing  Evidence: `reports/run4/economics_run4.md`. |

## 18 Final decisions

Simulation acceptance is limited to the stated evidence and gates; industrial site acceptance has not been performed.

| Decision | Disposition |
|---|---|
| D001 | Local reuse precedes shared transfer; residual source is required. |
| D002 | AI value depends on predictable uncertainty. |
| D003 | Oracle feasibility and first AI control: retain negative results. |
| D004 | Measured-cycle simulation: optimization carries the result. |
| D005 | Adopt peak-aware optimization; do not adopt AI for scheduling. |
| D006 | Default P0-E1-Peak; Run 3 analysis leaves the scheduling decision unchanged. |
| D007 | Battery cycling reference cell. |
| D008 | Semiconductor transfer conditional on station-boundary residual phases. |
| D009 | Software-first deployment with existing compatible infrastructure. |
| D010 | Retain ETA and advisory AI, subject to validation. |
| D011 | Conditional business case; full site costs required. |
| D012 | Electrical screening does not replace independent protection. |
| D013 | DS07 primary public facility dataset; DS08 optional. |
| D014 | TNB benchmark and Vietnam scenarios are counterfactual tariffs. |
| D015 | Evaluate monthly facility bills with actual tariff rules. |
| D016 | Separate hardware, topology, scheduling, peak and AI contributions. |
| D017 | Stop station scheduling AI and anomaly experiments; assess facility billing conditionally. |
| D018 | Prefer FIN-B at 5?10 cells conditionally; confirm 30-minute MD; site acceptance remains open. |
| D019 | Freeze architecture and reference AFE 20 / bus 32 kW; candidate AFE 20 / bus 16 kW; M12 FAIL. |
| D020 | AI-BILL NO-GO; retain AI for ETA and advisory. |
| D021 | Freeze architecture; E1-screened nominal fallback and AFE margin, with safety verification pending. |

Source: `docs/decisions.md`; D018 cell range is ASSUMED deployment scenario, baseline and n/CI not applicable, raw site binding NOT_VERIFIED.

| Gate | Status | Evidence and boundary |
|---|---|---|
| G01 Reference cell | PARTIAL | `docs/decisions.md`; ASSUMED, site NOT_VERIFIED. |
| G02 Physics | PARTIAL | `docs/decisions.md`; analytic/unit test, run output NOT_VERIFIED. |
| G03 Matched comparisons | PARTIAL | `reports/run3/metric_audit_v3.md`; SIM_DATA_PROFILE, matching NOT_VERIFIED. |
| G04 Information headroom | PARTIAL | `reports/run4/p0_architecture.md`; SIM_DATA_PROFILE, raw MyDrive/semiexpo/ai_runs/run3/v2_diag/results.csv (sha256 4a8d6b74b0c8a154). |
| G05 Energy AI | FAIL | `reports/run3/ai_run3.md`; SIM_DATA_PROFILE. |
| G06 ETA | PASS | `reports/run4/ai_eta.md`; MEASURED, `MyDrive/semiexpo/ai_runs/run4/eta/`. |
| G07 Production AI | FAIL | `reports/run4/ai_production_planning.md`; SIM_DATA_PROFILE. |
| G08 Electrical constraints | PASS | `reports/run3/e1_electrical_constraints.md`; SIM_DATA_PROFILE, `MyDrive/semiexpo/ai_runs/run3/v2_e1/results.csv`. |
| G09 Twin and protection | PARTIAL | `reports/run3/electrical_feasibility.md`; simulated screen, hardware NOT_VERIFIED. |
| G10 Facility billing | PARTIAL | `reports/run4/facility_billing.md`; SIM_DATA_PROFILE + MEASURED unsynchronized. |
| G11 Economics | PARTIAL | `reports/run4/economics_run4.md`; ASSUMED costs, site NOT_VERIFIED. |
| G12 Site acceptance | BLOCKED | `reports/run4/mentor_data_request.md`; SHADOW_SITE NOT_VERIFIED. |

Gate statuses are inherited assessments, not fresh validation (`reports/run4/mentor_compliance_run4.md`).

## 19 Research novelty

Simulation acceptance is limited to the stated evidence and gates; industrial site acceptance has not been performed.

Prior work includes the CMC hybrid flow-shop scheduling baseline; vendor equipment already offers regeneration and channel reuse (`CLAUDE.md`, `reports/run4/vendor_reference.md`). The incremental proposal combines production-constrained coordination, explicit M0 accounting, electrical screening and facility billing evaluation; it is a system integration and evaluation, not a claim to invent regenerative hardware or vendor reuse (`reports/run4/contribution_decomposition.md`, `docs/decisions.md`). Shared-link results combine topology and optimization; isolated topology and software effects are NOT_VERIFIED. AI has no demonstrated downstream energy or peak benefit, and no site, fab-wide, water or safety claim is supported (`reports/final/report_run4.md`). The requested `reports/sources` directory is MISSING locally; a complete prior-art comparison and novelty against all publications remain NOT_VERIFIED.

## 20 Executive summary

Simulation acceptance is limited to the stated evidence and gates; industrial site acceptance has not been performed.

The following are reported results, not independently reconciled site outcomes. Each interval is a 95% CI; differences are not additive. Drive raw bindings are listed in `docs/raw_binding_manifest.md`.

| Achievement / comparison | Mean and CI; n; boundary; raw path |
|---|---|
| B1 to P0-E1-Peak energy | 3.077 kWh [2.967, 3.186]; n=100; SIM_DATA_PROFILE; `ai_runs/run4_rt2/v2_e1_peak100` (`reports/final/report_run4.md`) |
| B1 to P0-E1-Peak peak | 4.54 kW [3.76, 5.31]; n=100; SIM_DATA_PROFILE; `ai_runs/run4_rt2/v2_e1_peak100` (`reports/final/report_run4.md`) |
| B2 to P0 energy | 0.160 kWh [0.080, 0.229]; n=100; SIM_DATA_PROFILE; `ai_runs/run4_rt2/v2_e1_peak100` (`reports/final/report_run4.md`) |
| B1p-OPT to ORACLE | 1.094 kWh [1.037, 1.148]; n=100; SIM_DATA_PROFILE; `MyDrive/semiexpo/ai_runs/run3/v2_diag/results.csv` (`reports/run3/root_cause_analysis.md`) |
| P0 to rolling truth | 0.094 kWh [0.077, 0.112]; n=100; SIM_DATA_PROFILE; same Drive path (`reports/run3/root_cause_analysis.md`) |
| P0 to queued truth | 0.049 kWh [0.035, 0.064]; n=100; SIM_DATA_PROFILE; same Drive path (`reports/run3/root_cause_analysis.md`) |
| P0 to running truth | 0.024 kWh [0.013, 0.037]; n=100; SIM_DATA_PROFILE; same Drive path (`reports/run3/root_cause_analysis.md`) |
| B2 to P0 facility demand, General, 5 cells | 5.99 kW [4.53, 7.41]; n=70 facility-months; SIM_DATA_PROFILE + MEASURED unsynchronized; MyDrive/semiexpo/ai_runs/run4/fac_gen_5cells (sha256 1263d44d) (`reports/final/report_run4.md`) |
| B2 to P0 facility demand, ToU, 5 cells | 5.11 kW [2.92, 7.42]; n=70 facility-months; same boundary, MyDrive/semiexpo/ai_runs/run4/fac_tou_5cells (sha256 53e74ab0) (`reports/final/report_run4.md`) |
| B2 to P0 facility demand, General, 10 cells | 15.12 kW [11.48, 18.12]; n=70 facility-months; same boundary, MyDrive/semiexpo/ai_runs/run4/fac_gen_10cells (sha256 7d0bf4f6) (`reports/final/report_run4.md`) |

Five principal weaknesses: site evidence absent; baseline matching and raw reconciliation incomplete; learned scheduling benefit failed; electrical protection and vendor access unvalidated; economics omit material site costs (`reports/final/report_run4.md`). Conditional GO for simulation and shadow preparation; NO-GO for site deployment and automatic station AI scheduling. Remaining work: independently retrieve reported AI-BILL and sizing results, verify D021 safety, reconcile remaining claims and matched runs, obtain site/mentor evidence and complete protection and economic qualification (`docs/handoff_run4.md`, `reports/run4/mentor_data_request.md`).


Run 4 default P0 has 1/100 modeled AFE-shortfall violations: instance `v2_test_n10_s62`, one step, 0.259 kWh (SIM_DATA_PROFILE; `MyDrive/semiexpo/ai_runs/run4_rt2/v2_e1_peak100/results.csv`, sha256 57cd90452ba6e187). D021 specifies an E1-screened nominal plan and fallback, FIFO only if infeasible with `initial_plan=fifo_unscreened`, and planning at 18 kW against a 20 kW scoring limit. Verification is pending at `ai_runs/run4/v2_safe_p0`; this is not a safety PASS.

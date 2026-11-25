# Run 4 integrated technical report

## Executive summary
SIM_DATA_PROFILE: DS06 uses measured DS05 battery-cycle shapes with assumed station scaling and operating windows. The study demonstrates modeled coordination and electrical screening, not site savings, quality preservation, vendor access or hardware safety. ETA accuracy passed on held-out measured data; downstream production scheduling and learned energy benefit failed. The default is optimization with advisory forecasting. Facility economics are optimistic counterfactual break-even conditions; site economics and deployment are NOT_VERIFIED. Sources: `reports/run3/ai_run3.md`, `reports/run4/ai_eta.md`, `reports/run4/ai_production_planning.md`, `reports/run4/economics_run4.md`.

## Reference cell and physics
D007 fixes a regenerative multi-channel battery module cycling reference: DS06 assumes 8 stations, 25 modules per station at 0.24 kW per module, a 20 kW AFE, 32 kW bus and 10 kW step; these are SIM_DATA_PROFILE assumptions, not Chroma specifications. Semiconductor transfer requires station-boundary residual source and sink evidence and mentor confirmation; vendor bus access is NOT_VERIFIED. Sources: `docs/decisions.md` D007-D008; `reports/run4/industrial_use_case_matrix.md`; `reports/run4/vendor_reference.md`.

The analytic kill test shows that when each station's demand always covers its own recovery, ideal matched in-rack and shared-bus cases tie; a useful residual source requires independent source/sink phases. In DS06, B1p-OPT to ORACLE is 1.094 kWh [1.037, 1.148], paired 95% CI; this combines topology and optimization, not AI, and matching limitations remain. Boundary: analytic/unit test and SIM_DATA_PROFILE; site NOT_VERIFIED. Sources: `docs/decisions.md` D001, D016; `reports/run3/root_cause_analysis.md`; `reports/run3/metric_audit_v3.md`.

## Engine, information and AI
P0 reoptimizes permitted starts with nominal recipes, freezes running work, and prioritizes tardiness then M0 energy; E1 adds modeled electrical constraints and the optional final peak objective. P0-E1-Peak is the documented default. The primary KPI is incremental M0 grid kWh versus B1; compare matched instances, profiles, bus limits and tardiness, alongside peak, matching, throughput and bus excursions. Boundary: SIM_DATA_PROFILE; independent matching NOT_VERIFIED. Sources: `reports/run4/p0_architecture.md`; `reports/run3/metric_audit_v3.md`; `reports/run3/mentor_compliance_audit.md`.

Perfect information saves 0.094 kWh [0.077, 0.112] against P0; true queued profiles save 0.049 [0.035, 0.064], and true running profiles 0.024 [0.013, 0.037], paired 95% CI, SIM_DATA_PROFILE. These shares are not additive causal effects. Perfect queued aggregate duration and energy save 0.008 kWh [-0.007, 0.022], illustrating the importance of phase trajectory. Source: `reports/run4/p0_architecture.md`.

Held-out measured-data ETA accuracy is reported PASS (MEASURED; run `MyDrive/semiexpo/ai_runs/run4/eta/`): T1 and T2 skill +0.60 each; coverage remains imperfect and the same source retains an older PENDING_COLAB placeholder. TCN is not justified for accuracy: remaining-duration MAE 104.1 min versus random forest 62.0 min (MEASURED held-out DS05; `reports/run4/ai_eta.md`, run `MyDrive/semiexpo/ai_runs/run4/eta_tcn/`). WP-C learned P-ETA-S fails downstream acceptance: tardiness reduction 0.0054 h [0.0000, 0.0158], while energy worsens 0.0274 kWh [0.0123, 0.0437], paired 95% CI, SIM_DATA_PROFILE. Energy AI also FAILS: P5s saves -0.004 kWh [-0.010, +0.004] versus P0; no demonstrated benefit. Monitoring also FAILS automatic detection at a usable false-alarm rate on SYNTHETIC_INJECTED tests; natural cycles have no fault labels and flags remain advisory (`reports/run4/ai_monitoring.md`, `MyDrive/semiexpo/ai_runs/run4/monitor/`). ETA remains advisory. Sources: `reports/run4/ai_eta.md`; `reports/run4/ai_production_planning.md`; `reports/run3/ai_run3.md`.

The default engine n=100 results at SIM_DATA_PROFILE give B1 to P0-E1-Peak 3.077 kWh [2.967, 3.186] and 4.54 kW [3.76, 5.31] peak reduction; B2 to P0 is 0.160 kWh [0.080, 0.229]. P0 has 1 modeled violation and B2 has 13; mean tardiness is 0.18 h for P0 versus 0.14 h for one-shot, so comparisons require matching scrutiny. Source and runs: `reports/run3/e1_electrical_constraints.md`, `ai_runs/run4_rt2/v2_e1_peak100` and `run4/v2_e1_peak_b`.

## Electrical feasibility
E1 constrains AFE import, bus throughput and step changes in the optimizer; the assumed 20 kW, 32 kW and 10 kW limits and dynamic twin provide SIM_DATA_PROFILE screening only. The E1 integration passed at simulation level; the transient model has assumed parameters and boundary-window screening, and hardware protection and sizing are NOT_VERIFIED. In the simulated 48 kW-rated cell, coordinated plans need approximately 15?20 kW AFE; 10 kW leaves 3/30 oracle workloads infeasible. FIFO requires 20 kW for zero reported violations in this sweep. Boundary: SIM_DATA_PROFILE, `reports/run3/e1_electrical_constraints.md`. Sources: `reports/run3/e1_electrical_constraints.md`; `reports/run3/electrical_feasibility.md`.

## Facility billing and economics
SOURCE_REPORTED: the official TNB schedule maps General demand to the whole month and ToU demand to peak periods. The later verification in `reports/run4/facility_billing.md` and `reports/run4/economics_run4.md` supersedes the older contradictory tariff registry entries (`reports/run4/tariff_registry.md`); interval alignment, holiday handling and the actual site contract remain NOT_VERIFIED. Rates are geographical counterfactuals, not Korean factory bills.

SIM_DATA_PROFILE DS06 cells plus MEASURED DS07 facility loads are unsynchronised counterfactuals. Factory-clustered paired 95% CIs supersede month-level intervals. B2 to P0-E1-Peak demand reductions are below; independently scheduled cells share a meter, with no cross-cell optimization. Source: `reports/run4/facility_billing.md`, runs `ai_runs/run4/fac_{gen,tou}_{3,5,10}cells` and `MyDrive/semiexpo/ai_runs/run4/fac_grid_tnb/`.

| Cells | General kW [95% CI] | ToU kW [95% CI] |
|---|---|---|
| 1 | 2.12 [0.86, 3.32] | 1.73 [0.73, 2.68] |
| 3 | 4.55 [2.59, 6.41] | 3.34 [1.07, 5.72] |
| 5 | 5.99 [4.53, 7.41] | 5.11 [2.92, 7.42] |
| 10 | 15.12 [11.48, 18.12] | 12.26 [9.14, 15.02] |

ToU B1p-OPT to P0-E1-Peak is 1.06 kW [-0.22, 2.30], not significant; factory-clustered SIM_DATA_PROFILE + MEASURED (`reports/run4/facility_billing.md`). P0-BILL's initial perfect-background cases do not show stable improvement; extension and AI-BILL rows are PENDING, and learned billing AI is not justified yet (`reports/run4/facility_billing.md`).

FIN-B is B2 to P0 on existing shared infrastructure. Under ASSUMED annualisation and FX and missing installation, requalification and support costs, the known CAPEX estimate is USD 4,220; the optimistic General/ToU five-cell paybacks are 3.0/3.3 years. General five-cell three-/five-year CAPEX ceilings are USD 4,164/6,940, and ten-cell ceilings are USD 10,445/17,408. These are break-even conditions, not site payback. D017 recommends FIN-B as the conditional candidate at scale; FIN-A has no energy value by physics and FIN-C has unscoped hardware costs. Boundary: SIM_DATA_PROFILE + MEASURED, ASSUMED finance; run `ai_runs/run4/fin_fac_{gen,tou}_fx{0.21,0.24}/`, sources `reports/run4/economics_run4.md`, `docs/decisions.md` D017. Three cells already reach an optimistic four-year General payback, so five cells are not a universal threshold; the source verdict text conflicts with its own table on this point and needs correction (`reports/run4/economics_run4.md`).

## Contribution decomposition
D016 distinguishes hardware recovery, topology, conventional scheduling, rolling, peak/billing and AI. The documented B0 to B1 hardware saving is 57.49 kWh [55.61, 59.41]; B2 to B3 scheduling is 0.218 [0.189, 0.248]; B3 to P0 rolling is 0.018 [0.009, 0.028], paired 95% CI, SIM_DATA_PROFILE. Different subsets, objectives, information and matching limitations prevent addition or isolated attribution; topology-only difference is NOT_VERIFIED. Source: `reports/run4/contribution_decomposition.md`.

## Gates
Statuses below summarize the cited evidence, not a fresh revalidation. PASS is limited to the stated boundary; site deployment remains NOT_VERIFIED.

| Gate | Status | Evidence and boundary |
|---|---|---|
| G01 Reference cell | PARTIAL | `docs/decisions.md` D007-D008; ASSUMED reference, semiconductor eligibility NOT_VERIFIED |
| G02 Physics / kill test | PARTIAL | `docs/decisions.md` D001; analytic and unit-test boundary; run output path NOT_VERIFIED |
| G03 Matched comparisons | PARTIAL | `reports/run3/metric_audit_v3.md`; SIM_DATA_PROFILE, matching NOT_VERIFIED |
| G04 Information headroom | PARTIAL | `reports/run4/p0_architecture.md`; SIM_DATA_PROFILE; exact run output path NOT_VERIFIED |
| G05 Energy AI | FAIL | `reports/run3/ai_run3.md`; SIM_DATA_PROFILE |
| G06 ETA accuracy | PASS | `reports/run4/ai_eta.md`; held-out MEASURED accuracy only; run `MyDrive/semiexpo/ai_runs/run4/eta/`; older placeholder superseded |
| G07 Downstream production AI | FAIL | `reports/run4/ai_production_planning.md`; SIM_DATA_PROFILE |
| G08 Electrical constraints | PASS | `reports/run3/e1_electrical_constraints.md`; SIM_DATA_PROFILE simulation only; run `MyDrive/semiexpo/ai_runs/run3/v2_e1/results.csv` |
| G09 Twin / protection | PARTIAL | `reports/run3/electrical_feasibility.md`; simulated screen, hardware NOT_VERIFIED |
| G10 Facility billing | PARTIAL | `reports/run4/facility_billing.md`; SIM_DATA_PROFILE + MEASURED unsynchronized, tariff schedule verified; site and interval details NOT_VERIFIED |
| G11 Economics | PARTIAL | `reports/run4/economics_run4.md`; SIM_DATA_PROFILE + MEASURED, optimistic ceilings; site NOT_VERIFIED |
| G12 Site acceptance | BLOCKED | `reports/run3/mentor_compliance_audit.md`; SHADOW_SITE NOT_VERIFIED |

## Open items and data requests
Reconcile raw matched runs and tardiness; complete P0-BILL extension and conditional AI-BILL evaluation; reconcile the tariff registry with the verified schedule and verify applicable interval, holiday and site contract rules; scope missing costs. Confirm the target application and obtain time-aligned station input/output, cell and facility meters, schedules and allowed start windows, converter curves, protection and vendor interface details, tariff and billing history, quality/FPY records, installation and requalification costs. Obtain cooling-loop measurements before any water claim. Sources: `reports/run3/metric_audit_v3.md`; `reports/run4/mentor_data_request.md`; `reports/run4/economics_run4.md`; `reports/run4/tariff_registry.md`; `reports/run3/mentor_compliance_audit.md`.

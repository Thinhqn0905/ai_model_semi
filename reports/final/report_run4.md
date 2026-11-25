# Run 4 integrated technical report

## Executive summary
SIM_DATA_PROFILE: DS06 uses measured DS05 battery-cycle shapes with assumed station scaling and operating windows. The study demonstrates modeled coordination and electrical screening, not site savings, quality preservation, vendor access or hardware safety. ETA accuracy passed on held-out measured data; downstream production scheduling and learned energy benefit failed. The default is optimization with advisory forecasting. Facility economics and deployment are NOT_VERIFIED. Sources: `reports/run3/ai_run3.md`, `reports/run4/ai_eta.md`, `reports/run4/ai_production_planning.md`, `reports/run4/economics_run4.md`.

## Reference cell and physics
D007 fixes a regenerative multi-channel battery module cycling reference: DS06 assumes 8 stations, 25 modules per station at 0.24 kW per module, a 20 kW AFE, 32 kW bus and 10 kW step; these are SIM_DATA_PROFILE assumptions, not Chroma specifications. Semiconductor transfer requires station-boundary residual source and sink evidence and mentor confirmation; vendor bus access is NOT_VERIFIED. Sources: `docs/decisions.md` D007-D008; `reports/run4/industrial_use_case_matrix.md`; `reports/run4/vendor_reference.md`.

The analytic kill test shows that when each station's demand always covers its own recovery, ideal matched in-rack and shared-bus cases tie; a useful residual source requires independent source/sink phases. In DS06, B1p-OPT to ORACLE is 1.094 kWh [1.037, 1.148], paired 95% CI; this combines topology and optimization, not AI, and matching limitations remain. Boundary: analytic/unit test and SIM_DATA_PROFILE; site NOT_VERIFIED. Sources: `docs/decisions.md` D001, D016; `reports/run3/root_cause_analysis.md`; `reports/run3/metric_audit_v3.md`.

## Engine, information and AI
P0 reoptimizes permitted starts with nominal recipes, freezes running work, and prioritizes tardiness then M0 energy; E1 adds modeled electrical constraints and the optional final peak objective. P0-E1-Peak is the documented default. The primary KPI is incremental M0 grid kWh versus B1; compare matched instances, profiles, bus limits and tardiness, alongside peak, matching, throughput and bus excursions. Boundary: SIM_DATA_PROFILE; independent matching NOT_VERIFIED. Sources: `reports/run4/p0_architecture.md`; `reports/run3/metric_audit_v3.md`; `reports/run3/mentor_compliance_audit.md`.

Perfect information saves 0.094 kWh [0.077, 0.112] against P0; true queued profiles save 0.049 [0.035, 0.064], and true running profiles 0.024 [0.013, 0.037], paired 95% CI, SIM_DATA_PROFILE. These shares are not additive causal effects. Perfect queued aggregate duration and energy save 0.008 kWh [-0.007, 0.022], illustrating the importance of phase trajectory. Source: `reports/run4/p0_architecture.md`.

Held-out measured-data ETA accuracy is reported PASS: T1 and T2 skill +0.60 each; coverage remains imperfect and the same source retains an older PENDING_COLAB placeholder. WP-C learned P-ETA-S fails downstream acceptance: tardiness reduction 0.0054 h [0.0000, 0.0158], while energy worsens 0.0274 kWh [0.0123, 0.0437], paired 95% CI, SIM_DATA_PROFILE. Energy AI also FAILS: P5s saves -0.004 kWh [-0.010, +0.004] versus P0; no demonstrated benefit. ETA remains advisory. Sources: `reports/run4/ai_eta.md`; `reports/run4/ai_production_planning.md`; `reports/run3/ai_run3.md`.

## Electrical feasibility
E1 constrains AFE import, bus throughput and step changes in the optimizer; the assumed 20 kW, 32 kW and 10 kW limits and dynamic twin provide SIM_DATA_PROFILE screening only. The E1 integration passed at simulation level; the transient model has assumed parameters and boundary-window screening, and hardware protection and sizing are NOT_VERIFIED. Sources: `reports/run3/e1_electrical_constraints.md`; `reports/run3/electrical_feasibility.md`.

## Facility billing and economics
DS07 measured Korean facility loads are combined with an unsynchronized simulated DS06 cell; this is a counterfactual, not an actual bill. Under the TNB peak-period scenario, B2 to P0-E1-Peak reduces billed-demand increment by 1.73 kW [0.78, 2.67], paired 95% CI, SIM_DATA_PROFILE + MEASURED. The TNB time-of-use peak-only rule is source-verified in the registry; applying it to the general tariff, interval length and alignment remain NOT_VERIFIED. Billing-aware perfect-background headroom is inconclusive. Sources: `reports/run4/facility_billing.md`; `reports/run4/tariff_registry.md`.

FIN-A compares B1 to B1-OPT, FIN-B B2 to P0 on compatible shared infrastructure, and FIN-C B1 to P0 with retrofit. DS06 cell-level economics report negative NPV under their assumptions and missing costs; extrapolation from cell peak to facility billing is superseded. Facility-level FIN sensitivity, option verdicts and intervals remain PENDING_COLAB; no site payback is established. Sources: `reports/run3/economics_v3.md`; `reports/run4/economics_run4.md`; `docs/decisions.md` D009, D015.

## Contribution decomposition
D016 distinguishes hardware recovery, topology, conventional scheduling, rolling, peak/billing and AI. The documented B0 to B1 hardware saving is 57.49 kWh [55.61, 59.41]; B2 to B3 scheduling is 0.218 [0.189, 0.248]; B3 to P0 rolling is 0.018 [0.009, 0.028], paired 95% CI, SIM_DATA_PROFILE. Different subsets, objectives, information and matching limitations prevent addition or isolated attribution; topology-only difference is NOT_VERIFIED. Source: `reports/run4/contribution_decomposition.md`.

## Gates
Statuses below summarize the cited evidence, not a fresh revalidation. PASS is limited to the stated boundary; site deployment remains NOT_VERIFIED.

| Gate | Status | Evidence and boundary |
|---|---|---|
| G01 Reference cell | PARTIAL | `docs/decisions.md` D007-D008; ASSUMED reference, semiconductor eligibility NOT_VERIFIED |
| G02 Physics / kill test | PASS | `docs/decisions.md` D001; analytic and unit-test boundary |
| G03 Matched comparisons | PARTIAL | `reports/run3/metric_audit_v3.md`; SIM_DATA_PROFILE, matching NOT_VERIFIED |
| G04 Information headroom | PASS | `reports/run3/root_cause_analysis.md`; SIM_DATA_PROFILE |
| G05 Energy AI | FAIL | `reports/run3/ai_run3.md`; SIM_DATA_PROFILE |
| G06 ETA accuracy | PASS | `reports/run4/ai_eta.md`; held-out MEASURED accuracy only, placeholder conflict remains |
| G07 Downstream production AI | FAIL | `reports/run4/ai_production_planning.md`; SIM_DATA_PROFILE |
| G08 Electrical constraints | PASS | `reports/run3/e1_electrical_constraints.md`; SIM_DATA_PROFILE simulation only |
| G09 Twin / protection | PARTIAL | `reports/run3/electrical_feasibility.md`; simulated screen, hardware NOT_VERIFIED |
| G10 Facility billing | PARTIAL | `reports/run4/facility_billing.md`; SIM_DATA_PROFILE + MEASURED unsynchronized, tariff details NOT_VERIFIED |
| G11 Economics | BLOCKED | `reports/run4/economics_run4.md`; PENDING_COLAB, site NOT_VERIFIED |
| G12 Site acceptance | BLOCKED | `reports/run3/mentor_compliance_audit.md`; SHADOW_SITE NOT_VERIFIED |

## Open items and data requests
Reconcile raw matched runs and tardiness; complete facility economics and billing-aware causal comparisons; verify applicable tariff intervals, rates and rules. Confirm the target application and obtain time-aligned station input/output, cell and facility meters, schedules and allowed start windows, converter curves, protection and vendor interface details, tariff and billing history, quality/FPY records, installation and requalification costs. Obtain cooling-loop measurements before any water claim. Sources: `reports/run3/metric_audit_v3.md`; `reports/run4/mentor_data_request.md`; `reports/run4/economics_run4.md`; `reports/run4/tariff_registry.md`; `reports/run3/mentor_compliance_audit.md`.

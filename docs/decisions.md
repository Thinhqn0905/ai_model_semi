# Decision log

## D001 (2026-11-24, lead) — why the shared DC bus loses the kill test: physics, not tuning
Evidence: `regenate.electrical.ledger` + tests ELEC-09 and `test_dc_gain_bound_exact_for_source_sink_pair`
(boundary: analytic + unit test, no site data).

1. With in-rack reuse, each station first feeds its own recovered power into its own supply.
   Residual source remains only when a station returns more than it draws **at that moment**.
2. Converter / power-supply burn-in: DUT output <= eta_dut * DUT input at every step, so the
   residual source is always 0 and **DC shared == B1p exactly** (ELEC-09). No schedule and no
   forecast can change that. This is why the 23/11 deck lost the kill test.
3. Where residual source exists, the shared link only saves the double conversion through AC:
   saved import per kWh of residual source = (eta_link - eta_afe_exp*eta_afe_imp)/eta_afe_imp
   = 5.1 % (AFE 97 %) ... 9.2 % (AFE 95 %), because AC netting behind M0 is already 1:1
   (the legacy B1 ledger wrongly credited AC return at alpha_ex = 0.5).
4. Therefore incremental kWh vs B1/B1p can be meaningful only if the target cell has
   **time-separated source and sink phases inside a station** and a large residual-source share:
   energy-storage / bidirectional DUT cycling (battery or supercap module charge/discharge,
   bidirectional converter/PCS test in discharge mode), or stations that cannot recirculate
   in-rack (legacy AC-fed supplies, voltage-incompatible DUT output).
5. Other value of the shared bus that is not kWh: peak import kW, central AFE sizing vs N
   regen-to-AC loads (CAPEX), grid-export restrictions (dump avoided when export is not allowed).

Consequence for the plan: WP02 must pick the target cell with this rule; WP05 oracle measures
the residual-source share first (flexibility gate M03). Decision on the target cell: USER.

## D002 (2026-11-24, lead) — AI can only add value where the uncertainty is predictable
In the legacy code and in bench_v1, the realised duration and power multiplier are i.i.d. noise
(dur_true = dur_nom*(1+eps), kappa ~ N(1, s)) with no observable cause. Then no forecaster can beat the
nominal recipe in expectation, so P - P0 ~ 0 by construction (the deck's +0.8 % "not significant" is
exactly this). Building learnable structure into synthetic data just to make AI win would be designing the
result.
Plan: (1) report P vs P0 on bench_v1 honestly as the "i.i.d. uncertainty" control; (2) ground predictable
uncertainty in real traces: DS05 Chroma battery cycling (charge/discharge phase durations depend on cell
capacity/SoH, observable from early-phase V/I) -> train F06 remaining-duration and F05 power quantile models on
DS05 with chronological/cell-level splits; (3) bench_v2 S3 samples phase durations and powers from DS05 cells,
and P uses in-progress M2 observations, P0 uses recipe nominal. AI value = P0 - P on bench_v2 with paired CI.
If that is ~0 too, recommend optimisation-only (mentor: "recommend the simpler solution").

## D003 (2026-11-25, lead) — WP05 Go/No-Go and first AI control result
Oracle campaign runs/oracle_v1 (SIM_ASSUMED_PROFILE, n=10, 18 paired instances per cell, 95 % bootstrap CI):
- S1 converter burn-in and S2 dynamic load: ORACLE == B1p-OPT exactly (0.00 kWh) -> NO-GO for shared DC on converter burn-in.
- S3 storage / bidirectional cycling: ORACLE beats B1p-OPT by 5.59 kWh (6.1 %), CI [5.33, 5.79], 18/18 at flex 1.0
  (4.2 % already at flex 0 = topology alone); peak 23.7 vs 40.8 kW. -> GO for the S3 cell type.
Rolling runs/rolling_v1 (S3, flex 0.25): P beats B1p-OPT by 4.3 kWh (4.7 %, 18/18) but P is WORSE than P0 by 0.9 kWh
(-1.0 %, 0/18) and its peak is higher: the in-progress estimator on i.i.d. deviations hurts (D002 control). Kept as a negative
result; AI is judged on bench v2 (DS06, measured DS05 cycles) with a reliability gate (AI-G10).
DS05 note: Cumulative_Time is in 10-s units (verified against REAL_TIME on 3 use cases); loader fixed before any use.
Target cell recommendation to the user: regenerative cycling of storage / bidirectional power modules (S3), not converter burn-in.

## D004 (2026-11-25, lead) — AI-EXP12 on measured cycles: optimisation carries the result
DS06 (bench v2, DS05 measured cycles, n=100 paired, reports/ai/ai_exp12_ds06.md): kill test PASSED (ORACLE -11.6 % vs
B1p-OPT, CI [1.04, 1.15] kWh, 100/100; P0 peak -20 %). Forecast variants P1..P4 are 0.2-0.3 % WORSE than P0 (CI excludes 0);
perfect-forecast headroom over P0 is only 1.1 %. Decision: energy KPI -> recommend P0 (optimisation-only, mentor p6);
AI is kept only if it improves PEAK under a peak-aware optimizer (third lexicographic level added to milp.solve, tested in
results/v2_peak). Forecast accuracy (Branch C) is reported separately and never presented as an energy saving.

## D005 (2026-11-25, lead) — Peak-aware optimizer adopted; AI not adopted for scheduling decisions
Third lexicographic level (min peak at equal TT and energy, milp.solve peak_stage) lowers P0 peak by 3.9 % (CI excludes 0) at no
energy cost on DS06 (n=50). AI variants P1..P4 do not beat P0 on energy (n=100 and n=50) or peak (n=50). Product configuration:
P0 + peak stage; AI forecasts shown to engineers (expected completion, uncertainty) behind AI-G10. Evidence: reports/ai/ai_exp12_ds06.md.

## D006-R3 (2026-11-25, lead) — Run 3: AI failure explained; decision unchanged (optimisation-only for scheduling)
Information decomposition on DS06 (n=100, reports/run3/root_cause_analysis.md): rolling oracle == one-shot ORACLE (gap is pure
information, 0.094 kWh = 1.1 % of P0); queued-job info 52 %, running-job info 26 %. The Run 2 integration fed PERFECT forecasts
captures 0 % or loses -> the Run 2 negative result is an integration failure, not a model failure. Run 3 integrations (P5/P5s
phase-aligned recipe, PQ/PQ5 cycle-level queued-job model with AI18 gate) do not beat P0 (several significantly worse); PQ* with
perfect cycle ratios recovers the tardiness value but not the energy value (n.s.), which lies in intra-cycle shape
(reports/run3/ai_run3.md). Decision: keep P0 + peak stage for scheduling; forecasts stay engineer information (ETA, anomaly flag)
behind AI-G10. No energy or peak saving is attributed to AI.

# Run 4 binding decisions (user, 2026-11-25; D006-R3 above is the Run 3 evidence record behind D006/D010)

## D006 — Default scheduling engine: P0-E1-Peak
Rolling-horizon MILP without learned forecasting (recipe nominal profiles, current telemetry, production constraints, job-completion
events) + E1 electrical limits (AFE import, bus throughput, slot step) + third lexicographic peak level; subject to dynamic twin
screening. Evidence: reports/run3/e1_electrical_constraints.md (kill test 1.09 kWh 50/50 with limits; peak -25.6 % vs B1p-OPT;
twin approval 100 % for P0 and ORACLE). Deterministic optimisation savings are never attributed to AI.

## D007 — Experimental reference test cell
Regenerative multi-channel battery module cycling test cell; commercial functional reference Chroma 17020 (not an internal circuit
model). DS05 = measured profiles, DS06 = integrated benchmark (8 stations, 25 modules x 0.24 kW, AFE 20 kW, link 32 kW, step 10 kW,
all ASSUMED, not Chroma specifications; kept for reproducibility, larger configurations only as sensitivity). Eligibility as the
final semiconductor competition application: pending mentor confirmation. Closes the WP02 target-cell question (Session_Checklist 17).

## D008 — Semiconductor transfer application (conditional)
Regenerative bidirectional power-electronics module testing (bidirectional DC-DC validation, battery-emulator PE testing, PE module
cycling, ESS module testing, EV power-conversion test). Eligible only with evidence of independently timed residual source and sink
phases at the station boundary after local reuse; a bidirectional DUT does not imply bidirectional net station power. The reference
cell is not changed again without evidence and explicit approval.

## D009 — Software-first deployment
ReGenATE is a coordination software platform on existing regenerative equipment. FIN-A (regen-to-AC), FIN-B (existing compatible
shared-energy infrastructure, PRIORITY), FIN-C (full retrofit). Contribution = incremental coordination, scheduling, billing
optimisation, operational intelligence; hardware regeneration and vendor channel-to-channel reuse are not ReGenATE novelty.

## D010 — AI operational intelligence
Priorities: completion-time (ETA), station availability, tardiness-aware planning, cycle-/energy-deviation monitoring, calibrated
uncertainty, risk advisory. AI enters automatic scheduling only after matched downstream improvement over a non-AI baseline
(Run 3: not yet shown for energy, peak or tardiness with learned models; PQd* shows a tardiness ceiling of 0.048 h/instance).

## D011 — Business feasibility
Routes: reduced incremental CAPEX, existing infrastructure, energy, facility-level demand charges, TOU, contracted capacity, verified
production benefits. No monetisation of unverified AI predictions, hypothetical avoided failures or unsupported productivity gains.

## D012 — Electrical acceptance
No optimizer or AI replaces independent electrical protection. Accepted schedules satisfy modelled hard constraints and pass the
dynamic twin screen.

## D013 — Public facility load: DS07 (primary), DS08 optional after DS07 works.
DS07 = Lee, Baek, Kim, Sci Data 2022, figshare 14822256 v9, CC BY 4.0: 10 Korean factories, 1-min kW, Mar-Sep 2019 (verified on Colab,
md5 match). Independent of DS05/DS06 (not synchronised).

## D014 — Public tariff benchmark: Malaysia TNB RP4 (primary, maximum demand), Vietnam actual + two-component trial (trial not
payable), Singapore SP Group. Geographical counterfactuals, not the DS07 factories' actual tariffs.

## D015 — Facility-level billing: monthly bills per tariff rules (billing interval, eligible periods) on facility load + cell load;
no extrapolation of instantaneous cell peak reductions.

## D016 — Contribution decomposition: report separately regenerative hardware (B0->B1), shared topology (B1p-OPT->B2 / ->B3),
conventional scheduling, rolling optimisation, peak/billing optimisation, AI operational benefit. The 11.6 % shared-link figure is
topology + optimisation, never AI or software-only.

## D017 (user, 2026-11-25) — Run 4 scope adjustments
1. AI retained for ETA prediction and engineer advisory only. Station-level AI scheduling (P1-P5, PQ, PQ5, PQd) and anomaly-detection
   experiments are STOPPED (failed: reports/run3/ai_run3.md, reports/run4/ai_production_planning.md, reports/run4/ai_monitoring.md;
   results kept). AI-assisted facility billing continues against P0-BILL and ORACLE-BILL.
2. FIN-B prioritised: evaluate 1, 3, 5, 10 cells with shared software/server costs and facility-level coordination; target 3-5 y
   payback without linear-savings assumptions or artificial cost cuts; otherwise report break-even conditions.
3. TNB tariffs from the official schedule PDF (data/tariffs/sources/Tariff-TNB-pdf.pdf): MV General, MV ToU, HV General, HV ToU with
   30-min MD, peak periods and holiday treatment (holidays: sensitivity, not documented in the schedule).
4. Reference cell (Chroma 17020-type battery cycling) and P0-E1-Peak default scheduler retained (D006, D007).
5. DS07 results reported with factory-clustered CIs; complete running experiments; preserve negative results.

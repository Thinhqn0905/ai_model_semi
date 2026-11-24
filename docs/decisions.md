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

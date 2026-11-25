# Run 4 facility economics ? PENDING_COLAB

Boundary: SIM_DATA_PROFILE cell with measured DS07 facility loads, not synchronised; billing and financial conclusions NOT_VERIFIED. The module pairs facility-month demand and DS06 instance energy, annualises seven months by 12/7, and reports per-factory values and factory-clustered bootstrap intervals. Multi-cell energy scales by cell count; demand uses the simulated multi-cell increments. Named site and per-cell costs are scaled by scope; unknown multi-cell scope is marked missing. MISSING costs remain OPTIMISTIC and suppress payback. USD cost conversion requires an explicit exchange rate. Without instance counts, the assumed 15-hour block protocol is used. TOU energy uses an off-peak flat proxy, NOT_VERIFIED because energy allocation is unavailable.

PENDING_COLAB: run with matched facility and DS06 inputs and validate tariff-window pairing. Hours and CAPEX factor sweeps are emitted; eta_AFE sensitivity, automatic option verdicts and demand-rate/cell-to-facility break-even conditions remain outstanding. Tariff windows, instance energy allocation, site costs and FX need verification. No investment conclusion is established.

## Results — FIN-B multi-cell on verified TNB RP4 tariffs (lead, Colab; Drive `ai_runs/run4/fin_fac_{gen,tou}_fx{0.21,0.24}/`)
Boundary: SIM_DATA_PROFILE cells + MEASURED DS07 facilities (not synchronised) + VERIFIED TNB rates (p.2 of the official schedule) +
ASSUMED annualisation (7 DS07 months x 12/7), FX USD/MYR 0.21 ASSUMED (0.24 sensitivity in the CSVs). FIN-B = B2 -> P0-E1-Peak on the
same existing shared-energy hardware; demand saving from the simulated n-cell billed-demand increments (not scaled linearly); energy
saving from DS06 at equal tardiness. Known FIN-B CAPEX USD 4,220 (site-level server/software/meters, ESTIMATE); installation,
requalification, annual support are MISSING -> every payback is OPTIMISTIC and stated as a break-even ceiling. Ranges = factory-clustered.
| Tariff | cells | annual net USD [clustered range] | CAPEX ceiling 3-y | 5-y | 10-y discounted | simple payback on known CAPEX |
|---|---|---|---|---|---|---|
| MV General | 1 | 484 [201, 755] | 1,452 | 2,421 | 3,248 | 8.7 y |
| MV General | 3 | 1,048 [608, 1,466] | 3,145 | 5,241 | 7,034 | 4.0 y |
| MV General | 5 | 1,388 [1,060, 1,707] | 4,164 | 6,940 | 9,314 | 3.0 y |
| MV General | 10 | 3,482 [2,662, 4,157] | 10,445 | 17,408 | 23,362 | 1.2 y |
| MV ToU | 1 | 430 [185, 663] | 1,290 | 2,150 | 2,886 | 9.8 y |
| MV ToU | 3 | 838 [284, 1,421] | 2,514 | 4,189 | 5,622 | 5.0 y |
| MV ToU | 5 | 1,288 [752, 1,851] | 3,863 | 6,438 | 8,641 | 3.3 y |
| MV ToU | 10 | 3,071 [2,310, 3,746] | 9,214 | 15,356 | 20,608 | 1.4 y |
| HV General | 10 | 1,305 [1,019, 1,541] | 3,916 | 6,527 | 8,759 | 3.2 y |
| HV ToU | 10 | 1,494 [1,142, 1,805] | 4,481 | 7,468 | 10,022 | 2.8 y |
(HV 1-5 cells: ceilings below the known CAPEX for 3-y payback; see clustered_summary.csv.)

## Verdict (D017.2)
- On known CAPEX only, three cells have reported payback of 4.0 y (MV General) and 5.0 y (MV ToU, rounded); the unrounded calculation from the displayed USD 838 annual net is 5.04 y. Both are optimistic: installation, requalification and support are missing.
- Five and ten cells offer shorter estimated payback, subject to the missing-cost limits below. These are conditional scenarios, not a demonstrated business case: simulated cells are combined with unsynchronised Korean facility loads under Malaysian tariffs; site tariff, contract and costs remain NOT_VERIFIED.
- FIN-A has no energy value by physics; FIN-C carries unscoped hardware items (MISSING) and is not preferred (D009).

## Missing-cost sensitivity ? DERIVED
Boundary: SIM_DATA_PROFILE + unsynchronised MEASURED DS07; ASSUMED annualisation and FX; site and missing costs NOT_VERIFIED. Each entry is simple payback in years / 10-year NPV in USD / thresholds met. M is additional upfront missing cost; recurring support is not quantified and is not represented as an upfront cost. Annual net is copied from the rounded table above; results use those displayed values, not underlying unrounded runs. Simple payback = (4,220 + M) / annual net; 10-year NPV at 8% = annual net ? 6.710 ? (4,220 + M), using the specified annuity factor 6.710. Thresholds use unrounded payback: 3 = ?3 years; 5 = ?5 years; ? = neither.

| Tariff; cells; annual net USD | M=0 | M=2,000 | M=5,000 | M=10,000 | M=20,000 |
|---|---|---|---|---|---|
| MV General; 1; 484 | 8.72 / -972 / ? | 12.85 / -2,972 / ? | 19.05 / -5,972 / ? | 29.38 / -10,972 / ? | 50.04 / -20,972 / ? |
| MV General; 3; 1,048 | 4.03 / 2,812 / 5 | 5.94 / 812 / ? | 8.80 / -2,188 / ? | 13.57 / -7,188 / ? | 23.11 / -17,188 / ? |
| MV General; 5; 1,388 | 3.04 / 5,093 / 5 | 4.48 / 3,093 / 5 | 6.64 / 93 / ? | 10.24 / -4,907 / ? | 17.45 / -14,907 / ? |
| MV General; 10; 3,482 | 1.21 / 19,144 / 3, 5 | 1.79 / 17,144 / 3, 5 | 2.65 / 14,144 / 3, 5 | 4.08 / 9,144 / 5 | 6.96 / -856 / ? |
| MV ToU; 1; 430 | 9.81 / -1,335 / ? | 14.47 / -3,335 / ? | 21.44 / -6,335 / ? | 33.07 / -11,335 / ? | 56.33 / -21,335 / ? |
| MV ToU; 3; 838 | 5.04 / 1,403 / ? | 7.42 / -597 / ? | 11.00 / -3,597 / ? | 16.97 / -8,597 / ? | 28.90 / -18,597 / ? |
| MV ToU; 5; 1,288 | 3.28 / 4,422 / 5 | 4.83 / 2,422 / 5 | 7.16 / -578 / ? | 11.04 / -5,578 / ? | 18.80 / -15,578 / ? |
| MV ToU; 10; 3,071 | 1.37 / 16,386 / 3, 5 | 2.03 / 14,386 / 3, 5 | 3.00 / 11,386 / 5 | 4.63 / 6,386 / 5 | 7.89 / -3,614 / ? |

## Holiday sensitivity ? scenario, not documented tariff rule
Boundary: SIM_DATA_PROFILE + unsynchronised MEASURED DS07; factory-clustered intervals; 100-instance pool, 70 factory-months. Malaysian 2019 public holidays treated as off-peak, B2 ? P0-E1-Peak; base case treats holidays by weekday. Raw: `ai_runs/run4_rt2/fac_tou_hol_1cells/`, `ai_runs/run4_rt2/fac_tou_hol_5cells/`; source: `reports/run4/facility_billing.md`.

| ToU scenario | Billed-demand reduction kW [95% CI] | Context |
|---|---|---|
| 1 cell, holidays off-peak | 0.97 [-0.01, 1.91] | 7/10 factories; base without holiday adjustment 1.93 kW; borderline |
| 5 cells, holidays off-peak | 3.13 [0.98, 5.20] | 8/10 factories; positive interval |

The holiday treatment is NOT_VERIFIED; no holiday-adjusted annual financial estimate is inferred from these demand effects.

## Corrections
- This report, Verdict (D017.2): replaced the contradictory claim that 1?3 cells cannot reach 3?5 years and the claim that only ?5 cells can do so. The three-cell results and missing-cost qualification are stated above.
- `reports/run4/tariff_registry.md`: corrected General demand eligibility to whole-month maximum and replaced stale unverified MV schedule entries with the verified PDF values.
- `reports/final/Run4_Final_Evaluation_Report.md` is outside this task's ownership: its table already gives 4.0 and 5.0 years, but its text says the report claims three cells do not reach five years. That stale commentary remains for its owner to reconcile.

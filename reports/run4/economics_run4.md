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
- A 3-5-year simple payback is reachable on paper only for FIN-B with >= 5 cells behind one MV meter (MV General 5 cells 3.0 y, MV ToU
  5 cells 3.3 y; 10 cells 1.2-1.4 y), and only if the MISSING items stay below the ceiling minus USD 4,220: <= ~0 (5 cells, 3 y),
  <= USD 2,700 (5 cells, 5 y, General), <= USD 6,200 (10 cells, 3 y, General), <= USD 13,200 (10 cells, 5 y, General).
- 1-3 cells do not reach 3-5 y (best 4.0 y for 3 cells MV General). HV tariffs (lower demand rates) need 10 cells.
- These are break-even CONDITIONS, not a demonstrated business case: savings rest on simulated cells added to Korean facility loads
  under Malaysian rates; installation/requalification costs and the site tariff/contract must be obtained (mentor data request).
- FIN-A has no energy value by physics; FIN-C carries un-scoped hardware items (MISSING) and is not preferred (D009).

# Run 4 WP-G/I — Test cell inside measured facility loads (DS07): monthly billed demand

Scope: additional research beyond the original mentor scope (D013-D015), supporting M16 (economics) and M10 (incremental KPI).
Boundary: **SIM_DATA_PROFILE cell + MEASURED DS07 facility load, not synchronised** (counterfactual: a simulated DS06 cell is ADDED
behind the facility meter; DS07 already contains whatever those factories run). Tariffs are geographical counterfactuals (D014).

## Data
DS07 (Lee, Baek, Kim, Sci Data 2022; figshare 14822256 v9, CC BY 4.0; md5/sha256 verified on Colab, Drive `MyDrive/semiexpo/ds07_raw`):
10 Korean factories, 1-min kW, 2019-03-01..2019-09-30. Missing minutes appear as missing rows (kept missing, never interpolated);
a 30-min window counts only with >= 80 % minute coverage; lowest monthly minute coverage 33.8 % (flagged; that facility-month's
billed demand uses only covered windows). Mean monthly billed demand (30-min aligned) per facility, kW: Forge_2 110, Steel_1 121,
Forge_1 127, Metal_1 202, Metal_3 270, Paper 590, Metal_2 657, Cement_2 752, Cement_1 1,491, Steel_2 12,740.

## Method (`src/regenate/evaluation/facility.py`, Colab notebook cells 55-59)
- Monthly cell workload: consecutive non-overlapping 15 h blocks (smallest whole hour >= the longest cell trace), each block one
  held-out DS06 instance drawn with seed 0 (SAME draw for every method), 49-49 blocks/month, 50 instances (those with both the
  Run 3 diag and the E1+peak schedules). Cell net AC power per 15-min slot from the same ledger as all campaigns (TRUE cycles),
  held constant over the slot's minutes; P_meter = P_facility + P_cell_net.
- Billed demand = max aligned 30-min mean of P_meter per calendar month (TNB-style MD interval; aligned/sliding rule NOT_VERIFIED,
  see reports/run4/tariff_registry.md). Increment = MD(facility + cell) - MD(facility).
- Methods: B1p-OPT (optimised in-rack), B2 (existing shared energy, FIFO), P0, ORACLE (Run 3 energy-only), P0-E1-Peak and
  ORACLE-E1-Peak (Run 3 E1 + peak level). ORACLE-BILL (one-shot, true cycles + true facility background, billing-aware peak level
  of `milp.solve`) is the billing headroom test (in progress).

## Results — 1 cell (48 kW rated, peak 15-25 kW), 70 facility-months, paired over facility-months
| Method | mean MD increment kW | median | min | max |
|---|---|---|---|---|
| B2 | 4.62 | 5.01 | -5.09 | 16.35 |
| B1p-OPT | 4.36 | 3.86 | -9.00 | 17.62 |
| P0 | 2.74 | 1.66 | -9.72 | 12.00 |
| P0-E1-Peak | 2.51 | 1.38 | -9.72 | 12.00 |
| ORACLE | 2.54 | 1.78 | -4.71 | 13.20 |
| ORACLE-E1-Peak | 2.28 | 1.78 | -4.71 | 10.47 |
| Comparison (paired 95 % CI) | MD increment reduction kW | wins |
|---|---|---|
| B2 -> P0-E1-Peak (software on existing shared energy, FIN-B) | +2.12 [+1.08, +3.11] | 45/70 |
| B1p-OPT -> P0-E1-Peak | +1.86 [+1.16, +2.57] | 49/70 |
| B2 -> P0 (energy-only rolling) | +1.89 [+0.86, +2.88] | 42/70 |
| P0 -> P0-E1-Peak (E1 + peak level) | +0.23 [-0.12, +0.60] n.s. | 23/70 |
| P0-E1-Peak -> ORACLE-E1-Peak (perfect cycle information) | +0.22 [-0.31, +0.77] n.s. | 26/70 |
Coincidence: the median share of the cell's own peak that appears in the facility's monthly billed demand is 0.09 (P0-E1-Peak),
0.24 (B2). Negative increments occur when cell export (behind the meter) coincides with the facility's billed interval.

Illustrative money value (TNB RP4 MV General demand-related components RM 29.43 + 59.84 per kW-month; verification status in the
tariff registry, still being checked): B2 -> P0-E1-Peak about RM 189 per facility-month (mean), RM 163 (median) for ONE cell.
This replaces the Run 3 instantaneous-peak extrapolation (D015): only 9-24 % of a cell's peak reaches the bill.

## Interpretation (so far)
- At facility level the scheduling software (P0-E1-Peak vs B2 on the same hardware) lowers the billed-demand increment of a cell by
  ~2 kW per month (CI excludes 0). Its money value is roughly an order of magnitude above the cell's energy saving.
- Perfect cycle information (ORACLE) adds nothing significant over P0-E1-Peak at facility level, consistent with Run 3 (AI energy).
- Billing-aware scheduling with the facility background (ORACLE-BILL headroom) is the remaining test before any AI facility-load
  forecasting is justified (WP-J rule).

## Limitations
One cell; one seed of block assignment; 15 h blocks (cell idle between instances is part of the assumption); DS07 Korean loads with
counterfactual Malaysian rates; no time-zone remapping (calendar months of the data); facility load is not reduced by any existing
test equipment (pure addition).

## TNB RP4 MD rule: only peak-period intervals are billed (Mon-Fri 14:00-22:00)
Source of the rule: https://www.mytnb.com.my/tariff (read 2026-11-25): "for Non-Domestic Medium Voltage and High Voltage customers,
Maximum Demand which occurs during Off-Peak period will not be charged"; peak "Monday to Friday / Peak : 2 PM to 10 PM". 30-min
interval length and aligned/sliding rule: NOT_VERIFIED (official MD page refused automated access). Run: Drive
`MyDrive/semiexpo/ai_runs/run4/fac_grid_tnb/facility_md.csv` (`--md_window 0,1,2,3,4:14:22`), same blocks/draw as above, n = 70.
| Method | mean MD increment kW | median |
|---|---|---|
| B2 | 3.86 | 2.55 |
| B1p-OPT | 3.19 | 2.91 |
| P0 | 2.65 | 1.33 |
| P0-E1-Peak | 2.13 | 0.99 |
| ORACLE | 1.92 | 0.99 |
| ORACLE-E1-Peak | 1.54 | 0.60 |
| Paired comparison | reduction kW [95 % CI] | wins |
|---|---|---|
| B2 -> P0-E1-Peak (FIN-B software) | +1.73 [+0.78, +2.67] | 39/70 |
| B1p-OPT -> P0-E1-Peak | +1.06 [+0.19, +1.94] | 41/70 |
| B2 -> P0 | +1.21 [+0.29, +2.11] | 38/70 |
| P0 -> P0-E1-Peak (E1 + peak level) | +0.52 [+0.14, +0.95] | 23/70 |
| P0-E1-Peak -> ORACLE-E1-Peak (perfect cycle info) | +0.59 [+0.14, +1.05] | 37/70 |
Per facility (B2 -> P0-E1-Peak mean kW): Forge_1 7.08 -> 4.14, Metal_1 6.16 -> 2.52, Metal_2 6.15 -> 3.68, Forge_2 5.42 -> 2.32,
Metal_3 2.64 -> -0.95, Cement_2 3.10 -> 1.74, Steel_1 3.55 -> 2.87, Paper 3.14 -> 2.58; Cement_1 0.12 -> 1.05 and Steel_2
1.24 -> 1.37 are worse (zero/negative-benefit facility cases kept). With the peak-only MD rule the E1 + peak level becomes significant
and perfect cycle information now has a significant billing value (+0.59 kW), unlike energy (Run 3) -> a candidate AI opportunity.

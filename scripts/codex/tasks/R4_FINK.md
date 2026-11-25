# R4_FINK — Run 4 WP-K FIN-A/B/C with facility-level monthly billing (code; lead runs it on Colab) (D009, D011, D015; mentor M16)
Account: .codex-B. Effort: medium.
Owner files: src/regenate/economics/fin_facility.py, tests/test_fin_facility.py, reports/run4/economics_run4.md (method + PENDING_COLAB)
Read: AGENTS.md, src/regenate/economics/{fin_options,billing}.py (reuse; do not edit), configs/economics_v3.yaml (CAPEX/OPEX items with
  QUOTED/ESTIMATE/MISSING), data/tariffs/*.yaml, reports/run4/facility_billing.md, reports/run3/economics_v3.md (DS06 section).
Inputs (CLI `python -m regenate.economics.fin_facility --facility CSV --energy CSV --tariff YAML --config YAML --out DIR`):
  facility CSV = facility.py output (facility, month, method, md_increment_kw, cell_kwh, ...); energy CSV = DS06 v2_campaign results
  (instance_id, method, net_kwh, TT_h). Method mapping: FIN-A B1 -> B1-OPT; FIN-B B2 -> P0@v2_e1_peak (default engine D006);
  FIN-C B1 -> P0@v2_e1_peak (or B1p-OPT -> P0 when B1 is not in the facility CSV: say which).
Contract:
1. Per facility-month: demand saving = delta md_increment_kw x tariff demand rates (all demand-dependent components once, no double
   counting of capacity+network if the tariff already defines them as the demand charge); energy saving = paired DS06 energy delta per
   instance x instances in the month x TOU-weighted energy rate (flat if TOU windows NOT_VERIFIED, flagged). Annualise from the 7 DS07
   months explicitly (x12/7) and report the month-to-month spread.
2. Per option: incremental CAPEX/OPEX items with status; MISSING items -> results flagged OPTIMISTIC and a break-even form instead of a
   payback; simple payback, 10-y NPV at 8 %, break-even CAPEX for 3-y and 5-y simple payback (3x / 5x annual net) and discounted
   (PV of 10 y). Non-positive annual net -> "no finite payback".
3. Uncertainty: per-facility distribution (10 facilities), n_cells sensitivity if several facility CSVs are given, tariff scenarios
   (each YAML separately; NOT_VERIFIED rates propagate a flag), CAPEX x0.5/1/2, operating hours, eta_AFE (from economics_v3 sensitivity).
4. Output CSV + a one-paragraph verdict per option: whether any software-first scenario reaches 3-5 y payback and positive NPV, else
   the required break-even conditions (CAPEX ceiling, demand rate, cell-to-facility ratio).
Gate: `python -m pytest -q -p no:cacheprovider --basetemp runs/tmp_pytest_fk tests/test_fin_facility.py` (hand example: 2 kW x RM 89.27
= RM 178.54/month demand saving; MISSING flag; no finite payback when net <= 0; 3x/5x break-even).

## Run 2 (lead) — D017 multi-cell FIN-B and verified TNB tariffs
Tariffs: data/tariffs/TAR01_MY_TNB_RP4_{MV,HV}_{general,TOU}.yaml are now VERIFIED from the official PDF (p.2). General = whole-month MD -> use facility CSVs WITHOUT md_window (fac_gen_*cells, fac_grid); ToU = peak-period MD -> facility CSVs with md_window (fac_tou_*cells, fac_grid_tnb, fac_grid_tnb_3cells). Inputs per n_cells in {1,3,5,10}: facility_md.csv with n_cells column. Cost structure (configs/economics_v3.yaml, keep statuses): SITE-LEVEL shared items (server, software licence/integration, facility meter) counted ONCE per site; PER-CELL items (cell meters, station integration, requalification) x n_cells; MISSING stays MISSING (break-even form). Savings are NOT scaled linearly: use the simulated n-cell MD increments and n x per-cell energy delta only where the energy campaign is per cell. Factory-clustered CIs: use regenate.evaluation.stats.cluster_paired_ci (cluster = facility). Output per (tariff, n_cells): annual demand saving, energy saving, net, payback, NPV, 3-y/5-y break-even CAPEX, with factory-clustered ranges. Verdict: does any defensible FIN-B scenario reach 3-5 y payback and NPV>0? If not, the break-even conditions. Complete and return ALL_PASS.

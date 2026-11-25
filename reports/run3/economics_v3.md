# Run 3 economics

**SIM_ASSUMED_PROFILE**: bench_v1 S3; simulated assumed power profiles. Financial inputs are ASSUMED and investment conclusions NOT_VERIFIED. Results exclude missing costs and are OPTIMISTIC. Matched instances with unequal tardiness are excluded. No site saving is established.

Assume 6,000 operating hours per year, one cell, 10 hours per instance (600 instances/year), and USD 0.0852/kWh weighted flat tariff. This is not a reconstructed TOU bill. Export is credited at alpha=1 for the behind-meter base; alpha=0/0.5 are sensitivities in the CSV. Physical net energy and import-bill and export-credit effects are separated in the CSV when import and export are available. Demand charge is unset; the separate tornado uses an ASSUMED USD 4/kW/month and simulated instance peaks as illustrative monthly peaks, not a bill. Ten years at 8%; no tax, inflation or replacements.

| Option | Pair | n (TT excluded) | physical kWh [paired 95% CI] | annual net USD [paired 95% CI] | break-even CAPEX USD [paired 95% CI] | NPV USD | payback years |
|---|---|---:|---:|---:|---:|---:|---:|
| FIN-A | B1 to B1-OPT | 16 (2) | 0.00 [-0.00, 0.00] | -0.00 [-0.00, 0.00] | -0.00 [-0.00, 0.00] | -4220.00 | not reached |
| FIN-B | B2 to P0 | 16 (2) | 1.31 [0.90, 1.72] | 66.91 [45.98, 87.83] | 448.94 [308.53, 589.35] | -3771.06 | 63.1 |
| FIN-C | B1 to P0 | 16 (2) | 9.65 [9.19, 10.12] | 493.49 [469.88, 517.11] | 3311.37 [3152.92, 3469.82] | -27152.63 | 61.7 |

FIN-A: not justified under these assumptions. FIN-B: justified only if verified net benefits exceed complete costs, potentially including an applicable demand charge. FIN-C: justified only if verified net benefits exceed complete retrofit costs.

Server, meters and converter/bus/safety are ESTIMATE; installation, requalification and annual support are MISSING for each applicable option. Missing items are excluded, never established as zero. See config and CSV for item-level statuses and output ranges. Tornado covers tariff, duty, demand and estimated CAPEX factors. DS06 rows are PENDING; use --results to rerun when available. With only net_kwh, export-credit decomposition and alpha sensitivities are unavailable. Without TT_h, matching on tardiness is NOT_VERIFIED.

The following eta_AFE sensitivity converts the existing S3 paired gain from B1p-OPT to ORACLE into the present value of energy savings; it is an **ORACLE-level gain (upper bound), SIM_ASSUMED_PROFILE**, not a P0 option result. The bounds propagate the source gain interval. It uses the same assumed annualisation, tariff and discounting above, excludes missing OPEX and demand charges, and is OPTIMISTIC. Source: [sensitivity results](../../runs/sens_v1/sensitivity_results.csv); output: [eta sensitivity](../../runs/run3/econ/eta_afe_v3.csv).

| eta_AFE | Break-even CAPEX USD [source interval] |
|---:|---:|
| 0.94 | 4,249 [4,074, 4,386] |
| 0.96 | 2,689 [2,577, 2,777] |
| 0.98 | 1,137 [1,090, 1,176] |

Water: qualitative only; cooling-loop and water metering are required.

## DS06 (measured-cycle bench v2) — lead rerun with `fin_options.build`, Colab
Source: Drive `MyDrive/semiexpo/ai_runs/run3/fin_v3_ds06.csv`; inputs `ai_runs/v2_flex025_n100.csv` (n=100) and the peak-aware
run `ai_runs/v2_peak/results.csv` (P0 relabelled P0-peak, n=50 subset). Boundary **SIM_DATA_PROFILE**; annualisation ASSUMED:
6,000 h/year, 1 cell, instance = mean P0 makespan 9.66 h; flat USD 0.0852/kWh; alpha=1 base; 10 y, 8 %. Cell size: 8 stations x
25 modules x 0.24 kW = 48 kW rated (ASSUMED scaling of DS05 modules). Missing cost items (installation, requalification,
annual support) excluded -> results OPTIMISTIC. Pairs with unequal tardiness excluded (n shown).

| Option | Pair | n | physical kWh/instance [CI] | peak kW [CI] | annual net USD (no demand charge) | break-even CAPEX USD | payback (y) at 0 / 4 / 10 USD/kW-month |
|---|---|---|---|---|---|---|---|
| FIN-A | B1 -> B1-OPT | 100 | 0.000 | 0.55 [-0.20, 1.29] | 0 | 0 | not reached / 160 / 64 |
| FIN-B | B2 -> P0 | 90 | 0.244 [0.213, 0.275] | 3.34 [2.59, 4.08] | 12.9 | 87 | 327 / 24 / 10.2 |
| FIN-B | B2 -> P0-peak | 43 | 0.242 [0.194, 0.290] | 3.73 [2.62, 4.84] | 12.8 | 86 | 330 / 22 / 9.2 |
| FIN-C | B1 -> P0 | 90 | 3.111 [2.993, 3.228] | 3.95 [3.19, 4.71] | 164.6 | 1,105 | 185 / 86 / 48 |
NPV (10 y, 8 %) is negative for every option and tariff case above (best: FIN-B P0-peak at 10 USD/kW-month, NPV -1,130 USD
against the ESTIMATE CAPEX of 4,220 USD).

Reading:
- Energy alone never pays back at this cell size: the physical saving per 9.7 h instance is 3.1 kWh (FIN-C) or 0.24 kWh (FIN-B).
- The demand charge dominates: FIN-B (software + meters on an existing shared DC bus) reaches ~9-10 y payback at 10 USD/kW-month
  and the peak-aware level helps (P0-peak 9.2 y vs P0 10.2 y). Peak savings count only if the site tariff has a demand charge.
- FIN-A (scheduling on regen-to-AC with behind-the-meter netting) has zero energy value by physics (1:1 netting) and only a small,
  non-significant peak effect.
- Scale: both kWh and kW savings scale with station power; DS06's 6 kW stations are small for burn-in/power-cycling racks. A linear
  scaling to larger stations is an ASSUMPTION, not a result; the break-even CAPEX per cell must be recomputed with site traces.
Status M16: **FAIL at the DS06 cell size for all options** (no positive NPV); FIN-B is the only option that approaches payback,
conditional on a demand charge and on complete (currently MISSING) installation/requalification costs.

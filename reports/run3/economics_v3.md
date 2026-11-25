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

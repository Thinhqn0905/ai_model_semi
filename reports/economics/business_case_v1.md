# Business case v1

**SIM_ASSUMED_PROFILE; ASSUMED financial inputs.** Results are modeled sensitivities, not site savings or investment approval. Inputs: runs/rolling_v1/ladder.csv; scenarios use matched instance IDs and equal TT only. Paired 95% t intervals are across instances.

One assumed 50 kW cell; 6,000 operating hours/year, 600 instances/year and 10 hours/instance are scaling assumptions, not measured duty cycles. This scaling does not rescale the simulated power; actual durations and peak powers differ. The profile is simulated and assumed, not a measured cell.

The baseline methods are absent from timeseries.parquet, so actual TOU cost cannot be recovered. We assume the same Monday?Saturday time-band mix for all imports and exports: 25% off-peak, 13/24 normal and 5/24 peak. Apply the configured EVN VND rates and an assumed 25,000 VND/USD conversion. This is a weighted-rate approximation, not a reconstructed TOU bill; no Sunday adjustment or schedule-dependent tariff shift is modeled. The base case uses alpha=1 because the cell is behind the plant main meter and its export is consumed by other plant loads 1:1 (D001). Alpha=0 and 0.5 are sensitivities for a facility that is net-exporting to the grid.

Slide-16 server $4,220 for A/B and meters $4,406 + server $4,220 + converter/bus/safety $21,838 for C are ASSUMED estimates; CAPEX multipliers 0.5, 1, 2 are swept. OPEX, installation and requalification are unknown: zero is an optimistic placeholder, not evidence of zero cost. NPV assumes 8% and 10 years, no taxes, inflation or replacement. Demand sensitivity assumes 100,000 VND/kW/month for 12 months using paired simulated instance peaks as representative monthly peaks; it is not a bill estimate. The no-demand case is the default.

Base assumptions: alpha=1, CAPEX factor=1, no demand charge. The previous alpha=0 headline overstated FIN-B because it counted only import reduction, ignoring the offsetting change in export. Delta is baseline minus intervention net M0 kWh per instance. Payback range uses the kWh CI bounds with demand and OPEX held fixed; not reached includes nonpositive savings. Full sensitivity sweep and CI payback ranges: [business_case.csv](../../runs/biz_v1/business_case.csv).

| Scenario | Option (baseline to intervention) | n (excluded TT) | Delta kWh mean [95% CI] | Annual USD | Payback years [CI range] | NPV USD |
|---|---|---:|---:|---:|---:|---:|
| S1 | FIN-A (B1 to B1-OPT) | 18 (0) | 0.00 [0.00, 0.00] | 0.00 | not reached | -4,220.00 |
| S1 | FIN-B (B2 to P0) | 16 (2) | 0.00 [0.00, 0.00] | 0.00 | not reached | -4,220.00 |
| S1 | FIN-B (B2 to P) | 18 (0) | 0.00 [0.00, 0.00] | 0.00 | not reached | -4,220.00 |
| S1 | FIN-C (B1 to P0) | 16 (2) | 23.16 [21.99, 24.33] | 1,184.27 | 25.72 [24.49, 27.09] | -22,517.44 |
| S3 | FIN-A (B1 to B1-OPT) | 16 (2) | 0.00 [0.00, 0.00] | 0.00 | not reached | -4,220.00 |
| S3 | FIN-B (B2 to P0) | 16 (2) | 1.31 [0.90, 1.72] | 66.92 | 63.06 [48.04, 91.76] | -3,770.96 |
| S3 | FIN-B (B2 to P) | 15 (3) | 0.37 [0.03, 0.72] | 19.03 | 221.72 [114.96, 3,107.27] | -4,092.29 |
| S3 | FIN-C (B1 to P0) | 16 (2) | 9.65 [9.19, 10.12] | 493.61 | 61.72 [58.90, 64.82] | -27,151.86 |

Under the alpha=1 base assumptions, no option has positive 10-year NPV. In the alpha=1 sweep, S3 FIN-B with P0 has positive NPV only with the assumed demand charge and CAPEX factor 0.5 or 1; S3 FIN-A does so only with that demand charge and factor 0.5. The other alpha=1 cases remain negative. None is established as financially justified until tariffs, profiles and complete costs are verified. FIN-B P is a separate comparison, not evidence that forecasting improves on P0.

D001: converter burn-in S1 has zero shared-DC saving relative to in-rack reuse (B1p), because no residual source exists. FIN-C instead compares P0 with B1, so its nonzero S1 delta includes in-rack reuse and scheduling effects and must not be attributed to shared DC. This D001 statement is analytic, not a measured site result.

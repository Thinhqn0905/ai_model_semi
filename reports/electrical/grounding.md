# Electrical grounding

Boundary: **SIM_ASSUMED_PROFILE + DATASHEET efficiencies**. The benchmark is synthetic, not a site measurement. Stage curves are proxies from a TI reference design, not demonstrated efficiencies of the proposed cell. All values below use load fraction 0.5, defined as stage output power divided by its nominal rating; fractional load is held constant for the campaign. Interpolation is linear between printed points; duplicate loads are averaged. The measured tables are not necessarily monotone, and no monotonicity is imposed. Calls outside a stage's observed range are rejected. Applying the same load fraction to consecutive stages is an approximation.

| Efficiency | Previous ledger default | Grounded proxy | Provenance |
|---|---:|---:|---|
| supply DC | 0.970 | 0.993167 | DATASHEET: TIDA-010938 battery buck 320 V, tiduf64c.pdf p. 39 |
| regen DC | 0.970 | 0.993000 | DATASHEET: battery boost 320 V, p. 41 |
| AFE export | 0.970 | 0.981000 | DATASHEET: DC/AC unipolar, p. 43 |
| AFE import | 0.970 | 0.981000 | ASSUMED: reverse direction equals the DC/AC export curve, p. 43; no import curve established |
| supply AC | 0.920 | 0.9742965 | DERIVED: import AFE × supply DC, pp. 39, 43 |
| regen AC | 0.940 | 0.974133 | DERIVED: regen DC × export AFE, pp. 41, 43 |
| link | 0.990 | 0.990000 | ASSUMED: docs/system_spec.md §5, 1% cable/breaker loss allowance; cable length, conductor and current are unspecified, so this is not a sizing calculation |

Cross-check only, VENDOR_REPORTED: Chroma 62450D-2000HL up to 94% recovery at rated conditions (DS03_Modeling/62000D-EN.pdf p. 2); Chroma 63700 advertises up to 93% (DS03_Modeling/63700 Regen DC Load 052024.pdf pp. 1–3). These are whole-device AC-boundary figures, not individual stage curves, and highlight that the TI-derived composite should not be treated as a measured Chroma efficiency.

## D001 analytical effect

ANALYTIC, defaults versus grounded proxies: `dc_gain_bound` is 0.050619 versus 0.028174 kWh saved per kWh residual source, respectively. Formula: `(eta_link - eta_afe_exp * eta_afe_imp) / eta_afe_imp`, assuming the displaced AC import exists and link transfer is feasible. This reduces the theoretical conversion-loss advantage; D001's need for simultaneous residual source and demand remains. It is not a prediction of cell savings.

## Matched oracle campaign

SIM_ASSUMED_PROFILE + DATASHEET efficiencies; `runs/oracle_grounded/results.csv`, `manifest.json`, `campaign.log`. Command parameters: n=10, seeds 0 and 1, flex=0.25, time limit 30 s, workers 6, `--prm` equal to configs/elec_grounded.yaml. All methods share instances and electrical settings; defaults include unlimited link and AFE capacity, with export allowed. Differences are baseline minus ORACLE net M0 kWh, paired by instance with equal realized total tardiness; 95% percentile bootstrap intervals from `regenate.evaluation.stats.ladder_table` (18 matched instances per row). Related instances share seeds, so these intervals do not establish independent real-world sampling uncertainty.

| Scenario | Baseline | Mean difference, kWh | 95% paired CI, kWh |
|---|---|---:|---:|
| S1 | B1p-OPT | 0.000 | [0.000, 0.000] |
| S1 | B1-OPT | 9.804 | [9.385, 10.154] |
| S3 | B1p-OPT | 3.090 | [2.978, 3.181] |
| S3 | B1-OPT | 3.090 | [2.978, 3.181] |

The S1 B1 difference includes modeled in-rack reuse relative to the separate B1 AC path and does not establish an incremental shared-link benefit over B1p. S3 ORACLE reached its time limit in 15 of 18 instances; these are incumbent solutions, not certified global optima or a proven ceiling. B1-OPT and B1p-OPT were reported optimal for all S1 and S3 instances. This evidence does not establish site performance or validate the assumed import symmetry and link loss.

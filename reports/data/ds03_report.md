# DS03 evidence and limitations

## Efficiency point (VENDOR_REPORTED)

| Device | Direction | Load fraction | Efficiency | Source and page | Qualification |
|---|---|---:|---:|---|---|
| Chroma 62450D-2000HL | regen | 1 | up to 0.94 | 62000D-EN.pdf, p. 2 | Rated conditions; voltage and grid-side output not specified. |

This is an upper-bound vendor statement, not an empirical load curve or a guaranteed efficiency. The interpolator has the singleton valid range [1, 1]; clamping outside that range is not validated extrapolation. No plotted curves were digitised. No forward or AFE curves are supported by these extracted points; querying them fails explicitly. Chroma 63700's advertised up-to-93% recovery (63700 Regen DC Load 052024.pdf, pp. 1–3) does not identify a load fraction and is not inserted as a curve point.

## Equipment ratings (VENDOR_REPORTED)

| Model | Power | DC voltage | DC current | Source |
|---|---:|---:|---:|---|
| 62450D-2000HL | 45 kW | 2000 V high / 650 V low | 60 A high / 180 A low | 62000D-EN.pdf, p. 1 |
| 63718-100-540 | 18 kW | 100 V | 540 A | 63700 Regen DC Load 052024.pdf, p. 12 |
| 63706-600-40 | 6 kW | 600 V | 40 A | same, p. 12 |
| 63712-600-80 | 12 kW | 600 V | 80 A | same, p. 12 |
| 63718-600-120 | 18 kW | 600 V | 120 A | same, p. 12 |
| 63712-1200-40 | 12 kW | 1200 V | 40 A | same, p. 12 |
| 63718-1200-40 | 18 kW | 1200 V | 40 A | same, p. 12 |
| 63718-1800-40 | 18 kW | 1800 V | 40 A | same, p. 12 |

The recovery figures are AC-boundary system efficiencies and may inform eta_rl_ac, not a separate DC-link eta_rl or eta_afe. Ratings constrain equipment power; eta_sup, eta_afe and load-dependent efficiencies remain ASSUMED until independently sourced. The 62000D and 63700 ratings are model-specific, not simultaneous series-wide operating limits.

## EDC (MEASURED / DERIVED)

Each January CSV is one recorded charge/discharge sequence. Voltage, power and SOC are measured as provided; current magnitude is derived as |power|/voltage. Phase follows signed supercapacitor power. Transformer-side import and export are integrated over elapsed seconds using the trapezoidal rule, then divided to obtain a per-file round-trip ratio. Ratios and current are DERIVED, not measurements. Endpoints are not necessarily at identical SOC, so ratios are observed sequence energy ratios, not closed-cycle device efficiencies. Data files and exact transformations are recorded in the provenance sidecar.
..                                                                       [100%]
2 passed in 1.41s


## Additional printed source data (VENDOR_REPORTED)

Chroma 62000D typical source/sink efficiencies are lower bounds, with no corresponding load fraction: page 13: 62060D-100 >91%/>90%, 62120D-100 >91%/>90%, 62180D-100 >92%/>90%, 62060D-600 >91%/>92%, 62120D-600 >92%/>93%, 62180D-600 >92%/>93%; page 15: 62120D-1200 >91%/>92%, 62180D-1200 >91%/>90%, 62180D-1800 >92%/>93%; page 17: 62300D-1300HL >94.3%/>94%, 62360D-2000HL >93.6%/>93.6%, 62450D-2000HL >94.3%/>94%. These bounds are not exact curve points. Page 9 states series PFC >0.97; page 17 onward specifies PF >0.99 under its table conditions. THD is not specified in the extracted efficiency/specification text.

Chroma 63700 advertises up to 93% recovery (pp. 1?3), with no load-specific curve values. Page 10 specifies 10 mA/ms?30 A/ms or 10 mA/ms?20 A/ms slew by model group and typical minimum rise time 2 ms; consult the source for model conditions. These are equipment characteristics, not site performance.

TI TIDUE53J p. 2 reports 11 kW, 800 V nominal DC and 98.6% efficiency without a tabulated load coordinate. Its curves were not eyeballed. TI TIDUF64C p. 5 specifies nominal 5 kW per PV boost stage, 10 kW bidirectional stage, and 4.6 kW rated DC/AC stage. The table below transcribes all printed power/efficiency pairs from pp. 38, 39, 41 and 43; DC bus is 400 V and the device name encodes battery/PV voltage or DC/AC modulation. Load fraction divides printed output by the relevant stage nominal/rated power; rounded printed values can duplicate a load fraction. No plot digitisation was used.

These reference-design measurements can inform candidate eta_sup, eta_rl or eta_afe only for their specified stages and conditions; actual station and link efficiencies remain ASSUMED until validated. Curves can rise and fall. `eta_curve` averages eta at duplicate load fractions and records the affected loads and counts in `duplicate_loads`; the data product retains all original points. The printed TI tables provide at least four points for multiple operating conditions.

| Device | Direction | Output kW | Load fraction | Efficiency | Source page |
|---|---|---:|---:|---:|---|
| TIDA-010938-pv-boost-50 | forward | 0.1 | 0.020000 | 0.9540 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-150 | forward | 0.4 | 0.080000 | 0.9770 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-200 | forward | 0.6 | 0.120000 | 0.9830 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-250 | forward | 0.7 | 0.140000 | 0.9850 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-300 | forward | 0.9 | 0.180000 | 0.9880 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-350 | forward | 1 | 0.200000 | 0.9900 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-50 | forward | 0.2 | 0.040000 | 0.9490 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-150 | forward | 0.6 | 0.120000 | 0.9810 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-200 | forward | 0.8 | 0.160000 | 0.9850 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-250 | forward | 1 | 0.200000 | 0.9880 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-300 | forward | 1.2 | 0.240000 | 0.9900 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-350 | forward | 1.4 | 0.280000 | 0.9920 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-50 | forward | 0.2 | 0.040000 | 0.9530 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-150 | forward | 0.7 | 0.140000 | 0.9830 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-200 | forward | 1 | 0.200000 | 0.9860 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-250 | forward | 1.2 | 0.240000 | 0.9890 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-300 | forward | 1.5 | 0.300000 | 0.9910 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-350 | forward | 1.7 | 0.340000 | 0.9920 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-50 | forward | 0.3 | 0.060000 | 0.9560 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-150 | forward | 0.9 | 0.180000 | 0.9830 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-200 | forward | 1.2 | 0.240000 | 0.9870 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-250 | forward | 1.5 | 0.300000 | 0.9900 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-300 | forward | 1.8 | 0.360000 | 0.9910 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-350 | forward | 2.1 | 0.420000 | 0.9920 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-50 | forward | 0.3 | 0.060000 | 0.9570 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-150 | forward | 1 | 0.200000 | 0.9840 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-200 | forward | 1.4 | 0.280000 | 0.9880 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-250 | forward | 1.7 | 0.340000 | 0.9900 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-300 | forward | 2.1 | 0.420000 | 0.9910 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-350 | forward | 2.4 | 0.480000 | 0.9930 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-50 | forward | 0.4 | 0.080000 | 0.9580 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-150 | forward | 1.2 | 0.240000 | 0.9850 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-200 | forward | 1.6 | 0.320000 | 0.9880 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-250 | forward | 2 | 0.400000 | 0.9900 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-300 | forward | 2.4 | 0.480000 | 0.9910 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-350 | forward | 2.8 | 0.560000 | 0.9930 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-50 | forward | 0.4 | 0.080000 | 0.9580 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-150 | forward | 1.3 | 0.260000 | 0.9850 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-200 | forward | 1.8 | 0.360000 | 0.9880 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-250 | forward | 2.2 | 0.440000 | 0.9900 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-300 | forward | 2.7 | 0.540000 | 0.9920 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-350 | forward | 3.1 | 0.620000 | 0.9930 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-50 | forward | 0.5 | 0.100000 | 0.9570 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-150 | forward | 1.5 | 0.300000 | 0.9850 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-200 | forward | 2 | 0.400000 | 0.9880 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-250 | forward | 2.5 | 0.500000 | 0.9900 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-300 | forward | 3 | 0.600000 | 0.9910 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-350 | forward | 3.5 | 0.700000 | 0.9920 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-50 | forward | 0.5 | 0.100000 | 0.9570 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-150 | forward | 1.6 | 0.320000 | 0.9840 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-200 | forward | 2.2 | 0.440000 | 0.9870 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-250 | forward | 2.7 | 0.540000 | 0.9890 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-300 | forward | 3.3 | 0.660000 | 0.9910 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-350 | forward | 3.8 | 0.760000 | 0.9920 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-50 | forward | 0.6 | 0.120000 | 0.9570 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-150 | forward | 1.8 | 0.360000 | 0.9840 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-200 | forward | 2.4 | 0.480000 | 0.9870 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-250 | forward | 3 | 0.600000 | 0.9890 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-300 | forward | 3.6 | 0.720000 | 0.9910 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-350 | forward | 4.2 | 0.840000 | 0.9920 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-50 | forward | 0.6 | 0.120000 | 0.9560 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-150 | forward | 1.9 | 0.380000 | 0.9830 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-200 | forward | 2.6 | 0.520000 | 0.9870 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-250 | forward | 3.2 | 0.640000 | 0.9890 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-300 | forward | 3.9 | 0.780000 | 0.9910 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-350 | forward | 4.6 | 0.920000 | 0.9920 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-50 | forward | 0.7 | 0.140000 | 0.9550 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-150 | forward | 2.1 | 0.420000 | 0.9830 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-200 | forward | 2.8 | 0.560000 | 0.9870 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-250 | forward | 3.5 | 0.700000 | 0.9890 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-300 | forward | 4.2 | 0.840000 | 0.9910 | tiduf64c.pdf p. 38 |
| TIDA-010938-pv-boost-350 | forward | 4.9 | 0.980000 | 0.9920 | tiduf64c.pdf p. 38 |
| TIDA-010938-battery-buck-80 | forward | 0.2 | 0.020000 | 0.9490 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-160 | forward | 0.3 | 0.030000 | 0.9700 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-240 | forward | 0.3 | 0.030000 | 0.9720 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-320 | forward | 0.4 | 0.040000 | 0.9820 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-80 | forward | 0.3 | 0.030000 | 0.9710 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-160 | forward | 0.7 | 0.070000 | 0.9820 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-240 | forward | 0.8 | 0.080000 | 0.9850 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-320 | forward | 1 | 0.100000 | 0.9910 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-80 | forward | 0.5 | 0.050000 | 0.9750 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-160 | forward | 1 | 0.100000 | 0.9860 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-240 | forward | 1.3 | 0.130000 | 0.9900 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-320 | forward | 1.7 | 0.170000 | 0.9930 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-80 | forward | 0.7 | 0.070000 | 0.9750 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-160 | forward | 1.3 | 0.130000 | 0.9880 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-240 | forward | 1.7 | 0.170000 | 0.9920 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-320 | forward | 2.3 | 0.230000 | 0.9930 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-80 | forward | 0.8 | 0.080000 | 0.9750 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-160 | forward | 1.6 | 0.160000 | 0.9890 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-240 | forward | 2.2 | 0.220000 | 0.9930 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-320 | forward | 3 | 0.300000 | 0.9930 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-80 | forward | 1 | 0.100000 | 0.9760 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-160 | forward | 2 | 0.200000 | 0.9870 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-240 | forward | 2.7 | 0.270000 | 0.9910 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-320 | forward | 3.6 | 0.360000 | 0.9930 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-80 | forward | 1.2 | 0.120000 | 0.9770 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-160 | forward | 2.3 | 0.230000 | 0.9870 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-240 | forward | 3.2 | 0.320000 | 0.9910 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-320 | forward | 4.2 | 0.420000 | 0.9940 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-80 | forward | 1.3 | 0.130000 | 0.9770 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-160 | forward | 2.6 | 0.260000 | 0.9880 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-240 | forward | 3.7 | 0.370000 | 0.9920 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-320 | forward | 4.9 | 0.490000 | 0.9930 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-80 | forward | 1.5 | 0.150000 | 0.9770 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-160 | forward | 2.9 | 0.290000 | 0.9880 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-240 | forward | 4.2 | 0.420000 | 0.9920 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-320 | forward | 5.5 | 0.550000 | 0.9940 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-80 | forward | 1.7 | 0.170000 | 0.9770 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-160 | forward | 3.2 | 0.320000 | 0.9870 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-240 | forward | 4.6 | 0.460000 | 0.9910 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-320 | forward | 6.1 | 0.610000 | 0.9930 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-80 | forward | 1.8 | 0.180000 | 0.9760 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-160 | forward | 3.6 | 0.360000 | 0.9870 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-240 | forward | 5.1 | 0.510000 | 0.9910 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-320 | forward | 6.5 | 0.650000 | 0.9930 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-80 | forward | 2 | 0.200000 | 0.9760 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-160 | forward | 3.9 | 0.390000 | 0.9870 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-240 | forward | 5.6 | 0.560000 | 0.9910 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-320 | forward | 6.7 | 0.670000 | 0.9930 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-80 | forward | 2.2 | 0.220000 | 0.9760 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-160 | forward | 4.2 | 0.420000 | 0.9870 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-240 | forward | 6.1 | 0.610000 | 0.9910 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-320 | forward | 7 | 0.700000 | 0.9920 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-80 | forward | 2.2 | 0.220000 | 0.9750 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-160 | forward | 4.6 | 0.460000 | 0.9860 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-240 | forward | 6.6 | 0.660000 | 0.9910 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-320 | forward | 7.4 | 0.740000 | 0.9920 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-buck-80 | forward | 2.3 | 0.230000 | 0.9740 | tiduf64c.pdf p. 39 |
| TIDA-010938-battery-boost-80 | regen | 0.1 | 0.010000 | 0.9390 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-160 | regen | 0.3 | 0.030000 | 0.9690 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-240 | regen | 0.7 | 0.070000 | 0.9840 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-320 | regen | 1 | 0.100000 | 0.9910 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-80 | regen | 0.3 | 0.030000 | 0.9620 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-160 | regen | 0.6 | 0.060000 | 0.9810 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-240 | regen | 1.2 | 0.120000 | 0.9900 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-320 | regen | 1.6 | 0.160000 | 0.9930 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-80 | regen | 0.4 | 0.040000 | 0.9680 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-160 | regen | 0.9 | 0.090000 | 0.9860 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-240 | regen | 1.7 | 0.170000 | 0.9920 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-320 | regen | 2.2 | 0.220000 | 0.9930 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-80 | regen | 0.6 | 0.060000 | 0.9690 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-160 | regen | 1.2 | 0.120000 | 0.9860 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-240 | regen | 2.1 | 0.210000 | 0.9920 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-320 | regen | 2.9 | 0.290000 | 0.9930 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-80 | regen | 0.7 | 0.070000 | 0.9710 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-160 | regen | 1.5 | 0.150000 | 0.9870 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-240 | regen | 2.6 | 0.260000 | 0.9910 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-320 | regen | 3.5 | 0.350000 | 0.9930 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-80 | regen | 0.9 | 0.090000 | 0.9720 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-160 | regen | 1.8 | 0.180000 | 0.9860 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-240 | regen | 3.1 | 0.310000 | 0.9910 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-320 | regen | 4.1 | 0.410000 | 0.9940 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-80 | regen | 1 | 0.100000 | 0.9740 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-160 | regen | 2.1 | 0.210000 | 0.9860 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-240 | regen | 3.5 | 0.350000 | 0.9910 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-320 | regen | 4.7 | 0.470000 | 0.9930 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-80 | regen | 1.1 | 0.110000 | 0.9740 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-160 | regen | 2.4 | 0.240000 | 0.9860 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-240 | regen | 4 | 0.400000 | 0.9910 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-320 | regen | 5.3 | 0.530000 | 0.9930 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-80 | regen | 1.3 | 0.130000 | 0.9730 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-160 | regen | 2.7 | 0.270000 | 0.9860 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-240 | regen | 4.5 | 0.450000 | 0.9910 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-320 | regen | 5.9 | 0.590000 | 0.9930 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-80 | regen | 1.4 | 0.140000 | 0.9730 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-160 | regen | 3 | 0.300000 | 0.9860 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-240 | regen | 4.9 | 0.490000 | 0.9910 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-320 | regen | 6.5 | 0.650000 | 0.9920 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-80 | regen | 1.5 | 0.150000 | 0.9730 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-160 | regen | 3.3 | 0.330000 | 0.9850 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-240 | regen | 5.4 | 0.540000 | 0.9900 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-320 | regen | 7.2 | 0.720000 | 0.9930 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-80 | regen | 1.7 | 0.170000 | 0.9720 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-160 | regen | 3.6 | 0.360000 | 0.9850 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-240 | regen | 5.8 | 0.580000 | 0.9890 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-320 | regen | 7.5 | 0.750000 | 0.9930 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-80 | regen | 1.9 | 0.190000 | 0.9710 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-160 | regen | 3.9 | 0.390000 | 0.9850 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-240 | regen | 6.3 | 0.630000 | 0.9900 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-320 | regen | 7.8 | 0.780000 | 0.9920 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-80 | regen | 1.9 | 0.190000 | 0.9690 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-160 | regen | 4.2 | 0.420000 | 0.9840 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-240 | regen | 6.7 | 0.670000 | 0.9890 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-80 | regen | 2.1 | 0.210000 | 0.9660 | tiduf64c.pdf p. 41 |
| TIDA-010938-battery-boost-160 | regen | 4.4 | 0.440000 | 0.9830 | tiduf64c.pdf p. 41 |
| TIDA-010938-dc-ac-unipolar | regen | 0.3 | 0.065217 | 0.9410 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-bipolar | regen | 0.3 | 0.065217 | 0.9520 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-heric | regen | 0.4 | 0.086957 | 0.9660 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-unipolar | regen | 0.5 | 0.108696 | 0.9560 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-bipolar | regen | 0.5 | 0.108696 | 0.9620 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-heric | regen | 0.5 | 0.108696 | 0.9730 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-unipolar | regen | 0.7 | 0.152174 | 0.9650 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-bipolar | regen | 0.7 | 0.152174 | 0.9680 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-heric | regen | 0.7 | 0.152174 | 0.9770 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-unipolar | regen | 0.9 | 0.195652 | 0.9700 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-bipolar | regen | 1 | 0.217391 | 0.9740 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-heric | regen | 0.9 | 0.195652 | 0.9800 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-unipolar | regen | 1 | 0.217391 | 0.9720 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-bipolar | regen | 1.4 | 0.304348 | 0.9760 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-heric | regen | 1.2 | 0.260870 | 0.9820 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-unipolar | regen | 1.4 | 0.304348 | 0.9780 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-bipolar | regen | 1.8 | 0.391304 | 0.9780 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-heric | regen | 1.4 | 0.304348 | 0.9830 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-unipolar | regen | 1.8 | 0.391304 | 0.9790 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-bipolar | regen | 2.1 | 0.456522 | 0.9790 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-heric | regen | 1.8 | 0.391304 | 0.9840 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-unipolar | regen | 2.1 | 0.456522 | 0.9800 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-bipolar | regen | 2.3 | 0.500000 | 0.9790 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-heric | regen | 2.1 | 0.456522 | 0.9840 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-unipolar | regen | 2.3 | 0.500000 | 0.9810 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-bipolar | regen | 2.5 | 0.543478 | 0.9790 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-heric | regen | 2.3 | 0.500000 | 0.9840 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-unipolar | regen | 2.5 | 0.543478 | 0.9810 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-bipolar | regen | 2.8 | 0.608696 | 0.9800 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-heric | regen | 2.5 | 0.543478 | 0.9840 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-unipolar | regen | 2.7 | 0.586957 | 0.9810 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-bipolar | regen | 3.2 | 0.695652 | 0.9790 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-heric | regen | 2.8 | 0.608696 | 0.9840 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-unipolar | regen | 2.9 | 0.630435 | 0.9820 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-bipolar | regen | 3.4 | 0.739130 | 0.9790 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-heric | regen | 3 | 0.652174 | 0.9840 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-unipolar | regen | 3 | 0.652174 | 0.9820 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-bipolar | regen | 3.8 | 0.826087 | 0.9790 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-heric | regen | 3.2 | 0.695652 | 0.9840 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-unipolar | regen | 3.2 | 0.695652 | 0.9820 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-bipolar | regen | 3.9 | 0.847826 | 0.9790 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-heric | regen | 3.4 | 0.739130 | 0.9830 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-unipolar | regen | 3.4 | 0.739130 | 0.9820 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-bipolar | regen | 4.1 | 0.891304 | 0.9780 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-heric | regen | 3.6 | 0.782609 | 0.9830 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-unipolar | regen | 3.6 | 0.782609 | 0.9820 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-bipolar | regen | 4.3 | 0.934783 | 0.9780 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-heric | regen | 3.8 | 0.826087 | 0.9830 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-unipolar | regen | 3.8 | 0.826087 | 0.9810 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-bipolar | regen | 4.4 | 0.956522 | 0.9780 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-heric | regen | 3.9 | 0.847826 | 0.9830 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-unipolar | regen | 3.9 | 0.847826 | 0.9810 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-bipolar | regen | 4.6 | 1.000000 | 0.9770 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-heric | regen | 4.1 | 0.891304 | 0.9820 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-unipolar | regen | 4.1 | 0.891304 | 0.9810 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-heric | regen | 4.3 | 0.934783 | 0.9820 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-unipolar | regen | 4.3 | 0.934783 | 0.9810 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-heric | regen | 4.4 | 0.956522 | 0.9820 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-unipolar | regen | 4.4 | 0.956522 | 0.9800 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-heric | regen | 4.5 | 0.978261 | 0.9810 | tiduf64c.pdf p. 43 |
| TIDA-010938-dc-ac-unipolar | regen | 4.6 | 1.000000 | 0.9800 | tiduf64c.pdf p. 43 |

## Gate output (local check; NOT_VERIFIED for system performance)

```text
> python -m pytest -q tests/test_ds03.py
. . .                                                                                                                                             [ 1 0 0 % ]  
 3   p a s s e d   i n   9 . 8 5 s  
 ```

# DS02 SHIFT2DC audit

Boundary: SOURCE_REPORTED / MEASURED operational traces, not ReGenATE performance. Source: [SHIFT2DC Zenodo](https://doi.org/10.5281/zenodo.18524234), CC BY 4.0.

Source clock timezone and clock source are undocumented; UTC labels assume UTC and do not establish actual UTC. No interpolation. A/B duplicate timestamps are retained. C uses the provider-aligned file; 12 connection events are omitted by that source. No input exceeds 2 million rows, so no downsampling or anti-alias filtering was applied. Above that threshold the loader uses time-bin means (boxcar low-pass; limited stopband rejection), with separate positive and negative C power magnitudes.

A/B V is the DC bus node; total bus I and P are unavailable, not zero. Additional infeed current (A), infeed power magnitude (kW) and source sign, battery current (A), and state (source code) are distinct channels. C contains SCCB/AFE-terminal V (V), signed I (A), power magnitude (kW), source power sign, temperature (°C), and state (source code). Current and power flow signs are not documented; sign does not identify import/export. A/B infeed source sign is preserved separately and does not identify flow direction.

## Dataset A
- Rows: 86399; span: 24.000 h; median positive interval: 1.000 s (~1.000 Hz); duplicate timestamps: 0.
- Missing values in applicable channels: {'dataset': 0, 'ts': 0, 'v_bus': 0, 'infeed_i_a': 0, 'infeed_p_kw': 0, 'infeed_power_sign': 0, 'battery_i_a': 0, 'state': 0, 'provenance': 0}.
- Voltage V min/p1/p50/p99/max: 374.300 / 374.800 / 375.400 / 395.000 / 398.500.
- Fraction of samples outside 380–420 V: 50.8895% (sample-weighted approximation to time share). Bus I/P unavailable; infeed I range 0.140–1.260 A; infeed P magnitude range 0.056–0.473 kW.

## Dataset B
- Rows: 86399; span: 24.000 h; median positive interval: 1.000 s (~1.000 Hz); duplicate timestamps: 1440.
- Missing values in applicable channels: {'dataset': 0, 'ts': 0, 'v_bus': 0, 'infeed_i_a': 0, 'infeed_p_kw': 0, 'infeed_power_sign': 0, 'battery_i_a': 0, 'state': 0, 'provenance': 0}.
- Voltage V min/p1/p50/p99/max: 348.100 / 366.400 / 372.400 / 393.600 / 398.000.
- Fraction of samples outside 380–420 V: 72.7416% (sample-weighted approximation to time share). Bus I/P unavailable; infeed I range -0.620–10.440 A; infeed P magnitude range 0.000–4.045 kW.

## Dataset C
- Rows: 122109; span: 47.784 h; median positive interval: 1.000 s (~1.000 Hz); duplicate timestamps: 0.
- Missing values in applicable channels: {'dataset': 0, 'ts': 0, 'v_bus': 0, 'i_bus': 0, 'p_kw': 0, 'power_direction_sign': 0, 'temperature_c': 0, 'state': 0, 'provenance': 0}.
- Voltage V min/p1/p50/p99/max: 672.810 / 673.960 / 684.030 / 711.520 / 728.920.
- I range -5.830–20.870 A; P magnitude range 0.000–14.110 kW.

## Calibration limits
A/B voltage distributions can inform an observed 380 V bus band, not protection limits or a universal operating band. C informs a separate 700 V bus context, not the 380 V band. C is passive ~1 s operational logging without commanded steps or setpoints: AFE step response and settling time are not identifiable; no defensible AFE time constant can be calibrated. Sample-to-sample changes can describe observed ramps at the logging rate, but do not establish equipment ramp limits or subsecond dynamics. None contains burn-in racks or measures their energy or scheduling behavior. A/B differ in date and power conditions; battery effects are not isolated.

## Gate run

Command: `python -m pytest -q tests/test_ds02.py`; boundary: MEASURED source data / loader validation.

`	ext
..                                                                       [100%]
2 passed in 2.45s
```

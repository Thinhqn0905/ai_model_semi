"""SHIFT2DC bus measurements; source clocks have undocumented time zones."""
from pathlib import Path
import json
import math
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'DS02_SHIFT2DC/data'
SOURCES = {
    'A': BASE / 'raw/LVDC_380V_hybrid_ACDC_battery_off_2025_05_02.csv',
    'B': BASE / 'raw/LVDC_380V_hybrid_ACDC_battery_on_2024_05_10.csv',
    'C': BASE / 'processed/LVDC_700V_AFE_2025_12_15_aligned.csv',
}
OUT = ROOT / 'data/processed/ds02_bus.parquet'
META = ROOT / 'data/processed/provenance_ds02.json'
REPORT = ROOT / 'reports/data/ds02_report.md'
LIMIT = 2_000_000


def load_dataset(dataset):
    """Load a dataset, preserving missing bus quantities and source-clock uncertainty."""
    raw = pd.concat(pd.read_csv(SOURCES[dataset], chunksize=200_000), ignore_index=True)
    if dataset in ('A', 'B'):
        df = pd.DataFrame({'ts': pd.to_datetime(raw['Time'], utc=True),
            'v_bus': raw['NRE DCbus U'], 'i_bus': float('nan'), 'p_kw': float('nan'),
            'infeed_i_a': raw['Nachladung I'], 'infeed_p_kw': raw['Nachladung P'].abs() / 1000,
            'infeed_power_sign': raw['Nachladung P'].apply(lambda x: (x > 0) - (x < 0)),
            'battery_i_a': raw['BAT I'], 'state': raw['DC Status']})
    else:
        df = pd.DataFrame({'ts': pd.to_datetime(raw['Timestamp'], utc=True),
            'v_bus': raw['upstreamvoltage'], 'i_bus': raw['upstreamcurrent'],
            'p_kw': raw['poweroutput'].abs(), 'power_direction_sign': raw['poweroutput'].apply(lambda x: (x > 0) - (x < 0)),
            'temperature_c': raw['temperature'], 'state': raw['systemstate']})
    # Equal-duration time bins with arithmetic means provide a boxcar anti-alias filter.
    # Directional powers must be aggregated independently, not averaged as signs.
    if len(df) > LIMIT:
        if dataset == 'C':
            df['p_positive_kw'] = df.p_kw.where(df.power_direction_sign > 0, 0)
            df['p_negative_kw'] = df.p_kw.where(df.power_direction_sign < 0, 0)
            df = df.drop(columns=['power_direction_sign', 'p_kw'])
        seconds = max(1, math.ceil((df.ts.max() - df.ts.min()).total_seconds() / (LIMIT - 1)))
        df = df.set_index('ts').resample(f'{seconds}s').mean().dropna(how='all').reset_index()
        if dataset == 'C':
            df['p_kw'] = df.p_positive_kw + df.p_negative_kw
    df.insert(0, 'dataset', dataset)
    df['provenance'] = 'MEASURED'
    return df


def build():
    frames = [load_dataset(d) for d in SOURCES]
    data = pd.concat(frames, ignore_index=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    data.to_parquet(OUT, index=False)
    meta = {'label': 'MEASURED', 'source_url': 'https://doi.org/10.5281/zenodo.18524234',
        'license': 'CC BY 4.0', 'sources': {k: str(v.relative_to(ROOT)).replace('\\', '/') for k, v in SOURCES.items()},
        'units': {'ts': 'UTC assumed; source timezone unknown', 'v_bus': 'V', 'i_bus': 'A', 'p_kw': 'kW magnitude', 'infeed_i_a': 'A', 'infeed_p_kw': 'kW magnitude', 'infeed_power_sign': 'source sign; direction undocumented', 'battery_i_a': 'A', 'temperature_c': 'degC', 'state': 'source code', 'power_direction_sign': 'source sign'},
        'transforms': 'C uses provider-aligned CSV, absolute power and separate source sign; A/B bus I and P unavailable; no interpolation. Only above 2,000,000 rows: time-bin arithmetic mean (boxcar anti-alias); source-sign separated power components are averaged independently. Naive source timestamps labeled UTC by assumption, not verified UTC.'}
    META.write_text(json.dumps(meta, indent=2), encoding='utf-8')
    lines = ['# DS02 SHIFT2DC audit', '', 'Boundary: SOURCE_REPORTED / MEASURED operational traces, not ReGenATE performance. Source: [SHIFT2DC Zenodo](https://doi.org/10.5281/zenodo.18524234), CC BY 4.0.', '', 'Source clock timezone and clock source are undocumented; UTC labels assume UTC and do not establish actual UTC. No interpolation. A/B duplicate timestamps are retained. C uses the provider-aligned file; 12 connection events are omitted by that source. No input exceeds 2 million rows, so no downsampling or anti-alias filtering was applied. Above that threshold the loader uses time-bin means (boxcar low-pass; limited stopband rejection), with separate positive and negative C power magnitudes.', '', 'A/B V is the DC bus node; total bus I and P are unavailable, not zero. Additional infeed current (A), infeed power magnitude (kW) and source sign, battery current (A), and state (source code) are distinct channels. C contains SCCB/AFE-terminal V (V), signed I (A), power magnitude (kW), source power sign, temperature (°C), and state (source code). Current and power flow signs are not documented; sign does not identify import/export. A/B infeed source sign is preserved separately and does not identify flow direction.', '']
    for f in frames:
        d = f.dataset.iloc[0]; delta = f.ts.diff().dt.total_seconds(); med = delta[delta > 0].median()
        lines += [f'## Dataset {d}', f'- Rows: {len(f)}; span: {(f.ts.max()-f.ts.min()).total_seconds()/3600:.3f} h; median positive interval: {med:.3f} s (~{1/med:.3f} Hz); duplicate timestamps: {int(f.ts.duplicated().sum())}.', f'- Missing values in applicable channels: {f.drop(columns=[c for c in ["i_bus", "p_kw"] if d != "C"]).isna().sum().to_dict()}.', f'- Voltage V min/p1/p50/p99/max: {f.v_bus.min():.3f} / {f.v_bus.quantile(.01):.3f} / {f.v_bus.quantile(.5):.3f} / {f.v_bus.quantile(.99):.3f} / {f.v_bus.max():.3f}.']
        if d != 'C':
            lines += [f'- Fraction of samples outside 380–420 V: {((f.v_bus < 380) | (f.v_bus > 420)).mean():.4%} (sample-weighted approximation to time share). Bus I/P unavailable; infeed I range {f.infeed_i_a.min():.3f}–{f.infeed_i_a.max():.3f} A; infeed P magnitude range {f.infeed_p_kw.min():.3f}–{f.infeed_p_kw.max():.3f} kW.']
        else:
            lines += [f'- I range {f.i_bus.min():.3f}–{f.i_bus.max():.3f} A; P magnitude range {f.p_kw.min():.3f}–{f.p_kw.max():.3f} kW.']
        lines.append('')
    lines += ['## Calibration limits', 'A/B voltage distributions can inform an observed 380 V bus band, not protection limits or a universal operating band. C informs a separate 700 V bus context, not the 380 V band. C is passive ~1 s operational logging without commanded steps or setpoints: AFE step response and settling time are not identifiable; no defensible AFE time constant can be calibrated. Sample-to-sample changes can describe observed ramps at the logging rate, but do not establish equipment ramp limits or subsecond dynamics. None contains burn-in racks or measures their energy or scheduling behavior. A/B differ in date and power conditions; battery effects are not isolated.', '']
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Wrote {OUT} ({len(data)} rows), {META}, {REPORT}')


if __name__ == '__main__':
    build()

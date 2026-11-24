"""DS03 source-limited efficiency points and measured EDC cycles."""
from pathlib import Path
import json
import re
import pdfplumber
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'data/processed'
SOURCE = 'DS03_Modeling/62000D-EN.pdf'

def efficiency_points():
    # Rated-condition recovery: the source does not identify a unique DC voltage
    # or grid-side output power for the two voltage ranges.
    rows = [dict(device='62450D-2000HL', direction='regen', v_dc=np.nan,
        load_frac=1.0, p_out_kw=np.nan, eta=0.94, source_file=SOURCE,
        page=2, provenance='DATASHEET')]
    # Printed tables: pairs are transcribed, not digitised from plots. Device
    # identifiers include operating voltage/mode so conditions cannot mix.
    source = 'DS03_Modeling/tiduf64c.pdf'
    with pdfplumber.open(ROOT / source) as pdf:
        for page, title, stop, volts, mode, direction, rating in [
            (38, 'Table 4-1. Boost Converter Efficiency', '4.3.1.3', [50,150,200,250,300,350], 'pv-boost', 'forward', 5),
            (39, 'Table 4-2. Bidirectional DC/DC Efficiency in Buck Mode', 'TIDUF64C', [80,160,240,320], 'battery-buck', 'forward', 10),
            (41, 'Table 4-3. Bidirectional DC/DC Efficiency in Boost Mode', 'The results for boost', [80,160,240,320], 'battery-boost', 'regen', 10),
            (43, 'Table 4-4. DC/AC Efficiency', 'TIDUF64C', ['unipolar','bipolar','heric'], 'dc-ac', 'regen', 4.6),
        ]:
            table = pdf.pages[page-1].extract_text().split(title, 1)[1].split(stop, 1)[0]
            for line in table.splitlines():
                pairs = re.findall(r'(\d+(?:\.\d+)?)\s*[kK][wW]\s+(\d+(?:\.\d+)?)%', line)
                if not pairs:
                    continue
                for col, (power, eta) in enumerate(pairs):
                    # Last DC/AC rows have only unipolar and HERIC columns.
                    if page == 43 and len(pairs) == 2:
                        col = (0, 2)[col]
                    power = float(power)
                    rows.append(dict(device=f'TIDA-010938-{mode}-{volts[col]}',
                        direction=direction, v_dc=400, load_frac=power/rating,
                        p_out_kw=power, eta=float(eta)/100, source_file=source,
                        page=page, provenance='DATASHEET'))
    return pd.DataFrame(rows)

class Curve:
    def __init__(self, x, y):
        self.x, self.y = np.asarray(x), np.asarray(y)
        self.valid_range = (float(self.x[0]), float(self.x[-1]))
    def __call__(self, load_frac):
        return np.interp(load_frac, self.x, self.y)

def eta_curve(device, direction):
    df = efficiency_points().query('device == @device and direction == @direction').sort_values('load_frac')
    if df.empty:
        raise ValueError('No sourced efficiency points for this device and direction')
    grouped = df.groupby('load_frac', sort=True).eta.agg(['mean', 'size'])
    curve = Curve(grouped.index.to_numpy(), grouped['mean'].to_numpy())
    curve.duplicate_loads = grouped.loc[grouped['size'] > 1, 'size'].to_dict()
    return curve

def edc_cycles():
    frames = []
    for path in sorted((ROOT / 'DS03_Modeling/edc/d1').rglob('January/*.csv')):
        raw = pd.read_csv(path)
        raw.columns = raw.columns.str.strip().str.replace(r'\s+', ' ', regex=True)
        soc = next(c for c in raw if c.lower().startswith('soc '))
        voltage = next(c for c in raw if c.lower().startswith('sc voltage'))
        p = raw['SC Power (kW)'].astype(float)
        phase = np.where(p > 0, 'charge', np.where(p < 0, 'discharge', 'rest'))
        t = pd.to_datetime(raw.iloc[:, 0]) + pd.to_timedelta(raw.iloc[:, 1], unit='s')
        # Transformer boundary: positive means import, negative export.
        grid = raw['Transformer Power (kW)'].astype(float).to_numpy()
        dt = np.diff(raw.iloc[:, 1].to_numpy(dtype=float)) / 3600
        # Trapezoidal integration; split each endpoint by sign before averaging.
        incoming = float(np.sum((np.maximum(grid[:-1], 0) + np.maximum(grid[1:], 0)) * dt / 2))
        outgoing = float(np.sum((np.maximum(-grid[:-1], 0) + np.maximum(-grid[1:], 0)) * dt / 2))
        frames.append(pd.DataFrame(dict(ts=t, phase=phase, v=raw[voltage],
            i=np.where(raw[voltage] != 0, np.abs(p)*1000/raw[voltage], np.nan),
            p_kw=np.abs(p), soc=raw[soc], provenance='MEASURED',
            current_provenance='DERIVED', cycle_id=path.name,
            grid_in_kwh=incoming, grid_out_kwh=outgoing,
            round_trip_efficiency=outgoing/incoming if incoming else np.nan,
            efficiency_provenance='DERIVED', source_file=path.relative_to(ROOT).as_posix())))
    if not frames:
        raise FileNotFoundError('No January EDC CSV files')
    return pd.concat(frames, ignore_index=True)

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    points, cycles = efficiency_points(), edc_cycles()
    points.to_parquet(OUT / 'efficiency_points.parquet', index=False)
    cycles.to_parquet(OUT / 'ds03_edc_cycles.parquet', index=False)
    meta = {'efficiency_points': {'sources': points.source_file.unique().tolist(), 'label': 'DATASHEET',
        'limitations': 'TI tables transcribed directly; load fraction is printed output kW divided by stage nominal/rated kW. Device IDs encode operating mode and voltage; interpolation averages duplicate loads and records their counts, preserving non-monotonic shape.'},
        'ds03_edc_cycles': {'sources': cycles.source_file.unique().tolist(), 'label': 'MEASURED',
        'transforms': 'Current magnitude is |SC power|*1000/voltage; sign of SC power gives phase. Transformer power sign gives charge/discharge energy, trapezoidal integration over recorded seconds; ratio is DERIVED. Each file is one recorded cycle; endpoints need not have equal SOC.',
        'units': {'ts':'datetime','v':'V','i':'A','p_kw':'kW','soc':'percent','grid_in_kwh':'kWh','grid_out_kwh':'kWh'}}}
    (OUT / 'provenance_ds03.json').write_text(json.dumps(meta, indent=2), encoding='utf-8')
    print('Built', OUT / 'efficiency_points.parquet', 'and', OUT / 'ds03_edc_cycles.parquet')

if __name__ == '__main__':
    main()

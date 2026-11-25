"""Causal DS07 facility-load forecasting; run the full experiment on Colab."""
import argparse
import json
import zipfile
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from regenate.evaluation.facility import bg_forecast, load_ds07, month_blocks

SLOT = pd.Timedelta(minutes=15)
LAGS = (1, 2, 4, 8, 16, 32, 96, 192, 288, 672, 1344, 2016, 2688)


def split_for(t):
    t = pd.Timestamp(t)
    if t.year != 2019:
        return None
    return 'train' if 3 <= t.month <= 6 else 'val' if t.month == 7 else 'test' if t.month in (8, 9) else None


def features(series, t, horizon, factory_id):
    """At decision time t only slots strictly before t have been observed."""
    t = pd.Timestamp(t)
    target = t + (horizon - 1) * SLOT
    past = series.reindex(pd.date_range(t - 672 * SLOT, periods=672, freq='15min'))
    values = [series.get(t - lag * SLOT, np.nan) for lag in LAGS]
    values += [series.get(target - pd.Timedelta(weeks=w), np.nan) for w in (1, 2, 3, 4)]
    for n in (4, 16, 96, 672):
        x = past.iloc[-n:]
        values.extend((x.mean(), x.std()))
    values += [target.hour * 4 + target.minute // 15, target.weekday(), horizon, factory_id]
    return np.asarray(values, dtype=float)


def make_rows(series, factory_id, scale, start, end, stride_min=15):
    rows, targets, times, horizons = [], [], [], []
    for t in pd.date_range(start, end, freq=f'{stride_min}min', inclusive='left'):   # shortcut: decision-time subsampling for speed
        for h in range(1, 61):
            target = t + (h - 1) * SLOT
            # Keep each target within its decision-time split.
            if split_for(target) != split_for(t):
                continue
            y = series.get(target, np.nan)
            if pd.notna(y):
                rows.append(features(series, t, h, factory_id)); targets.append(y / scale)
                times.append(t); horizons.append(h)
    return np.asarray(rows), np.asarray(targets), times, horizons


class FacilityPredictor:
    def __init__(self, models, series, scales, factory_ids, model='lightgbm'):
        self.models, self.series, self.scales, self.factory_ids, self.model = models, series, scales, factory_ids, model

    def predict(self, factory, t, n_slots):
        if not 1 <= n_slots <= 60:
            raise ValueError('n_slots must be between 1 and 60')
        x = np.asarray([features(self.series[factory], t, h, self.factory_ids[factory]) for h in range(1, n_slots + 1)])
        return np.asarray(self.models[self.model].predict(x)) * self.scales[factory]


def build_models():
    from xgboost import XGBRegressor
    from lightgbm import LGBMRegressor
    models = {
        'ridge': make_pipeline(SimpleImputer(add_indicator=True), StandardScaler(), Ridge()),
        'rf': make_pipeline(SimpleImputer(add_indicator=True), RandomForestRegressor(n_estimators=100, min_samples_leaf=10, n_jobs=-1, random_state=0)),
        'xgboost': XGBRegressor(n_estimators=300, max_depth=6, n_jobs=-1, random_state=0),
        'lightgbm': LGBMRegressor(n_estimators=300, n_jobs=-1, random_state=0, verbosity=-1),
    }
    for q in (0.1, 0.5, 0.9):
        models[f'q{int(q * 100)}'] = LGBMRegressor(objective='quantile', alpha=q, n_estimators=300, n_jobs=-1, random_state=0, verbosity=-1)
    return models


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ds07', required=True); ap.add_argument('--out', required=True)
    ap.add_argument('--stride_min', type=int, default=15, help='decision-time spacing for training/evaluation rows (block starts always kept)')
    args = ap.parse_args(); out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.ds07) as z:
        names = sorted(Path(n).stem for n in z.namelist() if n.startswith('Data_list/Factories/') and n.endswith('.csv'))
    if not names:
        raise ValueError('No factory CSVs found in DS07 zip')
    series = {name: load_ds07(args.ds07, name).resample('15min').mean() for name in names}
    ids = {name: i for i, name in enumerate(names)}
    scales = {name: float(s.loc['2019-03-01':'2019-06-30'].median()) for name, s in series.items()}
    if any(not np.isfinite(v) or v <= 0 for v in scales.values()):
        raise ValueError('Each factory needs a positive training median')
    batches = [make_rows(series[n], ids[n], scales[n], '2019-03-01', '2019-07-01', args.stride_min)[:2] for n in names]
    X = np.concatenate([b[0] for b in batches]); y = np.concatenate([b[1] for b in batches])
    models = build_models()
    for model in models.values():
        model.fit(X, y)
    predictor = FacilityPredictor(models, series, scales, ids)
    joblib.dump(predictor, out / 'facility_predictor.joblib')
    records = []
    for name in names:
        s = series[name]
        for month in ('2019-07', '2019-08', '2019-09'):
            # Block starts match facility.month_blocks, including monthly reset.
            start = pd.Timestamp(month + '-01')
            end = start + pd.offsets.MonthBegin(1)
            bstarts = set(month_blocks(month, 15))
            for t in sorted(set(pd.date_range(start, end, freq=f'{args.stride_min}min', inclusive='left')) | bstarts):
                idx = pd.date_range(t, periods=60, freq='15min')
                forecasts = {'persistence': bg_forecast(s, t, 60, 'persist'), 'hist': bg_forecast(s, t, 60, 'hist'),
                             'seasonal': s.reindex(idx - pd.Timedelta(weeks=1)).to_numpy()}
                x = np.asarray([features(s, t, h, ids[name]) for h in range(1, 61)])
                forecasts.update({key: model.predict(x) * scales[name] for key, model in models.items()})
                truth = s.reindex(idx).to_numpy()
                for h, target in enumerate(idx):
                    row = dict(factory=name, decision_time=t, target_time=target, horizon=h+1, split=split_for(target), actual_kw=truth[h])
                    row.update({key: values[h] for key, values in forecasts.items()}); records.append(row)
    df = pd.DataFrame(records)
    block_starts = {t for month in ('2019-07', '2019-08', '2019-09') for t in month_blocks(month, 15)}
    df[df.decision_time.isin(block_starts)].to_parquet(out / 'forecasts.parquet', index=False)
    # Peak threshold is derived separately for each factory and target month from observed peak-window slots.
    thresholds = {}
    for name, s in series.items():
        for month in ('2019-08', '2019-09'):
            v = s.loc[month]; v = v[(v.index.dayofweek < 5) & (v.index.hour >= 14) & (v.index.hour < 22)]
            thresholds[name, month] = v.quantile(.95)
    test = df[df['split'] == 'test'].copy()
    test['bucket'] = pd.cut(test.horizon, [0, 4, 16, 32, 60], labels=['1-4', '5-16', '17-32', '33-60'])
    test['threshold'] = [thresholds.get((f, str(t)[:7]), np.nan) for f, t in zip(test.factory, test.target_time)]
    test['peak_window'] = (test.target_time.dt.dayofweek < 5) & (test.target_time.dt.hour >= 14) & (test.target_time.dt.hour < 22)
    metrics = []
    for (factory, bucket), g in test.groupby(['factory', 'bucket'], observed=True):
        for model in ['persistence', 'seasonal', 'hist', 'ridge', 'rf', 'xgboost', 'lightgbm', 'q50']:
            # Identical observations for skill and model error.
            valid = g[['actual_kw', model, 'hist']].dropna(); mae = (valid[model] - valid.actual_kw).abs().mean()
            hist_mae = (valid['hist'] - valid.actual_kw).abs().mean()
            peaks = g[g.peak_window & (g.actual_kw >= g.threshold) & g[model].notna()]
            cover = g[['actual_kw', 'q10', 'q90']].dropna()
            metrics.append(dict(factory=factory, bucket=str(bucket), model=model, n=len(valid), mae=mae,
                                nmae=mae/scales[factory], skill_vs_hist=1-mae/hist_mae if hist_mae > 0 else np.nan,
                                peak_recall=(peaks[model] >= peaks.threshold).mean() if len(peaks) else np.nan,
                                p10_p90_coverage=((cover.actual_kw >= cover.q10) & (cover.actual_kw <= cover.q90)).mean()))
    pd.DataFrame(metrics).to_csv(out / 'metrics.csv', index=False)
    (out / 'manifest.json').write_text(json.dumps({'boundary': 'NOT_VERIFIED', 'ds07': str(args.ds07), 'factories': names, 'train': '2019-03..2019-06', 'validation': '2019-07', 'test': '2019-08..2019-09', 'note': 'No hyperparameter selection; validation forecasts exported.'}, indent=2))


if __name__ == '__main__':
    # Import the canonical module so joblib records an importable predictor class.
    from regenate.forecasting.facility_load import main as canonical_main
    canonical_main()

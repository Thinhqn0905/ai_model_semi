"""Chronological DS04 fixed-cadence power forecast benchmark."""
from pathlib import Path
from time import perf_counter
import numpy as np
import pandas as pd
from .baselines import Baseline
from .metrics import mae, rmse, nmae, pinball, interval_coverage

ROOT = Path(__file__).resolve().parents[3]
CAP = 30000


def features(frame, cadence, horizon):
    """Use completed right-closed bins; join only an exact future cadence slot."""
    d = frame.copy()
    d['ts'] = d['ts'].dt.ceil(cadence)
    # A bin crossing a stored split boundary is discarded, never reassigned.
    bins = d.groupby(['asset', 'ts'], sort=True, observed=True).agg(
        power_kw=('power_kw', 'mean'), status=('status', 'last'),
        split=('split', 'first'), splits=('split', 'nunique')).reset_index()
    bins = bins[bins.splits == 1].copy()
    bins['source_ts'] = bins.ts
    bins['lag1'] = bins.power_kw
    previous = bins[['asset', 'ts', 'power_kw']].copy()
    for lag in (1, 2, 3):
        prev = previous.copy()
        prev['ts'] += pd.Timedelta(cadence) * lag
        bins = bins.merge(prev, on=['asset', 'ts'], how='left', validate='one_to_one', suffixes=('', f'_lag{lag}'))
    cols = ['power_kw', 'power_kw_lag1', 'power_kw_lag2', 'power_kw_lag3']
    bins['rolling_mean'] = bins[cols].mean(axis=1)
    bins['rolling_std'] = bins[cols].std(axis=1)
    bins['hour'] = bins.ts.dt.hour
    target = bins[['asset', 'ts', 'power_kw', 'split']].copy()
    target['ts'] -= pd.Timedelta(cadence) * horizon
    target = target.rename(columns={'power_kw': 'y', 'split': 'target_split'})
    bins = bins.merge(target, on=['asset', 'ts'], how='inner', validate='one_to_one')
    bins = bins[(bins.split == bins.target_split) & bins[cols].notna().all(axis=1) & bins.y.notna()].copy()
    bins['target_ts'] = bins.ts + pd.Timedelta(cadence) * horizon
    return bins


def main():
    data = pd.read_parquet(ROOT / 'data/processed/ds04_machines.parquet', columns=['company', 'asset', 'ts', 'status', 'power_kw', 'split'])
    rows = []
    for company, cadence in [('A', '5min'), ('B', '1min')]:
        part = data[data.company == company].copy()
        for horizon in (1, 6, 12):
            frame = features(part, cadence, horizon)
            X = pd.get_dummies(frame[['lag1', 'power_kw_lag1', 'power_kw_lag2', 'power_kw_lag3', 'rolling_mean', 'rolling_std', 'hour', 'asset', 'status']].astype({'asset': 'category', 'status': 'category'}), dtype=float)
            train = np.flatnonzero(frame.split.to_numpy() == 'train')
            test = np.flatnonzero(frame.split.to_numpy() == 'test')
            if not len(train) or not len(test):
                raise ValueError(f'No train or test rows for {company}, horizon {horizon}')
            if len(train) > CAP:
                train = np.random.default_rng(0).choice(train, CAP, replace=False)
            for model in ('F01', 'F02', 'F03', 'F04', 'F05'):
                start = perf_counter()
                estimator = Baseline(model).fit(X.iloc[train], frame.y.iloc[train])
                fit_s = perf_counter() - start
                start = perf_counter()
                p = estimator.predict(X.iloc[test])
                predict_ms = (perf_counter() - start) * 1000
                y = frame.y.iloc[test].to_numpy()
                rows.append(dict(company=company, horizon=horizon, model=model, mae=mae(y, p['p50']), rmse=rmse(y, p['p50']), nmae=nmae(y, p['p50']), pinball10=pinball(y, p['p10'], .1), pinball50=pinball(y, p['p50'], .5), pinball90=pinball(y, p['p90'], .9), coverage80=interval_coverage(y, p['p10'], p['p90']), fit_s=fit_s, predict_ms=predict_ms))
                print(f'{company} h={horizon} {model} done', flush=True)
    result = pd.DataFrame(rows)
    out = ROOT / 'runs/forecast_ds04'
    out.mkdir(parents=True, exist_ok=True)
    result.to_csv(out / 'results.csv', index=False)
    report = ROOT / 'reports/forecast/ds04_bench.md'
    report.parent.mkdir(parents=True, exist_ok=True)
    table = '| ' + ' | '.join(result.columns) + ' |'
    table += '\n| ' + ' | '.join(['---'] * len(result.columns)) + ' |'
    table += ''.join('\n| ' + ' | '.join(map(str, row)) + ' |' for row in result.round(4).itertuples(index=False, name=None))
    report.write_text('# DS04 forecasting benchmark\n\nEvidence boundary: LOCAL_RUN; source observations MEASURED, features and metrics DERIVED. DS04 is not a semiconductor test cell; this only benchmarks the forecasting code path.\n\nRight-closed bins ending at cadence boundaries: Company A 5-minute mean, Company B 1-minute mean; last observed status in each bin. Bins crossing stored split boundaries are excluded. Forecasts use completed current and three preceding contiguous bins; targets must exist exactly 1, 6, or 12 slots later and share the origin split. Train is sampled to at most 30,000 rows per company and horizon with seed 0; test uses all eligible rows. F01 is a per-asset four-slot rolling mean with training residual quantiles; F02–F04 also use training residual quantiles, while F05 fits quantile models. Prediction time is total milliseconds for the test set. Source power contains extreme values (see DS04 audit); no outlier correction is applied.\n\n' + table + '\n', encoding='utf-8')
    print(f'LOCAL_RUN results: {out / "results.csv"}; report: {report}', flush=True)


if __name__ == '__main__':
    main()


import argparse
import json
import time
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from regenate.forecasting import cycle_model as cm
from regenate.forecasting import ds05_bench as bench

EPS = 1e-6
QS = (0.1, 0.5, 0.9)


def cqr_offset(y, lo, hi):
    scores = np.sort(np.maximum(lo - y, y - hi))
    if not len(scores):
        raise ValueError('CQR requires validation samples')
    k = min(len(scores), int(np.ceil((len(scores) + 1) * .8)))
    return float(scores[k - 1])


def abnormal(true, prev):
    return np.abs(np.log(np.maximum(true, EPS) / np.maximum(prev, EPS))) > np.log(1.5)


def remaining_samples(cyc, arrays):
    rows = []
    for uc, group in cyc.sort_values(['use_case', 'ord']).groupby('use_case', sort=False):
        prev = None
        for r in group.itertuples():
            a = arrays.get(r.cycle_file)
            if a is None:
                prev = None
                continue
            for b in range(60, len(a[0]), 15):
                f = bench.features_at(*a, b, prev)
                rows.append(dict(use_case=uc, cycle_file=r.cycle_file, split=r.split,
                                 true=len(a[0])-b, total=len(a[0]),
                                 previous_total=len(prev[0]) if prev is not None else np.nan, **f))
            prev = a
    return pd.DataFrame(rows)


def _ewma(c, alpha):
    return c.groupby('use_case')['dur_h'].transform(lambda x: x.shift().ewm(alpha=alpha, adjust=False).mean()).to_numpy() * 60


def _metrics(d, predictions, times):
    rows = []
    y = d.true.to_numpy(); base = predictions['previous'][:, 1]
    for uc in ['ALL'] + sorted(d.use_case.unique()):
        for status in ['ALL', 'normal', 'abnormal']:
            for progress in (['ALL'] if 'progress' not in d else ['ALL', '0-25', '25-50', '50-75', '75-100']):
                mask = np.ones(len(d), dtype=bool)
                if uc != 'ALL': mask &= d.use_case.to_numpy() == uc
                if status != 'ALL': mask &= d.abnormal.to_numpy() == (status == 'abnormal')
                if progress != 'ALL': mask &= d.progress.to_numpy() == progress
                if not mask.any(): continue
                yy = y[mask]; denom = np.mean(np.abs(base[mask] - yy))
                for name, p in predictions.items():
                    pp = p[mask]; err = pp[:, 1] - yy
                    pin = np.mean([np.mean(np.maximum(q * (yy - pp[:, i]), (q - 1) * (yy - pp[:, i]))) for i, q in enumerate(QS)])
                    rows.append(dict(use_case=uc, subset=status, progress=progress, model=name, n=len(yy),
                        mae=np.mean(abs(err)), rmse=np.sqrt(np.mean(err**2)), skill_vs_previous=1-np.mean(abs(err))/denom if denom else np.nan,
                        median_ape=np.median(abs(err)/np.maximum(yy, EPS)), pinball=pin,
                        coverage80=np.mean((yy>=pp[:, 0]) & (yy<=pp[:, 2])), width80=np.mean(pp[:, 2]-pp[:, 0]),
                        predict_ms=times[name], boundary='NOT_VERIFIED_INPUT_DATA'))
    return pd.DataFrame(rows)


def _fit_task(d, features, baseline, out, task, seed):
    from sklearn.linear_model import Ridge
    from sklearn.ensemble import RandomForestRegressor
    from xgboost import XGBRegressor
    from lightgbm import LGBMRegressor
    train, val, test = [d[d.split == s].copy() for s in ('train', 'val', 'test')]
    if min(len(train), len(val), len(test)) == 0: raise ValueError(f'{task}: empty train, val or test split')
    X, Xv, Xt = [x[features].replace([np.inf, -np.inf], np.nan).fillna(-1) for x in (train, val, test)]
    y, yv = train.true.to_numpy(), val.true.to_numpy()
    preds, times, models = {}, {}, {}
    def add(name, p, seconds=0):
        p = np.asarray(p); p = np.repeat(p[:, None], 3, axis=1) if p.ndim == 1 else p
        preds[name] = p; times[name] = 1000*seconds/max(len(test), 1)
    for name, values in baseline.items(): add(name, values)
    makers = {'ridge': Ridge(), 'rf': RandomForestRegressor(n_estimators=100, min_samples_leaf=5, n_jobs=-1, random_state=seed),
              'xgboost': XGBRegressor(n_estimators=200, max_depth=5, n_jobs=1, random_state=seed),
              'lightgbm': LGBMRegressor(n_estimators=200, verbosity=-1, n_jobs=1, random_state=seed)}
    for name, model in makers.items():
        model.fit(X, y); start = time.perf_counter(); p = model.predict(Xt); add(name, p, time.perf_counter()-start); models[name] = model
    quant = []
    for q in QS:
        m = LGBMRegressor(objective='quantile', alpha=q, n_estimators=200, verbosity=-1, n_jobs=1, random_state=seed)
        m.fit(X, y); quant.append(m)
    start = time.perf_counter(); qt = np.sort(np.column_stack([m.predict(Xt) for m in quant]), axis=1); elapsed = time.perf_counter()-start
    qv = np.sort(np.column_stack([m.predict(Xv) for m in quant]), axis=1)
    offset = cqr_offset(yv, qv[:, 0], qv[:, 2]); calibrated = qt.copy()
    calibrated[:, 0] -= offset; calibrated[:, 2] += offset
    calibrated[:, 0] = np.minimum(calibrated[:, 0], calibrated[:, 1]); calibrated[:, 2] = np.maximum(calibrated[:, 2], calibrated[:, 1])
    add('quantile_lightgbm', qt, elapsed); add('quantile_lightgbm_cqr', calibrated, elapsed)
    models.update(quantiles=quant, cqr_offset=offset, features=features)
    return test, preds, times, models


def run(proc, out, seed=0):
    proc, out = Path(proc), Path(out); out.mkdir(parents=True, exist_ok=True)
    cyc = pd.read_parquet(proc / 'ds05_cycles.parquet')
    if 'split' not in cyc or 'ord' not in cyc: cyc = bench.order_cycles(cyc)
    else: cyc = cyc[cyc.error.fillna('') == ''].sort_values(['use_case', 'ord']).copy()
    c = cm.build_table(cyc); c['true'] = c.dur_h * 60
    c['abnormal'] = abnormal(c.true, np.exp(c.dur_lag1)*60)
    val = c.split == 'val'; test = c.split == 'test'
    alphas = (.1, .3, .5, .8, 1.)
    ewmas = {a: _ewma(cyc, a) for a in alphas}
    # Align EWMA by cycle identity because build_table removes each module's first cycle.
    lookup = {a: pd.Series(v, index=cyc.cycle_file).reindex(c.cycle_file).to_numpy() for a, v in ewmas.items()}
    alpha = min(alphas, key=lambda a: np.mean(abs(lookup[a][val] - c.loc[val, 'true'])))
    base = {'previous': np.exp(c.loc[test, 'dur_lag1'].to_numpy())*60,
            'median5': np.exp(c.loc[test, 'dur_med5'].to_numpy())*60, 'ewma': lookup[alpha][test]}
    t1, p1, tm1, m1 = _fit_task(c, cm.feature_cols(c), base, out, 'T1', seed)
    models, features, selection = cm.fit(c, seed); gates = cm.select_gates(c, models, features)
    start = time.perf_counter(); gated = np.exp(t1.dur_lag1.to_numpy() + cm.gated_log_ratio(t1, models, features, gates, 'dur'))*60
    p1['ai18_gated'] = np.repeat(gated[:, None], 3, axis=1); tm1['ai18_gated'] = 1000*(time.perf_counter()-start)/len(t1)
    m1.update(ai18_models=models, ai18_features=features, ai18_gates=gates, ai18_selection=selection, ewma_alpha=alpha)
    arrays = {}
    for path in sorted((proc / 'ds05_traces').glob('*.parquet')): arrays.update(bench.cycle_arrays(pd.read_parquet(path)))
    d = remaining_samples(cyc, arrays)
    d = d[d.previous_total.notna()].copy()
    d['abnormal'] = abnormal(d.total, d.previous_total)
    d['progress'] = pd.cut(d.elapsed_min / d.total, [0, .25, .5, .75, 1], labels=['0-25','25-50','50-75','75-100'], include_lowest=True).astype(str)
    features2 = list(bench.features_at(*next(iter(arrays.values())), 60, None))
    te = d[d.split == 'test']; base2 = {'previous': np.maximum(te.prev_rem_min.to_numpy(), 0)}
    for name in ('median5', 'ewma', 'ai18_gated'):
        by_cycle = pd.Series(p1[name][:, 1], index=t1.cycle_file)
        base2[name] = np.maximum(te.cycle_file.map(by_cycle).to_numpy() - te.elapsed_min.to_numpy(), 0)
    t2, p2, tm2, m2 = _fit_task(d, features2, base2, out, 'T2', seed)
    for task, data, pred, times in [('T1', t1, p1, tm1), ('T2', t2, p2, tm2)]:
        _metrics(data, pred, times).to_csv(out / f'metrics_{task}.csv', index=False)
        frames = []
        for name, p in pred.items():
            frame = data[['cycle_file', 'use_case', 'true'] + (['elapsed_min'] if task == 'T2' else [])].copy()
            frame['model'] = name; frame[['q10', 'q50', 'q90']] = p; frames.append(frame)
        pd.concat(frames, ignore_index=True).to_parquet(out / f'predictions_{task}.parquet', index=False)
    joblib.dump({'T1': m1, 'T2': m2}, out / 'eta_models.joblib')
    (out / 'manifest.json').write_text(json.dumps({'proc': str(proc), 'seed': seed, 'split': 'input chronological per module', 'ewma_alpha_val': alpha,
        'T1_features': cm.feature_cols(c), 'T2_features': features2, 'boundary': 'NOT_VERIFIED_INPUT_DATA'}, indent=2))


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--proc', required=True); parser.add_argument('--out', required=True); parser.add_argument('--seed', type=int, default=0)
    a = parser.parse_args(); run(a.proc, a.out, a.seed)


if __name__ == '__main__': main()


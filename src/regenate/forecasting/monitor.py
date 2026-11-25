"""Completed-cycle advisory monitoring; injected examples are not fault labels."""
import argparse
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest, GradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import average_precision_score, precision_recall_fscore_support
from sklearn.svm import OneClassSVM
from regenate.forecasting.cycle_model import build_table, feature_cols, TARGETS, EPS

COLS = list(TARGETS.values()) + ['rte', 'h_rest', 'h_charge', 'h_discharge', 'v_min', 'v_max', 'i_abs_max', 't_amb_mean_c']
METHODS = ['recipe', 'quantile', 'mad', 'ewma', 'shewhart', 'cusum', 'isolation_forest', 'one_class_svm', 'cqr']


def inject(frame, kind):
    out = frame.copy()
    if kind == 'duration': out['dur_h'] *= 1.3
    elif kind == 'charge_energy': out['e_charge_kwh'] *= 1.2
    elif kind == 'rte': out['rte'] *= 0.9
    elif kind == 'missing_rest': out['h_rest'] = 0.0
    else: raise ValueError(kind)
    return out


def matrix(c):
    x = c[COLS].apply(pd.to_numeric, errors='coerce').copy()
    for col in TARGETS.values(): x[col] = np.log(x[col].clip(lower=EPS))
    return x.replace([np.inf, -np.inf], np.nan)


def fit_models(c, seed=0):
    tr = c[c.split == 'train']
    if len(tr) < 10 or not (c.split == 'val').any() or not (c.split == 'test').any():
        raise ValueError('Need at least 10 training cycles and nonempty validation and test splits')
    imp = SimpleImputer(strategy='median', keep_empty_features=True)
    x = imp.fit_transform(matrix(tr))
    iso = IsolationForest(n_estimators=100, random_state=seed, n_jobs=1).fit(x)
    svm = OneClassSVM(nu=0.05).fit(x)
    feats = feature_cols(c)
    fi = SimpleImputer(strategy='median', keep_empty_features=True).fit(tr[feats])
    xf = fi.transform(tr[feats]); models = {}
    for t in TARGETS:
        y = tr[f'y_{t}'].to_numpy(); valid = np.isfinite(y)
        if valid.sum() < 10: raise ValueError('Insufficient finite training targets for ' + t)
        models[t] = [GradientBoostingRegressor(loss='quantile', alpha=q, n_estimators=80, max_depth=2, random_state=seed).fit(xf[valid], y[valid]) for q in (0.1, 0.9)]
    return imp, iso, svm, feats, fi, models


def score(c, models, observed=None):
    """History and lag features come from unmodified cycles; observed may contain a counterfactual."""
    observed = c if observed is None else observed
    imp, iso, svm, feats, fi, qr = models
    x = imp.transform(matrix(observed)); xf = fi.transform(c[feats])
    result = pd.DataFrame(index=c.index, columns=METHODS, dtype=float)
    result['isolation_forest'] = -iso.score_samples(x)
    result['one_class_svm'] = -svm.score_samples(x)
    bands = []
    for t, col in TARGETS.items():
        actual = np.log(observed[col].clip(lower=EPS).to_numpy()) - c[f'{t}_lag1'].to_numpy()
        lo, hi = (m.predict(xf) for m in qr[t]); lower, upper = np.minimum(lo, hi), np.maximum(lo, hi)
        bands.append(np.maximum(np.maximum(lower - actual, actual - upper), 0))
    result['cqr'] = np.nanmax(np.vstack(bands), axis=0)
    # Each statistic uses only the last 50 actual preceding cycles in the same use case.
    for _, indices in c.groupby('use_case', sort=False).groups.items():
        hist = []; cusum = np.zeros(3); ew = None
        for idx in indices:
            cur = matrix(observed.loc[[idx]])[COLS[:3] + ['rte', 'h_rest']].to_numpy()[0]
            if hist:
                h = np.asarray(hist[-50:]); med = np.nanmedian(h, axis=0)
                scale = np.maximum(1.4826 * np.nanmedian(np.abs(h - med), axis=0), 0.02)
                delta = np.abs(cur - h[-1]); z = np.abs(cur - med) / scale
                qlo, qhi = np.nanquantile(h, [0.05, 0.95], axis=0)
                result.loc[idx, 'recipe'] = np.nanmax(np.r_[np.abs(np.exp(cur[:3] - h[-1, :3]) - 1), delta[3:] / np.maximum(np.abs(h[-1, 3:]), 0.02)])
                result.loc[idx, 'quantile'] = np.nanmax(np.maximum(np.maximum(qlo-cur, cur-qhi), 0) / scale)
                result.loc[idx, 'mad'] = np.nanmax(z)
                result.loc[idx, 'ewma'] = np.nanmax(np.abs(cur[:3] - ew) / scale[:3])
                result.loc[idx, 'shewhart'] = np.nanmax(z[:3])
                residual = (cur[:3] - med[:3]) / scale[:3]
                result.loc[idx, 'cusum'] = np.nanmax(np.maximum(np.abs(cusum + residual) - 0.5, 0))
                # State advances only with real observations, never counterfactual injections.
                actual = matrix(c.loc[[idx]])[COLS[:3] + ['rte', 'h_rest']].to_numpy()[0]
                cusum = np.sign(cusum + (actual[:3]-med[:3])/scale[:3]) * np.maximum(np.abs(cusum + (actual[:3]-med[:3])/scale[:3])-0.5, 0)
                ew = 0.2 * actual[:3] + 0.8 * ew
            else:
                actual = matrix(c.loc[[idx]])[COLS[:3] + ['rte', 'h_rest']].to_numpy()[0]
                ew = actual[:3].copy()
            hist.append(actual)
    return result


def run(c, out, seed=0, false_alarm=0.05):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    c = build_table(c).reset_index(drop=True)
    models = fit_models(c, seed)
    start = time.perf_counter(); natural = score(c, models); elapsed = time.perf_counter() - start
    val = c.split.eq('val'); test = c.split.eq('test')
    thresholds = natural.loc[val].quantile(1-false_alarm).to_dict()
    if any(not np.isfinite(v) for v in thresholds.values()): raise ValueError('Non-finite validation threshold')
    natural.insert(0, 'cycle_file', c.cycle_file); natural.insert(1, 'use_case', c.use_case); natural.insert(2, 'split', c.split)
    natural.to_csv(out / 'natural_scores.csv', index=False)
    rows = []; top = []; distributions = []
    for method in METHODS:
        s = natural[method]; threshold = thresholds[method]
        for split in ('val', 'test'):
            z = s[c.split.eq(split)].dropna()
            for q in (0.0, 0.5, 0.9, 0.95, 0.99, 1.0): distributions.append(dict(method=method, split=split, quantile=q, score=z.quantile(q)))
        selected = natural.loc[test & (s > threshold)].nlargest(10, method).index
        for i in selected:
            top.append(dict(method=method, score=s[i], threshold=threshold, **c.loc[i, ['cycle_file', 'use_case', 'ord'] + COLS].to_dict()))
    for kind in ('duration', 'charge_energy', 'rte', 'missing_rest'):
        changed = c.copy(); changed.loc[test] = inject(c.loc[test], kind)
        stressed = score(c, models, changed)
        for method in METHODS:
            normal = natural.loc[test, method].to_numpy(); abnormal = stressed.loc[test, method].to_numpy()
            valid = np.isfinite(normal) & np.isfinite(abnormal); normal, abnormal = normal[valid], abnormal[valid]
            if not len(normal): continue
            y = np.r_[np.zeros(len(normal)), np.ones(len(abnormal))]; scores = np.r_[normal, abnormal]
            pred = scores > thresholds[method]; p, r, f, _ = precision_recall_fscore_support(y, pred, average='binary', zero_division=0)
            hours = c.loc[test, 'dur_h'].to_numpy()[valid].sum(); alarms = int((normal > thresholds[method]).sum())
            rows.append(dict(boundary='SYNTHETIC_INJECTED', perturbation=kind, method=method, threshold=thresholds[method], precision=p, recall=r, f1=f, pr_auc=average_precision_score(y, scores), detection_rate=r, false_alarms_per_1000=1000*alarms/len(normal), false_alarms_per_operating_hour=alarms/hours if hours > 0 else np.nan, n_normal=len(normal)))
    pd.DataFrame(rows).to_csv(out / 'synthetic_metrics.csv', index=False)
    pd.DataFrame(top).to_csv(out / 'natural_top.csv', index=False)
    pd.DataFrame(distributions).to_csv(out / 'natural_distributions.csv', index=False)
    (out / 'manifest.json').write_text(json.dumps(dict(boundary='SYNTHETIC_INJECTED for stress metrics; natural DS05 cycles are unlabelled', thresholds_source='val', thresholds=thresholds, target_val_false_alarm_rate=false_alarm, inference_seconds_per_cycle=elapsed/len(c), n_cycles=len(c), seed=seed), indent=2))
    return natural, pd.DataFrame(rows), thresholds


def main():
    from regenate.forecasting.ds05_bench import order_cycles
    ap = argparse.ArgumentParser(); ap.add_argument('--proc', required=True); ap.add_argument('--out', required=True); ap.add_argument('--seed', type=int, default=0)
    a = ap.parse_args(); c = order_cycles(pd.read_parquet(Path(a.proc) / 'ds05_cycles.parquet'))
    run(c, a.out, a.seed)
    print('Monitoring outputs:', a.out)


if __name__ == '__main__': main()


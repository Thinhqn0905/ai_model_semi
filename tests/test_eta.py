from pathlib import Path
import subprocess
import os
import sys

import numpy as np
import pandas as pd
from regenate.forecasting import eta, cycle_model, ds05_bench


def test_cqr_and_abnormal():
    y = np.arange(20.0)
    lo, hi = y - 3, y - 2
    offset = eta.cqr_offset(y, lo, hi)
    assert np.mean((y >= lo - offset) & (y <= hi + offset)) > np.mean((y >= lo) & (y <= hi))
    assert eta.abnormal(np.array([100., 151.]), np.array([100., 100.])).tolist() == [False, True]


def test_features_use_past_only():
    a = np.arange(150., dtype=float)
    old = (a.copy(), a.copy(), a.copy(), a.copy())
    changed = tuple(x.copy() for x in old)
    for x in changed: x[75:] = -999
    assert ds05_bench.features_at(*old, 75, None) == ds05_bench.features_at(*changed, 75, None)
    df = make_cycles()
    c = cycle_model.build_table(df)
    features = cycle_model.feature_cols(c)
    df.loc[10, ['dur_h', 'e_charge_kwh', 'e_discharge_kwh']] = 999
    changed = cycle_model.build_table(df)
    pd.testing.assert_series_equal(c.loc[9, features], changed.loc[9, features])


def make_cycles():
    rows = []
    for i in range(30):
        length = 100 + (i % 4) * 15
        rows.append(dict(use_case='test', cycle_file=f'c{i}', ord=i, split='train' if i < 20 else 'val' if i < 25 else 'test',
            error='', dur_h=length/60, e_charge_kwh=1+i/100, e_discharge_kwh=.8+i/100,
            h_charge=1., h_discharge=.5, h_rest=.1, t_amb_mean_c=20., rte=.8, v_max=4., v_min=3., t0_s=i*10000, t1_s=i*10000+length*60))
    return pd.DataFrame(rows)


def test_cli(tmp_path):
    proc = tmp_path / 'proc'; traces = proc / 'ds05_traces'; traces.mkdir(parents=True)
    cyc = make_cycles(); cyc.to_parquet(proc / 'ds05_cycles.parquet', index=False)
    frames = []
    for r in cyc.itertuples():
        n = round(r.dur_h*60)
        frames.append(pd.DataFrame(dict(cycle_file=r.cycle_file, t_s=np.arange(n)*60, p_charge_w=np.ones(n),
            p_discharge_w=np.ones(n), v=np.ones(n)*3, t_amb_c=np.ones(n)*20)))
    pd.concat(frames).to_parquet(traces / 'traces.parquet', index=False)
    out = tmp_path / 'out'
    env = os.environ.copy(); env['PYTHONPATH'] = str(Path(__file__).resolve().parents[1] / 'src') + os.pathsep + env.get('PYTHONPATH', '')
    subprocess.run([sys.executable, '-m', 'regenate.forecasting.eta', '--proc', str(proc), '--out', str(out)], check=True, env=env)
    for name in ['metrics_T1.csv', 'metrics_T2.csv', 'predictions_T1.parquet', 'predictions_T2.parquet', 'eta_models.joblib', 'manifest.json']:
        assert (out / name).is_file()
    assert {'cycle_file', 'q10', 'q50', 'q90', 'true'} <= set(pd.read_parquet(out / 'predictions_T2.parquet'))

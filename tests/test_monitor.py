import json
import os
import subprocess
import sys
import numpy as np
import pandas as pd
from regenate.forecasting.monitor import run, inject


def cycles(n=100):
    rng = np.random.default_rng(42); rows = []
    for i in range(n):
        rows.append(dict(cycle_file=f'Cycle_{i}.csv', use_case='A', period='Period_1', cycle_no=i, ord=i,
                         split='train' if i < 70 else ('val' if i < 85 else 'test'), error='',
                         t0_s=i*7200, t1_s=i*7200+3600, dur_h=1+rng.normal(0,.01),
                         e_charge_kwh=2+rng.normal(0,.02), e_discharge_kwh=1.8+rng.normal(0,.02),
                         h_charge=.4, h_discharge=.4, h_rest=.2+rng.normal(0,.002),
                         v_min=7.9, v_max=8.1, i_abs_max=2, rte=.9+rng.normal(0,.005), t_amb_mean_c=25))
    return pd.DataFrame(rows)


def test_synthetic_and_validation_thresholds(tmp_path):
    c = cycles(); _, m, th = run(c, tmp_path / 'one')
    assert set(m.boundary) == {'SYNTHETIC_INJECTED'}
    assert (m[m.method == 'mad'].pr_auc > .5).all()
    changed = c.copy(); changed.loc[changed.split == 'test', 'dur_h'] *= 3
    _, _, th2 = run(changed, tmp_path / 'two')
    assert th == th2
    assert (inject(c.iloc[:1], 'missing_rest').h_rest == 0).all()


def test_cli(tmp_path):
    proc = tmp_path / 'proc'; proc.mkdir(); out = tmp_path / 'out'
    cycles().drop(columns=['ord', 'split']).to_parquet(proc / 'ds05_cycles.parquet')
    env = os.environ.copy(); env['PYTHONPATH'] = os.pathsep.join(['src', env.get('PYTHONPATH', '')])
    p = subprocess.run([sys.executable, '-m', 'regenate.forecasting.monitor', '--proc', str(proc), '--out', str(out)], env=env, capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    assert json.loads((out / 'manifest.json').read_text())['thresholds_source'] == 'val'
    for name in ('natural_scores.csv', 'natural_top.csv', 'natural_distributions.csv', 'synthetic_metrics.csv'):
        assert (out / name).exists()

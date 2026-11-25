import json
import numpy as np
import pandas as pd
from regenate.forecasting import eta, eta_tcn


def fixture():
    cyc = pd.DataFrame([dict(use_case='A', cycle_file=f'c{i}', ord=i, split=('train' if i < 3 else 'val' if i == 3 else 'test'), error='') for i in range(5)])
    arrays = {f'c{i}': tuple(np.arange(91, dtype=float) + i + j for j in range(4)) for i in range(5)}
    return cyc, arrays


def test_past_only_and_keys():
    cyc, arrays = fixture()
    before = eta_tcn.past_window(arrays, 'c1', 60, 80)
    assert np.all(before[:, :20] == 0)
    changed = {k: tuple(x.copy() for x in v) for k, v in arrays.items()}
    for x in changed['c1']: x[60:] = 1e9
    np.testing.assert_array_equal(before, eta_tcn.past_window(changed, 'c1', 60, 80))
    expected = eta.remaining_samples(cyc, arrays); expected = expected[expected.previous_total.notna()]
    keys = ['use_case', 'cycle_file', 'elapsed_min', 'split']
    pd.testing.assert_frame_equal(eta_tcn.prepare(cyc, arrays)[keys], expected[keys].reset_index(drop=True))


def test_cpu_run(tmp_path):
    cyc, arrays = fixture(); proc = tmp_path / 'proc'; trace = proc / 'ds05_traces'; trace.mkdir(parents=True)
    cyc.to_parquet(proc / 'ds05_cycles.parquet')
    rows = []
    for name, a in arrays.items():
        for i in range(len(a[0])): rows.append(dict(cycle_file=name, t_s=i*60, p_charge_w=a[0][i]*1000, p_discharge_w=a[1][i]*1000, v=a[2][i], t_amb_c=a[3][i]))
    pd.DataFrame(rows).to_parquet(trace / 'synthetic.parquet')
    out = tmp_path / 'output'; eta_tcn.run(proc, out, lookback=16, epochs=1)
    metrics = pd.read_csv(out / 'metrics_tcn.csv'); preds = pd.read_parquet(out / 'predictions_tcn.parquet')
    assert set(metrics.model) == {'AI11_tcn', 'AI11_tcn_cqr'}
    assert set(preds.model) == set(metrics.model)
    assert (preds.q10 <= preds.q50).all() and (preds.q50 <= preds.q90).all()
    assert json.loads((out / 'manifest.json').read_text())['epochs_run'] == 1

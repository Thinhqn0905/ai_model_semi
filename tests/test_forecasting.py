import numpy as np
import pandas as pd
from regenate.forecasting.metrics import mae, rmse, nmae, pinball, interval_coverage
from regenate.forecasting.baselines import Baseline
from regenate.forecasting.ds04_bench import features


def test_metrics():
    y, p = np.array([1., 3.]), np.array([2., 1.])
    assert mae(y, p) == 1.5
    assert np.isclose(rmse(y, p), np.sqrt(2.5))
    assert nmae(y, p) == .75
    assert np.isclose(pinball(y, p, .1), .55)
    assert interval_coverage(y, [0, 0], [2, 2]) == .5


def test_quantiles_monotone():
    X = pd.DataFrame({'rolling_mean': np.arange(30, dtype=float), 'lag1': np.arange(30, dtype=float)})
    y = np.sin(np.arange(30))
    for model in ('F01', 'F02', 'F03', 'F04', 'F05'):
        p = Baseline(model).fit(X, y).predict(X)
        assert np.all(p['p10'] <= p['p50']) and np.all(p['p50'] <= p['p90'])


def test_no_future_or_split_leakage():
    ts = pd.date_range('2022-01-01', periods=25, freq='1min', tz='UTC')
    data = pd.DataFrame({'asset': 0, 'ts': ts, 'power_kw': np.arange(25.), 'status': 'idle', 'split': ['train'] * 15 + ['test'] * 10})
    data = data.drop(index=8)
    result = features(data, '1min', 2)
    assert (result.source_ts < result.target_ts).all()
    assert (result.y == result.lag1 + 2).all()
    assert (result.power_kw_lag3 == result.lag1 - 3).all()
    assert (result.split == result.target_split).all()
    assert not result.ts.isin(ts[9:12]).any()

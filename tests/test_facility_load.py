import numpy as np
import pandas as pd
from regenate.forecasting.facility_load import FacilityPredictor, features, split_for


class ConstantModel:
    def predict(self, x):
        return np.ones(len(x))


def test_features_are_causal():
    idx = pd.date_range('2019-03-01', periods=4000, freq='15min')
    s = pd.Series(np.arange(len(idx), dtype=float), index=idx)
    t = idx[3000]
    original = features(s, t, 60, 0)
    s.loc[t:] = -99999
    np.testing.assert_allclose(original, features(s, t, 60, 0), equal_nan=True)


def test_split_order():
    assert [split_for(t) for t in ('2019-06-30', '2019-07-01', '2019-08-01', '2019-09-30', '2019-10-01')] == ['train', 'val', 'test', 'test', None]


def test_predict_shape():
    s = pd.Series([2.], index=pd.to_datetime(['2019-06-30 23:45']))
    p = FacilityPredictor({'lightgbm': ConstantModel()}, {'f': s}, {'f': 2.}, {'f': 0})
    np.testing.assert_array_equal(p.predict('f', pd.Timestamp('2019-07-01'), 60), np.full(60, 2.))

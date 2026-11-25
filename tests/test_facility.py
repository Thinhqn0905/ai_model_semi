import numpy as np
import pandas as pd
from regenate.evaluation.facility import billed_demand, place, month_blocks, to_minutes, topo_of


def test_billed_demand_aligned_and_coverage():
    idx = pd.date_range("2019-03-01", periods=120, freq="min")
    p = pd.Series(100.0, index=idx); p.iloc[40:50] = 400.0           # 10-min spike inside the 30-59 window
    md, t = billed_demand(p, 30)
    assert md == np.mean([100.0] * 10 + [400.0] * 10 + [100.0] * 10) and t == idx[30]
    q = p.copy(); q.iloc[30:60] = np.nan; q.iloc[30:33] = 400.0      # 10 % coverage window is excluded
    assert billed_demand(q, 30)[0] == 100.0


def test_place_and_blocks():
    idx = pd.date_range("2019-03-01", periods=48 * 60, freq="min")
    b = month_blocks("2019-03", 12)[:4]
    s = place(b, [to_minutes([1.0, 2.0])] * 4, idx)
    assert s.sum() == 4 * 15 * 3 and s.iloc[0] == 1.0 and s.iloc[15] == 2.0 and s.iloc[12 * 60] == 1.0
    assert topo_of("B1p-OPT") == "B1p" and topo_of("P0@v2_e1_peak") == "DC"


def test_md_window_ignores_offpeak():
    idx = pd.date_range("2019-03-04 00:00", periods=24 * 60, freq="min")     # a Monday
    p = pd.Series(100.0, index=idx); p["2019-03-04 03:00":"2019-03-04 03:59"] = 900.0   # off-peak spike
    p["2019-03-04 15:00":"2019-03-04 15:29"] = 300.0                                     # peak-period interval
    assert billed_demand(p, 30)[0] == 900.0
    assert billed_demand(p, 30, md_window=([0, 1, 2, 3, 4], 14, 22))[0] == 300.0


def test_bg_forecast_is_causal():
    from regenate.evaluation.facility import bg_forecast
    idx = pd.date_range("2019-03-01", periods=4 * 24 * 35, freq="15min")
    bg = pd.Series(np.arange(len(idx), dtype=float), index=idx)
    t = idx[4 * 24 * 30]
    assert bg_forecast(bg, t, 3, "persist")[0] == bg[t - pd.Timedelta(minutes=15)]          # last slot strictly before t
    h = bg_forecast(bg, t, 2, "hist"); assert h[0] == np.mean([bg[t - pd.Timedelta(weeks=w)] for w in (1, 2, 3, 4)])
    assert bg_forecast(bg, t, 2, "oracle")[1] == bg[idx[4 * 24 * 30 + 1]]

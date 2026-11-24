"""Branch C sample builder: causality and split hygiene on synthetic cycles."""
import numpy as np
from pytest import approx
import pandas as pd
from regenate.forecasting.ds05_bench import make_samples, order_cycles, period_key


def synth(n_cyc=6, L=300):
    cyc = pd.DataFrame(dict(use_case="TOU", period="2020_March", cycle_file=[f"c{k}" for k in range(n_cyc)],
                            cycle_no=range(n_cyc), error=""))
    arrs = {}
    for k in range(n_cyc):
        t = np.arange(L)
        arrs[f"c{k}"] = (np.where(t < 150, 0.2, 0.0), np.where(t >= 150, 0.15 + 0.001 * k, 0.0),
                         np.full(L, 8.0), np.full(L, 25.0))
    return order_cycles(cyc), arrs


def test_period_key_orders_years_and_months():
    assert period_key("2019_February_March") < period_key("2019_November_January") < period_key("2020_March")


def test_split_chronological_and_disjoint():
    cyc, _ = synth(20)
    o = cyc.set_index("cycle_file").ord
    assert o[cyc[cyc.split == "train"].cycle_file].max() < o[cyc[cyc.split == "test"].cycle_file].min()


def test_targets_are_future_and_features_past():
    cyc, arrs = synth()
    df = make_samples(cyc, arrs, stride=15)
    r = df[(df.cycle_file == "c3") & (df.elapsed_min == 135)].iloc[0]
    assert r.ch_l1 == approx(0.2) and r.y_ch_h1 == approx(0.2)          # bins 120..134 charge, slot 135..149 still charge
    assert r.y_ds_h4 == approx(0.15 + 0.003)                      # slot 180..194 discharging at cycle-3 level
    assert r.prev_ds_h4 == approx(0.15 + 0.002)                   # previous cycle (c2), same elapsed time
    assert r.y_rem_min == 300 - 135
    assert df[df.cycle_file == "c0"].prev_ch_h1.isna().all()   # first cycle has no history

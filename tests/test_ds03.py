import numpy as np
from regenate.data.ds03 import efficiency_points, eta_curve, edc_cycles

def test_efficiency_points_and_clamping():
    points = efficiency_points()
    assert ((points.eta > 0) & (points.eta <= 1)).all()
    curve = eta_curve('62450D-2000HL', 'regen')
    assert curve.valid_range == (1., 1.)
    assert np.allclose(curve([0, 1, 2]), .94)

def test_measured_cycle_energy():
    cycles = edc_cycles()
    assert set(cycles.phase) >= {'charge', 'discharge'}
    summary = cycles.groupby('cycle_id').first()
    assert len(summary) == 3
    assert np.isfinite(summary.round_trip_efficiency).all()
    assert (summary.grid_in_kwh > 0).all() and (summary.grid_out_kwh > 0).all()
    assert np.allclose(summary.round_trip_efficiency, summary.grid_out_kwh / summary.grid_in_kwh)


def test_printed_ti_tables_preserve_measured_shape():
    points = efficiency_points()
    group = points.query("device == 'TIDA-010938-battery-buck-80' and direction == 'forward'")
    assert len(group) == 15
    assert ((group.p_out_kw == 0.2) & np.isclose(group.eta, 0.949)).any()
    assert group.load_frac.duplicated().any()
    curve = eta_curve('TIDA-010938-battery-buck-80', 'forward')
    expected = group.groupby('load_frac').eta.mean().sort_index()
    assert np.allclose(curve(expected.index), expected)
    assert curve.duplicate_loads == group.groupby('load_frac').size().loc[lambda s: s > 1].to_dict()
    assert np.any(np.diff(expected) < 0)
    assert curve.valid_range == (expected.index.min(), expected.index.max())
    assert np.allclose(curve([-1, 2]), [expected.iloc[0], expected.iloc[-1]])
    assert ((curve(np.linspace(*curve.valid_range, 100)) > 0) &
            (curve(np.linspace(*curve.valid_range, 100)) <= 1)).all()

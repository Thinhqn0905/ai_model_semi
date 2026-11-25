import pytest
from regenate.simulation.transient import Params, simulate


def test_conservation_and_losses():
    r = simulate(lambda t: 5 if t < .1 else -2)
    assert r['source_j'] == pytest.approx(r['load_j'] + r['loss_j'] + r['stored_j'], rel=1e-6, abs=1e-6)
    assert r['loss_j'] >= 0


def test_controls():
    assert not simulate(0)['violated']
    assert simulate(50)['violated']
    assert simulate(5, params=Params(capacitance_f=0.00001))['violated']


def test_trips():
    assert simulate(5, afe_trip=True)['violated']
    assert simulate(5, link_trip=True)['violated']


def test_trip_occurs_after_pretrip_dynamics():
    baseline = simulate(5, duration_s=.09)
    delayed = simulate(5, duration_s=.09, afe_trip=.1)
    assert delayed['voltage_v'][-1] == pytest.approx(baseline['voltage_v'][-1])

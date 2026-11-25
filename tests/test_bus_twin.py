import pytest
from regenate.simulation.bus_twin import TwinParams, check_plan


def test_synchronous_burst_rejected():
    result = check_plan([[0, 15]] * 4, [[0, 0]] * 4, 4)
    assert not result['approved']
    assert any(v[1] in ('overvoltage', 'overcurrent') for v in result['violations'])


def test_smooth_balanced_plan_approved():
    result = check_plan([[0, 2, 4]], [[0, 2, 4]], 4)
    assert result['approved']


def test_afe_saturation_rejected():
    result = check_plan([[0, 0]], [[0, 25]], 4)
    assert any(v[1] == 'undervoltage' for v in result['violations'])


def test_balanced_energy_stays_nominal():
    result = check_plan([[0, 5, 2]], [[0, 5, 2]], 4)
    assert result['v_min'] == pytest.approx(400, abs=1e-6)
    assert result['v_max'] == pytest.approx(400, abs=1e-6)
    assert result['p_chop_kwh'] == 0


def test_direct_limit_and_invalid_input():
    result = check_plan([[10]], [[10]], 1, TwinParams(p_link_max_kw=5))
    assert any(v[1] == 'direct_power' for v in result['violations'])
    with pytest.raises(ValueError):
        check_plan([[float('nan')]], [[0]], 1)


def test_all_violations_include_duration_and_later_events():
    # At 100 kW demand, even a fully loaded 20 kW AFE exhausts the
    # capacitor's nominal-to-minimum energy in 0.0039 s once ramped.
    result = check_plan([0, 100], [100, 0], 4, all_violations=True)
    stats = result['violation_stats']
    assert stats['undervoltage']['count'] > 0
    assert stats['undervoltage']['duration_s'] > 0
    assert stats['undervoltage']['first_time_s'] is not None
    assert stats['ramp']['count'] > 0
    assert not check_plan([0], [0], 1, all_violations=True)['violations']



def test_collapse_stops_before_later_power():
    a = check_plan([0, 0], [100, 500], 4, all_violations=True)
    b = check_plan([0, 0], [100, 0], 4, all_violations=True)
    assert a == b
    assert a['violation_stats']['collapse']['count'] == 1
    assert a['i_peak'] < 1000

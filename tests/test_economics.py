import pytest
from regenate.economics.model import annualise, energy_cost, incremental_case, sensitivity_grid

TARIFF = {'import_price': {'off_peak': 1, 'normal': 2, 'peak': 4}, 'alpha_ex': .5}

def run(imp, exp=(0, 0), times=(6, 18)):
    return {'p_import': imp, 'p_export': exp, 'dt_h': 1, 'times': times}

def cfg(tariff=TARIFF):
    return {'tariff': tariff, 'operating_hours_per_year': 2, 'horizon_years': 2, 'discount_rate': 0}

def test_hand_calculated_and_tou():
    assert energy_cost([2, 3], [1, 1], 1, [6, 18], TARIFF) == 13
    assert energy_cost([1, 1], [0, 0], 1, ['2026-11-23 17:00', '2026-11-23 18:00'], TARIFF) == 6
    assert energy_cost([1], [0], 1, ['2026-11-22 18:00'], TARIFF) == 2
    assert annualise(10, 2, 100) == 500

def test_payback_and_npv():
    result = incremental_case(run([2, 3]), run([1, 2]), 12, 0, cfg())
    assert result['annual_saving'] == 6
    assert result['simple_payback_y'] == 2
    assert result['npv'] == 0
    assert result['irr'] == pytest.approx(0)
    assert incremental_case(run([1, 1]), run([1, 1]), 2, 0, cfg())['simple_payback_y'] is None
    assert incremental_case(run([1, 1]), run([2, 2]), 2, 0, cfg())['simple_payback_y'] is None

def test_demand_only_when_configured():
    times = ['2026-11-01 06:00', '2026-11-01 07:00']
    base, new = run([4, 1], times=times), run([2, 2], times=times)
    no_demand = incremental_case(base, new, 0, 0, cfg())['annual_saving']
    with_demand = incremental_case(base, new, 0, 0, cfg({**TARIFF, 'demand_charge_per_kw_month': 3}))['annual_saving']
    assert no_demand == 2
    assert with_demand == 8
    with pytest.raises(ValueError):
        energy_cost([1], [0], 1, [6], {**TARIFF, 'demand_charge_per_kw_month': 1})

def test_sensitivity_and_explicit_cooling():
    assert len(sensitivity_grid(run([2, 3]), run([1, 2]), 12, 0, cfg())) == 27
    result = incremental_case(run([1, 1]), run([1, 1]), 0, 0, {**cfg(), 'annual_cooling_saving': 7})
    assert result['annual_saving'] == 7


import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from regenate.economics.business_case import finance, paired_ci, build


def test_hand_example_and_zero():
    result = finance(1000, 300, 4000, 200, False)
    assert result['annual_net_saving'] == 800
    assert result['payback_years'] == 5
    assert abs(result['npv'] - (-4000 + sum(800 / 1.08**y for y in range(1, 11)))) < 1e-9
    assert finance(200, 0, 4000, 200, False)['payback_years'] is None
    assert finance(100, 0, 4000, 200, False)['payback_years'] is None


def test_demand_toggle_and_ci():
    assert finance(1000, 300, 4000, 200, True)['annual_net_saving'] == 1100
    assert paired_ci([2, 2, 2]) == (2, 2, 2)


def test_actual_evidence_fails_closed():
    rows = build()
    assert len(rows) == 144
    assert rows.boundary.eq('NOT_VERIFIED').all()
    assert rows.annual_net_saving_usd.isna().all()
    assert rows.reason.str.contains('time series missing').all()

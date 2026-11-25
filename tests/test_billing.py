import pandas as pd
import pytest
import yaml
from pathlib import Path
from src.regenate.economics.billing import monthly_bill


def bill(p, tariff, start='2026-01-05 00:00'):
    return next(iter(monthly_bill(p, pd.date_range(start, periods=len(p), freq='min'), tariff)['months'].values()))


def test_flat():
    b = bill([10]*60, {'energy_rates': {'normal': 0.2}, 'billing_interval_minutes': 30, 'demand_rates': {'md': 3}, 'fixed_fees': {'retail': 2}})
    assert b['total'] == pytest.approx(34)
    assert b['billed_demand_kw'] == 10


def test_spike():
    b = bill([40]+[10]*59, {'billing_interval_minutes': 30})
    assert b['billed_demand_kw'] == 11


def test_tou():
    b = bill([10]*60, {'energy_rates': {'normal': 1, 'peak': 2}, 'windows': [{'days': [0], 'start': '00:30', 'end': '01:00', 'period': 'peak'}]})
    assert b['energy_charge'] == pytest.approx(15)


def test_contract():
    b = bill([12]*30, {'contract_kw': 10, 'contract_rate': 3, 'excess_rate': 5})
    assert b['contract_charge'] == 30 and b['excess_charge'] == 10
    assert bill([8]*30, {'contract_kw': 10, 'contract_rate': 3, 'excess_rate': 5})['excess_charge'] == 0


def test_unverified():
    assert bill([1]*30, {'billing_interval_minutes': {'value': 30, 'status': 'NOT_VERIFIED'}})['not_verified']


def test_registry_loads():
    paths = list(Path('data/tariffs').glob('*.yaml'))
    assert len(paths) == 7                     # MV/HV general + ToU (TNB RP4), VN actual + trial, SG
    for p in paths:
        assert yaml.safe_load(p.read_text(encoding='utf-8'))['id']


def test_missing_tou_rate_rejected():
    with pytest.raises(ValueError, match='missing energy rate'):
        bill([1]*30, {'energy_rates': {'peak': 2}, 'windows': []})


def test_sliding_and_bad_mode():
    p = [0]*15 + [30]*30 + [0]*15
    assert bill(p, {'interval_mode': 'sliding'})['billed_demand_kw'] == 30
    assert bill(p, {'interval_mode': 'aligned'})['billed_demand_kw'] == 15
    with pytest.raises(ValueError, match='interval_mode'):
        bill(p, {'interval_mode': 'bad'})


def test_tnb_peak_only_and_weekend():
    tariff = yaml.safe_load(Path('data/tariffs/TAR01_MY_TNB_RP4_MV_TOU.yaml').read_text(encoding='utf-8'))
    # Higher off-peak load must not determine the weekday maximum demand.
    b = bill([100]*30 + [10]*30, tariff, '2026-01-05 13:30')
    assert b['billed_demand_kw'] == 10
    assert b['energy_charge'] == pytest.approx(50*0.2723 + 5*0.3132)
    weekend = bill([100]*30, tariff, '2026-01-10 14:00')
    assert weekend['billed_demand_kw'] == 0 and weekend['not_verified']


def test_tnb_general_vs_tou_md_rule():
    """General: month's max 30-min demand at any hour; ToU: only in the peak window (schedule p.2 wording)."""
    load = [100.0] * (24 * 60); load[180:210] = [500.0] * 30               # Monday 03:00-03:29 off-peak spike
    gen = yaml.safe_load(Path('data/tariffs/TAR01_MY_TNB_RP4_MV_general.yaml').read_text(encoding='utf-8'))
    tou = yaml.safe_load(Path('data/tariffs/TAR01_MY_TNB_RP4_MV_TOU.yaml').read_text(encoding='utf-8'))
    assert bill(load, gen, '2019-03-04 00:00')['billed_demand_kw'] == 500.0
    assert bill(load, tou, '2019-03-04 00:00')['billed_demand_kw'] == 100.0

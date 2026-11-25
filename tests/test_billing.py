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
    assert len(paths) == 5
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

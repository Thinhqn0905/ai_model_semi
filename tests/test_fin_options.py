import pandas as pd
import pytest
from regenate.economics.business_case import finance
from regenate.economics.fin_options import build, afe_sensitivity


def config(demand=None):
    case = {'capex': [{'name': 'server', 'value': 100, 'status': 'ESTIMATE'}, {'name': 'install', 'value': None, 'status': 'MISSING'}], 'opex': [{'name': 'support', 'value': None, 'status': 'MISSING'}]}
    return {'annualisation': {'hours_per_year': 10, 'instance_hours': 10, 'cells': 1}, 'tariff': {'price_usd_kwh': 1, 'demand_charge': demand}, 'finance': {'rate': .08, 'years': 10}, 'cases': {k: case for k in ('FIN-A', 'FIN-B', 'FIN-C')}}


def data():
    return pd.DataFrame([dict(instance_id=i, method=m, net_kwh=e, peak_kw=p, import_kwh=e, export_kwh=0) for i in (1, 2) for m, e, p in [('B1', 10, 5), ('B1-OPT', 8, 4), ('B2', 8, 4), ('P0', 7, 3)]])


def test_finance_and_break_even():
    factor = sum(1 / 1.08**i for i in range(1, 11))
    assert finance(10, 0, 100, 0, False)['npv'] == pytest.approx(-100 + 10 * factor)
    row = build(data(), config()).iloc[0]
    assert finance(row.annual_net_usd, 0, row.break_even_capex_usd, 0, False)['npv'] == pytest.approx(0)
    assert row.qualification == 'OPTIMISTIC' and 'install' in row['missing']


def test_demand_and_nonpositive():
    assert not build(data(), config()).demand_enabled.any()
    rows = build(data(), config(2))
    assert rows[rows.demand_enabled].annual_net_usd.iloc[0] > rows[~rows.demand_enabled].annual_net_usd.iloc[0]
    assert finance(0, 0, 100, 0, False)['payback_years'] is None


def test_afe_oracle_gain_conversion():
    sensitivity = pd.DataFrame([dict(sweep='eta_afe', scenario='S3', value=.96,
                                     gain_kwh_mean=2, gain_kwh_lo=1, gain_kwh_hi=3)])
    row = afe_sensitivity(sensitivity, config()).iloc[0]
    factor = sum(1 / 1.08**i for i in range(1, 11))
    assert row.break_even_capex_usd == pytest.approx(2 * factor)
    assert row.break_even_ci_low == pytest.approx(factor)
    assert 'ORACLE-level gain' in row.comparison

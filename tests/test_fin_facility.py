import math
import pandas as pd
import pytest
from regenate.economics.fin_facility import build, financials, tariff_rates


def test_demand_hand_example():
    tariff = {'energy_rates': {'normal': {'value': .3, 'currency': 'MYR'}},
              'demand_rates': {'capacity': {'value': 29.43, 'currency': 'MYR'},
                               'network': {'value': 59.84, 'currency': 'MYR'}}}
    rate, _, _ = tariff_rates(tariff)
    assert 2 * rate == pytest.approx(178.54)


def test_missing_and_break_even():
    f = financials(100, 1000, True)
    assert math.isnan(f['payback_years']) and f['payback_status'] == 'OPTIMISTIC_BREAK_EVEN_ONLY'
    assert f['ceiling_3y'] == 300 and f['ceiling_5y'] == 500
    assert financials(0, 100, False)['payback_status'] == 'no finite payback'


def test_facility_annualisation_and_matching():
    rows = []
    for month in pd.period_range('2019-03', periods=7, freq='M'):
        for method, md in [('B2', 3), ('P0@v2_e1_peak', 1)]:
            rows.append(dict(facility='f', month=str(month), method=method, md_increment_kw=md, instances=2))
    energy = pd.DataFrame([dict(instance_id=1, method=m, net_kwh=k, TT_h=0) for m,k in [('B2', 4), ('P0@v2_e1_peak', 3)]])
    tariff = {'energy_rates': {'normal': {'value': 1, 'currency': 'USD'}}, 'demand_rates': {'d': {'value': 10, 'currency': 'USD'}}}
    cfg = {'cases': {'FIN-B': {'capex': [{'name':'x','value':100,'status':'ESTIMATE'}], 'opex': []}}}
    monthly, summary = build(pd.DataFrame(rows), energy, tariff, cfg)
    assert monthly.demand_saving.iloc[0] == 20
    assert summary.annual_net_usd.iloc[0] == 264
    energy.loc[1, 'TT_h'] = 1
    with pytest.raises(ValueError, match='tardiness'):
        build(pd.DataFrame(rows), energy, tariff, cfg)


def test_multicell_energy_costs_and_clustered_ranges():
    from regenate.economics.fin_facility import clustered_summary
    rows = [dict(facility=f, month=str(month), method=method, md_increment_kw=md,
                 instances=2, n_cells=3)
            for f in ('f1', 'f2') for month in pd.period_range('2019-03', periods=7, freq='M')
            for method, md in [('B2', 3), ('P0@v2_e1_peak', 1)]]
    energy = pd.DataFrame([dict(instance_id=1, method=m, net_kwh=k, TT_h=0)
                           for m, k in [('B2', 4), ('P0@v2_e1_peak', 3)]])
    tariff = {'energy_rates': {'normal': {'value': 1, 'currency': 'USD'}},
              'demand_rates': {'d': {'value': 10, 'currency': 'USD'}}}
    cfg = {'cases': {'FIN-B': {'capex': [
        {'name': 'server', 'value': 100, 'status': 'ESTIMATE'},
        {'name': 'cell_meters', 'value': 10, 'status': 'ESTIMATE'}], 'opex': []}}}
    monthly, summary = build(pd.DataFrame(rows), energy, tariff, cfg)
    assert monthly.energy_saving.iloc[0] == 6
    assert monthly.capex_usd.iloc[0] == 130
    assert summary.annual_demand_local.iloc[0] == 240
    result = clustered_summary(summary).iloc[0]
    assert result.annual_net_usd == pytest.approx(312)
    assert result.annual_net_usd_lo == pytest.approx(312)

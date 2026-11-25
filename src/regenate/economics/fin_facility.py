"""Facility-month counterfactual economics; no site savings are implied."""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import yaml
from .fin_options import costs
from regenate.evaluation.stats import cluster_paired_ci

BOUNDARY = 'SIM_DATA_PROFILE+MEASURED_DS07_NOT_SYNCHRONISED;NOT_VERIFIED'
TARGET = 'P0@v2_e1_peak'


def financials(annual_net, capex, missing):
    pv = sum(1 / 1.08**y for y in range(1, 11))
    return dict(payback_years=(capex / annual_net if annual_net > 0 and not missing else np.nan),
                payback_status=('OPTIMISTIC_BREAK_EVEN_ONLY' if missing else
                                'no finite payback' if annual_net <= 0 else 'finite'),
                npv=annual_net * pv - capex, ceiling_3y=3 * annual_net,
                ceiling_5y=5 * annual_net, ceiling_10y_discounted=annual_net * pv)


def tariff_rates(tariff):
    if tariff.get('tariff_status') == 'TRIAL_NOT_PAYABLE' or tariff.get('contract_rate'):
        raise ValueError('tariff needs payable rates and explicit contract billing model')
    demand = tariff.get('demand_rates', {})
    rates = tariff.get('energy_rates', {})
    if not rates or any(v.get('value') is None for v in rates.values()):
        raise ValueError('missing energy rates')
    currencies = {v.get('currency') for v in list(demand.values()) + list(rates.values())}
    if len(currencies) != 1 or None in currencies:
        raise ValueError('missing or inconsistent tariff currency')
    if any(v.get('value') is None for v in demand.values()):
        raise ValueError('missing demand rates')
    # No load-time distribution is supplied: a normal rate is the only defensible flat proxy.
    flat = rates.get('normal', rates.get('offpeak'))
    if flat is None:
        raise ValueError('normal or offpeak proxy required without interval energy weights')
    return sum(float(v['value']) for v in demand.values()), float(flat['value']), currencies.pop()


def build(facility, energy, tariff, cfg, fx=None, hours_factor=1, capex_factor=1):
    demand_rate, energy_rate, currency = tariff_rates(tariff)
    if hours_factor <= 0 or capex_factor <= 0:
        raise ValueError('sensitivity factors must be positive')
    methods = set(facility.method)
    target = TARGET if TARGET in methods else 'P0-E1-Peak' if 'P0-E1-Peak' in methods else TARGET
    options = [('FIN-A', 'B1', 'B1-OPT'), ('FIN-B', 'B2', target),
               ('FIN-C', 'B1' if 'B1' in methods else 'B1p-OPT', target)]
    out = []
    for option, base, method in options:
        if base not in methods or method not in methods:
            continue
        a = facility[facility.method == base].set_index(['facility', 'month'])
        b = facility[facility.method == method].set_index(['facility', 'month'])
        if not a.index.is_unique or not b.index.is_unique or set(a.index) != set(b.index):
            raise ValueError('unmatched or duplicate facility-months')
        b = b.loc[a.index]
        if any(len(g) != 7 for _, g in a.groupby(level=0)):
            raise ValueError('exactly seven months per facility required')
        emethod = method if method in set(energy.method) else ('P0-peak' if method in (TARGET, 'P0-E1-Peak') and 'P0-peak' in set(energy.method) else method)
        ea = energy[energy.method == base].set_index('instance_id')
        eb = energy[energy.method == emethod].set_index('instance_id')
        if ea.empty or eb.empty or not ea.index.is_unique or not eb.index.is_unique or set(ea.index) != set(eb.index):
            raise ValueError(f'unmatched energy instances: {base}/{emethod}')
        eb = eb.loc[ea.index]
        if 'TT_h' not in energy or not np.isfinite(ea.TT_h).all() or not np.isfinite(eb.TT_h).all():
            raise ValueError('finite matched tardiness required')
        eq = np.isclose(ea.TT_h, eb.TT_h, atol=1e-8, rtol=0)      # energy compared at equal production (tardiness) only
        if eq.sum() == 0:
            raise ValueError('no instance with equal tardiness')
        excluded_tt = int((~eq).sum())
        delta = (ea.net_kwh[eq] - eb.net_kwh[eq]).mean()
        c, missing = costs(cfg['cases'][option])
        cells = int(a.n_cells.iloc[0]) if 'n_cells' in a else 1
        if cells < 1 or ('n_cells' in a and (not (a.n_cells == cells).all() or not (b.n_cells == cells).all())):
            raise ValueError('n_cells must be consistent and positive')
        # Unspecified scope is not safely scalable; preserve it as an unresolved cost.
        for kind in ('capex', 'opex'):
            for item in cfg['cases'][option][kind]:
                scope = item.get('scope')
                if scope is None:
                    scope = ('site' if item['name'] in ('server', 'software_licence', 'software_integration', 'facility_meter') else
                             'cell' if item['name'] in ('cell_meters', 'station_integration', 'requalification') else None)
                if scope not in ('site', 'cell') and cells > 1:
                    missing.append('scope:' + item['name'])
                if scope == 'cell' and item['value'] is not None:
                    c[kind] += item['value'] * (cells - 1)
        for (fac, month), x in a.iterrows():
            instances = x.get('instances', x.get('n_instances', np.nan))
            if not np.isfinite(instances):
                # Facility protocol: complete 15-hour blocks per calendar month.
                instances = int(pd.Period(str(month), freq='M').days_in_month * 24 // 15)
            md = x.md_increment_kw - b.loc[(fac, month), 'md_increment_kw']
            out.append(dict(option=option, baseline=base, method=method, energy_method=emethod, energy_excluded_tt=excluded_tt,
                            facility=fac, month=month, md_delta_kw=md, demand_rate=demand_rate,
                            demand_saving=md*demand_rate, energy_saving=delta*instances*energy_rate*hours_factor*cells, n_cells=cells,
                            instances=instances, currency=currency, boundary=BOUNDARY,
                            energy_basis='paired instance mean; assumed 15h blocks if count absent',
                            tariff_flag='NOT_VERIFIED; flat normal/offpeak proxy; no TOU load weights',
                            capex_usd=c['capex']*capex_factor, opex_usd=c['opex'],
                            cost_items=str(cfg['cases'][option]), missing=';'.join(missing),
                            qualification='OPTIMISTIC' if missing else 'COMPLETE'))
    if not out:
        raise ValueError('no comparable facility options')
    monthly = pd.DataFrame(out)
    summary = []
    for (option, fac), g in monthly.groupby(['option', 'facility']):
        annual_local = (g.demand_saving.sum()+g.energy_saving.sum())*12/7
        row = dict(option=option, facility=fac, n_cells=int(g.n_cells.iloc[0]), currency=currency, annual_demand_local=g.demand_saving.sum()*12/7, annual_energy_local=g.energy_saving.sum()*12/7, annual_gross_local=annual_local,
                   monthly_spread_local=(g.demand_saving+g.energy_saving).max()-(g.demand_saving+g.energy_saving).min(),
                   mean_md_delta_kw=g.md_delta_kw.mean(), capex_usd=g.capex_usd.iloc[0],
                   missing=g.missing.iloc[0], qualification=g.qualification.iloc[0], boundary=BOUNDARY)
        if currency == 'USD' or fx is not None:
            annual_net = annual_local*(1 if currency == 'USD' else fx)-g.opex_usd.iloc[0]
            row.update(annual_net_usd=annual_net, **financials(annual_net, row['capex_usd'], bool(row['missing'])))
        else:
            row.update(annual_net_usd=np.nan, payback_status='NOT_VERIFIED: exchange rate required')
        summary.append(row)
    return monthly, pd.DataFrame(summary)


def clustered_summary(summary):
    rows = []
    for (option, cells), g in summary.groupby(['option', 'n_cells']):
        row = dict(option=option, n_cells=cells, n_facilities=len(g), boundary=BOUNDARY,
                   qualification=';'.join(sorted(set(g.qualification))), missing=';'.join(sorted(set(g.missing))))
        for metric in ('annual_demand_local', 'annual_energy_local', 'annual_gross_local', 'annual_net_usd', 'npv', 'ceiling_3y', 'ceiling_5y', 'ceiling_10y_discounted'):
            if metric not in g:
                continue
            c = cluster_paired_ci(g[metric], np.zeros(len(g)), g.facility)
            row.update({metric: c['mean'], metric+'_lo': c['lo'], metric+'_hi': c['hi']})
        row['payback_status'] = ';'.join(sorted(set(g.payback_status)))
        rows.append(row)
    return pd.DataFrame(rows)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--facility', required=True, nargs='+'); p.add_argument('--energy', required=True)
    p.add_argument('--tariff', required=True, nargs='+'); p.add_argument('--config', required=True)
    p.add_argument('--out', required=True); p.add_argument('--usd-per-tariff-unit', type=float)
    args = p.parse_args()
    if args.usd_per_tariff_unit is not None and args.usd_per_tariff_unit <= 0:
        p.error('exchange rate must be positive')
    cfg = yaml.safe_load(Path(args.config).read_text(encoding='utf-8-sig'))
    energy = pd.read_csv(args.energy); output = Path(args.out); output.mkdir(parents=True, exist_ok=True)
    months, summaries, aggregates, sensitivities = [], [], [], []
    for f in args.facility:
        facility = pd.read_csv(f)
        for t in args.tariff:
            tariff = yaml.safe_load(Path(t).read_text(encoding='utf-8-sig'))
            m, s = build(facility, energy, tariff, cfg, args.usd_per_tariff_unit)
            for frame in (m, s):
                frame['facility_input'] = str(f); frame['tariff'] = tariff['id']
            months.append(m); summaries.append(s)
            aggregate = clustered_summary(s)
            aggregate['facility_input'] = str(f); aggregate['tariff'] = tariff['id']
            aggregates.append(aggregate)
            for hours in (0.5, 1, 2):
                for capex in (0.5, 1, 2):
                    _, scenario = build(facility, energy, tariff, cfg, args.usd_per_tariff_unit, hours, capex)
                    scenario['facility_input'] = str(f); scenario['tariff'] = tariff['id']
                    scenario['hours_factor'] = hours; scenario['capex_factor'] = capex
                    sensitivities.append(scenario)
    pd.concat(months).to_csv(output/'monthly.csv', index=False)
    pd.concat(summaries).to_csv(output/'facility_summary.csv', index=False)
    pd.concat(aggregates).to_csv(output/'clustered_summary.csv', index=False)
    pd.concat(sensitivities).to_csv(output/'sensitivities.csv', index=False)
    print(f'wrote {output} boundary={BOUNDARY}')

if __name__ == '__main__':
    main()


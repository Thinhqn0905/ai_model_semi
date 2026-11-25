"""Paired, assumption-bound incremental economics; no energy ledger is reproduced."""
import argparse
from copy import deepcopy
from pathlib import Path
import numpy as np
import pandas as pd
import yaml
from .business_case import finance, paired_ci

ROOT = Path(__file__).resolve().parents[3]
OPTIONS = [('FIN-A', 'B1', 'B1-OPT'), ('FIN-B', 'B2', 'P0'), ('FIN-C', 'B1', 'P0')]


def costs(case):
    totals, missing = {}, []
    for kind in ('capex', 'opex'):
        totals[kind] = 0.
        for item in case[kind]:
            status, value = item['status'], item['value']
            if status not in ('QUOTED', 'ESTIMATE', 'MISSING'):
                raise ValueError('invalid cost status')
            if status == 'MISSING':
                if value is not None:
                    raise ValueError('missing cost must have null value')
                missing.append(item['name'])
            elif value is None or not np.isfinite(value) or value < 0:
                raise ValueError('invalid cost value')
            else:
                totals[kind] += value
    return totals, missing


def build(df, cfg):
    df = df.copy()
    if 'peak_kw' not in df and 'peak_import_kw' in df:
        df['peak_kw'] = df.peak_import_kw
    if 'scenario' not in df:
        df['scenario'] = 'ALL'
    annual = cfg['annualisation']
    scale = annual['hours_per_year'] / annual['instance_hours'] * annual['cells']
    if scale <= 0:
        raise ValueError('invalid annualisation')
    price = cfg['tariff']['price_usd_kwh']
    rate, years = cfg['finance']['rate'], cfg['finance']['years']
    choices = OPTIONS + [('FIN-B', 'B2', m) for m in ('P0-peak', 'P0_PEAK', 'P0-PEAK', 'P0_peak') if m in set(df.method)]
    rows = []
    for scenario, group in df.groupby('scenario'):
        if scenario != 'S3' and scenario != 'ALL':
            continue
        for option, baseline, method in choices:
            a = group[group.method.eq(baseline)].set_index('instance_id')
            b = group[group.method.eq(method)].set_index('instance_id')
            if a.empty or b.empty:
                continue
            if not a.index.is_unique or not b.index.is_unique or set(a.index) != set(b.index):
                raise ValueError(f'unmatched or duplicate instances: {baseline}/{method}')
            b = b.loc[a.index]
            if 'TT_h' in a:
                keep = (a.TT_h - b.TT_h).abs() <= 1e-8
                excluded = int((~keep).sum())
                a, b = a.loc[keep], b.loc[keep]
            else:
                excluded = 0
            if len(a) < 2:
                raise ValueError('at least two matched instances required')
            physical = a.net_kwh - b.net_kwh
            peak = a.peak_kw - b.peak_kw
            imp_exp = {'import_kwh', 'export_kwh'} <= set(df.columns)
            imp = a.import_kwh - b.import_kwh if imp_exp else None
            exp = a.export_kwh - b.export_kwh if imp_exp else None
            c, missing = costs(cfg['cases'][option])
            for alpha in (0, .5, 1):
                if not imp_exp and alpha != 1:
                    continue
                saving = imp - alpha * exp if imp_exp else physical
                for demand in (False, True) if cfg['tariff'].get('demand_charge') is not None else (False,):
                    demand_rate = cfg['tariff'].get('demand_charge') or 0
                    peak_money = peak * 12 * demand_rate * annual['cells'] if demand else peak * 0
                    cash = saving * price * scale + peak_money - c['opex']
                    mean, low, high = paired_ci(cash)
                    result = finance(mean, 0, c['capex'], 0, False, rate, years)
                    pv = sum(1 / (1 + rate) ** y for y in range(1, years + 1))
                    pmean, plo, phi = paired_ci(physical)
                    pkmean, pklo, pkhi = paired_ci(peak)
                    rows.append(dict(boundary=group.boundary.iloc[0] if 'boundary' in group else 'NOT_VERIFIED', scenario=scenario, option=option, baseline=baseline, method=method, n=len(a), excluded_tt=excluded, alpha=alpha, demand_enabled=demand, physical_kwh=pmean, physical_ci_low=plo, physical_ci_high=phi, peak_kw=pkmean, peak_ci_low=pklo, peak_ci_high=pkhi, energy_bill_usd=(imp.mean() * price * scale if imp_exp else np.nan), export_credit_effect_usd=(-alpha * exp.mean() * price * scale if imp_exp else np.nan), demand_saving_usd=peak_money.mean(), annual_net_usd=mean, annual_ci_low=low, annual_ci_high=high, capex_usd=c['capex'], opex_usd=c['opex'], missing=';'.join(missing), qualification='OPTIMISTIC' if missing else 'COMPLETE', break_even_capex_usd=mean*pv, break_even_ci_low=low*pv, break_even_ci_high=high*pv, npv_usd=result['npv'], payback_years=result['payback_years']))
    if not rows:
        raise ValueError('no comparable option')
    return pd.DataFrame(rows)


def afe_sensitivity(sensitivity, cfg):
    """Convert the existing Oracle-level gain, not a P0 option, to PV savings."""
    data = sensitivity[(sensitivity.sweep == 'eta_afe') & (sensitivity.scenario == 'S3')].copy()
    if data.empty or data[['gain_kwh_mean', 'gain_kwh_lo', 'gain_kwh_hi']].isna().any().any():
        raise ValueError('missing S3 eta_AFE gain or uncertainty')
    annual = cfg['annualisation']
    scale = annual['hours_per_year'] / annual['instance_hours'] * annual['cells']
    pv = sum(1 / (1 + cfg['finance']['rate']) ** y for y in range(1, cfg['finance']['years'] + 1))
    multiplier = scale * cfg['tariff']['price_usd_kwh'] * pv
    for source, target in [('gain_kwh_mean', 'break_even_capex_usd'),
                           ('gain_kwh_lo', 'break_even_ci_low'),
                           ('gain_kwh_hi', 'break_even_ci_high')]:
        data[target] = data[source] * multiplier
    data['comparison'] = 'B1p-OPT -> ORACLE; ORACLE-level gain (upper bound)'
    data['qualification'] = 'OPTIMISTIC; excludes missing OPEX and demand charge'
    return data


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--results', default=str(ROOT / 'runs/rolling_v1/ladder.csv'))
    p.add_argument('--config', default=str(ROOT / 'configs/economics_v3.yaml'))
    args = p.parse_args()
    cfg = yaml.safe_load(Path(args.config).read_text(encoding='utf-8-sig'))
    df = pd.read_csv(args.results)
    out = ROOT / 'runs/run3/econ'
    out.mkdir(parents=True, exist_ok=True)
    rows = build(df, cfg)
    rows.to_csv(out / 'fin_v3.csv', index=False)
    tornado = []
    for variable, factors in [('tariff', (.5, 1, 2)), ('duty_cycle', (.5, 1, 2)), ('capex', (.5, 1, 2)), ('demand_charge', (0, cfg['tariff']['demand_sensitivity_usd_kw_month']))]:
        for factor in factors:
            variant = deepcopy(cfg)
            if variable == 'tariff':
                variant['tariff']['price_usd_kwh'] *= factor
            elif variable == 'duty_cycle':
                variant['annualisation']['hours_per_year'] *= factor
            elif variable == 'demand_charge':
                variant['tariff']['demand_charge'] = factor
            else:
                for case in variant['cases'].values():
                    for item in case['capex']:
                        if item['value'] is not None:
                            item['value'] *= factor
            result = build(df, variant)
            result = result[(result.alpha == 1) & (result.demand_enabled == (variable == 'demand_charge'))].copy()
            result['variable'], result['value'] = variable, factor
            tornado.append(result)
    pd.concat(tornado, ignore_index=True).to_csv(out / 'tornado_v3.csv', index=False)
    afe = afe_sensitivity(pd.read_csv(ROOT / 'runs/sens_v1/sensitivity_results.csv'), cfg)
    afe.to_csv(out / 'eta_afe_v3.csv', index=False)
    print(f'wrote {out / "fin_v3.csv"} boundary={rows.boundary.unique()}')

if __name__ == '__main__':
    main()

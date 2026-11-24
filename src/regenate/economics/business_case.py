"""Business case calculations; fail closed where matched billing data are absent."""
from pathlib import Path
import itertools
import math
import numpy as np
import pandas as pd
from scipy.stats import t
import yaml

ROOT = Path(__file__).resolve().parents[3]
OPTIONS = [('FIN-A', 'B1', 'B1-OPT'), ('FIN-B', 'B2', 'P0'), ('FIN-B', 'B2', 'P'), ('FIN-C', 'B1', 'P0')]
# Assumptions, not site measurements. USD conversion is illustrative, not a spot rate.
ASSUMED = dict(operating_hours_per_year=6000, instances_per_year=600,
               cell_kw=50, vnd_per_usd=25000, demand_vnd_per_kw_month=100000,
               discount_rate=.08, horizon_years=10, instance_hours=10,
               tou_off_peak_fraction=.25, tou_normal_fraction=13/24, tou_peak_fraction=5/24)


def finance(annual_energy_saving, annual_peak_saving, capex, opex, demand_enabled, rate=.08, years=10):
    saving = annual_energy_saving + (annual_peak_saving if demand_enabled else 0) - opex
    if abs(saving) < 1e-9:
        saving = 0.0
    return {'annual_net_saving': saving, 'payback_years': capex / saving if saving > 0 else None,
            'npv': -capex + sum(saving / (1 + rate) ** y for y in range(1, years + 1))}


def paired_ci(values):
    values = np.asarray(values, dtype=float)
    if len(values) < 2 or not np.isfinite(values).all():
        raise ValueError('at least two finite paired values required')
    mean = values.mean()
    margin = t.ppf(.975, len(values)-1) * values.std(ddof=1) / math.sqrt(len(values))
    return mean, mean-margin, mean+margin


def build():
    ladder = pd.read_csv(ROOT / 'runs/rolling_v1/ladder.csv')
    cfg = yaml.safe_load((ROOT / 'configs/economics_v1.yaml').read_text(encoding='utf-8'))
    prices = cfg['tariff']['import_price']
    # Assumed representative Monday-Saturday TOU distribution; no baseline traces exist.
    price = sum(prices[band] * ASSUMED['tou_' + band + '_fraction']
                for band in ('off_peak', 'normal', 'peak')) / ASSUMED['vnd_per_usd']
    if ASSUMED['instances_per_year'] * ASSUMED['instance_hours'] != ASSUMED['operating_hours_per_year']:
        raise ValueError('annual operating hours and instance scaling disagree')
    rows = []
    for scenario, (option, base, new) in itertools.product(('S1', 'S3'), OPTIONS):
        subset = ladder[ladder.scenario.eq(scenario)]
        a = subset[subset.method.eq(base)].set_index('instance_id')
        b = subset[subset.method.eq(new)].set_index('instance_id')
        if not a.index.is_unique or not b.index.is_unique or set(a.index) != set(b.index):
            raise ValueError('unmatched or duplicate instances')
        b = b.loc[a.index]
        equal = (a.TT_h - b.TT_h).abs() <= 1e-8
        excluded = int((~equal).sum())
        a, b = a.loc[equal], b.loc[equal]
        capex = sum(item['amount'] for item in cfg['cases'][option]['capex'])
        opex = sum(item['amount'] for item in cfg['cases'][option]['opex'])
        peak = (a.peak_import_kw - b.peak_import_kw).mean() * 12 * ASSUMED['demand_vnd_per_kw_month'] / ASSUMED['vnd_per_usd']
        for alpha, factor, demand in itertools.product((0, .5, 1), (.5, 1, 2), (False, True)):
            net_delta = (a.import_kwh - b.import_kwh) - alpha * (a.export_kwh - b.export_kwh)
            mean, low, high = paired_ci(net_delta)
            scale = price * ASSUMED['instances_per_year']
            result = finance(mean * scale, peak, capex * factor, opex, demand)
            optimistic = finance(high * scale, peak, capex * factor, opex, demand)
            pessimistic = finance(low * scale, peak, capex * factor, opex, demand)
            rows.append(dict(boundary='SIM_ASSUMED_PROFILE', scenario=scenario, option=option,
                baseline=base, method=new, n_pairs=len(a), n_tt_excluded=excluded, alpha=alpha,
                capex_factor=factor, demand_enabled=demand, capex_usd=capex*factor,
                delta_kwh_mean=mean, delta_kwh_ci_low=low, delta_kwh_ci_high=high,
                annual_net_saving_usd=result['annual_net_saving'], payback_years=result['payback_years'],
                payback_ci_low_years=optimistic['payback_years'], payback_ci_high_years=pessimistic['payback_years'],
                npv_usd=result['npv'], assumed_tou_price_usd_per_kwh=price,
                annual_peak_saving_usd=peak if demand else 0))
    return pd.DataFrame(rows)


def main():
    out = ROOT / 'runs/biz_v1/business_case.csv'
    out.parent.mkdir(parents=True, exist_ok=True)
    build().to_csv(out, index=False)
    print(f'SIM_ASSUMED_PROFILE: wrote {out}; TOU mix and costs assumed')

if __name__ == '__main__':
    main()

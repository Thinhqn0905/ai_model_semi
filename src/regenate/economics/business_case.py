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
               discount_rate=.08, horizon_years=10)


def finance(annual_energy_saving, annual_peak_saving, capex, opex, demand_enabled, rate=.08, years=10):
    saving = annual_energy_saving + (annual_peak_saving if demand_enabled else 0) - opex
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
    ts = pd.read_parquet(ROOT / 'runs/rolling_v1/timeseries.parquet')
    cfg = yaml.safe_load((ROOT / 'configs/economics_v1.yaml').read_text(encoding='utf-8'))
    rows = []
    for scenario, (option, base, new) in itertools.product(('S1', 'S3'), OPTIONS):
        subset = ladder[ladder.scenario.eq(scenario)]
        a = subset[subset.method.eq(base)].set_index('instance_id')
        b = subset[subset.method.eq(new)].set_index('instance_id')
        if not a.index.is_unique or not b.index.is_unique or set(a.index) != set(b.index):
            raise ValueError('unmatched or duplicate instances')
        b = b.loc[a.index]
        delta = a.import_kwh - b.import_kwh
        mean, low, high = paired_ci(delta)
        mismatch = int(((a.TT_h-b.TT_h).abs() > 1e-8).sum())
        available = set(ts.loc[ts.method.eq(base), 'instance_id']) >= set(a.index) and set(ts.loc[ts.method.eq(new), 'instance_id']) >= set(a.index)
        reasons = []
        if not available: reasons.append('baseline time series missing: TOU unavailable')
        if mismatch: reasons.append(f'tardiness differs in {mismatch} paired instances')
        reasons.append('OPEX, installation and requalification costs unknown')
        capex = sum(item['amount'] for item in cfg['cases'][option]['capex'])
        for alpha, factor, demand in itertools.product((0, .5, 1), (.5, 1, 2), (False, True)):
            # Aggregate import/export can show a sensitivity in kWh, but cannot establish TOU cost.
            net_delta = delta - alpha * (a.export_kwh-b.export_kwh)
            m, lo, hi = paired_ci(net_delta)
            rows.append(dict(boundary='NOT_VERIFIED', simulation_boundary='SIM_ASSUMED_PROFILE', scenario=scenario,
                option=option, baseline=base, method=new, n_pairs=len(a), alpha=alpha, capex_factor=factor,
                demand_enabled=demand, capex_usd=capex*factor, delta_kwh_mean=m, delta_kwh_ci_low=lo,
                delta_kwh_ci_high=hi, annual_net_saving_usd=None, payback_years=None, payback_ci_low_years=None,
                payback_ci_high_years=None, npv_usd=None, reason='; '.join(reasons)))
    return pd.DataFrame(rows)


def main():
    out = ROOT / 'runs/biz_v1/business_case.csv'
    out.parent.mkdir(parents=True, exist_ok=True)
    build().to_csv(out, index=False)
    print(f'NOT_VERIFIED: wrote {out}; matched TOU and complete costs unavailable')

if __name__ == '__main__':
    main()

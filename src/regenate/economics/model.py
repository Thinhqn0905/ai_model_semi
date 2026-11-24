"""Electricity tariff and incremental project economics; monetary units are caller-defined."""
from copy import deepcopy
from itertools import product
import math

import numpy as np
import pandas as pd


def energy_cost(p_import, p_export, dt_h, times, tariff):
    """Cost of piecewise-constant kW steps; times are local step starts or hours.

    TOU boundaries must align with step boundaries. Demand charges require real
    timestamps and cover each calendar month represented by the supplied steps.
    """
    imp, exp = np.asarray(p_import, dtype=float), np.asarray(p_export, dtype=float)
    if imp.ndim != 1 or exp.shape != imp.shape or len(imp) != len(times) or not len(imp):
        raise ValueError('power arrays and times must be nonempty and equal length')
    if not np.isfinite(imp).all() or not np.isfinite(exp).all() or (imp < 0).any() or (exp < 0).any() or not math.isfinite(dt_h) or dt_h <= 0:
        raise ValueError('power and step duration must be finite and nonnegative')
    alpha = tariff.get('alpha_ex', 0)
    if alpha not in (0, 0.5, 1):
        raise ValueError('alpha_ex must be 0, 0.5 or 1')
    prices = tariff['import_price']
    charges = 0.0
    timestamps = []
    for i, t in enumerate(times):
        numeric = isinstance(t, (int, float, np.number))
        stamp = None if numeric else pd.Timestamp(t)
        if stamp is not None and pd.isna(stamp):
            raise ValueError('invalid timestamp')
        hour = float(t) if numeric else stamp.hour + stamp.minute / 60 + stamp.second / 3600
        if not 0 <= hour < 24:
            raise ValueError('hour must be in [0, 24)')
        sunday = False if numeric else stamp.dayofweek == 6
        band = 'off_peak' if hour < 6 else ('peak' if not sunday and 17.5 <= hour < 22.5 else 'normal')
        price = float(prices[band])
        export_price = float(tariff.get('export_price', alpha * price))
        if not math.isfinite(price) or not math.isfinite(export_price) or price < 0 or export_price < 0:
            raise ValueError('prices must be finite and nonnegative')
        charges += (imp[i] * price - exp[i] * export_price) * dt_h
        timestamps.append(stamp)
    demand = float(tariff.get('demand_charge_per_kw_month', 0))
    if not math.isfinite(demand) or demand < 0:
        raise ValueError('demand charge must be finite and nonnegative')
    if demand:
        if any(t is None for t in timestamps):
            raise ValueError('monthly demand charges require timestamps')
        peaks = {}
        for stamp, power in zip(timestamps, imp):
            key = (stamp.year, stamp.month)
            peaks[key] = max(peaks.get(key, 0), power)
        charges += demand * sum(peaks.values())
    return float(charges)


def annualise(run_cost, run_hours, operating_hours_per_year):
    if not all(math.isfinite(x) for x in (run_cost, run_hours, operating_hours_per_year)) or run_hours <= 0 or operating_hours_per_year < 0:
        raise ValueError('invalid annualisation inputs')
    return run_cost * operating_hours_per_year / run_hours


def _total(items):
    if isinstance(items, (int, float)):
        value = float(items)
    else:
        value = sum(float(item['amount']) for item in items)
    if not math.isfinite(value) or value < 0:
        raise ValueError('costs must be finite and nonnegative')
    return value


def incremental_case(base_run, new_run, capex_add, opex_add, cfg):
    """Compare matched runs: mappings contain p_import, p_export, dt_h, times."""
    if base_run['dt_h'] != new_run['dt_h'] or list(base_run['times']) != list(new_run['times']):
        raise ValueError('runs must have matched time grids')
    tariff = cfg['tariff']
    costs = [energy_cost(r['p_import'], r['p_export'], r['dt_h'], r['times'], tariff) for r in (base_run, new_run)]
    hours = len(base_run['times']) * base_run['dt_h']
    saving = annualise(costs[0] - costs[1], hours, cfg['operating_hours_per_year']) - _total(opex_add) + float(cfg.get('annual_cooling_saving', 0))
    capex = _total(capex_add)
    years, rate = cfg['horizon_years'], float(cfg['discount_rate'])
    if not isinstance(years, int) or years <= 0 or not math.isfinite(rate) or rate <= -1 or not math.isfinite(saving):
        raise ValueError('invalid financial assumptions')
    npv = -capex + sum(saving / (1 + rate) ** year for year in range(1, years + 1))
    irr = None
    if capex > 0 and saving > 0:
        def f(r):
            return -capex + sum(saving / (1 + r) ** y for y in range(1, years + 1))
        lo, hi = -0.999, 1.0
        while f(hi) > 0 and hi < 1e10:
            hi *= 2
        if f(lo) >= 0 and f(hi) <= 0:
            for _ in range(100):
                mid = (lo + hi) / 2
                if f(mid) > 0:
                    lo = mid
                else:
                    hi = mid
            irr = (lo + hi) / 2
    return {'annual_saving': saving, 'simple_payback_y': capex / saving if saving > 0 else None, 'npv': npv, 'irr': irr}


def sensitivity_grid(base_run, new_run, capex_add, opex_add, cfg):
    """Flat USD price scenarios are assumed; do not mix them with VND costs."""
    rows = []
    for (label, price), alpha, factor in product((('low', .046), ('base', .078), ('high', .132)), (0, .5, 1), (.5, 1, 2)):
        case_cfg = deepcopy(cfg)
        case_cfg['tariff'] = {'import_price': dict.fromkeys(('off_peak', 'normal', 'peak'), price), 'alpha_ex': alpha}
        result = incremental_case(base_run, new_run, _total(capex_add) * factor, opex_add, case_cfg)
        rows.append({'price_scenario': label, 'price_per_kwh': price, 'alpha_ex': alpha, 'capex_factor': factor, **result})
    return pd.DataFrame(rows)

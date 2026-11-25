"""Monthly single-meter billing; timestamps are already in tariff local time."""
import numpy as np
import pandas as pd


def _value(x, default=0):
    if isinstance(x, dict):
        x = x.get('value')
    return default if x is None else x


def _period(ts, windows):
    minute = ts.hour * 60 + ts.minute
    for w in windows:
        start, end = (int(w[k][:2])*60+int(w[k][3:]) for k in ('start', 'end'))
        if ts.weekday() in w['days'] and start <= minute < end:
            return w['period']
    return 'normal'


def my_public_holidays(year):
    try:
        import holidays
    except ImportError as exc:
        raise ImportError("Install the 'holidays' package to obtain Malaysian public holidays") from exc
    return holidays.country_holidays('MY', subdiv=None, years=year)


def monthly_bill(power_kw, timestamps, tariff, holidays=None):
    if tariff.get('tariff_status') == 'TRIAL_NOT_PAYABLE':
        raise ValueError('paper trial tariff is not payable')
    if tariff.get('id') == 'TAR03_SG' and tariff.get('contract_kw') is None:
        raise ValueError('Singapore contracted capacity must be supplied')
    p = np.asarray(power_kw, dtype=float)
    t = pd.DatetimeIndex(timestamps)
    if len(p) != len(t) or len(t) < 2 or not np.isfinite(p).all() or t.hasnans:
        raise ValueError('need matching finite power and at least two timestamps')
    delta = np.diff(t.asi8)
    if (delta <= 0).any() or not (delta == delta[0]).all():
        raise ValueError('timestamps must be strictly increasing and regular')
    step = pd.Timedelta(int(delta[0]), unit='ns')
    minutes = step.total_seconds()/60
    interval = float(_value(tariff.get('billing_interval_minutes'), 30))
    n = interval/minutes
    if n < 1 or not float(n).is_integer():
        raise ValueError('billing interval must be a multiple of sample interval')
    n = int(n)
    def unverified(obj):
        if isinstance(obj, dict):
            return obj.get('status') == 'NOT_VERIFIED' or any(unverified(v) for v in obj.values())
        if isinstance(obj, list):
            return any(unverified(v) for v in obj)
        return False
    mode = tariff.get('interval_mode', 'aligned')
    if mode not in ('aligned', 'sliding'):
        raise ValueError('interval_mode must be aligned or sliding')
    if tariff.get('contract_kw') is not None and float(_value(tariff['contract_kw'])) < 0:
        raise ValueError('contract capacity must be nonnegative')
    windows = tariff.get('windows', [])
    holiday_dates = set(tariff.get('holiday_dates', []) if holidays is None else holidays)
    period = np.array(['offpeak' if windows and x.date() in holiday_dates else _period(x, windows) for x in t])
    rates = tariff.get('energy_rates', {})
    months = {}
    for month in sorted(set(t.strftime('%Y-%m'))):
        ix = np.flatnonzero(t.strftime('%Y-%m') == month)
        if rates and any(rates.get(period[i], rates.get('normal')) is None or _value(rates.get(period[i], rates.get('normal')), None) is None for i in ix):
            raise ValueError('missing energy rate for a consumed period')
        energy = sum(max(p[i], 0)*minutes/60*float(_value(rates.get(period[i], rates.get('normal')))) for i in ix)
        export = sum(max(-p[i], 0)*minutes/60 for i in ix)*float(_value(tariff.get('export_rate')))
        candidates = []
        for i in ix:
            if i+n > len(t) or t[i+n-1].strftime('%Y-%m') != month:
                continue
            if mode == 'aligned' and (t[i] - t[i].normalize()) % pd.Timedelta(minutes=interval) != pd.Timedelta(0):
                continue
            eligible = tariff.get('demand_eligible_periods')
            if eligible and not all(x in eligible for x in period[i:i+n]):
                continue
            candidates.append((float(np.maximum(p[i:i+n], 0).mean()), t[i]))
        demand, stamp = max(candidates, default=(0.0, None), key=lambda x:x[0])
        demand_components = {k: demand*float(_value(v)) for k, v in tariff.get('demand_rates', {}).items()}
        fixed_components = {k: float(_value(v)) for k, v in tariff.get('fixed_fees', {}).items()}
        demand_charge = sum(demand_components.values())
        fixed = sum(fixed_components.values())
        contract = tariff.get('contract_kw')
        capacity = excess = 0.0
        if contract is not None:
            contract = float(_value(contract))
            capacity = contract*float(_value(tariff.get('contract_rate')))
            excess = max(0, demand-contract)*float(_value(tariff.get('excess_rate')))
        months[month] = {'energy_charge': energy, 'demand_charge': demand_charge, 'demand_components': demand_components, 'fixed_fees': fixed, 'fixed_components': fixed_components, 'contract_charge': capacity, 'excess_charge': excess, 'export_credit': export, 'billed_demand_kw': demand, 'demand_timestamp': stamp.isoformat() if stamp is not None else None, 'total': energy+demand_charge+fixed+capacity+excess-export, 'not_verified': unverified(tariff) or not candidates}
    return {'months': months, 'not_verified': any(m['not_verified'] for m in months.values())}

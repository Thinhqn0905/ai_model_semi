"""DS03 stage-efficiency proxy; the TI hardware is not a measured test cell."""
from functools import lru_cache
from regenate.data.ds03 import eta_curve
from regenate.electrical.ledger import ElecParams

_STAGES = {
    'eta_sup_dc': ('TIDA-010938-battery-buck-320', 'forward', 39),
    'eta_rl_dc': ('TIDA-010938-battery-boost-320', 'regen', 41),
    'eta_afe_exp': ('TIDA-010938-dc-ac-unipolar', 'regen', 43),
}

@lru_cache(maxsize=None)
def _curve(param):
    device, direction, _ = _STAGES[param]
    return eta_curve(device, direction)

def eta_at(param, load_frac):
    """Interpolate within each stage's measured range; curves may be non-monotone.

    AC import assumes the export curve is symmetric; composite stages use the
    same nominal fraction, an approximation rather than a power-flow solution.
    """
    x = float(load_frac)
    if param in _STAGES:
        curve = _curve(param)
        if not curve.valid_range[0] <= x <= curve.valid_range[1]:
            raise ValueError(f'{param}: load fraction outside {curve.valid_range}')
        return float(curve(x))
    if param == 'eta_afe_imp':
        return eta_at('eta_afe_exp', x)
    if param == 'eta_sup_ac':
        return eta_at('eta_afe_imp', x) * eta_at('eta_sup_dc', x)
    if param == 'eta_rl_ac':
        return eta_at('eta_rl_dc', x) * eta_at('eta_afe_exp', x)
    if param == 'eta_link':
        if not 0 <= x <= 1:
            raise ValueError('load fraction outside [0, 1]')
        return 0.99
    raise ValueError(f'unknown efficiency: {param}')

def grounded_params(load_frac=0.5):
    names = ('eta_sup_ac', 'eta_sup_dc', 'eta_rl_ac', 'eta_rl_dc', 'eta_afe_imp', 'eta_afe_exp', 'eta_link')
    values = {name: eta_at(name, load_frac) for name in names}
    source = 'DS03_Modeling/tiduf64c.pdf'
    provenance = {name: {'label': 'DATASHEET', 'file': source, 'page': page,
                         'device': device, 'direction': direction, 'load_frac': load_frac}
                  for name, (device, direction, page) in _STAGES.items()}
    provenance['eta_afe_imp'] = {'label': 'ASSUMED', 'file': source, 'page': 43,
        'load_frac': load_frac, 'note': 'Symmetric reverse direction; table measures DC to AC only.'}
    for name, stages in [('eta_sup_ac', 'eta_afe_imp * eta_sup_dc'), ('eta_rl_ac', 'eta_rl_dc * eta_afe_exp')]:
        provenance[name] = {'label': 'DERIVED', 'file': source, 'page': '39, 41, 43',
                            'load_frac': load_frac, 'note': stages}
    provenance['eta_link'] = {'label': 'ASSUMED', 'file': 'docs/system_spec.md', 'page': 'section 5',
        'load_frac': load_frac, 'note': '1% cable/breaker loss allowance; not a cable sizing calculation.'}
    return ElecParams(**values), provenance

from dataclasses import asdict
from pathlib import Path

import pandas as pd
import yaml

from regenate.electrical.ledger import ElecParams
from regenate.data.recipes import recipes

ROOT = Path(__file__).resolve().parents[3]
COLUMNS = ['name', 'value', 'unit', 'module', 'provenance', 'source', 'grounding_candidate', 'sensitivity_priority']


def collect():
    """Collect current configured and default assumptions, without asserting validation."""
    rows = []
    def add(name, value, unit, module, provenance, source, candidate, priority='medium'):
        rows.append(dict(zip(COLUMNS, (name, value, unit, module, provenance, source, candidate, priority))))

    high = {'eta_sup_dc', 'eta_rl_dc', 'eta_afe_imp', 'eta_afe_exp', 'eta_link', 'P_link_max'}
    for name, value in asdict(ElecParams()).items():
        unit = 'kW' if name.startswith('P_') else ('boolean' if isinstance(value, bool) else 'dimensionless')
        add(name, value, unit, 'electrical.ledger', 'ASSUMED', 'src/regenate/electrical/ledger.py:ElecParams', 'data/processed/efficiency_points.parquet (TIDA-010938 curves); site equipment and HVAC measurements', 'high' if name in high else 'medium')
    try:
        from regenate.simulation.bus_twin import TwinParams
    except ImportError as exc:
        if exc.name != 'regenate.simulation.bus_twin':
            raise
    else:
        for name, value in asdict(TwinParams()).items():
            units = {'v_nom':'V','v_min':'V','v_max':'V','capacitance_f':'F','p_afe_max_kw':'kW','k_droop_kw_per_v':'kW/V','tau_afe_s':'s','v_chop':'V','p_chop_max_kw':'kW','i_link_max_a':'A','p_link_max_kw':'kW','ramp_kw_per_s':'kW/s','loss_fraction':'dimensionless','dt_s':'s'}
            add(name, value, units[name], 'simulation.bus_twin', 'ASSUMED', 'src/regenate/simulation/bus_twin.py:TwinParams', 'DS02 LVDC traces and site converter specifications')
    bench = yaml.safe_load((ROOT / 'configs/bench_v1.yaml').read_text(encoding='utf-8'))
    units = {'unit_h':'h/abstract unit', 'p_rated_kw':'kW', 'aux_kw':'kW', 'downtime_probability_per_day':'1/day', 'downtime_mean_h':'h', 'release_delay_mean_h':'h', 'max_shift_h':'h', 'dt_h':'h'}
    for name, value in bench.items():
        add(name, str(value) if isinstance(value, list) else value, units.get(name, 'dimensionless'), 'configs.bench_v1', 'SYNTHETIC' if name in {'n','tau','reps','scenarios','seeds'} else 'ASSUMED', 'configs/bench_v1.yaml', 'DS01 instances or site production and station traces', 'high' if name in {'scenarios','cycle_scale','p_rated_kw'} else 'medium')
    for scenario in ('S1', 'S2', 'S3'):
        frame = recipes(scenario, aux_kw=bench['aux_kw'], cycle_scale=bench['cycle_scale'])
        for _, phase in frame.iterrows():
            for key in ('dur_frac', 'p_in_frac', 'p_rec_frac'):
                provenance = 'DERIVED' if scenario == 'S3' and phase['kind'] != 'rest' else 'ASSUMED'
                add(f"{scenario}.{int(phase['phase_idx'])}.{phase['kind']}.{key}", phase[key], 'dimensionless', 'data.recipes', provenance, 'src/regenate/data/recipes.py; data/processed/provenance_ds03.json' if scenario == 'S3' else 'src/regenate/data/recipes.py', 'time-aligned site station power profiles; data/processed/ds03_edc_cycles.parquet', 'high')
    econ = yaml.safe_load((ROOT / 'configs/economics_v1.yaml').read_text(encoding='utf-8'))
    tariff = econ['tariff']
    for key, value in tariff.items():
        if key in ('source', 'hours_source', 'currency'):
            continue
        for sub, val in (value.items() if isinstance(value, dict) else [(None, value)]):
            name = f'tariff.{key}' + (f'.{sub}' if sub else '')
            label = 'DERIVED' if key == 'import_price' else 'ASSUMED'
            add(name, val, 'VND/kWh' if key == 'import_price' else ('VND/kW/month' if key == 'demand_charge_per_kw_month' else 'dimensionless'), 'configs.economics_v1', label, 'configs/economics_v1.yaml' + ('; ' + tariff['source'] if key == 'import_price' else ''), 'site electricity supply and export contract')
    for case, details in econ['cases'].items():
        for category in ('capex', 'opex'):
            for item in details[category]:
                add(f"{case}.{category}.{item['name']}", item['amount'], econ['financial_currency'], 'configs.economics_v1', 'ASSUMED', 'configs/economics_v1.yaml', 'site vendor quote including installation and requalification')
    return pd.DataFrame(rows, columns=COLUMNS)


if __name__ == '__main__':
    output = ROOT / 'reports/audit/assumption_register.csv'
    output.parent.mkdir(parents=True, exist_ok=True)
    collect().to_csv(output, index=False)

"""One-at-a-time sensitivity campaign; all measurements use assumed profiles."""
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from regenate.data.generator import generate
from regenate.data.ds01 import SOURCE, load_instance
from regenate.evaluation.stats import paired_ci

ROOT = Path('runs/sens_v1')
BOUNDARY = 'SIM_ASSUMED_PROFILE'


def points():
    out = []
    def add(sweep, value, **kw):
        out.append(dict(sweep=sweep, value=str(value), **kw))
    for v in [0, .1, .25, .5, 1]: add('flex', v, flex=v)
    for v in [.94, .96, .98]: add('eta_afe', v, prm={'eta_afe_imp': v, 'eta_afe_exp': v})
    for v in [.97, .99, 1.0]: add('eta_link', v, prm={'eta_link': v})
    for v in [5, 10, 20, 'inf']: add('p_link_max', v, link=str(v))
    for v in [4, 8, 16]: add('n_stations', v, config={'n_stations': v})
    for v in [True, False]: add('allow_export', str(v).lower(), prm={'allow_export': v})
    for v in [.5, 1, 2]: add('cycle_scale', v, config={'cycle_scale': v})
    for v in [.5, 1, 2]: add('unit_h', v, config={'unit_h': v})
    for f in [0, .25, 1]:
        for e in [.97, .99, 1.0]: add('grid', f'{f}_eta_{e}', flex=f, prm={'eta_link': e}, scenarios=['S3'])
    return out


def aggregate(path, sweep, value, scenario):
    df = pd.read_csv(path)
    df = df[df.scenario == scenario]
    required = ['B1-OPT', 'B1p-OPT', 'ORACLE']
    if df.duplicated(['instance_id', 'method']).any(): raise ValueError('duplicate instance/method')
    w = df.pivot(index='instance_id', columns='method')
    if any(m not in w['net_kwh'] for m in required): raise ValueError('missing required method')
    for column in ['net_kwh', 'peak_import_kw', 'TT_h', 'completed_jobs', 'violations', 'mip_gap', 'direct_reuse_kwh', 'recoverable_kwh']:
        if column not in w or w[column][required].isna().any().any(): raise ValueError(f'missing {column}')
    if not ((w['TT_h'][required].max(axis=1) - w['TT_h'][required].min(axis=1)).abs() <= 1e-6).all(): raise ValueError('unequal tardiness')
    if not (w['completed_jobs'][required].nunique(axis=1) == 1).all(): raise ValueError('unequal throughput')
    if (w['violations'][required] != 0).any().any(): raise ValueError('constraint violations')
    if (w['net_kwh']['B1p-OPT'] <= 0).any(): raise ValueError('nonpositive percentage denominator')
    result = dict(sweep=sweep, value=value, scenario=scenario, n=len(w), boundary=BOUNDARY, error='')
    def stat(name, a, b):
        r = paired_ci(a, b)
        for k in ('mean', 'lo', 'hi'): result[f'{name}_{k}'] = r[k]
        return r
    base, oracle = w['net_kwh']['B1p-OPT'], w['net_kwh']['ORACLE']
    r = stat('gain_kwh', base, oracle)
    stat('gain_pct', 100 * (base-oracle)/base, np.zeros(len(w)))
    stat('b1_gain_kwh', w['net_kwh']['B1-OPT'], oracle)
    stat('peak_diff_kw', w['peak_import_kw']['B1p-OPT'], w['peak_import_kw']['ORACLE'])
    rec = w['recoverable_kwh']['ORACLE']
    if (rec <= 0).any(): raise ValueError('nonpositive recoverable energy')
    stat('r_match', w['direct_reuse_kwh']['ORACLE']/rec, np.zeros(len(w)))
    result['share_gain_positive'] = r['wins']/len(w)
    result['max_mip_gap'] = float(w['mip_gap'][required].max().max())
    return result


def make_bench(config):
    cfg = yaml.safe_load(Path('configs/bench_v1.yaml').read_text())
    cfg.update(config); cfg.update(n=[10], seeds=[0, 1], scenarios=['S1', 'S3'])
    key = '_'.join(f'{k}_{v}' for k, v in config.items())
    out = Path('data/generated/sens_' + key)
    manifest = out / 'manifest.json'
    if manifest.exists() and json.loads(manifest.read_text()).get('config') == cfg: return out
    out.mkdir(parents=True, exist_ok=True)
    ids = []
    for path in sorted(SOURCE.glob('n*_tau*_r*.json')):
        ds = load_instance(path)
        if ds['n'] not in cfg['n'] or ds['tau'] not in cfg['tau'] or ds['replicate'] not in cfg['reps']: continue
        for scenario in cfg['scenarios']:
            for seed in cfg['seeds']:
                inst = generate(ds, scenario, seed, cfg); iid = inst['instance_id']; dest = out/iid
                dest.mkdir(parents=True, exist_ok=True)
                for name, frame in [('jobs', inst['jobs']), ('stations', inst['stations']), ('recipes', inst['recipe'])]: frame.to_parquet(dest/(name+'.parquet'), index=False)
                ids.append(iid)
    if not ids: raise ValueError('no matching instances')
    manifest.write_text(json.dumps(dict(config=cfg, instances=ids, splits={'test': ids}, boundary=BOUNDARY), indent=2))
    return out


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rows = []
    for p in points():
        folder = ROOT / (p['sweep'] + '_' + p['value']); folder.mkdir(parents=True, exist_ok=True)
        scenarios = p.get('scenarios', ['S3', 'S1'])
        try:
            bench = make_bench(p['config']) if 'config' in p else Path('data/generated/bench_v1')
            cmd = [sys.executable, '-m', 'regenate.evaluation.oracle_campaign', '--out', str(folder), '--bench', str(bench), '--n', '10', '--seeds', '0', '1', '--flex', str(p.get('flex', 1.0)), '--scenarios', *scenarios, '--time_limit', '30', '--workers', '8', '--prm', json.dumps(p.get('prm', {})), '--P_link_max', p.get('link', 'inf')]
            man = folder/'manifest.json'
            expected = json.loads((bench/'manifest.json').read_text())
            expected_ids = {i for i in expected['instances'] if int(i[1:4]) == 10 and int(i.split('_')[-1]) in (0, 1) and i.split('_')[3] in scenarios}
            if not expected_ids: raise ValueError('no expected instances')
            valid = False
            if man.exists() and (folder/'results.csv').exists():
                args = json.loads(man.read_text())['args']
                valid = args['bench'] == str(bench) and args['flex'] == [float(p.get('flex', 1))] and set(args['scenarios']) == set(scenarios) and json.loads(args['prm']) == p.get('prm', {}) and args['time_limit'] == 30 and args['workers'] == 8 and args['P_link_max'] == float(p.get('link', 'inf'))
            if not valid:
                env = dict(os.environ); env['PYTHONPATH'] = str(Path('src').resolve()) + os.pathsep + env.get('PYTHONPATH', '')
                with (folder/'campaign.log').open('w') as log: subprocess.run(cmd, env=env, stdout=log, stderr=subprocess.STDOUT, check=True)
            df = pd.read_csv(folder/'results.csv')
            if set(df.instance_id) != expected_ids: raise ValueError('instance set incomplete')
            for scenario in scenarios:
                try: rows.append(aggregate(folder/'results.csv', p['sweep'], p['value'], scenario))
                except Exception as exc: rows.append(dict(sweep=p['sweep'], value=p['value'], scenario=scenario, n=0, boundary='NOT_VERIFIED', error=str(exc)))
        except Exception as exc:
            for scenario in scenarios: rows.append(dict(sweep=p['sweep'], value=p['value'], scenario=scenario, n=0, boundary='NOT_VERIFIED', error=str(exc)))
        pd.DataFrame(rows).to_csv(ROOT/'sensitivity_results.csv', index=False)
        print(f"{p['sweep']} {p['value']}: recorded", flush=True)
    df = pd.DataFrame(rows)
    report = Path('reports/sensitivity/sens_v1.md'); report.parent.mkdir(parents=True, exist_ok=True)
    lines = ['# Sensitivity campaign', '', 'Boundary: SIM_ASSUMED_PROFILE. Bench v1 uses assumed station powers and synthetic phase profiles; these are not site measurements. Comparisons use net grid energy at M0, matched instances and equal tardiness. Positive gain is B1p-OPT minus ORACLE. Bootstrap 95% confidence intervals are paired by instance.', '', '| Sweep | Value | Scenario | n | Gain kWh (mean; 95% CI) | Error |', '|---|---|---|---:|---|---|']
    for r in rows:
        gain = f"{r['gain_kwh_mean']:.4g} [{r['gain_kwh_lo']:.4g}, {r['gain_kwh_hi']:.4g}]" if 'gain_kwh_mean' in r else 'NOT_VERIFIED'
        lines.append(f"| {r['sweep']} | {r['value']} | {r['scenario']} | {r['n']} | {gain} | {r['error']} |")
    significant = [f"{r['sweep']}={r['value']} ({r['scenario']})" for r in rows if r.get('gain_kwh_lo', -float('inf')) > 0]
    lines += ['', 'Positive shared-DC gain with CI excluding zero: ' + (', '.join(significant) if significant else 'none verified') + '.', 'Full metrics and errors: runs/sens_v1/sensitivity_results.csv. Solver gaps are reported there; no measured bus-stability or site evidence is implied.']
    report.write_text('\n'.join(lines)+'\n', encoding='utf-8')
    return int(bool(df.error.fillna('').ne('').any()))

if __name__ == '__main__': sys.exit(main())

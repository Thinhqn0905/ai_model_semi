"""Rolling replay campaign on bench_v1; simulated profiles only."""
import argparse
import json
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

from regenate.data.generator import fifo_schedule, render
from regenate.electrical.ledger import ElecParams, ledger
from regenate.evaluation import oracle_campaign as oracle
from regenate.evaluation.stats import ladder_table, match_ratio, paired_ci
from regenate.optimization.rolling import Replanner
from regenate.simulation.replay import Replay


def run_instance(args):
    iid, bench, flex, slot, limit, max_solve = args
    oracle.set_bench(bench)
    inst = oracle.load(iid)
    assign, starts = fifo_schedule(inst)
    initial = {j: (assign[j], starts[j]) for j in assign}
    prm = ElecParams()
    rows, schedules, series = [], [], []
    for method in ('P0', 'P'):
        replanner = Replanner(inst, mode=method, slot_h=slot, prm=prm, flex=flex, time_limit=limit)
        plan, log = Replay(inst, initial, replanner, period_h=slot, max_solve_s=max_solve).run()
        a = {j: v[0] for j, v in plan.items()}
        st = {j: v[1] for j, v in plan.items()}
        row, sch = oracle.score(inst, method, 'DC', a, st, slot, prm, replanner.solve_s, np.nan)
        replans = log[log.event == 'replan']
        row.update(instance_id=iid, scenario=iid.split('_')[3], n_jobs=len(inst['jobs']),
                   n_stations=len(inst['stations']), seed=int(iid.split('_')[-1]), flex=flex,
                   boundary='SIM_ASSUMED_PROFILE', n_replans=len(replans),
                   n_rejected=int((~replans.accepted.astype(bool)).sum()))
        rows.append(row)
        fifo = starts
        schedules.extend(dict(instance_id=iid, shift_h=s['start_h'] - fifo[s['job_id']], **s) for s in sch)
        traces = render(inst, a, st, slot, truth=True)
        result = ledger(*traces, slot, 'DC', prm)
        for k in range(len(result['p_import'])):
            one = ledger(*(x[:, k:k+1] for x in traces), slot, 'DC', prm)
            series.append(dict(instance_id=iid, method=method, t_h=k*slot,
                               p_import_kw=result['p_import'][k], p_export_kw=result['p_export'][k],
                               direct_kw=result['direct'][k], self_use_kw=result['self_use'][k],
                               recoverable_kw=one['recoverable_kwh']/slot, dump_kw=result['dump'][k]))
    return rows, schedules, series


def campaign(bench, oracle_csv, out, report, ids, workers=8, flex=0.25, slot=0.25, limit=10, max_solve=60):
    bench, out, report = Path(bench), Path(out), Path(report)
    man = json.loads((bench / 'manifest.json').read_text())
    split = {i: s for s, group in man['splits'].items() for i in group}
    base = pd.read_csv(oracle_csv)
    base = base[base.instance_id.isin(ids) & np.isclose(base.flex, flex)].copy()
    expected = {'B0', 'B1', 'B1p', 'B2', 'B1-OPT', 'B1p-OPT', 'B3', 'ORACLE'}
    for iid in ids:
        subset = base[base.instance_id == iid]
        if set(subset.method) != expected or subset.method.duplicated().any() or subset.net_kwh.isna().any():
            raise ValueError(f'incomplete oracle ladder for {iid}')
    tasks = [(i, str(bench), flex, slot, limit, max_solve) for i in ids]
    rows, schedules, series = [], [], []
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for r, s, t in pool.map(run_instance, tasks):
            rows.extend(r); schedules.extend(s); series.extend(t)
    df = pd.DataFrame(rows); df['split'] = df.instance_id.map(split)
    out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / 'results.csv', index=False)
    pd.DataFrame(schedules).to_parquet(out / 'schedules.parquet', index=False)
    pd.DataFrame(series).to_parquet(out / 'timeseries.parquet', index=False)
    ladder = pd.concat([base, df], ignore_index=True)
    ladder.to_csv(out / 'ladder.csv', index=False)
    equal = ladder_table(ladder, equal_tt=True); all_rows = ladder_table(ladder, equal_tt=False)
    equal.to_csv(out / 'ladder_equal_tt.csv', index=False)
    all_rows.to_csv(out / 'ladder_all.csv', index=False)
    summary = ladder.copy(); summary['matching_ratio'] = match_ratio(summary)
    lines = ['# Rolling ladder', '', 'Boundary: SIM_ASSUMED_PROFILE; bench_v1 synthetic assumed power profiles. D002: i.i.d. uncertainty makes P vs P0 a control, not an AI claim.', '',
             'Net M0 kWh, import peak, matching ratio, tardiness and makespan are means over available instances; violations include AFE violation steps. Bus voltage excursions are not simulated.', '',
             '| Method | n | net kWh | peak kW | matching ratio | TT h | makespan h | completed | violations |', '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for method in ['B0','B1','B1-OPT','B1p','B1p-OPT','B2','B3','P0','P','ORACLE']:
        x = summary[summary.method == method]
        lines.append(f"| {method} | {len(x)} | {x.net_kwh.mean():.4g} | {x.peak_import_kw.mean():.4g} | {x.matching_ratio.mean():.4g} | {x.TT_h.mean():.4g} | {x.makespan_h.mean():.4g} | {x.completed_jobs.mean():.4g} | {x.violations.sum():.4g} |")
    for title, table in [('Equal tardiness', equal), ('All instances (tardiness may differ)', all_rows)]:
        lines += ['', '## '+title, '', '| Comparison | n | mean kWh | 95% paired bootstrap CI |', '|---|---:|---:|---:|']
        for r in table.itertuples():
            lines.append(f'| {r.comparison} | {r.n} | {r.mean:.4g} | [{r.lo:.4g}, {r.hi:.4g}] |')
        # Direct primary KPI vs B1 for each method, paired and subject to same TT filter.
        for method in ['B1-OPT','B1p','B1p-OPT','B2','B3','P0','P','ORACLE']:
            a = ladder[ladder.method == 'B1'].set_index('instance_id')
            b = ladder[ladder.method == method].set_index('instance_id')
            pair = a[['net_kwh','TT_h']].join(b[['net_kwh','TT_h']], lsuffix='_a', rsuffix='_b').dropna()
            if title == 'Equal tardiness': pair = pair[(pair.TT_h_a-pair.TT_h_b).abs() <= 1e-6]
            ci = paired_ci(pair.net_kwh_a, pair.net_kwh_b)
            lines.append(f"| B1 minus {method} | {ci['n']} | {ci['mean']:.4g} | [{ci['lo']:.4g}, {ci['hi']:.4g}] |")
    report.parent.mkdir(parents=True, exist_ok=True); report.write_text('\n'.join(lines)+'\n', encoding='utf-8')
    (out / 'manifest.json').write_text(json.dumps(dict(bench=str(bench), oracle_csv=str(oracle_csv), ids=ids, flex=flex, slot_h=slot, time_limit=limit, max_solve_s=max_solve, workers=workers, code_sha256_16=oracle.code_hash(), boundary='SIM_ASSUMED_PROFILE'), indent=2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--bench', default='data/generated/bench_v1'); ap.add_argument('--oracle', default='runs/oracle_v1/results.csv')
    ap.add_argument('--out', default='runs/rolling_v1'); ap.add_argument('--report', default='reports/benchmark/rolling_v1.md')
    ap.add_argument('--workers', type=int, default=8)
    args = ap.parse_args()
    man = json.loads((Path(args.bench)/'manifest.json').read_text())
    ids = [i for i in man['instances'] if int(i[1:4]) == 10 and i.split('_')[3] in ('S1','S3') and int(i.split('_')[-1]) in (0,1)]
    campaign(args.bench, args.oracle, args.out, args.report, ids, args.workers)


if __name__ == '__main__': main()

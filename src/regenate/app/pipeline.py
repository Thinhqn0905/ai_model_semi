"""Offline replay of one benchmark instance; screening is not protection."""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
from regenate.data.generator import fifo_schedule, render
from regenate.electrical.ledger import ElecParams, ledger
from regenate.evaluation import oracle_campaign as oc
from regenate.optimization.milp import solve, assign_stations
from regenate.optimization.rolling import Replanner
from regenate.simulation.replay import Replay
from regenate.simulation.bus_twin import check_plan


def production_errors(inst, plan):
    errors = []
    jobs = inst['jobs'].set_index('job_id')
    stations = inst['stations'].set_index('station_id')
    intervals = {}
    for j, (s, start) in plan.items():
        row = jobs.loc[j]; end = start + oc.true_dur(inst, j)
        if s not in row.eligible_stations or start < row.release_h - 1e-9 or end > row.deadline_h + 1e-9:
            errors.append(f'job {j}: eligibility/release/deadline')
        if any(start < b and end > a for a, b in json.loads(stations.loc[s, 'downtime_json'])):
            errors.append(f'job {j}: downtime')
        intervals.setdefault(s, []).append((start, end, j))
    for spans in intervals.values():
        spans.sort()
        for a, b in zip(spans, spans[1:]):
            if b[0] < a[1] - 1e-9: errors.append(f'jobs {a[2]},{b[2]}: overlap')
    return errors


def run(inst, out, reject=(), models=None, time_limit=2.0, report=None):
    from regenate.data.bench_v2 import fifo as fifo_v2
    from regenate.forecasting.ai_engine import AIEngine, make_profile_fn
    from regenate.evaluation import v2_campaign
    dt = inst['dt_h']; prm = ElecParams(); v2 = 'traces' in inst
    boundary = inst.get('meta', {}).get('boundary', 'SIM_ASSUMED_PROFILE')
    if models and not v2: raise ValueError('--models requires a bench v2 instance with telemetry')
    engine = AIEngine.load(models) if models else None
    profile = make_profile_fn(inst, 'P3' if engine else 'P0', engine, dt) if v2 else None
    a, starts = fifo_v2(inst) if v2 else fifo_schedule(inst)
    initial = {j: (a[j], starts[j]) for j in a}
    planner = Replanner(inst, 'P3' if engine else 'P0', dt, prm, time_limit=time_limit, profile_fn=profile)
    rejected = set(reject); checks = []
    def approve(old, new, obs):
        errors = production_errors(inst, new)
        if not errors:
            pi, pr, _ = render(inst, {j:v[0] for j,v in new.items()}, {j:v[1] for j,v in new.items()}, dt)
            twin = check_plan(pr * prm.eta_rl_dc, pi / prm.eta_sup_dc, dt * 3600)
            if not twin['approved']: errors.append('bus twin: ' + str(twin.get('violations', 'violation')))
        checks.append('; '.join(errors))
        return not errors and len(checks) not in rejected
    real, events = Replay(inst, initial, planner, period_h=dt, approve=approve, max_solve_s=3*time_limit).run()
    log = events[events.event == 'replan'].copy().reset_index(drop=True)
    # Replay records failures before the approval callback as well.
    it = iter(checks)
    log['validation'] = [next(it, '') if reason == 'engineer_reject' or accepted else '' for accepted, reason in zip(log.accepted, log.reason)]
    log['boundary'] = boundary
    assign = {j:v[0] for j,v in real.items()}; st = {j:v[1] for j,v in real.items()}
    rows = []
    for name, topo, aa, ss in [('B1', 'B1', a, starts), ('pipeline', 'DC', assign, st)]:
        row, _ = oc.score(inst, name, topo, aa, ss, dt, prm); rows.append(row)
    jobs = v2_campaign.milp_jobs(inst, 'truth', 1.0, starts, dt) if v2 else oc.milp_jobs(inst, dt, True, 1.0, starts)
    result = solve(jobs, len(inst['stations']), max(j.latest+j.dur for j in jobs)+1, 'B1p', prm, dt, time_limit=time_limit)
    if result.starts:
        ids = list(inst['jobs'].job_id); ssn = assign_stations(result.starts, [j.dur for j in jobs], len(inst['stations']))
        aa = dict(zip(ids, ssn)); ss = oc.execute(inst, aa, dict(zip(ids, [x*dt for x in result.starts])))
        row, _ = oc.score(inst, 'B1p-OPT', 'B1p', aa, ss, dt, prm, gap=result.mip_gap); row['status'] = result.status; rows.append(row)
    powers = render(inst, assign, st, dt); led = ledger(*powers, dt, 'DC', prm)
    series = {k:v for k,v in led.items() if isinstance(v, np.ndarray) and v.ndim == 1 and len(v) == powers[0].shape[1]}
    frame = pd.DataFrame(series); frame.insert(0, 't_h', np.arange(len(frame))*dt); frame['boundary'] = boundary
    schedule = pd.DataFrame([dict(stage=stage, job_id=j, station=s, start_h=t, end_h=t+oc.true_dur(inst,j), boundary=boundary) for stage,plan in [('before',initial),('after',real)] for j,(s,t) in plan.items()])
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    log.to_csv(out/'decision_log.csv', index=False); frame.to_csv(out/'ledger.csv', index=False); schedule.to_csv(out/'schedule.csv', index=False)
    summary = dict(instance=inst['instance_id'], boundary=boundary, profile='DS05 measured traces, assumed scaling and timing' if v2 else 'synthetic assumed recipe and power', forecast='P3' if engine else 'P0', comparisons=rows, approvals=int(log.accepted.sum()), rejections=int((~log.accepted).sum()), production_errors=production_errors(inst, real), screening_failures=checks, note='Single instance; no confidence interval or statistical claim. Energy comparisons require equal tardiness. Twin uses assumed parameters and is not protection.')
    (out/'summary.json').write_text(json.dumps(summary, indent=2, default=str), encoding='utf-8')
    if report:
        write_report(summary, report)
    return summary


def write_report(summary, report):
    rows = summary['comparisons']
    columns = ['method', 'net_kwh', 'peak_import_kw', 'TT_h', 'completed_jobs', 'violations']
    lines = ['# Offline demonstrator', '', 'Boundary: ' + summary['boundary'] + '; ' + summary['profile'] + '.', '',
             'Single instance; no confidence interval. Compare energy only at equal tardiness. The twin uses assumed parameters and is not protection.', '',
             '| ' + ' | '.join(columns) + ' |', '| ' + ' | '.join(['---'] * len(columns)) + ' |']
    lines += ['| ' + ' | '.join(str(row.get(k, 'unavailable')) for k in columns) + ' |' for row in rows]
    by_method = {r['method']: r for r in rows}
    for baseline in ('B1', 'B1p-OPT'):
        if baseline in by_method:
            lines.append(f"\n{baseline} minus pipeline net kWh: {by_method[baseline]['net_kwh'] - by_method['pipeline']['net_kwh']}; check tardiness above.")
    lines += ['', f"Approvals: {summary['approvals']}; rejections: {summary['rejections']}.",
              '', 'Production violations: ' + str(summary['production_errors']), '', 'Screening: ' + str(summary['screening_failures'])]
    path = Path(report); path.parent.mkdir(parents=True, exist_ok=True); path.write_text('\n'.join(lines) + '\n', encoding='utf-8')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--instance'); ap.add_argument('--proc'); ap.add_argument('--models'); ap.add_argument('--split', default='test'); ap.add_argument('--seed', type=int, default=0); ap.add_argument('--n-jobs', type=int, default=10); ap.add_argument('--time-limit', type=float, default=2); ap.add_argument('--report', nargs='?', const='reports/run3/demonstrator.md'); args=ap.parse_args()
    if args.proc:
        from regenate.data.bench_v2 import load_proc, make_instance
        inst=make_instance(*load_proc(args.proc), args.seed, n_jobs=args.n_jobs, split=args.split)
    else:
        manifest=json.loads((oc.BENCH/'manifest.json').read_text()); inst=oc.load(args.instance or manifest['instances'][0])
    out=Path('runs/run3/demo')/inst['instance_id']; run(inst,out,models=args.models,time_limit=args.time_limit,report=args.report); print(f"{out} [{inst.get('meta', {}).get('boundary', 'SIM_ASSUMED_PROFILE')}]")
if __name__ == '__main__': main()


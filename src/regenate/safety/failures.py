"""Failure-injection campaign on the assumed-profile benchmark."""
import json
import time
from pathlib import Path

from regenate.data.generator import fifo_schedule, render
from regenate.electrical.ledger import ElecParams, ledger
from regenate.evaluation.oracle_campaign import load, score, true_dur
from regenate.optimization.rolling import Replanner
from regenate.simulation.bus_twin import check_plan
from regenate.simulation.replay import Replay

IDS = [f'n010_tau{tau}_r00_S3_0' for tau in ('02', '05', '08')]
CASES = ('forecast_wrong', 'sensor_loss', 'mes_disconnect', 'afe_saturation',
         'bus_overvoltage', 'test_delay', 'engineer_reject', 'solver_timeout', 'replanner_exception')


def run_case(case, iid):
    inst = load(iid)
    assign, starts = fifo_schedule(inst)
    initial = {j: (assign[j], starts[j]) for j in assign}
    observed, approvals = [], []
    base = Replanner(inst, mode='P0', flex=0.25, time_limit=10)
    events, approve, limit = [], None, 60
    def capture(obs):
        observed.append(obs)
        return base(obs)
    replanner = capture
    if case == 'forecast_wrong':
        original = base.predict
        base.predict = lambda j, obs: tuple(x * 1.5 for x in original(j, obs))
    elif case == 'sensor_loss':
        events = [(0, 'sensor_loss', {'station': next(iter(assign.values())), 'duration_h': 2})]
    elif case == 'mes_disconnect':
        events = [(0, 'mes_disconnect', {'duration_h': 2})]
    elif case == 'test_delay':
        job = min(starts, key=starts.get)
        events = [(0, 'delay', {'job_id': job, 'duration_h': 2})]
        def approve(old, new, obs):
            frozen = set(obs['running']) | set(obs['done'])
            approvals.append({'frozen_unchanged': all(new[j] == old[j] for j in frozen),
                              'frozen_count': len(frozen),
                              'other_queued_changed': any(new[j] != old[j] for j in obs['queued'] if j != job)})
            return True
    elif case == 'afe_saturation':
        def approve(old, new, obs):
            a = {j: v[0] for j, v in new.items()}
            st = {j: v[1] for j, v in new.items()}
            violations = ledger(*render(inst, a, st, inst['dt_h'], truth=True), inst['dt_h'],
                                'DC', ElecParams(P_afe_max=0.01))['afe_violation_steps']
            approvals.append(int(violations))
            return violations == 0
    elif case == 'engineer_reject':
        approve = lambda *_: False
    elif case == 'solver_timeout':
        def replanner(obs):
            time.sleep(2)
            return {}
        limit = 0.5
    elif case == 'replanner_exception':
        def replanner(obs):
            raise RuntimeError('injected failure')
    elif case == 'bus_overvoltage':
        replanner = None
    replay = Replay(inst, initial, replanner, period_h=2, approve=approve, events=events, max_solve_s=limit)
    realised, log = replay.run()
    a = {j: v[0] for j, v in realised.items()}
    st = {j: v[1] for j, v in realised.items()}
    prm = ElecParams(P_afe_max=0.01) if case == 'afe_saturation' else ElecParams()
    totals = ledger(*render(inst, a, st, inst['dt_h'], truth=True), inst['dt_h'], 'DC', prm)
    summary, schedule = score(inst, case, 'DC', a, st, inst['dt_h'], prm)
    no_overlap = all(x['end_h'] <= y['start_h'] + 1e-9 for s in set(a.values())
                     for x, y in zip(sorted((r for r in schedule if r['station'] == s), key=lambda r: r['start_h']),
                                     sorted((r for r in schedule if r['station'] == s), key=lambda r: r['start_h'])[1:]))
    reasons = log.reason.fillna('').tolist()
    details = {'no_overlap': no_overlap, 'deadline_violations': summary['violations'],
               'afe_violation_steps': int(totals['afe_violation_steps'])}
    if case == 'forecast_wrong':
        ok = no_overlap and bool(observed)
    elif case == 'sensor_loss':
        ok = any(o['stations'][events[0][2]['station']]['stale'] for o in observed) and 'sensor_loss' in log.event.tolist()
    elif case == 'mes_disconnect':
        window = log[(log.event == 'replan') & (log.t_h < 2)]
        ok = len(window) > 0 and not window.accepted.any() and all(window.reason == 'mes_disconnect')
    elif case == 'afe_saturation':
        details['candidate_afe_violation_steps'] = approvals
        details['validator_rejected'] = bool(approvals and max(approvals) > 0 and 'engineer_reject' in reasons)
        ok = details['validator_rejected'] and replay.plan == initial
    elif case == 'bus_overvoltage':
        twin = check_plan([[100, 100]], [[0, 0]], 1)
        details['twin'] = twin
        ok = not twin['approved'] and any(v[1] == 'overvoltage' for v in twin['violations'])
    elif case == 'test_delay':
        ok = (st[job] >= 2 and no_overlap and any(x['other_queued_changed'] for x in approvals)
              and any(x['frozen_count'] for x in approvals) and all(x['frozen_unchanged'] for x in approvals))
        details['delayed_job'] = job
        details['approval_checks'] = approvals
        details['replans_accepted'] = int(((log.event == 'replan') & log.accepted).sum())
    elif case == 'engineer_reject':
        ok = 'engineer_reject' in reasons and all(sorted((j for j in a if a[j] == s), key=st.get) == sorted((j for j in assign if assign[j] == s), key=starts.get) for s in set(assign.values()))
    elif case == 'solver_timeout':
        ok = any('TimeoutError' in x for x in reasons) and replay.plan == initial
    else:
        ok = any('RuntimeError' in x for x in reasons) and replay.plan == initial
    return {'instance': iid, 'pass': bool(ok), 'details': details, 'decision_log': log.to_dict('records'),
            'realised_plan': schedule, 'ledger_totals': totals}


def run_campaign(out=Path('runs/fail_v1')):
    out.mkdir(parents=True, exist_ok=True)
    results = {}
    for case in CASES:
        rows = [run_case(case, iid) for iid in IDS]
        results[case] = rows
        (out / f'{case}.json').write_text(json.dumps({'boundary': 'SIM_ASSUMED_PROFILE', 'profile': 'bench_v1 S3 assumed/derived recipe', 'cases': rows}, indent=2, default=lambda x: x.tolist() if hasattr(x, 'tolist') else str(x)), encoding='utf-8')
    return results




def run_v2_cases(inst, out=Path('runs/run3/fail')):
    """Exercise synthetic bench-v2 fallback paths and persist observed evidence."""
    import numpy as np
    from regenate.data.bench_v2 import fifo, job_profile, render_traces
    from regenate.forecasting.ai_engine import make_profile_fn

    out.mkdir(parents=True, exist_ok=True)
    a, s = fifo(inst)
    initial = {j: (a[j], s[j]) for j in a}
    results = {}

    def replay(replanner, approve=None):
        r = Replay(inst, initial, replanner, period_h=0.25, approve=approve, max_solve_s=5)
        realised, log = r.run()
        return r, realised, log

    def metrics(plan):
        aa = {j: v[0] for j, v in plan.items()}
        ss = {j: v[1] for j, v in plan.items()}
        return ledger(*render_traces(inst, aa, ss, inst['dt_h'], True), inst['dt_h'], 'DC', ElecParams())

    def no_overlap(plan):
        for station in set(v[0] for v in plan.values()):
            jobs = sorted((j for j in plan if plan[j][0] == station), key=lambda j: plan[j][1])
            if any(plan[x][1] + true_dur(inst, x) > plan[y][1] + 1e-9 for x, y in zip(jobs, jobs[1:])):
                return False
        return True

    def fail(_):
        raise TimeoutError('injected solver timeout')
    r, actual, log = replay(fail)
    reasons = log.reason.fillna('').tolist()
    results['solver_timeout'] = dict(pass_=r.plan == initial and set(actual) == set(initial) and no_overlap(actual)
                                    and any('TimeoutError' in x for x in reasons),
                                    plan_kept=r.plan == initial, all_jobs=set(actual) == set(initial),
                                    no_overlap=no_overlap(actual), decision_log=log.to_dict('records'))

    class Stub:
        def __init__(self, mode): self.mode = mode
        def predict(self, *args):
            if self.mode == 'exception': raise RuntimeError('injected AI failure')
            q = np.array([np.nan, np.nan, np.nan])
            return dict(prediction_valid=self.mode == 'nan', sink_power={h: q for h in (1, 4, 16)},
                        source_power={h: q for h in (1, 4, 16)}, remaining_duration=np.array([45., 45., 45.]))

    jid = next(iter(initial)); obs = {'elapsed_h': 1.0}
    nominal = job_profile(inst, jid, inst['dt_h'], 'nominal')
    def equal_profile(p): return all(np.array_equal(x, y) for x, y in zip(p, nominal))
    p0 = Replanner(inst, mode='P0', profile_fn=make_profile_fn(inst, 'P0'), time_limit=5)
    _, p0_plan, _ = replay(p0)
    outcomes = {}
    for mode in ('invalid', 'exception'):
        fn = make_profile_fn(inst, 'P1', Stub(mode))
        _, plan, logs = replay(Replanner(inst, mode='P1', profile_fn=fn, time_limit=5))
        outcomes[mode] = dict(nominal_profile=equal_profile(fn(jid, obs)), schedule_equals_p0=plan == p0_plan,
                              decision_log=logs.to_dict('records'))
    results['ai_invalid'] = dict(pass_=all(x['nominal_profile'] and x['schedule_equals_p0'] for x in outcomes.values()), outcomes=outcomes)
    nan_profile = make_profile_fn(inst, 'P1', Stub('nan'))(jid, obs)
    finite = all(np.isfinite(x).all() for x in nan_profile)
    results['ai_nan'] = dict(pass_=finite and equal_profile(nan_profile), finite=finite,
                             nominal_profile=equal_profile(nan_profile),
                             history='NaN fallback issue found by R3_FAIL; guard fixed by lead')

    base_metrics = metrics(initial)
    r, realised, log = replay(Replanner(inst, mode='P0', profile_fn=make_profile_fn(inst, 'P0'), time_limit=5), lambda *_: False)
    actual_metrics = metrics(realised)
    same = all(np.allclose(actual_metrics[k], base_metrics[k], equal_nan=True) for k in base_metrics
               if isinstance(base_metrics[k], (int, float, np.number, np.ndarray)))
    results['engineer_reject_all'] = dict(pass_=r.plan == initial and realised == initial and same
                                         and 'engineer_reject' in log.reason.tolist(),
                                         initial_plan_executed=realised == initial, kpis_equal_fifo_dc=same,
                                         fifo_dc=base_metrics, realised_dc=actual_metrics, decision_log=log.to_dict('records'))
    for case, row in results.items():
        row['pass'] = bool(row.pop('pass_'))
        (out / (case + '.json')).write_text(json.dumps(dict(boundary='SIM_ASSUMED_PROFILE', profile='synthetic bench-v2', **row),
             indent=2, default=lambda x: x.tolist() if hasattr(x, 'tolist') else str(x)), encoding='utf-8')
    return results

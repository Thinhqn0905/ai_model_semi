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


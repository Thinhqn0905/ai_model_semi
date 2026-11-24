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
    observed = []
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
    elif case == 'engineer_reject':
        approve = lambda *_: False
    elif case == 'solver_timeout':
        def replanner(obs):
            time.sleep(0.002)
            return {}
        limit = 0.001
    elif case == 'replanner_exception':
        def replanner(obs):
            raise RuntimeError('injected failure')
    elif case in ('afe_saturation', 'bus_overvoltage'):
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
        ok = totals['afe_violation_steps'] > 0
        details['validator_rejected'] = bool(ok)
    elif case == 'bus_overvoltage':
        twin = check_plan([[100, 100]], [[0, 0]], 1)
        details['twin'] = twin
        ok = not twin['approved'] and any(v[1] == 'overvoltage' for v in twin['violations'])
    elif case == 'test_delay':
        ok = st[job] >= 2 and bool(observed) and no_overlap
        details['delayed_job'] = job
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


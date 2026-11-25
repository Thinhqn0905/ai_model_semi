from regenate.app.pipeline import production_errors
from regenate.evaluation.oracle_campaign import load
from regenate.data.generator import fifo_schedule
import json
from pathlib import Path

def test_fifo_production_validation():
    manifest = json.loads(Path('data/generated/bench_v1/manifest.json').read_text())
    inst = load(manifest['instances'][0])
    a, t = fifo_schedule(inst)
    plan = {j: (a[j], t[j]) for j in a}
    assert not production_errors(inst, plan)
    j = next(iter(plan)); plan[j] = (a[j], -1)
    assert production_errors(inst, plan)

def test_rejection_fallback_and_ledger(tmp_path, monkeypatch):
    import numpy as np
    import pandas as pd
    from types import SimpleNamespace
    from regenate.app import pipeline
    from regenate.data.generator import render
    from regenate.electrical.ledger import ledger
    manifest = json.loads(Path('data/generated/bench_v1/manifest.json').read_text())
    inst = load(manifest['instances'][0])
    inst['jobs'] = inst['jobs'].iloc[:1].copy()
    a, t = fifo_schedule(inst)
    jid = next(iter(a))
    class Proposal:
        def __init__(self, *args, **kwargs): pass
        def __call__(self, obs):
            return {jid: (a[jid], t[jid] + inst['dt_h'])} if jid in obs['queued'] else {}
    monkeypatch.setattr(pipeline, 'Replanner', Proposal)
    monkeypatch.setattr(pipeline, 'check_plan', lambda *a, **k: {'approved': True})
    monkeypatch.setattr(pipeline, 'solve', lambda *a, **k: SimpleNamespace(starts=None))
    summary = pipeline.run(inst, tmp_path, reject=range(1, 10000))
    schedule = pd.read_csv(tmp_path/'schedule.csv')
    before = schedule[schedule.stage == 'before'].iloc[0]
    after = schedule[schedule.stage == 'after'].iloc[0]
    assert after.start_h == before.start_h and after.station == before.station
    decisions = pd.read_csv(tmp_path/'decision_log.csv')
    assert len(decisions) and not decisions.accepted.any()
    actual = pd.read_csv(tmp_path/'ledger.csv')
    expected = ledger(*render(inst, a, t, inst['dt_h']), inst['dt_h'], 'DC')
    assert np.isclose(actual.p_import.sum() * inst['dt_h'], expected['import_kwh'])
    assert np.isclose(actual.p_export.sum() * inst['dt_h'], expected['export_kwh'])
    assert summary['rejections'] == len(decisions)

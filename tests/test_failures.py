from regenate.safety.failures import run_campaign


def test_failure_campaign():
    results = run_campaign()
    failures = [(case, row['instance'], row['details']) for case, rows in results.items() for row in rows if not row['pass']]
    assert not failures, failures



def test_failure_v2():
    from regenate.data.bench_v2 import make_instance
    from regenate.safety.failures import run_v2_cases
    from test_v2_campaign import synth
    cyc, arrs = synth()
    inst = make_instance(cyc, arrs, 0, n_jobs=4, n_stations=2, split="train")
    results = run_v2_cases(inst)
    assert all(results[k]['pass'] for k in ('solver_timeout', 'ai_invalid', 'engineer_reject_all')), results
    # An inconsistent validity flag must still trigger the nominal fallback.
    assert results['ai_nan']['pass'], results['ai_nan']

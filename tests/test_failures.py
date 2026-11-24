from regenate.safety.failures import run_campaign


def test_failure_campaign():
    results = run_campaign()
    failures = [(case, row['instance'], row['details']) for case, rows in results.items() for row in rows if not row['pass']]
    assert not failures, failures

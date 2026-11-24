import json
from pathlib import Path
import pandas as pd
from app.dashboard import append_decision, kpis, paired_difference
from regenate.evaluation.mock_results import make_mock_campaign, RESULT_COLUMNS, SCHEDULE_COLUMNS, TIME_COLUMNS

def test_mock_schema(tmp_path):
    make_mock_campaign(tmp_path, 7)
    result = pd.read_csv(tmp_path / 'results.csv')
    assert result.columns.tolist() == RESULT_COLUMNS
    assert set(result.boundary) == {'MOCK'}
    assert pd.read_parquet(tmp_path / 'schedules.parquet').columns.tolist() == SCHEDULE_COLUMNS
    assert pd.read_parquet(tmp_path / 'timeseries.parquet').columns.tolist() == TIME_COLUMNS
    assert {'config', 'code_hash_sha256', 'command', 'timestamps'} <= json.loads((tmp_path / 'manifest.json').read_text()).keys()

def test_kpis_and_paired_ci():
    rows = []
    for method, energy in [('B1', 10), ('P0', 8), ('P', 6), ('ORACLE', 5)]:
        rows.append(dict(instance_id='one', method=method, net_kwh=energy, peak_import_kw=3, direct_reuse_kwh=2, recoverable_kwh=4, violations=0))
    frame = pd.DataFrame(rows)
    values = kpis(frame)
    assert values['incremental kWh vs B1'] == 4
    assert values['dE_AI (P0 − P)'] == 2
    assert values['oracle gap (P − ORACLE)'] == 1
    assert values['R_match'] == .5
    assert paired_difference(frame, 'B1', 'P') == (4, 4, 4)

def test_decision_append(tmp_path):
    append_decision(tmp_path, 'i', 'P', 'Reject', 'Needs review')
    append_decision(tmp_path, 'i', 'P', 'Approve', 'Reviewed')
    log = pd.read_csv(tmp_path / 'decision_log.csv')
    assert list(log.decision) == ['Reject', 'Approve']
    assert list(log.columns) == ['timestamp', 'instance', 'method', 'decision', 'reason']


def test_dashboard_pages(tmp_path):
    from streamlit.testing.v1 import AppTest

    make_mock_campaign(tmp_path, 7)
    at = AppTest.from_file(Path("app/dashboard.py").resolve(), default_timeout=30).run()
    at.sidebar.text_input[0].set_value(str(tmp_path)).run()
    for page in ('Overview', 'Baseline ladder', 'Schedule', 'Energy',
                 'Engineer approval', 'Finance'):
        at.sidebar.radio[0].set_value(page).run()
        assert not at.exception, (page, list(at.exception))
        assert any('MOCK' in warning.value for warning in at.warning)


def test_dashboard_missing_proposals(tmp_path):
    from streamlit.testing.v1 import AppTest

    make_mock_campaign(tmp_path, 7)
    results = pd.read_csv(tmp_path / 'results.csv')
    results = results[~results.method.isin(['P', 'P0'])]
    results['boundary'] = 'SIM_ASSUMED_PROFILE'
    results.to_csv(tmp_path / 'results.csv', index=False)
    at = AppTest.from_file(Path("app/dashboard.py").resolve(), default_timeout=30).run()
    at.sidebar.text_input[0].set_value(str(tmp_path)).run()
    for page in ('Overview', 'Baseline ladder', 'Schedule', 'Energy',
                 'Engineer approval', 'Finance'):
        at.sidebar.radio[0].set_value(page).run()
        assert not at.exception, (page, list(at.exception))
        assert any('Not available yet' in item.value for item in at.info)


def test_oracle_campaign_if_present():
    from pathlib import Path
    from streamlit.testing.v1 import AppTest
    import pytest

    campaign = Path('runs/oracle_v1')
    if not (campaign / 'results.csv').exists():
        pytest.skip('oracle campaign not present')
    at = AppTest.from_file(Path('app/dashboard.py').resolve(), default_timeout=30).run()
    at.sidebar.text_input[0].set_value(str(campaign)).run()
    for page in ('Overview', 'Baseline ladder', 'Schedule', 'Energy',
                 'Engineer approval', 'Finance'):
        at.sidebar.radio[0].set_value(page).run()
        assert not at.exception, (page, list(at.exception))
        assert any('SIM_ASSUMED_PROFILE' in warning.value for warning in at.warning)

import json
from pathlib import Path

import numpy as np
import pandas as pd

from regenate.evaluation import oracle_campaign as oracle
from regenate.evaluation.rolling_campaign import campaign


def test_tiny_campaign(tmp_path):
    original = Path('data/generated/bench_v1')
    manifest = json.loads((original / 'manifest.json').read_text())
    iid = next(i for i in manifest['instances'] if i[1:4] == '010' and i.split('_')[3] == 'S1')
    bench = tmp_path / 'bench'; target = bench / iid; target.mkdir(parents=True)
    for name in ('jobs', 'stations', 'recipes'):
        frame = pd.read_parquet(original / iid / (name + '.parquet'))
        if name == 'jobs': frame = frame.iloc[:1]
        frame.to_parquet(target / (name + '.parquet'), index=False)
    (bench / 'manifest.json').write_text(json.dumps(dict(config=manifest['config'], instances=[iid], splits={'test': [iid]})))
    rows, _ = oracle.run_instance((iid, .25, .25, {}, 10, str(bench)))
    baseline = tmp_path / 'baseline.csv'; pd.DataFrame(rows).to_csv(baseline, index=False)
    out = tmp_path / 'out'; report = tmp_path / 'report.md'
    campaign(bench, baseline, out, report, [iid], workers=1)
    results = pd.read_csv(out / 'results.csv'); ladder = pd.read_csv(out / 'ladder.csv')
    schedule = pd.read_parquet(out / 'schedules.parquet'); ts = pd.read_parquet(out / 'timeseries.parquet')
    assert set(results.method) == {'P0', 'P'} and len(ladder) == 10
    assert {'n_replans', 'n_rejected', 'flex', 'boundary', 'split'} <= set(results)
    assert {'shift_h', 'start_h', 'end_h'} <= set(schedule)
    assert {'p_import_kw', 'p_export_kw', 'direct_kw', 'recoverable_kw'} <= set(ts)
    for row in results.itertuples():
        trace = ts[ts.method == row.method]
        assert np.isclose(trace.p_import_kw.sum() * .25, row.import_kwh)
        assert np.isclose(trace.direct_kw.sum() * .25, row.direct_reuse_kwh)
    assert 'SIM_ASSUMED_PROFILE' in report.read_text(encoding='utf-8')

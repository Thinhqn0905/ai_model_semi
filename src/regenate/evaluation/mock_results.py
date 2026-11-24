"""Deterministic synthetic campaign for offline dashboard development."""
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

METHODS = ['B0', 'B1', 'B1-OPT', 'B1p', 'B1p-OPT', 'B2', 'B3', 'P0', 'P', 'ORACLE']
RESULT_COLUMNS = 'instance_id scenario n_jobs n_stations seed split method topology TT_h makespan_h completed_jobs violations import_kwh export_kwh net_kwh peak_import_kw direct_reuse_kwh self_use_kwh recoverable_kwh dump_kwh loss_kwh solve_s mip_gap boundary'.split()
SCHEDULE_COLUMNS = 'instance_id method job_id station start_h end_h shift_h'.split()
TIME_COLUMNS = 'instance_id method t_h p_import_kw p_export_kw direct_kw self_use_kw recoverable_kw dump_kw'.split()

def make_mock_campaign(out_dir, seed=0):
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    results, schedules, series = [], [], []
    for i in range(4):
        instance = f'mock-{i:02d}'
        for j, method in enumerate(METHODS):
            powers = 10 + rng.random(8) - j * .2
            direct = np.full(8, j * .1)
            for t, p in enumerate(powers):
                series.append([instance, method, float(t), p, 0., direct[t], 0., 2., 0.])
            for job in range(4):
                shift = 0. if method in ('B0', 'B1', 'B2', 'B3') else (job % 2) * .25
                schedules.append([instance, method, str(job), job % 2, float(job) + shift, float(job + 2) + shift, shift])
            results.append([instance, 'synthetic', 4, 2, seed, 'mock', method, 'mock', 0., 5.25, 4, 0, powers.sum(), 0., powers.sum(), powers.max(), direct.sum(), 0., 16., 0., 0., 0., None, 'MOCK'])
    pd.DataFrame(results, columns=RESULT_COLUMNS).to_csv(out / 'results.csv', index=False)
    pd.DataFrame(schedules, columns=SCHEDULE_COLUMNS).to_parquet(out / 'schedules.parquet', index=False)
    pd.DataFrame(series, columns=TIME_COLUMNS).to_parquet(out / 'timeseries.parquet', index=False)
    digest = hashlib.sha256()
    for path in sorted(Path('src').rglob('*.py')):
        digest.update(path.as_posix().encode()); digest.update(path.read_bytes())
    from datetime import datetime, timezone
    (out / 'manifest.json').write_text(json.dumps({'config': {'seed': seed, 'boundary': 'MOCK'}, 'code_hash_sha256': digest.hexdigest(), 'command': f'make_mock_campaign({str(out)!r}, {seed})', 'timestamps': {'created_utc': datetime.now(timezone.utc).isoformat()}}, indent=2), encoding='utf-8')
    return out

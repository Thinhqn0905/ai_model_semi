from pathlib import Path
import json
import pandas as pd
from regenate.visualization.run4_figs import main


def test_facility_figure_and_missing_inputs(tmp_path):
    root = tmp_path / 'runs'
    path = root / 'run4/fac_grid_tnb/facility_md.csv'
    path.parent.mkdir(parents=True)
    pd.DataFrame([{'facility': 'A', 'month': '2020-01', 'method': 'P0',
                   'cell_peak_kw': 3, 'md_increment_kw': 1,
                   'boundary': 'SIM_DATA_PROFILE'}]).to_csv(path, index=False)
    out = tmp_path / 'figures'
    main(['--runs', str(root), '--out', str(out)])
    for ext in ('png', 'pdf', 'svg', 'json'):
        assert (out / f'F27.{ext}').is_file()
    provenance = json.loads((out / 'F27.json').read_text(encoding='utf-8'))
    assert provenance['boundary'] == 'SIM_DATA_PROFILE'
    assert len(provenance['inputs'][0]['sha256']) == 64
    index = (out / 'INDEX.md').read_text(encoding='utf-8')
    assert 'F17: BLOCKED' in index and 'metrics_T1.csv' in index
    assert 'F27: GENERATED' in index


def test_missing_boundary_fails_closed_and_clears_stale_output(tmp_path):
    p = tmp_path / 'run4/fac_grid_tnb/facility_md.csv'
    p.parent.mkdir(parents=True)
    pd.DataFrame([{'facility': 'A', 'month': '2020-01', 'method': 'P0', 'cell_peak_kw': 2, 'md_increment_kw': 1}]).to_csv(p, index=False)
    out = tmp_path / 'out'; out.mkdir()
    (out / 'F27.png').write_text('stale')
    main(['--runs', str(tmp_path), '--out', str(out)])
    assert not (out / 'F27.png').exists()
    assert 'F27: BLOCKED' in (out / 'INDEX.md').read_text(encoding='utf-8')


def test_f24_pairs_only_within_campaigns(tmp_path):
    root = tmp_path / 'runs'
    root.mkdir()
    methods = ['B0', 'B1', 'B1p-OPT', 'B2', 'B3', 'P0']
    rows = [dict(instance_id=i, method=m, net_kwh=10-j, TT_h=0,
                 boundary='SIM_DATA_PROFILE')
            for i in range(2) for j, m in enumerate(methods)]
    pd.DataFrame(rows).to_csv(root / 'v2_flex025_n100.csv', index=False)
    for campaign, value, peak in [('v2_e1', 5, False), ('v2_e1_peak', 4.9, True)]:
        folder = root / 'run3' / campaign
        folder.mkdir(parents=True)
        pd.DataFrame([dict(instance_id=i, method='P0', net_kwh=value, TT_h=0,
                           boundary='SIM_DATA_PROFILE') for i in range(2)]).to_csv(folder / 'results.csv', index=False)
        (folder / 'manifest.json').write_text(json.dumps({'args': {'flex': 0.25, 'peak': peak}}))
    out = tmp_path / 'out'
    main(['--runs', str(root), '--out', str(out)])
    assert all((out / f'F24.{ext}').is_file() for ext in ('png', 'pdf', 'svg', 'json'))
    provenance = json.loads((out / 'F24.json').read_text(encoding='utf-8'))
    assert len(provenance['inputs']) == 5
    assert provenance['boundary'] == 'SIM_DATA_PROFILE'
    assert 'F24: GENERATED' in (out / 'INDEX.md').read_text(encoding='utf-8')


def test_f24_rejects_nonfinite_campaign_values(tmp_path):
    root = tmp_path / 'runs'
    root.mkdir()
    methods = ['B0', 'B1', 'B1p-OPT', 'B2', 'B3', 'P0']
    pd.DataFrame([dict(instance_id=i, method=m, net_kwh=float('inf') if m == 'B0' else 5,
                       TT_h=0, boundary='SIM_DATA_PROFILE')
                  for i in range(2) for m in methods]).to_csv(root / 'v2_flex025_n100.csv', index=False)
    for campaign in ('v2_e1', 'v2_e1_peak'):
        folder = root / 'run3' / campaign
        folder.mkdir(parents=True)
        pd.DataFrame([dict(instance_id=i, method='P0', net_kwh=5, TT_h=0,
                           boundary='SIM_DATA_PROFILE') for i in range(2)]).to_csv(folder / 'results.csv', index=False)
        (folder / 'manifest.json').write_text(json.dumps({'args': {'flex': 0.25}}))
    out = tmp_path / 'out'
    main(['--runs', str(root), '--out', str(out)])
    assert 'F24: BLOCKED' in (out / 'INDEX.md').read_text(encoding='utf-8')
    assert not (out / 'F24.png').exists()

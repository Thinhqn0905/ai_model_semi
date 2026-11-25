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
    assert 'F17: BLOCKED' in index and 'predictions_T1.parquet' in index
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


def test_real_eta_screen_finance_and_facility_schemas(tmp_path, capsys):
    from regenate.visualization.run4_figs import generate
    import matplotlib.pyplot as plt
    root = tmp_path
    def csv(rel, rows):
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(rows).to_csv(p, index=False)
    eta = dict(use_case='ALL', subset='ALL', progress='0-25', model='q', n=3,
               mae=2, rmse=3, skill_vs_previous=0, median_ape=0, pinball=1,
               coverage80=.8, width80=4, predict_ms=1, boundary='SIM_DATA_PROFILE')
    csv('run4/eta/metrics_T2.csv', [eta])
    screen = dict(run='v2_diag', instance_id='x', method='P0', afe_kw=20, link_a=80,
                  approved=True, v_min=380, v_max=420, i_peak=10, kinds='',
                  peak_sink_kw=2, peak_src_kw=2, max_step_kw=1)
    csv('run3/screen_e1.csv', [screen])
    csv('run4_rt3/screen_sizing_summary.csv', [dict(afe_kw=20, bus_kw=10, method='P0', n=1, approved=1, kinds='')])
    csv('run3/fin_v3_ds06.csv', [dict(annual_net_usd=5, break_even_capex_usd=10, payback_years=2, option='A', method='P0', set='S', dc_usd_kw_month=1, boundary='SIM_DATA_PROFILE')])
    csv('run4/fin_fac_gen_fx0.21/clustered_summary.csv', [dict(option='A', n_cells=1, annual_net_usd=5, ceiling_3y=10, ceiling_5y=20, ceiling_10y_discounted=30, tariff='gen')])
    facility = dict(facility='A', month='2020-01', method='P0@v2_e1_peak', md_window=15, n_cells=1, block_h=1, n_blocks=1, md_bg_kw=10, md_kw=11, md_increment_kw=1, md_time='t', bg_md_time='t', cell_kwh=1, cell_peak_kw=2, coverage=1, boundary='SIM_DATA_PROFILE')
    csv('run4/fac_grid_tnb/facility_md.csv', [facility])
    csv('run4/fac_p0bill_x/facility_md.csv', [facility, dict(facility, method='P0-BILL:hist@etol0.02')])
    csv('run4/fac_aibill_x/facility_md.csv', [facility, dict(facility, method='P0-BILL:ai@etol0.02')])
    for n in (18, 22, 25, 26, 30, 32):
        fig, boundary, paths = generate(n, root)
        assert boundary == 'SIM_DATA_PROFILE'
        assert all(path.is_file() for path in paths)
        plt.close(fig)
    assert 'deduplicated' in capsys.readouterr().out


def test_real_t1_parquet_schema(tmp_path):
    import pytest
    from regenate.visualization.run4_figs import generate
    pytest.importorskip('pyarrow')
    p = tmp_path / 'run4/eta/predictions_T1.parquet'
    p.parent.mkdir(parents=True)
    pd.DataFrame([dict(cycle_file='a', use_case='x', true=2, model='quantile_lightgbm_cqr', q10=1, q50=2, q90=3)]).to_parquet(p)
    fig, b, paths = generate(17, tmp_path)
    assert b == 'NOT_VERIFIED' and paths == [p]
    import matplotlib.pyplot as plt
    plt.close(fig)

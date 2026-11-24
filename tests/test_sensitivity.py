from pathlib import Path
import pandas as pd
import pytest
from regenate.evaluation.sensitivity import aggregate, points


def test_aggregate_paired_results():
    tmp_path = Path("runs/sens_v1/test_fixture"); tmp_path.mkdir(parents=True, exist_ok=True)
    rows = []
    for iid, b, oracle in [('a', 10., 8.), ('b', 20., 19.)]:
        for method, energy in [('B1-OPT', b+1), ('B1p-OPT', b), ('ORACLE', oracle)]:
            rows.append(dict(instance_id=iid, scenario='S3', method=method, net_kwh=energy, peak_import_kw=energy/2, TT_h=0, completed_jobs=10, violations=0, mip_gap=0, direct_reuse_kwh=2, recoverable_kwh=4))
    path = tmp_path/'results.csv'; pd.DataFrame(rows).to_csv(path, index=False)
    r = aggregate(path, 'flex', '1', 'S3')
    assert r['n'] == 2 and r['gain_kwh_mean'] == pytest.approx(1.5)
    assert r['gain_pct_mean'] == pytest.approx(12.5)
    assert r['b1_gain_kwh_mean'] == pytest.approx(2.5)
    assert r['r_match_mean'] == pytest.approx(.5)
    assert r['share_gain_positive'] == 1
    rows[0]['TT_h'] = 1
    pd.DataFrame(rows).to_csv(path, index=False)
    with pytest.raises(ValueError, match='unequal tardiness'): aggregate(path, 'flex', '1', 'S3')


def test_point_coverage():
    assert len(points()) == 35



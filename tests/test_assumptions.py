from dataclasses import fields

from regenate.electrical.ledger import ElecParams
from regenate.evaluation.assumptions import collect


def test_register_contract():
    df = collect()
    assert set(df.provenance) <= {'MEASURED', 'DATASHEET', 'DERIVED', 'SYNTHETIC', 'ASSUMED'}
    assert df.notna().all().all()
    assert not df.duplicated(['module', 'name']).any()
    assert {f.name for f in fields(ElecParams)} <= set(df.loc[df.module == 'electrical.ledger', 'name'])
    assert {'data.recipes', 'configs.bench_v1', 'configs.economics_v1'} <= set(df.module)

import pandas as pd
from regenate.data.ds02 import OUT, load_dataset


def test_schema_units_and_source_semantics():
    for name in 'ABC':
        df = load_dataset(name)
        assert {'dataset', 'ts', 'v_bus', 'i_bus', 'p_kw', 'state', 'provenance'} <= set(df.columns)
        assert df.ts.is_monotonic_increasing and str(df.ts.dtype).endswith('UTC]')
        assert df.v_bus.between(300, 800).all()
        assert (df.provenance == 'MEASURED').all()
        if name in 'AB':
            assert df.i_bus.isna().all() and df.p_kw.isna().all()
        else:
            assert df.i_bus.notna().all() and (df.p_kw >= 0).all()
            assert (df.p_kw - (df.v_bus * df.i_bus / 1000).abs()).abs().median() < 0.05


def test_parquet_exists_and_schema():
    assert OUT.exists()
    df = pd.read_parquet(OUT, columns=['dataset', 'provenance'])
    assert set(df.dataset) == set('ABC') and set(df.provenance) == {'MEASURED'}

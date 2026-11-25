import numpy as np
from regenate.forecasting.xbench import collect, skill, MAPPING

def test_skill():
    assert skill(2, 4) == .5
    assert np.isnan(skill(2, np.nan)) and np.isnan(skill(2, 0))

def test_existing_mapping_and_boundaries():
    df=collect()
    assert set(df.legacy_model) <= set(MAPPING)
    assert df.model_id.notna().all()
    assert df.loc[(df.dataset=='DS05') & (df.task=='duration'),'skill_vs_persistence'].isna().all()
    assert df.loc[df.dataset.str.startswith('DS02'),'skill_vs_domain_baseline'].isna().all()
    assert set(df.loc[df.dataset=='DS02-A','horizon_min']) == {1/6,1,5}

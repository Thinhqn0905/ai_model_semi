import io, zipfile
import pandas as pd
from regenate.data.ds07 import load_factory, gaps, monthly_summary

def test_factory_gap_outlier_and_summary(tmp_path):
    ts=pd.date_range('2019-03-01',periods=61,freq='min').delete(35)
    power=[1.0]*len(ts); power[10]=100; power[11]=0
    raw=pd.DataFrame({'Time':ts.astype(str),'Power consumption':power}).to_csv(index=False)
    z=tmp_path/'data.zip'
    with zipfile.ZipFile(z,'w') as f: f.writestr('Data_list/Factories/Paper.csv',raw)
    d=load_factory(z,'Paper'); g=gaps(d); s=monthly_summary(d).iloc[0]
    assert g.iloc[0].minutes == 1 and g.iloc[0].start == pd.Timestamp('2019-03-01 00:35')
    assert d.iloc[10].data_quality_flag == 'outlier' and d.iloc[11].data_quality_flag == 'zero'
    assert s.coverage_percent == 100*60/(31*24*60)
    assert abs(s.max_30min_kw - (128/30)) < 1e-10
    assert s.max_30min_timestamp == pd.Timestamp('2019-03-01')

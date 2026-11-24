import numpy as np
import pandas as pd
from regenate.forecasting.framework import WindowSpec,windows
from regenate.forecasting.metrics import mae,rmse,pinball,interval_coverage
from regenate.forecasting.tcn import TCN

def test_windows_causal_and_split():
    f=pd.DataFrame({'group':['a']*12+['b']*12,'ts':list(pd.date_range('2020',periods=12,freq='10s'))*2,'y':range(24),'split':(['train']*7+['test']*5)*2})
    pairs=list(windows(f,WindowSpec(3,2,10)))
    assert pairs
    for features,target in pairs:
        assert f.loc[features,'ts'].max()<f.loc[target,'ts']
        assert (f.loc[features,'split']==f.loc[target,'split']).all()
        assert (f.loc[features,'group']==f.loc[target,'group']).all()

def test_metrics_hand():
    assert mae([1,3],[2,1])==1.5
    assert np.isclose(rmse([1,3],[2,1]),np.sqrt(2.5))
    assert pinball([1,3],[2,1],.5)==.75
    assert interval_coverage([1,3],[0,0],[2,2])==.5

def test_tcn_tiny_sine():
    x=np.sin(np.arange(180)*.15); X=np.array([x[i:i+8] for i in range(150)]); y=x[8:158]
    m=TCN(epochs=100,patience=20).fit(X,y,X,y)
    assert np.mean(np.abs(m.predict(X)['p50']-y)) < .15

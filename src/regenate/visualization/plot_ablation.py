import numpy as np
import matplotlib.pyplot as plt
from .common import save

def f08(df,out):
    keys=[c for c in ('instance_id','flex') if c in df.columns]; baseline=df[df.method=='B1']; rows=[]; rng=np.random.default_rng(0)
    for method,g in df.groupby('method'):
        paired=baseline.merge(g,on=keys,suffixes=('_base','_method')); d=(paired.net_kwh_base-paired.net_kwh_method).dropna().to_numpy()
        if len(d):
            means=rng.choice(d,size=(10000,len(d)),replace=True).mean(axis=1); lo,hi=np.quantile(means,[.025,.975]); rows.append((method,d.mean(),lo,hi))
    fig,ax=plt.subplots(); y=np.arange(len(rows)); vals=np.array([r[1] for r in rows]); ax.barh(y,vals); ax.errorbar(vals,y,xerr=np.array([[r[1]-r[2] for r in rows],[r[3]-r[1] for r in rows]]),fmt='none',color='black',capsize=3); ax.set_yticks(y,[r[0] for r in rows]); ax.set_xlabel('Paired net grid savings vs B1 (kWh)'); save(fig,df,out)

def f09(df,out):
    fig,ax=plt.subplots(); ax.bar(df['variant'],df['value']); ax.set_ylabel('Ablation metric'); save(fig,df,out)

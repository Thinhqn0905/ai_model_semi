from pathlib import Path
import numpy as np
import pandas as pd
from .framework import WindowSpec, windows, run_benchmark, report
from .models import REGISTRY
ROOT=Path(__file__).resolve().parents[3]
def main():
    d=pd.read_parquet(ROOT/'data/processed/ds02_bus.parquet'); tasks=[]
    for dataset,part in d.groupby('dataset'):
        col='p_kw' if dataset=='C' else 'infeed_p_kw'
        part=part.assign(ts=pd.to_datetime(part.ts).dt.ceil('10s')).groupby('ts',as_index=False)[col].mean().dropna(); part['group']=dataset; part['y']=part[col]
        n=len(part); part['split']=np.where(np.arange(n)<int(.7*n),'train',np.where(np.arange(n)<int(.85*n),'val','test'))
        for h in (1,6,30):
            pairs=list(windows(part,WindowSpec(4,h,10))); X=np.array([part.loc[a,'y'].to_numpy() for a,b in pairs]); idx=np.array([b for a,b in pairs])
            tasks.append(dict(dataset=dataset,task='power',horizon=h,X=X,y=part.loc[idx,'y'],split=part.loc[idx,'split'],group=part.loc[idx,'group'],t=part.loc[idx,'ts']))
    out=ROOT/'runs/ai/ds02'; run_benchmark(tasks,REGISTRY,out); report(out,ROOT/'reports/ai/branch_A_ds02.md','SHIFT2DC LVDC traces are not semiconductor test-cell or energy-saving evidence. Right-closed 10-second means, chronological 70/15/15 split, exact contiguous windows.')
if __name__=='__main__': main()

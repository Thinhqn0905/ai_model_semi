from pathlib import Path
import numpy as np
import pandas as pd
from .framework import run_benchmark,report
from .models import REGISTRY
from .ds04_bench import features
ROOT=Path(__file__).resolve().parents[3]
def main():
    d=pd.read_parquet(ROOT/'data/processed/ds04_machines.parquet',columns=['company','asset','ts','status','power_kw','split']); tasks=[]
    for company,cadence in [('A','5min'),('B','1min')]:
        for h in (1,6,12):
            f=features(d[d.company==company],cadence,h)
            X=f[['power_kw_lag3','power_kw_lag2','power_kw_lag1','lag1']].to_numpy()
            tasks.append(dict(dataset=company,task='power',horizon=h,X=X,y=f.y,split=f.split,group=f.asset,t=f.target_ts))
    out=ROOT/'runs/ai/ds04'; run_benchmark(tasks,REGISTRY,out); report(out,ROOT/'reports/ai/branch_B_ds04.md','DS04 manufacturing machines are not semiconductor test cells. Company A uses 5-minute and B 1-minute bins, stored split, exact future slot, and uncorrected extreme values. Features are four completed power bins; other DS04 baseline features are excluded for common model input.')
if __name__=='__main__': main()

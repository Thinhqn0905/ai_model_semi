"""Standardise existing forecasting results; no model fitting."""
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
MAPPING = {'M0':'AI01','M1':'AI03','M2':'AI04','M3':'AI05','M4':'AI06','M5':'AI10','M6':'AI11', 'F01':'AI00','F02':'AI03','F03':'AI04','F04':'AI06','F05':'AI10', 'AI00_prev_cycle':'AI00','AI01_persistence':'AI01','AI02_uc_median':'AI02','AI03_ridge':'AI03','AI04_rf':'AI04','AI05_xgb':'AI05','AI10_lgbm_quantile':'AI10'}
IDS = ['AI00','AI01','AI02','AI03','AI04','AI05','AI06','AI10','AI11']

def skill(mae, baseline):
    return 1 - mae / baseline if pd.notna(baseline) and baseline > 0 and pd.notna(mae) else np.nan

def collect(root=ROOT):
    root=Path(root); rows=[]
    for branch in ('ds02','ds04'):
        path=f'runs/ai/{branch}/model_metrics.csv'; df=pd.read_csv(root/path)
        runtime=pd.read_csv(root/f'runs/ai/{branch}/runtime_metrics.csv')
        df=df.merge(runtime[['dataset','task','model','horizon','predict_ms_per_sample']],on=['dataset','task','model','horizon'],validate='one_to_one')
        for _, r in df.iterrows():
            # Stored skill uses last observation, whereas M0 P50 includes median residual.
            rows.append(dict(dataset=f'{branch.upper()}-{r.dataset}',task=r.task,target='power',horizon_min=r.horizon*(1/6 if branch=='ds02' else (5 if r.dataset=='A' else 1)),model_id=MAPPING[r.model],legacy_model=r.model,MAE=r.mae,RMSE=r.rmse,NMAE=r.nmae,skill_vs_persistence=r.skill_vs_persistence,skill_vs_domain_baseline=np.nan,persistence_reason='',domain_reason='domain baseline absent on this split',coverage80=r.coverage80,width80=np.nan,latency_ms=r.predict_ms_per_sample,source_file=path,split_id=path))
    path='runs/forecast_ds04/results.csv'; df=pd.read_csv(root/path)
    for _,r in df.iterrows():
        base=df[(df.company==r.company)&(df.horizon==r.horizon)&(df.model=='F01')].mae
        rows.append(dict(dataset=f'DS04-{r.company} legacy',task='power',target='power',horizon_min=r.horizon*(5 if r.company=='A' else 1),model_id=MAPPING[r.model],legacy_model=r.model,MAE=r.mae,RMSE=r.rmse,NMAE=r.nmae,skill_vs_persistence=np.nan,skill_vs_domain_baseline=skill(r.mae,base.iloc[0] if len(base)==1 else np.nan),persistence_reason='persistence absent on this split',domain_reason='' if len(base)==1 and base.iloc[0]>0 else 'domain baseline absent or zero',coverage80=r.coverage80,width80=np.nan,latency_ms=np.nan,source_file=path,split_id=path))
    path='results/ai_ds05_branchC/model_metrics.csv'; df=pd.read_csv(root/path)
    for _,r in df.iterrows():
        group=df[df.target==r.target]; p=group[group.model=='AI01_persistence'].mae; d=group[group.model=='AI00_prev_cycle'].mae
        is_duration=r.target=='y_rem_min'; h=np.nan if is_duration else int(r.target.split('_h')[1])*15
        rows.append(dict(dataset='DS05',task='duration' if is_duration else 'power',target=r.target.split('_h')[0],horizon_min=h,model_id=MAPPING[r.model],legacy_model=r.model,MAE=r.mae,RMSE=r.rmse,NMAE=r.nmae,skill_vs_persistence=skill(r.mae,p.iloc[0] if len(p)==1 else np.nan),skill_vs_domain_baseline=skill(r.mae,d.iloc[0] if len(d)==1 else np.nan),persistence_reason='' if len(p)==1 and p.iloc[0]>0 else 'persistence absent or zero on this split',domain_reason='' if len(d)==1 and d.iloc[0]>0 else 'domain baseline absent or zero on this split',coverage80=r.coverage80,width80=np.nan,latency_ms=np.nan,source_file=path,split_id=path))
    return pd.DataFrame(rows)

def main():
    from regenate.visualization.plot_cross_dataset import f04_v3
    out=ROOT/'runs/run3/xbench'; out.mkdir(parents=True,exist_ok=True)
    df=collect(); df.to_csv(out/'metrics.csv',index=False)
    fig=ROOT/'reports/run3/figures/F04_v3'; fig.parent.mkdir(parents=True,exist_ok=True)
    f04_v3(df,fig)
    (fig.parent/'F04_v3.provenance.json').write_text(json.dumps({'boundary':'LOCAL_RUN; source observations MEASURED; metrics DERIVED','sources':sorted(df.source_file.unique().tolist()),'output_table':'runs/run3/xbench/metrics.csv','command':'python -m regenate.forecasting.xbench','reruns':[]},indent=2),encoding='utf8')
if __name__=='__main__': main()

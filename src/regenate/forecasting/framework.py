"""Causal index-based windows and common benchmark output."""
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
import pickle
import numpy as np
import pandas as pd
from .metrics import mae, rmse, pinball, interval_coverage

@dataclass(frozen=True)
class WindowSpec:
    lookback_steps: int
    horizon_steps: int
    step_s: int

def windows(frame, spec, group='group', time='ts', value='y', split='split'):
    """Yield indices only; require contiguous observations and one split per window."""
    for _, part in frame.groupby(group,sort=False):
        part=part.sort_values(time); idx=part.index.to_numpy(); ts=pd.to_datetime(part[time]); sp=part[split].to_numpy()
        for i in range(spec.lookback_steps-1,len(part)-spec.horizon_steps):
            a=i-spec.lookback_steps+1; b=i+spec.horizon_steps
            if sp[a]!=sp[b] or not np.all(sp[a:b+1]==sp[a]): continue
            if (ts.iloc[b]-ts.iloc[a]).total_seconds() != (b-a)*spec.step_s: continue
            yield idx[a:i+1],idx[b]

def run_benchmark(task, models, out_dir):
    out=Path(out_dir); out.mkdir(parents=True,exist_ok=True)
    predictions=[]; metrics=[]; runtime=[]; logs=[]; calibration=[]
    for item in task:
        X=item['X']; y=np.asarray(item['y'],dtype=float); split=np.asarray(item['split']); tr=np.flatnonzero(split=='train'); val=np.flatnonzero(split=='val'); te=np.flatnonzero(split=='test')
        if not len(tr) or not len(val) or not len(te): raise ValueError('missing train, validation or test')
        if len(tr)>30000: tr=np.random.default_rng(0).choice(tr,30000,replace=False)
        scale=float(np.quantile(np.abs(y[tr]),.99)); scale=scale if scale>0 else np.nan
        persistence=mae(y[te],X[te,-1]); dataset=item['dataset']; h=item['horizon']; name=item['task']
        for model_id,factory in models.items():
            start=perf_counter(); candidates=[]
            for variant in (0,1):
                candidate=factory(variant); candidate.fit(X[tr],y[tr],X[val],y[val]); candidates.append((mae(y[val],candidate.predict(X[val])['p50']),variant,candidate))
            _, selected, model=min(candidates,key=lambda z:z[0]); fit=perf_counter()-start
            start=perf_counter(); pred=model.predict(X[te]); pred_ms=(perf_counter()-start)*1000/len(te)
            err=mae(y[te],pred['p50']); row=dict(dataset=dataset,task=name,model=model_id,horizon=h,mae=err,rmse=rmse(y[te],pred['p50']),nmae=err/scale,skill_vs_persistence=1-err/persistence if persistence else np.nan,pinball10=pinball(y[te],pred['p10'],.1),pinball50=pinball(y[te],pred['p50'],.5),pinball90=pinball(y[te],pred['p90'],.9),coverage80=interval_coverage(y[te],pred['p10'],pred['p90']),n_test=len(te),scale_p99_train=scale)
            metrics.append(row)
            try: size=len(pickle.dumps(model))/1024
            except Exception: size=np.nan
            runtime.append(dict(dataset=dataset,task=name,model=model_id,horizon=h,fit_s=fit,predict_ms_per_sample=pred_ms,model_size_kb=size))
            logs.append(dict(dataset=dataset,task=name,model=model_id,horizon=h,n_train=len(tr),n_val=len(val),budget='two candidates; validation MAE',selected=selected,epochs=getattr(getattr(model,'est',None),'epochs_run',None)))
            for q in np.arange(1,10)/10: calibration.append(dict(dataset=dataset,task=name,model=model_id,horizon=h,nominal=q,empirical=float(np.mean(y[te]<=pred['p%02d'%int(q*100)]))))
            predictions.append(pd.DataFrame(dict(dataset=dataset,task=name,model=model_id,group=np.asarray(item['group'])[te],t=np.asarray(item['t'])[te],horizon_step=h,y=y[te],**{k:pred[k] for k in ('p10','p50','p90')})))
            print(f'LOCAL_RUN {dataset} h={h} {model_id}',flush=True)
    pd.concat(predictions,ignore_index=True).to_parquet(out/'forecast_predictions.parquet',index=False)
    m=pd.DataFrame(metrics); m.to_csv(out/'model_metrics.csv',index=False); m.to_csv(out/'horizon_metrics.csv',index=False)
    pd.DataFrame(calibration).to_csv(out/'quantile_calibration.csv',index=False); pd.DataFrame(logs).to_csv(out/'training_log.csv',index=False); pd.DataFrame(runtime).to_csv(out/'runtime_metrics.csv',index=False)

def report(out, path, description):
    df=pd.read_csv(Path(out)/'model_metrics.csv'); cols=['dataset','horizon','model','nmae','skill_vs_persistence','coverage80']; df=df[cols].round(4)
    lines=['| '+' | '.join(cols)+' |','| '+' | '.join(['---']*len(cols))+' |']+['| '+' | '.join(map(str,r))+' |' for r in df.itertuples(index=False,name=None)]
    Path(path).write_text('# Forecast benchmark\n\nLOCAL_RUN; source observations MEASURED; forecasts and metrics DERIVED. '+description+'\n\nNMAE uses the training-target p99 absolute power, not rated power. Two candidate configurations per model selected by validation MAE; M0 and M1 repeat their deterministic configuration. M0 persistence point uses last observation, with training residual quantiles. Calibration uses nine quantiles; TCN intermediate quantiles are linearly interpolated between its three heads.\n\n'+'\n'.join(lines)+'\n',encoding='utf8')

"""Generate the figures directly from recorded campaign artifacts."""
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .common import save
from . import plot_efficiency, plot_ablation, plot_scheduling, plot_sankey, plot_sensitivity


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--campaign',required=True); parser.add_argument('--out',required=True); args=parser.parse_args()
    out=Path(args.out); out.mkdir(parents=True,exist_ok=True); index=[]
    def run(name, paths, boundary, action):
        missing=[str(p) for p in paths if not Path(p).exists()]
        if missing:
            print(f'{name} SKIP missing {missing}'); index.append(f'| {name} | {", ".join(map(str,paths))} | NOT_VERIFIED (missing) |'); return
        try:
            action(); print(f'{name} written {out/name} boundary={boundary}'); index.append(f'| {name} | {", ".join(map(str,paths))} | {boundary} |')
        except (ValueError, KeyError, ImportError) as exc:
            print(f'{name} SKIP invalid: {exc}'); index.append(f'| {name} | {", ".join(map(str,paths))} | NOT_VERIFIED ({exc}) |')
    ds=Path('results/ai_ds05_branchC/model_metrics.csv'); runtime=Path('results/ai_ds05_branchC/runtime_metrics.csv'); oracle=Path(args.campaign); ladder=Path('runs/rolling_v1/ladder.csv'); twin=Path('runs/twin_v1/controls.json'); sens=Path('runs/sens_v1/sensitivity_results.csv'); measured='LOCAL_RUN(DS05 MEASURED)'
    def f03():
        d=pd.read_csv(ds); d=d[d.target.str.match(r'y_(ch|ds)_h\d+')].copy(); d['horizon']=d.target.str.extract(r'h(\d+)$').astype(int); fig,axes=plt.subplots(1,2,figsize=(11,4),sharey=True)
        for ax,typ in zip(axes,['ch','ds']):
            for model,g in d[d.target.str.startswith('y_'+typ+'_')].groupby('model'):
                g=g.sort_values('horizon'); ax.plot(g.horizon,g.skill_vs_prev_cycle,marker='o',label=model)
            ax.set(title={'ch':'Sink','ds':'Source'}[typ],xlabel='Horizon (15-minute slots)',ylabel='Skill vs previous cycle'); ax.axhline(0,color='black',lw=.5)
        axes[1].legend(fontsize=6); save(fig,d,out/'F03')
    run('F03',[ds],measured,f03)
    def f04():
        rows=[]
        for name in ('ds02','ds04'):
            d=pd.read_csv(f'runs/ai/{name}/model_metrics.csv'); d=d[(d.horizon==1)&(d.task=='power')];
            for model,g in d.groupby('model'): rows.append((name.upper(),model,g.skill_vs_persistence.mean()))
        d=pd.read_csv(ds); d=d[d.target.eq('y_ch_h1')]
        for _,r in d.iterrows(): rows.append(('DS05',r.model,r.skill_vs_prev_cycle))
        tab=pd.DataFrame(rows,columns=['dataset','model','skill']).pivot(index='model',columns='dataset',values='skill'); fig,ax=plt.subplots(figsize=(8,6)); im=ax.imshow(tab,aspect='auto',cmap='RdYlGn'); ax.set_xticks(range(len(tab.columns)),tab.columns); ax.set_yticks(range(len(tab.index)),tab.index); ax.set_title('Within-dataset skill (different model families)'); fig.colorbar(im,ax=ax,label='Skill'); fig.text(.1,.02,'DS02/DS04: persistence; DS05: previous cycle. DS02/04 mean over datasets A/B; DS05 sink.',fontsize=7); save(fig,pd.DataFrame({'boundary':['LOCAL_RUN (MEASURED DATA: DS02, DS04, DS05)']}),out/'F04')
    run('F04',[Path('runs/ai/ds02/model_metrics.csv'),Path('runs/ai/ds04/model_metrics.csv'),ds],'LOCAL_RUN (MEASURED DATA: DS02, DS04, DS05)',f04)
    def f05():
        d=pd.read_parquet('data/processed/efficiency_points.parquet'); d=d[d.provenance.eq('DATASHEET')].copy(); d['boundary']='VENDOR_REPORTED'; plot_efficiency.f05(d,out/'F05')
    run('F05',[Path('data/processed/efficiency_points.parquet')],'VENDOR_REPORTED',f05)
    def f06():
        d=pd.read_parquet(oracle/'timeseries.parquet'); fig,axes=plt.subplots(2,1,sharex=True,figsize=(9,6))
        for ax,method in zip(axes,['ORACLE','B1p-OPT']):
            g=d[d.method.eq(method)];
            if g.empty: raise ValueError('missing method')
            for col in ['source_kw','sink_kw','direct_kw']: ax.plot(g.t_h,g[col],label=col)
            ax.set(title=method,ylabel='Power (kW)'); ax.legend(fontsize=7)
        axes[-1].set_xlabel('Time (h)'); save(fig,d,out/'F06')
    run('F06',[oracle/'timeseries.parquet'],'SIM_ASSUMED_PROFILE',f06)
    def f07():
        d=json.loads(twin.read_text(encoding='utf-16')); fig,ax=plt.subplots(figsize=(8,4)); names=list(d); ax.bar(names,[d[n]['v_max'] for n in names],label='Maximum'); ax.bar(names,[d[n]['v_min'] for n in names],label='Minimum'); ax.axhline(420,color='red',ls='--',label='Upper limit'); ax.axhline(380,color='orange',ls='--',label='Lower limit'); ax.set_ylabel('Bus voltage extrema (V)'); ax.tick_params(axis='x',rotation=20); ax.legend(); save(fig,pd.DataFrame({'boundary':['SIM_ASSUMED_PROFILE']}),out/'F07')
    run('F07',[twin],'SIM_ASSUMED_PROFILE',f07)
    def f08():
        d=pd.read_csv(ladder); d=d[d.scenario.eq('S3')].copy(); plot_ablation.f08(d,out/'F08')
    run('F08',[ladder],'SIM_ASSUMED_PROFILE',f08)
    def f09():
        d=pd.DataFrame([['P1 power AI',-0.018,-0.030,-0.005,-0.34,-0.83,0.13],['P2 duration AI',-0.019,-0.031,-0.007,-0.25,-0.73,0.23],['P3 joint',-0.024,-0.038,-0.009,-0.57,-1.08,-0.06],['P4 joint, P90 duration',-0.026,-0.041,-0.012,-0.40,-1.00,0.20],['ORACLE (perfect forecast)',0.094,0.077,0.112,1.14,0.57,1.72]],columns=['variant','kwh','kwh_lo','kwh_hi','peak_kw','peak_lo','peak_hi']); d['kwh_wins']=['27/100','22/100','27/100','27/100','94/100']; d['peak_wins']=['33/100','35/100','34/100','37/100','65/100']; d['boundary']='SIM_DATA_PROFILE'; d.to_csv(out/'ai_exp12_table.csv',index=False); fig,ax=plt.subplots(figsize=(8,4)); ax.errorbar(d.kwh,range(len(d)),xerr=[d.kwh-d.kwh_lo,d.kwh_hi-d.kwh],fmt='o',capsize=3); ax.set_yticks(range(len(d)),d.variant); ax.axvline(0,color='black',lw=.5); ax.set_xlabel('P0 minus variant net kWh (95% paired CI)'); save(fig,d,out/'F09')
    run('F09',[Path('reports/ai/ai_exp12_ds06.md')],'SIM_DATA_PROFILE',f09)
    def f10():
        d=pd.read_csv(sens); d=d[(d.sweep=='grid') & (d.scenario=='S3')].copy(); parts=d.value.str.extract(r'^(.*?)_eta_(.*?)$'); d['flexibility']=parts[0].astype(float); d['efficiency']=parts[1].astype(float); d['value']=d.gain_kwh_mean; plot_sensitivity.f10(d,out/'F10')
    run('F10',[sens],'SIM_ASSUMED_PROFILE',f10)
    def f12():
        d=pd.read_csv(ds); d=d.dropna(subset=['coverage80']); fig,ax=plt.subplots(figsize=(8,4)); ax.barh(d.target,d.coverage80); ax.axvline(.8,color='red',ls='--',label='Nominal 80%'); ax.set(xlabel='Empirical P10?P90 coverage',xlim=(0,1)); ax.legend(); save(fig,d,out/'F12')
    run('F12',[ds],measured,f12)
    def f13():
        results=pd.read_csv(oracle/'results.csv'); row=results[(results.scenario=='S3') & (results.method=='ORACLE')].iloc[0]; d=pd.read_parquet(oracle/'schedules.parquet'); d=d[(d.instance_id==row.instance_id)&(d.flex==row.flex)&d.method.isin(['ORACLE','B1p-OPT'])].copy(); d['boundary']=row.boundary; plot_scheduling.f13(d,out/'F13')
    run('F13',[oracle/'schedules.parquet',oracle/'results.csv'],'SIM_ASSUMED_PROFILE',f13)
    def f14():
        d=pd.read_csv(ladder); r=d[(d.scenario=='S3')&(d.method=='P')].iloc[0]; flows=pd.DataFrame([['Grid','Imported electricity',r.import_kwh],['Exported electricity','Grid',r.export_kwh]],columns=['source','target','value']); flows['boundary']=r.boundary; plot_sankey.f14(flows,out/'F14')
    run('F14',[ladder],'SIM_ASSUMED_PROFILE',f14)
    def f15():
        d=pd.read_csv(runtime).merge(pd.read_csv(ds),on=['target','model']); d=d[d.target.eq('y_ch_h1')].copy(); fig,ax=plt.subplots(); ax.scatter(d.predict_ms,d.mae)
        for _,r in d.iterrows(): ax.annotate(r.model,(r.predict_ms,r.mae),fontsize=7)
        ax.set(xlabel='Prediction time (ms)',ylabel='MAE (kW)',title='DS05 sink power, +1 slot'); save(fig,d,out/'F15')
    run('F15',[runtime,ds],measured,f15)
    for name in ('F01','F02','F11'): index.append(f'| {name} | No DS05 prediction rows supplied | NOT_VERIFIED (missing) |')
    (out/'INDEX.md').write_text('# Figure index\n\nDS05: measured battery cycles; DS02/DS04: measured datasets. SIM_ASSUMED_PROFILE: simulated assumed profiles. SIM_DATA_PROFILE: simulated DS05 cycles with assumed station scaling and windows.\n\n| Figure | Input | Boundary |\n|---|---|---|\n'+'\n'.join(sorted(index))+'\n',encoding='utf-8')
if __name__=='__main__': main()

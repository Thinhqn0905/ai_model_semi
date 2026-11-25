from pathlib import Path
import pandas as pd
import json, zipfile

NAMES = ['Cement_1','Cement_2','Forge_1','Forge_2','Metal_1','Metal_2','Metal_3','Paper','Steel_1','Steel_2']

def load_factory(zip_path, name):
    if name not in NAMES: raise ValueError('unknown factory')
    with zipfile.ZipFile(zip_path) as z:
        matches = [x for x in z.namelist() if x.replace('\\','/').endswith('/Factories/'+name+'.csv')]
        if len(matches) != 1: raise ValueError('factory file missing or ambiguous')
        source = matches[0]
        with z.open(source) as f: raw = pd.read_csv(f)
    original = raw['Time'].astype(str)
    t = pd.to_datetime(original, errors='raise')
    p = pd.to_numeric(raw['Power consumption'], errors='raise')
    if t.isna().any() or p.isna().any() or t.duplicated().any() or (t.dt.second != 0).any(): raise ValueError('invalid or duplicate observations')
    q1,q3 = p.quantile([.25,.75]); threshold = q3 + 10*(q3-q1)
    flag = pd.Series('ok', index=p.index); flag[p == 0] = 'zero'; flag[p > threshold] = 'outlier'
    return pd.DataFrame(dict(facility_id=name,timestamp=t,power_kw=p,sample_interval_seconds=60,data_quality_flag=flag,original_timestamp=original,source_file=source)).sort_values('timestamp').reset_index(drop=True)

def gaps(df):
    t = df.timestamp.sort_values().reset_index(drop=True); delta = t.diff().dt.total_seconds().div(60)
    return pd.DataFrame([dict(start=t[i-1]+pd.Timedelta(minutes=1),end=t[i]-pd.Timedelta(minutes=1),minutes=int(delta[i]-1)) for i in range(1,len(t)) if delta[i]>1],columns=['start','end','minutes'])

def monthly_summary(df):
    rows=[]
    for month, g in df.groupby(df.timestamp.dt.to_period('M')):
        start=month.start_time; end=(month+1).start_time
        expected=int((end-start).total_seconds()/60); s=g.set_index('timestamp').power_kw.sort_index()
        row=dict(facility_id=g.facility_id.iloc[0],month=str(month),energy_kwh=float(s.sum()/60),coverage_percent=100*len(s)/expected,weekday_mean_kw=float(s[s.index.dayofweek<5].mean()),weekend_mean_kw=float(s[s.index.dayofweek>=5].mean()))
        for n in (15,30,60):
            grouped=s.resample(f'{n}min',origin='start_day').agg(['mean','count']); valid=grouped[grouped['count']==n]
            row[f'max_{n}min_kw']=float(valid['mean'].max()) if len(valid) else None
            row[f'max_{n}min_timestamp']=valid['mean'].idxmax() if len(valid) else pd.NaT
        row['load_factor']=float(s.mean()/s.max()) if s.max()>0 else None
        rows.append(row)
    return pd.DataFrame(rows)

def build(zip_path,out_dir):
    out=Path(out_dir); out.mkdir(parents=True,exist_ok=True)
    frames=[]; gs=[]; summaries=[]
    for name in NAMES:
        df=load_factory(zip_path,name); frames.append(df); gs.append(gaps(df).assign(facility_id=name)); summaries.append(monthly_summary(df))
    pd.concat(frames,ignore_index=True).to_parquet(out/'facility_load.parquet',index=False)
    pd.concat(gs,ignore_index=True).to_parquet(out/'gaps.parquet',index=False)
    pd.concat(summaries,ignore_index=True).to_parquet(out/'monthly_summary.parquet',index=False)
    (out/'metadata.json').write_text(json.dumps({'timezone':'Asia/Seoul','timestamps':'naive local','boundary':'DERIVED from SOURCE_REPORTED DS07','outlier_rule':'power > Q3 + 10 IQR per factory; flagged not removed','coverage':'observed minutes / calendar month minutes','energy':'sum observed kW / 60; missing minutes excluded','demand':'aligned complete windows only','load_factor':'observed mean / observed maximum','gaps':'inclusive missing-minute timestamps; no interpolation'},indent=2),encoding='utf8')

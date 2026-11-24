import argparse
from pathlib import Path
import pandas as pd
from . import plot_forecasting as forecasting, plot_cross_dataset, plot_efficiency, plot_energy_matching, plot_bus_transients, plot_scheduling, plot_ablation, plot_sensitivity, plot_pareto, plot_sankey

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--campaign',required=True); parser.add_argument('--out',required=True); args=parser.parse_args(); campaign=Path(args.campaign); out=Path(args.out)
    def run(number, filename, fn, transform=None):
        path=campaign / filename
        if not path.exists(): print(f'{number} SKIP missing {path}'); return
        try:
            df=pd.read_parquet(path) if path.suffix=='.parquet' else pd.read_csv(path)
            if transform: df=transform(df)
            fn(df,out/number); print(f'{number} written {out/number} boundary={df.boundary.iloc[0]}')
        except (ValueError, KeyError, ImportError) as exc: print(f'{number} SKIP invalid input {path}: {exc}')
    run('F01','forecast_predictions.parquet',forecasting.f01)
    run('F02','forecast_predictions.parquet',forecasting.f02)
    run('F03','horizon_metrics.csv',forecasting.f03)
    run('F04','benchmark/results.csv',plot_cross_dataset.f04)
    p=Path('data/processed/efficiency_points.parquet')
    if p.exists():
        df=pd.read_parquet(p); df=df[df.provenance.eq('DATASHEET')].copy(); df['boundary']='VENDOR_REPORTED'; plot_efficiency.f05(df,out/'F05'); print(f'F05 written {out / "F05"} boundary=VENDOR_REPORTED')
    else: print(f'F05 SKIP missing {p}')
    run('F06','timeseries.parquet',plot_energy_matching.f06, lambda df: df[df.method.eq('ORACLE')].copy() if 'method' in df else df)
    run('F07','bus_transients.csv',plot_bus_transients.f07)
    run('F08','results.csv',plot_ablation.f08)
    run('F09','ablation_results.csv',plot_ablation.f09)
    run('F10','sensitivity_results.csv',plot_sensitivity.f10)
    run('F11','forecast_predictions.parquet',forecasting.f11)
    run('F12','quantile_calibration.csv',forecasting.f12)
    def schedule(df):
        results=pd.read_csv(campaign/'results.csv'); instance=results.instance_id.iloc[0]; selected=results[results.instance_id.eq(instance)]; flex=selected.flex.iloc[0] if 'flex' in selected else None
        if flex is not None: selected=selected[selected.flex.eq(flex)]; df=df[df.flex.eq(flex)]
        boundary=selected.boundary.dropna().unique()
        if len(boundary)!=1: raise ValueError('ambiguous schedule boundary')
        methods=[m for m in ('B1','ORACLE') if m in selected.method.values]; df=df[df.instance_id.eq(instance)&df.method.isin(methods)].copy()
        if len(methods)!=2 or df.empty: raise ValueError('B1 and ORACLE schedules required')
        df['boundary']=boundary[0]; return df
    run('F13','schedules.parquet',plot_scheduling.f13,schedule)
    run('F14','ledger_totals.csv',plot_sankey.f14)
    run('F15','runtime_metrics.csv',plot_pareto.f15)
if __name__=='__main__': main()


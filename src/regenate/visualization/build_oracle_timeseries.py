"""Reconstruct one campaign instance's plotted time series from saved schedules."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from regenate.data.generator import render
from regenate.evaluation.oracle_campaign import load, set_bench
from regenate.electrical.ledger import ledger, ElecParams


def main():
    campaign = Path('runs/oracle_v1')
    manifest = json.loads((campaign / 'manifest.json').read_text())
    set_bench(manifest['bench'])
    results = pd.read_csv(campaign / 'results.csv')
    schedules = pd.read_parquet(campaign / 'schedules.parquet')
    chosen = results[(results.scenario == 'S3') & (results.method == 'ORACLE')].iloc[0]
    iid, flex = chosen.instance_id, chosen.flex
    inst = load(iid)
    dt = manifest['args']['slot_h']
    prm = ElecParams(P_link_max=manifest['args']['P_link_max'], **json.loads(manifest['args'].get('prm', '{}')))
    frames = []
    for method, topology in [('ORACLE', 'DC'), ('B1p-OPT', 'B1p')]:
        sch = schedules[(schedules.instance_id == iid) & (schedules.flex == flex) & (schedules.method == method)]
        if sch.empty or sch.job_id.duplicated().any():
            raise ValueError('missing or duplicate schedule jobs')
        pin, prec, aux = render(inst, dict(zip(sch.job_id, sch.station)), dict(zip(sch.job_id, sch.start_h)), dt, truth=True)
        totals = ledger(pin, prec, aux, dt, topology, prm)
        row = results[(results.instance_id == iid) & (results.flex == flex) & (results.method == method)].iloc[0]
        if not np.isclose(totals['net_kwh'], row.net_kwh, atol=1e-7):
            raise ValueError('rendered ledger does not match campaign result')
        # B1p exposes residual station DC demand and source before any shared link.
        residual = ledger(pin, prec, aux, dt, 'B1p', prm)
        frames.append(pd.DataFrame(dict(instance_id=iid, flex=flex, method=method, t_h=np.arange(pin.shape[1])*dt,
            p_import_kw=totals['p_import'], p_export_kw=totals['p_export'], direct_kw=totals['direct'],
            self_use_kw=totals['self_use'], recoverable_kw=prec.sum(axis=0), dump_kw=totals['dump'],
            source_kw=residual['afe_exp_dc'] * prm.eta_link, sink_kw=residual['afe_imp_dc'],
            link_cap_kw=prm.P_link_max, boundary=row.boundary)))
    out = campaign / 'timeseries.parquet'
    pd.concat(frames, ignore_index=True).to_parquet(out, index=False)
    print(f'{out}: {iid}, flex={flex}, boundary={chosen.boundary}; ledger net verified')

if __name__ == '__main__':
    main()

"""Offline, evidence-labelled campaign viewer."""
from pathlib import Path
import sys
import os
from datetime import datetime, timezone
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from regenate.evaluation.mock_results import METHODS

TITLE = 'ReGenATE — Intelligent Energy Coordination for Regenerative Test Cells'
FOOTER = 'Offline functional demonstrator / shadow-mode emulator — not connected to a real MES'

def paired_difference(results, base, method, column='net_kwh'):
    pivot = results.pivot(index='instance_id', columns='method', values=column)
    if base not in pivot or method not in pivot:
        return None
    diff = (pivot[base] - pivot[method]).dropna().to_numpy()
    if not len(diff): return None
    rng = np.random.default_rng(0)
    means = rng.choice(diff, (10000, len(diff)), replace=True).mean(axis=1)
    return float(diff.mean()), *map(float, np.quantile(means, [.025, .975]))

def kpis(results):
    pivot = results.pivot(index='instance_id', columns='method', values='net_kwh')
    def diff(a, b):
        return (pivot[a] - pivot[b]).mean() if a in pivot and b in pivot else float('nan')
    p = results[results.method == 'P']
    rec = p.recoverable_kwh.sum()
    return {'incremental kWh vs B1': diff('B1', 'P'), 'peak kW': p.peak_import_kw.mean(), 'R_match': p.direct_reuse_kwh.sum() / rec if rec > 0 else float('nan'), 'dE_AI (P0 − P)': diff('P0', 'P'), 'oracle gap (P − ORACLE)': diff('P', 'ORACLE'), 'violations': p.violations.sum() if len(p) else float('nan')}

def append_decision(campaign, instance, method, decision, reason):
    if decision not in ('Approve', 'Reject') or not reason.strip(): raise ValueError('Decision and reason required')
    path = Path(campaign) / 'decision_log.csv'
    pd.DataFrame([{'timestamp': datetime.now(timezone.utc).isoformat(), 'instance': instance, 'method': method, 'decision': decision, 'reason': reason.strip()}]).to_csv(path, mode='a', header=not path.exists(), index=False)

def main():
    st.set_page_config(page_title='ReGenATE', layout='wide')
    st.title(TITLE)
    results_root = Path(os.environ.get('REGENATE_RESULTS', 'runs'))
    campaigns = sorted(p for p in results_root.glob('*') if p.is_dir() and ((p / 'ladder.csv').exists() or (p / 'results.csv').exists()))
    default = campaigns.index(Path('runs/rolling_v1')) if Path('runs/rolling_v1') in campaigns else 0
    selected = st.sidebar.selectbox('Campaign', campaigns, index=default, format_func=str) if campaigns else None
    override = st.sidebar.text_input('Campaign folder override', '')
    campaign = Path(override) if override else selected
    page = st.sidebar.radio('Page', ['Overview', 'Baseline ladder', 'Schedule', 'Energy', 'Engineer approval', 'Finance', 'AI forecasting', 'Pipeline run', 'Facility load', 'Tariff selector', 'Monthly bill', 'FIN comparison'])
    if page in ('Facility load', 'Tariff selector', 'Monthly bill', 'FIN comparison'):
        from regenate.app.facility_view import render
        render(page, results_root)
        st.caption(FOOTER)
        return
    if page == 'Pipeline run':
        import json
        runs = sorted(p for p in Path('runs/run3/demo').glob('*') if (p / 'summary.json').exists())
        if not runs:
            st.info('No pipeline runs available.')
        else:
            run = st.selectbox('Pipeline instance', runs, format_func=lambda p: p.name)
            summary = json.loads((run / 'summary.json').read_text(encoding='utf-8'))
            st.warning('Evidence boundary: ' + summary.get('boundary', 'NOT_VERIFIED'))
            st.write('Approvals', summary['approvals'], 'Rejections', summary['rejections'])
            for label, name in [('Decision log', 'decision_log.csv'), ('Schedule before and after', 'schedule.csv'), ('Ledger', 'ledger.csv')]:
                st.subheader(label); st.dataframe(pd.read_csv(run / name))
            st.json(summary)
        st.caption(FOOTER); return
    try:
        if campaign is None: raise ValueError('No campaign found')
        source = campaign / ('ladder.csv' if (campaign / 'ladder.csv').exists() else 'results.csv')
        results = pd.read_csv(source)
        schedules = pd.read_parquet(campaign / 'schedules.parquet') if (campaign / 'schedules.parquet').exists() else pd.DataFrame()
        ts = pd.read_parquet(campaign / 'timeseries.parquet') if (campaign / 'timeseries.parquet').exists() else pd.DataFrame()
    except (OSError, ValueError) as exc:
        st.error(f'Cannot load campaign: {exc}'); st.caption(FOOTER); return
    boundaries = results.boundary.fillna('NOT_VERIFIED').astype(str).unique()
    st.warning('Evidence boundary: ' + ', '.join(boundaries))
    if 'scenario' in results and results.scenario.notna().any():
        scenarios = sorted(results.scenario.dropna().unique())
        scenario = st.sidebar.selectbox('Scenario', scenarios, index=scenarios.index('S3') if 'S3' in scenarios else 0)
        results = results[results.scenario == scenario]
    if 'flex' in results and results.flex.nunique() > 1:
        flex = st.sidebar.selectbox('Flexibility', sorted(results.flex.dropna().unique()))
        results = results[results.flex == flex]
        if 'flex' in schedules: schedules = schedules[schedules.flex == flex]
        if 'flex' in ts: ts = ts[ts.flex == flex]
    instances = sorted(results.instance_id.unique())
    instance = st.sidebar.selectbox('Instance', instances)
    methods = [m for m in METHODS if m in results.method.unique()]
    missing = [m for m in ('P0', 'P') if m not in methods]
    if missing:
        st.info('Not available yet: ' + ', '.join(missing))
    if page == 'Overview':
        cols = st.columns(3)
        for i, (label, value) in enumerate(kpis(results).items()): cols[i % 3].metric(label, f'{value:.3f}' if pd.notna(value) else 'Unavailable')
        st.caption('Means over instances; R_match is total direct reuse / total recoverable. Compare energy only at equal tardiness.')
        st.dataframe(results[['instance_id', 'method', 'TT_h', 'makespan_h', 'completed_jobs', 'violations']])
    elif page == 'Baseline ladder':
        chart = results.groupby('method', as_index=False).net_kwh.mean()
        st.plotly_chart(px.bar(chart, x='method', y='net_kwh', category_orders={'method': METHODS}), use_container_width=True)
        rows = []
        for method in methods:
            val = paired_difference(results, 'B1', method)
            if val: rows.append({'method': method, 'B1 − method mean kWh': val[0], '95% CI lower': val[1], '95% CI upper': val[2]})
        st.dataframe(pd.DataFrame(rows)); st.caption('Paired bootstrap over matched instances; inspect TT before comparing energy.')
    elif page == 'Schedule':
        originals = [m for m in ('B3', 'B1') if m in methods]
        if not originals or not methods:
            st.info('Schedule comparison not available yet.')
            st.caption(FOOTER)
            return
        if schedules.empty:
            st.info('Schedule data not available yet.')
            st.caption(FOOTER)
            return
        if 'shift_h' not in schedules: schedules['shift_h'] = float('nan')
        original = st.selectbox('Original method', originals)
        proposed = st.selectbox('Proposed method', methods, index=methods.index('P') if 'P' in methods else 0)
        frame = schedules[(schedules.instance_id == instance) & schedules.method.isin([original, proposed])].copy()
        frame['duration_h'] = frame.end_h - frame.start_h
        st.plotly_chart(px.bar(frame, x='duration_h', y='job_id', base='start_h', color='method', facet_row='method', hover_data=['station', 'shift_h'], orientation='h', barmode='overlay'), use_container_width=True)
        st.dataframe(frame[['method', 'job_id', 'station', 'start_h', 'end_h', 'shift_h']])
    elif page == 'Energy':
        if ts.empty:
            st.info('Time series data not available yet.')
            st.caption(FOOTER)
            return
        selected = st.multiselect('Methods', methods, default=[m for m in ('B1', 'P') if m in methods])
        frame = ts[(ts.instance_id == instance) & ts.method.isin(selected)].melt(id_vars=['t_h', 'method'], value_vars=['p_import_kw', 'p_export_kw', 'direct_kw'], var_name='flow', value_name='kW')
        st.plotly_chart(px.line(frame, x='t_h', y='kW', color='flow', line_dash='method'), use_container_width=True)
    elif page == 'Engineer approval':
        method = st.selectbox('Proposed method', methods, index=methods.index('P') if 'P' in methods else 0)
        decision = st.radio('Decision', ['Approve', 'Reject']); reason = st.text_input('Reason')
        if st.button('Record decision'):
            try:
                append_decision(campaign, instance, method, decision, reason)
                st.success('Decision recorded. ' + ('Original plan remains active.' if decision == 'Reject' else 'Approval recorded for review.'))
            except ValueError as exc: st.error(str(exc))
        log = campaign / 'decision_log.csv'
        if log.exists(): st.dataframe(pd.read_csv(log))
    elif page == 'Finance':
        path = Path('runs/biz_v1/business_case.csv')
        if not path.exists():
            st.info('Business case data not available yet.')
        else:
            finance = pd.read_csv(path)
            st.warning('Finance evidence boundary: ' + ', '.join(finance.boundary.fillna('NOT_VERIFIED').astype(str).unique()))
            for column, label in [('alpha', 'Export credit fraction'), ('capex_factor', 'CAPEX factor'), ('demand_enabled', 'Demand charge enabled')]:
                options = sorted(finance[column].dropna().unique())
                choice = st.selectbox(label, options)
                finance = finance[finance[column] == choice]
            st.dataframe(finance)
            st.caption('Payback and NPV are taken directly from the business case CSV; blank payback means no value was recorded.')
    else:
        path = Path('results/ai_ds05_branchC/model_metrics.csv')
        if not path.exists():
            st.info('Forecast metrics not available yet.')
        else:
            metrics = pd.read_csv(path)
            st.warning('Forecast evidence boundary: ' + ', '.join(metrics.boundary.fillna('NOT_VERIFIED').astype(str).unique()))
            st.dataframe(metrics.pivot(index='target', columns='model', values='skill_vs_prev_cycle'))
            st.write('Coverage vs nominal 0.8')
            st.dataframe(metrics.loc[metrics.coverage80.notna(), ['target', 'model', 'coverage80']])
            st.caption('Forecast accuracy is not the energy claim; AI-EXP12 is a separate evaluation.')
    st.caption(FOOTER)

if __name__ == '__main__': main()

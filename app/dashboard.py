"""Offline, evidence-labelled campaign viewer."""
from pathlib import Path
import sys
from datetime import datetime, timezone
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from regenate.economics.model import incremental_case
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
    campaign = Path(st.sidebar.text_input('Campaign folder', 'runs/mock_dashboard'))
    page = st.sidebar.radio('Page', ['Overview', 'Baseline ladder', 'Schedule', 'Energy', 'Engineer approval', 'Finance'])
    try:
        results = pd.read_csv(campaign / 'results.csv')
        schedules = pd.read_parquet(campaign / 'schedules.parquet')
        ts = pd.read_parquet(campaign / 'timeseries.parquet')
    except (OSError, ValueError) as exc:
        st.error(f'Cannot load campaign: {exc}'); st.caption(FOOTER); return
    boundaries = results.boundary.fillna('NOT_VERIFIED').astype(str).unique()
    st.warning('Evidence boundary: ' + ', '.join(boundaries))
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
        original = st.selectbox('Original method', originals)
        proposed = st.selectbox('Proposed method', methods, index=methods.index('P') if 'P' in methods else 0)
        frame = schedules[(schedules.instance_id == instance) & schedules.method.isin([original, proposed])].copy()
        frame['duration_h'] = frame.end_h - frame.start_h
        st.plotly_chart(px.bar(frame, x='duration_h', y='job_id', base='start_h', color='method', facet_row='method', hover_data=['station', 'shift_h'], orientation='h', barmode='overlay'), use_container_width=True)
        st.dataframe(frame[['method', 'job_id', 'station', 'start_h', 'end_h', 'shift_h']])
    elif page == 'Energy':
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
    else:
        price = st.sidebar.number_input('Import price per kWh', min_value=0., value=0.1)
        alpha = st.sidebar.selectbox('Export credit fraction', [0., .5, 1.])
        hours = st.sidebar.number_input('Operating hours per year', min_value=0., value=4000.)
        capex = st.sidebar.number_input('Incremental CAPEX', min_value=0., value=10000.)
        opex = st.sidebar.number_input('Annual incremental OPEX', min_value=0., value=0.)
        method = st.selectbox('Proposed method', methods, index=methods.index('P') if 'P' in methods else 0)
        try:
            def run(m):
                x = ts[(ts.instance_id == instance) & (ts.method == m)].sort_values('t_h')
                t = x.t_h.to_numpy(); delta = np.diff(t)
                if len(t) < 2 or not np.allclose(delta, delta[0]) or delta[0] <= 0: raise ValueError('Time grid must be regular with at least two steps')
                return {'p_import': x.p_import_kw.to_numpy(), 'p_export': x.p_export_kw.to_numpy(), 'dt_h': float(delta[0]), 'times': list(t % 24)}
            cfg = {'tariff': {'import_price': dict.fromkeys(['off_peak', 'normal', 'peak'], price), 'alpha_ex': alpha}, 'operating_hours_per_year': hours, 'horizon_years': 10, 'discount_rate': 0.}
            case = incremental_case(run('B1'), run(method), capex, opex, cfg)
            st.metric('Annual saving (input currency)', f"{case['annual_saving']:.2f}")
            st.write('Payback: ' + (f"{case['simple_payback_y']:.2f} years" if case['simple_payback_y'] is not None else 'payback not reached'))
            st.caption('Illustrative annualisation of this instance; enter site-specific costs and operating hours.')
        except (ValueError, KeyError) as exc: st.error(str(exc))
    st.caption(FOOTER)

if __name__ == '__main__': main()

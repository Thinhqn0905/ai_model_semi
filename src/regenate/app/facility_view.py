"""File-backed Run 4 views; calculations are illustrative incremental charges."""
import os
from pathlib import Path
import zipfile
import pandas as pd
import plotly.express as px
import streamlit as st
import yaml
from regenate.evaluation.facility import load_ds07, billed_demand

TARIFFS = Path('data/tariffs')


def fields(obj, prefix=''):
    if isinstance(obj, dict) and 'value' in obj:
        yield prefix, obj.get('value'), obj.get('status', 'NOT_VERIFIED'), obj.get('unit', '')
    elif isinstance(obj, dict):
        for key, value in obj.items():
            yield from fields(value, f'{prefix}.{key}' if prefix else key)
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            yield from fields(value, f'{prefix}[{i}]')
    else:
        yield prefix, obj, 'NOT_VERIFIED', ''


def select_tariff():
    paths = sorted(TARIFFS.glob('*.yaml'))
    if not paths:
        st.info('Tariff data not available'); return None
    path = st.selectbox('Tariff', paths, format_func=lambda p: p.stem)
    return yaml.safe_load(path.read_text(encoding='utf-8'))


def find_file(root, name):
    return sorted(root.rglob(name)) if root.exists() else []


def render(page, root):
    st.header(page)
    report = [f'# {page}', 'Boundary: NOT_VERIFIED unless explicitly labelled otherwise.']
    if page == 'Facility load':
        path = Path(st.text_input('DS07 zip path', os.environ.get('REGENATE_DS07', '')) or '.')
        if not path.is_file() or not zipfile.is_zipfile(path):
            st.info('data not available')
        else:
            with zipfile.ZipFile(path) as z:
                names = sorted(Path(n).stem for n in z.namelist() if n.startswith('Data_list/Factories/') and n.endswith('.csv'))
            if not names:
                st.info('data not available')
            else:
                fac = st.selectbox('Facility', names)
                series = load_ds07(path, fac)
                months = sorted(series.index.strftime('%Y-%m').unique())
                month = st.selectbox('Month', months)
                series = series[series.index.strftime('%Y-%m') == month]
                md, stamp = billed_demand(series)
                st.warning('MEASURED DS07 facility; DERIVED billed demand; ASSUMED aligned 30-minute interval and 80% coverage.')
                st.plotly_chart(px.line(series.rename('MEASURED kW')), use_container_width=True)
                st.write(f'DERIVED billed demand: {md:.3f} kW; interval start: {stamp}')
                if stamp is not None:
                    st.dataframe(series.loc[stamp:stamp + pd.Timedelta(minutes=29)].rename('MEASURED kW'))
                report += [f'Facility: {fac}; month: {month}', f'DERIVED billed demand: {md:.3f} kW at {stamp}', 'ASSUMED aligned 30-minute interval; minimum 80% coverage.']
    elif page == 'Tariff selector':
        tariff = select_tariff()
        if tariff:
            rows = pd.DataFrame(fields(tariff), columns=['field', 'value', 'status', 'unit'])
            st.warning('Tariff fields: VERIFIED or NOT_VERIFIED; values are SOURCE_REPORTED.')
            st.dataframe(rows)
            report += ['SOURCE_REPORTED tariff fields', rows.to_csv(index=False)]
    elif page == 'Monthly bill':
        tariff = select_tariff()
        files = find_file(root, 'facility_md.csv')
        if not tariff or not files:
            st.info('Facility billing data not available')
        else:
            path = st.selectbox('Facility results', files, format_func=str)
            df = pd.read_csv(path)
            fac = st.selectbox('Facility', sorted(df.facility.dropna().unique()))
            sub = df[df.facility == fac]
            month = st.selectbox('Month', sorted(sub.month.dropna().unique()))
            sub = sub[sub.month == month]
            methods = sorted(sub.method.dropna().unique())
            base = st.selectbox('Baseline', methods)
            method = st.selectbox('Method', methods, index=min(1, len(methods)-1))
            rates = tariff.get('demand_rates', {})
            energies = tariff.get('energy_rates', {})
            er = st.selectbox('Energy rate', list(energies), format_func=str) if energies else None
            demand = [v.get('value') if isinstance(v, dict) else v for v in rates.values()]
            energy = energies.get(er, {}).get('value') if er else None
            st.warning('NOT_VERIFIED — incremental estimate; SIM_DATA_PROFILE cell + MEASURED DS07, not synchronised. Tariff and billing assumptions require verification.')
            if tariff.get('tariff_status') == 'TRIAL_NOT_PAYABLE' or energy is None or any(x is None for x in demand) or 'cell_kwh' not in sub or not rates:
                st.info('NOT_VERIFIED: required payable rates or cell energy are unavailable.')
            else:
                rows = sub[sub.method.isin([base, method])].copy()
                rows['DERIVED incremental demand charge'] = rows.md_increment_kw * sum(map(float, demand))
                rows['DERIVED cell energy charge'] = rows.cell_kwh * float(energy)
                rows['DERIVED incremental total'] = rows['DERIVED incremental demand charge'] + rows['DERIVED cell energy charge']
                st.dataframe(rows)
                st.caption('ASSUMED single selected energy rate for all cell kWh; excludes facility energy, fixed fees, export credits, contract and excess charges, taxes and adjustments. Not a complete payable bill.')
                report += [f'Source: {path}; tariff: {tariff.get("id")}; facility: {fac}; month: {month}', 'NOT_VERIFIED incremental estimate; SIM_DATA_PROFILE cell + MEASURED DS07, not synchronised.', 'ASSUMED single selected energy rate; excludes facility energy, fixed fees, export credits, contract and excess charges, taxes and adjustments.', rows.to_csv(index=False)]
    else:
        files = find_file(root, 'fin_v3_ds06.csv')
        if not files:
            st.info('FIN data not available')
        else:
            path = st.selectbox('FIN results', files, format_func=str)
            df = pd.read_csv(path)
            st.warning('NOT_VERIFIED unless source rows supply a boundary; DERIVED break-even assumes constant annual net savings.')
            st.dataframe(df)
            report += [f'Source: {path}', 'NOT_VERIFIED source rows unless otherwise labelled.', df.to_csv(index=False)]
            if 'annual_net_usd' not in df:
                st.info('NOT_VERIFIED: annual_net_usd is unavailable; break-even cannot be calculated.')
            else:
                savings = pd.to_numeric(df['annual_net_usd'], errors='coerce')
                st.caption('ASSUMED constant annual net savings; no escalation or tax. Break-even uses annual_net_usd, including the source operating costs.')
                out = pd.DataFrame({'source row': df.index, 'boundary': df['boundary'].fillna('NOT_VERIFIED') if 'boundary' in df else 'NOT_VERIFIED', 'DERIVED 3-year CAPEX USD': savings * 3, 'DERIVED 5-year CAPEX USD': savings * 5, 'DERIVED 10-year CAPEX USD at 8%': savings * sum(1 / 1.08**y for y in range(1, 11))})
                st.dataframe(out)
                report += ['ASSUMED constant annual_net_usd; no escalation or tax.', out.to_csv(index=False)]
    st.download_button('Export current page (markdown)', '\n\n'.join(report), file_name='regenate_report.md', mime='text/markdown')


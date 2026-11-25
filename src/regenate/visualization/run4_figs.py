"""Generate Run 4 figures from available result CSVs; missing evidence fails closed."""
import argparse
import hashlib
import json
import shlex
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from regenate.evaluation.stats import paired_ci
from regenate.visualization.common import save


class Blocked(Exception):
    pass


def read(path):
    if not path.is_file():
        raise Blocked(f"missing input: {path}")
    try:
        return pd.read_csv(path)
    except (ValueError, pd.errors.ParserError) as exc:
        raise Blocked(f"invalid input {path}: {exc}") from exc


def require(df, columns, path):
    missing = set(columns) - set(df.columns)
    if missing:
        raise Blocked(f"{path}: missing columns {', '.join(sorted(missing))}")


def boundary(df, path):
    require(df, ['boundary'], path)
    values = df.boundary.dropna().astype(str).unique()
    if len(values) != 1 or not values[0].strip() or df.boundary.isna().any():
        raise Blocked(f"{path}: missing or inconsistent evidence boundary")
    return values[0]


def paired(df, method, metric, path, base='P0', equal_tt=False):
    require(df, ['instance_id', 'method', metric, 'TT_h'], path)
    d = df[df.method.isin([base, method])].copy()
    if d.duplicated(['instance_id', 'method']).any():
        raise Blocked(f"{path}: duplicate instance/method records")
    w = d.pivot(index='instance_id', columns='method', values=metric)
    if base not in w or method not in w:
        raise Blocked(f"{path}: missing method {base} or {method}")
    w = w[[base, method]].dropna()
    if not np.isfinite(w.to_numpy(dtype=float)).all():
        raise Blocked(f"{path}: non-finite metric values")
    if equal_tt:
        t = d.pivot(index='instance_id', columns='method', values='TT_h').reindex(w.index)
        w = w.loc[(t[base] - t[method]).abs() <= 1e-6]
    if w.empty:
        raise Blocked(f"{path}: no matched pairs for {method} vs {base}")
    return paired_ci(w[base], w[method])


def comparison(ax, df, methods, metric, path, ylabel, equal_tt=False):
    results = [paired(df, m, metric, path, equal_tt=equal_tt) for m in methods]
    means = np.array([r['mean'] for r in results])
    errors = np.array([[r['mean'] - r['lo'] for r in results],
                       [r['hi'] - r['mean'] for r in results]])
    ax.bar(range(len(methods)), means, yerr=errors, capsize=3)
    ax.axhline(0, color='black', lw=.7)
    ax.set_xticks(range(len(methods)), methods, rotation=30, ha='right')
    ax.set_ylabel(ylabel)


def generate(number, root):
    p = root / 'run3/v2_diag/results.csv'
    if number in (16, 19, 21, 24):
        if number in (16, 19):
            campaigns = ['v2_diag', 'v2_pqstar', 'v2_pqd']
            files = [root / 'run3' / c / 'results.csv' for c in campaigns]
            manifests = [f.parent / 'manifest.json' for f in files]
            frames = [read(f) for f in files]
            labels = [boundary(d, f) for d, f in zip(frames, files)]
            if len(set(labels)) != 1:
                raise Blocked('campaigns have inconsistent evidence boundaries')
            settings = []
            for manifest in manifests:
                if not manifest.is_file():
                    raise Blocked(f'missing input: {manifest}')
                try:
                    args = json.loads(manifest.read_text(encoding='utf-8'))['args']
                    settings.append({k: args.get(k) for k in ('seeds', 'flex', 'split', 'n_jobs', 'n_stations', 'time_limit', 'prm', 'peak')})
                except (ValueError, KeyError, TypeError) as exc:
                    raise Blocked(f'invalid manifest: {manifest}: {exc}') from exc
            if any(x != settings[0] for x in settings[1:]):
                raise Blocked(f'campaign settings differ: {manifests}')
            for frame, file in zip(frames, files):
                require(frame, ['instance_id', 'method', 'net_kwh', 'TT_h'], file)
            ids = [set(d.loc[d.method == 'P0', 'instance_id']) for d in frames]
            if not ids[0] or any(x != ids[0] for x in ids[1:]):
                raise Blocked(f'campaign instance sets differ: {files}')
            # Baseline observations must match across campaigns as well.
            baselines = [d[d.method == 'P0'].set_index('instance_id')[['net_kwh', 'TT_h']].sort_index() for d in frames]
            if any(not x.equals(baselines[0]) for x in baselines[1:]):
                raise Blocked(f'P0 observations differ across campaigns: {files}')
            choices = ([('TR_ALL', 0), ('TR_Q', 0), ('PQ*', 1), ('PQd*', 2), ('TR_RUN', 0)]
                       if number == 16 else [('PQd', 2), ('PQd*', 2)])
            fig, axes = plt.subplots(1, 2, figsize=(10, 4))
            for ax, metric, title in zip(axes, ['net_kwh', 'TT_h'], ['Energy saved vs P0 (kWh)', 'Tardiness saved vs P0 (h)']):
                stats = [paired(frames[i], method, metric, files[i], equal_tt=(metric == 'net_kwh')) for method, i in choices]
                means = np.array([r['mean'] for r in stats])
                ax.bar(range(len(choices)), means, yerr=[[r['mean']-r['lo'] for r in stats], [r['hi']-r['mean'] for r in stats]], capsize=3)
                ax.axhline(0, color='black', lw=.7)
                ax.set_xticks(range(len(choices)), [m for m, _ in choices], rotation=30, ha='right'); ax.set_ylabel(title)
            return fig, labels[0], files + manifests
        if number == 24:
            files = [root / 'v2_flex025_n100.csv', root / 'run3/v2_e1/results.csv',
                     root / 'run3/v2_e1_peak/results.csv']
            frames = [read(f) for f in files]
            labels = [boundary(d, f) for d, f in zip(frames, files)]
            if len(set(labels)) != 1:
                raise Blocked(f"inconsistent evidence boundaries: {files}")
            manifests = [f.parent / 'manifest.json' for f in files[1:]]
            settings = []
            for manifest in manifests:
                if not manifest.is_file():
                    raise Blocked(f"missing input: {manifest}")
                try:
                    args = json.loads(manifest.read_text(encoding='utf-8'))['args']
                    settings.append({k: v for k, v in args.items()
                                     if k not in ('out', 'methods', 'workers', 'peak')})
                except (ValueError, KeyError, TypeError) as exc:
                    raise Blocked(f"invalid manifest: {manifest}: {exc}") from exc
            if settings[0] != settings[1]:
                raise Blocked(f"campaign settings differ: {manifests}")
            comparisons = [('B0 -> B1', 'B0', 'B1'), ('B1p-OPT -> B2', 'B1p-OPT', 'B2'),
                           ('B1p-OPT -> B3', 'B1p-OPT', 'B3'), ('B2 -> B3', 'B2', 'B3'),
                           ('B3 -> P0', 'B3', 'P0')]
            stats = [paired(frames[0], target, 'net_kwh', files[0], base=base, equal_tt=True)
                     for _, base, target in comparisons]
            for frame, file in zip(frames[1:], files[1:]):
                require(frame, ['instance_id', 'method', 'net_kwh', 'TT_h'], file)
            e1 = frames[1][frames[1].method == 'P0'].copy()
            peak = frames[2][frames[2].method == 'P0'].copy()
            if set(e1.instance_id) != set(peak.instance_id) or e1.empty:
                raise Blocked(f"P0 instance sets differ: {files[1:]}")
            peak['method'] = 'P0-E1-Peak'
            stats.append(paired(pd.concat([e1, peak]), 'P0-E1-Peak', 'net_kwh',
                                str(files[1:]), base='P0', equal_tt=True))
            names = [x[0] for x in comparisons] + ['P0-E1 -> P0-E1-Peak']
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(range(len(names)), [r['mean'] for r in stats],
                   yerr=[[r['mean']-r['lo'] for r in stats], [r['hi']-r['mean'] for r in stats]], capsize=3)
            ax.axhline(0, color='black', lw=.7)
            ax.set_xticks(range(len(names)), names, rotation=30, ha='right')
            ax.set_ylabel('Energy saved (kWh), paired 95% CI')
            ax.set_title('Peak comparison: E1 vs E1-Peak; other pairs: Run 2')
            return fig, labels[0], files + manifests
        d = read(p); b = boundary(d, p)
        methods = [m for m in ['P1*', 'P2*', 'P3*', 'P4*', 'P5', 'P5s', 'PQ', 'PQ5', 'PQd'] if m in set(d.method)]
        if not methods:
            raise Blocked(f"{p}: no AI variants")
        fig, axes = plt.subplots(1, 2, figsize=(10, 4))
        for ax, metric, title in zip(axes, ['net_kwh', 'TT_h'],
                                      ['Energy saved vs P0 (kWh)', 'Tardiness saved vs P0 (h)']):
            results = [paired(d, m, metric, p, equal_tt=(metric == 'net_kwh')) for m in methods]
            means = np.array([r['mean'] for r in results])
            ax.errorbar(means, range(len(methods)),
                        xerr=[[r['mean']-r['lo'] for r in results], [r['hi']-r['mean'] for r in results]],
                        fmt='o', capsize=3)
            ax.axvline(0, color='black', lw=.7)
            ax.set_yticks(range(len(methods)), methods)
            ax.set_xlabel(title + ' (paired 95% CI)')
        return fig, b, [p]
    if number in (17, 18):
        p = root / ('run4/eta/predictions_T1.parquet' if number == 17 else 'run4/eta/metrics_T2.csv')
        if number == 17:
            if not p.is_file():
                raise Blocked(f'missing input: {p}')
            d = pd.read_parquet(p)
            require(d, ['cycle_file', 'use_case', 'true', 'model', 'q10', 'q50', 'q90'], p)
            models = d.model.dropna().astype(str).unique().tolist()
            model = 'quantile_lightgbm_cqr' if 'quantile_lightgbm_cqr' in models else next((m for m in models if 'quantile' in m.lower() or m.lower().startswith('q')), None)
            if model is None:
                raise Blocked(f'{p}: no quantile model')
            d = d[d.model == model].head(30).reset_index(drop=True)
            if d.empty:
                raise Blocked(f'{p}: no predictions')
            fig, ax = plt.subplots(figsize=(9, 4))
            x = np.arange(len(d))
            ax.plot(x, d['true'].to_numpy(), 'o', label='True')
            ax.plot(x, d.q50.to_numpy(), '.', label='Median')
            ax.fill_between(x, d.q10.to_numpy(dtype=float), d.q90.to_numpy(dtype=float), alpha=.2)
            ax.set_xlabel('Sample cycle'); ax.set_ylabel('ETA'); ax.legend()
            return fig, 'NOT_VERIFIED', [p]
        d = read(p); b = boundary(d, p)
        require(d, ['use_case', 'subset', 'progress', 'model', 'mae'], p)
        d = d[(d.use_case == 'ALL') & (d.subset == 'ALL') & (d.progress != 'ALL')]
        if d.empty:
            raise Blocked(f'{p}: no aggregate progress rows')
        fig, ax = plt.subplots(figsize=(8, 4))
        d.pivot(index='progress', columns='model', values='mae').reindex(['0-25', '25-50', '50-75', '75-100']).plot.bar(ax=ax)
        ax.set_ylabel('MAE'); ax.set_xlabel('Cycle progress')
        return fig, b, [p]
    if number in (27, 28, 30):
        paths = sorted((root / 'run4').glob('fac_bill_tnb_*/facility_md.csv')) if number == 30 else [root / 'run4/fac_grid_tnb/facility_md.csv']
        if number == 30:
            paths += sorted((root / 'run4').glob('fac_p0bill_*/facility_md.csv'))
            paths += sorted((root / 'run4').glob('fac_aibill_*/facility_md.csv'))
            if not paths:
                raise Blocked(f"missing input: {root / 'run4/fac_bill_tnb_*/facility_md.csv'} and {root / 'run4/fac_p0bill_*/facility_md.csv'}")
        frames = [read(x) for x in paths]
        labels = [boundary(d, x) for d, x in zip(frames, paths)]
        if len(set(labels)) != 1:
            raise Blocked('facility inputs have inconsistent evidence boundaries')
        d = pd.concat(frames, ignore_index=True)
        require(d, ['method', 'facility', 'month', 'md_increment_kw'], ', '.join(map(str, paths)))
        fig, ax = plt.subplots(figsize=(8, 4))
        if number == 27:
            require(d, ['cell_peak_kw'], paths[0]); ax.scatter(d.cell_peak_kw, d.md_increment_kw)
            ax.set_xlabel('Cell peak (kW)'); ax.set_ylabel('Facility MD increment (kW)')
        else:
            if number == 30:
                methods = d.method.astype(str)
                d = d[methods.str.match(r'^(P0@v2_e1_peak|P0-BILL:(hist|ai|oracle)@etol0\.02|ORACLE(?:-BILL)?(?:[:@].*)?)$')].copy()
                if d.empty:
                    raise Blocked(f'{paths}: missing billing methods')
                count = int(d.duplicated(['facility', 'month', 'method']).sum())
                if count:
                    print(f'F30: deduplicated {count} facility/month/method records (kept first)')
                    d = d.drop_duplicates(['facility', 'month', 'method'], keep='first')
            elif d.duplicated(['facility', 'month', 'method']).any():
                raise Blocked(f"{paths}: ambiguous duplicate facility/month/method records")
            pivot = d.pivot(index=['facility', 'month'], columns='method', values='md_increment_kw')
            pivot.plot.bar(ax=ax); ax.set_ylabel('Billed demand increment (kW)')
        return fig, labels[0], paths
    required = {
        22: root / 'run3/screen_e1.csv',
        25: root / 'run3/fin_v3_ds06.csv',
        26: root / 'ds07/facility_monthly_summary.csv',
        32: root / 'run3/fin_v3_ds06.csv',
    }
    p = required[number]
    paths = [p]
    if number == 26 and not p.is_file():
        paths = sorted((root / 'run4').glob('fac_grid*/facility_md.csv'))
        if not paths:
            raise Blocked(f'missing input: {p} and run4/fac_grid*/facility_md.csv')
        frames = [read(x) for x in paths]
        labels = [boundary(d, x) for d, x in zip(frames, paths)]
        if len(set(labels)) != 1:
            raise Blocked('facility inputs have inconsistent evidence boundaries')
        d = pd.concat(frames, ignore_index=True); b = labels[0]
        require(d, ['facility', 'month', 'md_bg_kw'], paths)
        if (d.groupby(['facility', 'month']).md_bg_kw.nunique() > 1).any():
            raise Blocked('inconsistent background demand for facility/month')
        d = d.drop_duplicates(['facility', 'month']).copy()
        d['md_kw'] = d['md_bg_kw']
    else:
        d = read(p)
        b = 'SIM_DATA_PROFILE' if number == 22 and 'boundary' not in d else boundary(d, p)
    if number == 22:
        require(d, ['run', 'method', 'approved'], p)
        sizing = root / 'run4_rt3/screen_sizing_summary.csv'
        fig, axes = plt.subplots(1, 2 if sizing.is_file() else 1, figsize=(11 if sizing.is_file() else 7, 4), squeeze=False)
        d = d.copy(); d['run'] = d['run'].replace({'v2_diag': 'E0', 'v2_e1': 'E1'})
        d.groupby(['run', 'method']).approved.mean().unstack().plot.bar(ax=axes[0, 0])
        axes[0, 0].set_ylabel('Approval fraction')
        if sizing.is_file():
            z = read(sizing); require(z, ['afe_kw', 'bus_kw', 'method', 'n', 'approved', 'kinds'], sizing)
            z = z.copy(); z['setting'] = z.afe_kw.astype(str) + '/' + z.bus_kw.astype(str)
            z.pivot_table(index='setting', columns='method', values='approved', aggfunc='mean').plot.bar(ax=axes[0, 1])
            axes[0, 1].set_xlabel('AFE / bus (kW)'); axes[0, 1].set_ylabel('Approved')
            paths.append(sizing)
        return fig, b, paths
    if number == 26:
        require(d, ['facility', 'month', 'md_kw'], p)
        fig, ax = plt.subplots(figsize=(8, 4))
        d.pivot(index='month', columns='facility', values='md_kw').plot(ax=ax)
        ax.set_ylabel('Background demand (kW)'); return fig, b, paths
    require(d, ['option', 'annual_net_usd', 'break_even_capex_usd'], p)
    extras = [x for x in (root / 'run4/fin_fac_gen_fx0.21/clustered_summary.csv', root / 'run4/fin_fac_tou_fx0.21/clustered_summary.csv') if x.is_file()]
    fig, axes = plt.subplots(1, 2 if extras else 1, figsize=(12 if extras else 7, 4), squeeze=False)
    ax = axes[0, 0]
    ax.scatter(d.annual_net_usd, d.break_even_capex_usd)
    for row in d.itertuples(): ax.annotate(str(row.option), (row.annual_net_usd, row.break_even_capex_usd))
    ax.set_xlabel('Annual net (USD/year)'); ax.set_ylabel('Break-even CAPEX (USD)')
    if extras:
        frames = [read(x) for x in extras]
        for frame, path in zip(frames, extras):
            require(frame, ['option', 'n_cells', 'annual_net_usd', 'ceiling_3y', 'ceiling_5y', 'ceiling_10y_discounted', 'tariff'], path)
        z = pd.concat(frames, ignore_index=True)
        for (option, tariff), group in z.groupby(['option', 'tariff']):
            axes[0, 1].plot(group.n_cells, group.annual_net_usd, marker='o', label=f'{option} / {tariff}')
        axes[0, 1].set_xlabel('Cells'); axes[0, 1].set_ylabel('Annual net (USD/year)'); axes[0, 1].legend(fontsize=6)
        paths += extras
    return fig, b, paths


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runs', required=True); parser.add_argument('--out', required=True)
    args = parser.parse_args(argv); root = Path(args.runs); out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    command = shlex.join([sys.executable, '-m', 'regenate.visualization.run4_figs', '--runs', args.runs, '--out', args.out])
    lines = ['# Run 4 figures', '', 'Generated from supplied CSVs; blocked figures require the listed evidence.', '']
    existing = Path('reports/figures')
    for n in range(1, 16):
        name = f'F{n:02d}'
        files = sorted(existing.glob(f'{name}.*'))
        links = ', '.join(f'[{f.name}]({f.resolve().as_posix()})' for f in files)
        lines.append(f'- {name}: ' + (f'PASS (NOT_VERIFIED; existing files): {links}' if files else 'MISSING'))
    for n in (16, 17, 18, 19, 21, 22, 24, 25, 26, 27, 28, 30, 32):
        name = f'F{n}'
        try:
            fig, b, paths = generate(n, root)
            save(fig, pd.DataFrame({'boundary': [b]}), out / name)
            fig.savefig(out / f'{name}.svg')
            provenance = {'inputs': [{'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths], 'command': command, 'boundary': b}
            (out / f'{name}.json').write_text(json.dumps(provenance, indent=2), encoding='utf-8')
            lines.append(f'- {name}: GENERATED ({b}); [{name}.png]({name}.png)')
        except (Blocked, ValueError, KeyError, TypeError) as exc:
            plt.close('all')
            for ext in ('png', 'pdf', 'svg', 'json'):
                (out / f'{name}.{ext}').unlink(missing_ok=True)
            lines.append(f'- {name}: BLOCKED — {exc}')
    (out / 'INDEX.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()

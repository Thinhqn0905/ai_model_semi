"""Collect local and Drive Run 4 figure inputs without changing source files."""
import argparse
import fnmatch
import shutil
from pathlib import Path

FIGURES = {
    'F16': ['run3/v2_diag/results.csv', 'run3/v2_diag/manifest.json', 'run3/v2_pqstar/results.csv', 'run3/v2_pqstar/manifest.json', 'run3/v2_pqd/results.csv', 'run3/v2_pqd/manifest.json'],
    'F17': ['run4/eta/metrics_T1.csv'], 'F18': ['run4/eta/metrics_T2.csv'],
    'F19': ['run3/v2_diag/results.csv', 'run3/v2_diag/manifest.json', 'run3/v2_pqstar/results.csv', 'run3/v2_pqstar/manifest.json', 'run3/v2_pqd/results.csv', 'run3/v2_pqd/manifest.json'],
    'F21': ['run3/v2_diag/results.csv'], 'F22': ['run3/screen_e1.csv'],
    'F24': ['v2_flex025_n100.csv', 'run3/v2_e1/results.csv', 'run3/v2_e1/manifest.json', 'run3/v2_e1_peak/results.csv', 'run3/v2_e1_peak/manifest.json'],
    'F25': ['run3/fin_v3_ds06.csv'], 'F26': ['ds07/facility_monthly_summary.csv'],
    'F27': ['run4/fac_grid_tnb/facility_md.csv'], 'F28': ['run4/fac_grid_tnb/facility_md.csv'],
    'F30': ['run4/fac_bill_tnb_*/facility_md.csv', 'run4/fac_p0bill_*/facility_md.csv'],
    'F32': ['run3/fin_v3_ds06.csv'],
}


def collect(drive, local, out):
    roots = [Path(local).resolve(), Path(drive).resolve()]
    out = Path(out).resolve()
    for root in roots:
        if out == root or root in out.parents or out in root.parents:
            raise ValueError('output and source directories must not overlap')
    # The named run directories are the only recursively searched source trees.
    candidates = {}
    for root in roots:
        for run in ('run3', 'run4', 'run4_rt2', 'run4_rt3'):
            directory = root / run
            if not directory.is_dir():
                continue
            for path in directory.rglob('*'):
                if not path.is_file():
                    continue
                rel = path.relative_to(directory).as_posix()
                canonical = ('run3' if run == 'run3' else 'run4') + '/' + rel
                candidates.setdefault(canonical, []).append(path)
                # Some Drive exports contain an additional run3/run4 directory.
                if rel.startswith(('run3/', 'run4/', 'ds07/')):
                    candidates.setdefault(rel, []).append(path)
                if path.name in ('v2_flex025_n100.csv', 'fin_v3_ds06.csv'):
                    key = 'v2_flex025_n100.csv' if path.name.startswith('v2_') else 'run3/fin_v3_ds06.csv'
                    candidates.setdefault(key, []).append(path)
                if path.name == 'facility_monthly_summary.csv':
                    candidates.setdefault('ds07/facility_monthly_summary.csv', []).append(path)
        for name, dest in [('v2_flex025_n100.csv', 'v2_flex025_n100.csv'), ('fin_v3_ds06.csv', 'run3/fin_v3_ds06.csv')]:
            path = root / name
            if path.is_file():
                candidates.setdefault(dest, []).append(path)
    # Copy all campaign CSVs and manifests, including optional campaigns.
    copied = set()
    for dest, paths in sorted(candidates.items()):
        if not (dest.endswith('.csv') or dest.endswith('/manifest.json')):
            continue
        unique = set(paths)
        selected = max(unique, key=lambda p: (p.stat().st_mtime_ns, str(p)))
        target = out / dest
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(selected, target)
        copied.add(dest)
        print(f'COPY {dest} <- {selected}' + (f' (newest of {len(unique)})' if len(unique) > 1 else ''))
    print('Figure | Status | Inputs')
    for figure, patterns in FIGURES.items():
        found = [p for p in patterns if any(fnmatch.fnmatchcase(x, p) for x in copied)]
        missing = [p for p in patterns if p not in found]
        # F30 generator accepts either family, subject to its own schema checks.
        status = 'FOUND' if not missing or (figure == 'F30' and found) else 'MISSING'
        print(f"{figure} | {status} | " + ', '.join(f'{p}: {"missing" if p in missing else "found"}' for p in patterns))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--drive', required=True)
    parser.add_argument('--local', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    collect(args.drive, args.local, args.out)


if __name__ == '__main__':
    main()

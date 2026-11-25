import os
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'colab_collect_run4.py'


def test_collect_newest_sources_and_figure_table(tmp_path):
    local, drive, out = (tmp_path / n for n in ('local', 'drive', 'out'))
    old = local / 'run3/v2_diag/results.csv'
    new = drive / 'run3/v2_diag/results.csv'
    for path, content in [(old, 'old'), (new, 'new')]:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    os.utime(old, (100, 100)); os.utime(new, (200, 200))
    manifest = drive / 'run3/v2_diag/manifest.json'
    manifest.write_text('{}')
    extra = drive / 'run4_rt2/fac_bill_tnb_x/facility_md.csv'
    extra.parent.mkdir(parents=True)
    extra.write_text('facility')
    flex = local / 'v2_flex025_n100.csv'
    flex.write_text('flex')
    result = subprocess.run([sys.executable, str(SCRIPT), '--drive', str(drive), '--local', str(local), '--out', str(out)], capture_output=True, text=True, check=True)
    assert (out / 'run3/v2_diag/results.csv').read_text() == 'new'
    assert old.read_text() == 'old' and new.read_text() == 'new'
    assert (out / 'run3/v2_diag/manifest.json').read_text() == '{}'
    assert (out / 'run4/fac_bill_tnb_x/facility_md.csv').read_text() == 'facility'
    assert (out / 'v2_flex025_n100.csv').read_text() == 'flex'
    assert 'newest of 2' in result.stdout
    assert 'F16 | MISSING' in result.stdout and 'F21 | FOUND' in result.stdout


def test_reject_overlapping_output(tmp_path):
    local = tmp_path / 'local'
    local.mkdir()
    result = subprocess.run([sys.executable, str(SCRIPT), '--drive', str(tmp_path / 'drive'), '--local', str(local), '--out', str(local / 'out')], capture_output=True, text=True)
    assert result.returncode != 0
    assert 'must not overlap' in result.stderr

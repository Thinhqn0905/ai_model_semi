from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'font.family': 'serif', 'axes.spines.top': False, 'axes.spines.right': False})

def save(fig, frame, out):
    labels = frame['boundary'].dropna().astype(str).unique()
    if len(labels) != 1 or not labels[0].strip():
        raise ValueError('exactly one nonempty evidence boundary is required')
    fig.text(.99, .01, labels[0], ha='right', va='bottom', fontsize=8)
    fig.tight_layout(rect=(0, .04, 1, 1))
    path = Path(out)
    path.parent.mkdir(parents=True, exist_ok=True)
    for ext in ('png', 'pdf'):
        fig.savefig(path.with_suffix('.'+ext), dpi=300)
    plt.close(fig)

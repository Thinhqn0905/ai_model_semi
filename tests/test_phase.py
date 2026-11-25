import numpy as np
from regenate.forecasting.phase import segments, transitions, aligned_forecast, transition_errors


def prof(lens):                      # lens: [(state, n)] -> ch, ds at 1 kW
    ch = np.concatenate([np.full(n, 1.0 if s == "C" else 0.0) for s, n in lens])
    ds = np.concatenate([np.full(n, 1.0 if s == "D" else 0.0) for s, n in lens])
    return ch, ds


def test_segments_and_flicker():
    ch, ds = prof([("C", 10), ("I", 1), ("C", 10), ("D", 20)])
    assert [(s, n) for s, _, n in segments(ch, ds)] == [("C", 21), ("D", 20)]
    assert transitions(ch, ds) == [21]


def test_aligned_beats_time_indexed_when_first_phase_runs_long():
    prev = prof([("C", 30), ("D", 30), ("C", 20)])
    cur = prof([("C", 40), ("D", 30), ("C", 20)])        # charge ran 10 bins longer than the recipe
    errs = transition_errors(*cur, *prev, at_bins=[45])  # inside D phase; next true transition at 70
    b, e_rec, e_al = errs[0]
    assert e_rec == 10 and e_al == 0                     # recipe says 60 (next after 45), aligned says 40+30=70
    (fc, fd), ok = aligned_forecast(cur[0][:45], cur[1][:45], *prev)
    assert ok and len(fc) == 25 + 20

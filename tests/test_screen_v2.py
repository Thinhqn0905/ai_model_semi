import numpy as np
import pandas as pd
from regenate.simulation.screen_v2 import residuals
from regenate.electrical.ledger import ElecParams


def test_residuals_remove_self_use():
    import sys; sys.path.insert(0, "tests")
    from test_v2_campaign import synth
    from regenate.data.bench_v2 import make_instance, fifo
    cyc, arrs = synth(); inst = make_instance(cyc, arrs, 0, n_jobs=4, n_stations=2, split="train")
    a, s = fifo(inst)
    sch = pd.DataFrame(dict(job_id=list(a), station=[a[j] for j in a], start_h=[s[j] for j in a]))
    src, sink = residuals(inst, sch, ElecParams())
    assert (src >= 0).all() and (sink >= 0).all() and not np.any((src > 1e-12) & (sink > 1e-12))   # never both on one station

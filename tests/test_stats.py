import numpy as np
import pandas as pd
from regenate.evaluation.stats import paired_ci, ladder_table


def test_paired_ci_hand():
    r = paired_ci([10, 12, 14], [9, 11, 13])
    assert r["mean"] == 1 and r["lo"] == 1 and r["hi"] == 1 and r["wins"] == 3


def test_ladder_equal_tt_filter():
    rows = []
    for i, (p0, p, ttp) in enumerate([(10, 9, 1.0), (10, 8, 1.0), (10, 5, 0.0)]):
        rows += [dict(instance_id=i, method="P0", net_kwh=p0, TT_h=1.0),
                 dict(instance_id=i, method="P", net_kwh=p, TT_h=ttp)]
    t = ladder_table(pd.DataFrame(rows)).set_index("a")
    assert t.loc["P0", "n"] == 2 and t.loc["P0", "mean"] == 1.5


def test_cluster_ci_wider_than_iid_when_clusters_differ():
    import numpy as np
    from regenate.evaluation.stats import cluster_paired_ci, paired_ci
    rng = np.random.default_rng(1)
    g = np.repeat(np.arange(10), 7)                               # 10 factories x 7 months
    d = np.repeat(rng.normal(1.0, 2.0, 10), 7) + rng.normal(0, 0.1, 70)   # strong factory effect
    c, i = cluster_paired_ci(d, np.zeros(70), g), paired_ci(d, np.zeros(70))
    assert c["n_clusters"] == 10 and abs(c["mean"] - i["mean"]) < 1e-12
    assert (c["hi"] - c["lo"]) > 1.5 * (i["hi"] - i["lo"])

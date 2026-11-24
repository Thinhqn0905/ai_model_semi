import json
import io
import numpy as np
import pandas as pd
import pytest
import yaml
from regenate.data.ds01 import SOURCE, load_instance
from regenate.data.generator import generate, fifo_schedule, render, job_slot_profile, _phase_steps
from regenate.electrical.ledger import ledger

CFG=yaml.safe_load(open("configs/bench_v1.yaml"))
DS=load_instance(sorted(SOURCE.glob("n010_tau02_r00.json"))[0])

@pytest.mark.parametrize("scenario", ["S1","S2","S3"])
def test_deterministic_and_energy(scenario):
    a=generate(DS,scenario,0,CFG); b=generate(DS,scenario,0,CFG)
    for key in ("jobs","stations","recipe"):
        first=io.BytesIO(); second=io.BytesIO()
        a[key].to_parquet(first,index=False); b[key].to_parquet(second,index=False)
        assert first.getvalue()==second.getvalue()
    ass,starts=fifo_schedule(a); pin,prec,aux=render(a,ass,starts,.25)
    recipe=a["recipe"]
    expected=np.zeros(3)
    for j in a["jobs"].itertuples():
        steps=_phase_steps(recipe,j.dur_true_h,.25)
        expected += .25*np.array([(steps*recipe.p_in_frac).sum()*j.kappa_true*CFG["p_rated_kw"], (steps*recipe.p_rec_frac).sum()*j.kappa_true*CFG["p_rated_kw"], (steps*recipe.p_aux_kw).sum()])
    np.testing.assert_allclose([pin.sum()*.25,prec.sum()*.25,aux.sum()*.25],expected,rtol=0,atol=1e-9)
    profile=job_slot_profile(a,a["jobs"].iloc[0],15.0)
    assert np.array_equal(profile["mixed_slots"],(profile["p_in"]>1e-12)&(profile["p_rec"]>1e-12))
    if scenario != "S3": assert np.all(prec <= pin + 1e-12)
    else: assert not np.any((pin > 1e-12) & (prec > 1e-12))

def test_fifo_and_ledger():
    inst=generate(DS,"S1",0,CFG); assign,starts=fifo_schedule(inst)
    jobs=inst["jobs"]
    for j in jobs.itertuples():
        assert starts[j.job_id] >= j.release_h and assign[j.job_id] in j.eligible_stations
        for k in jobs.itertuples():
            if j.job_id < k.job_id and assign[j.job_id] == assign[k.job_id]:
                assert starts[j.job_id]+j.dur_true_h <= starts[k.job_id]+1e-12 or starts[k.job_id]+k.dur_true_h <= starts[j.job_id]+1e-12
    powers=render(inst,assign,starts,.25)
    outputs={top:ledger(*powers,.25,topology=top) for top in ("B0","B1","B1p","DC")}
    assert abs(outputs["DC"]["net_kwh"]-outputs["B1p"]["net_kwh"]) < 1e-9


def test_manifest_splits():
    with open("data/generated/bench_v1/manifest.json", encoding="utf-8") as f:
        manifest=json.load(f)
    splits=[set(manifest["splits"][k]) for k in ("train","val","test")]
    assert all(splits)
    assert not (splits[0]&splits[1] or splits[0]&splits[2] or splits[1]&splits[2])
    assert set.union(*splits)==set(manifest["instances"])

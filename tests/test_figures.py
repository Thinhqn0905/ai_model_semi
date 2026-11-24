import pandas as pd
import pytest
from regenate.visualization import plot_forecasting as f, plot_cross_dataset as cross, plot_efficiency as eff, plot_energy_matching as energy, plot_bus_transients as bus, plot_scheduling as sched, plot_ablation as ab, plot_sensitivity as sens, plot_pareto as pareto

def frame(**kw): return pd.DataFrame(dict(boundary=['MOCK']*len(next(iter(kw.values()))), **kw))

@pytest.mark.parametrize('fn,data',[
(f.f01,frame(t=[0,1],actual=[1,2],pred=[1,2],lower=[0,1],upper=[2,3])),
(f.f02,frame(actual=[1,2],pred=[1,2])),
(f.f03,frame(horizon=[1,2],mae=[.1,.2])),
(f.f11,frame(model=['a','a'],error=[.1,.2])),
(f.f12,frame(nominal=[.5,.9],empirical=[.4,.8])),
(cross.f04,frame(train_dataset=['a'],test_dataset=['b'],metric=['nmae'],value=[.2])),
(eff.f05,frame(device=['a'],load_frac=[1],eta=[.9])),
(energy.f06,frame(t_h=[0],source_kw=[2],sink_kw=[3],link_cap_kw=[1])),
(bus.f07,frame(t_s=[0],v_bus=[400],v_min=[380],v_max=[420])),
(ab.f08,frame(instance_id=['i','i'],method=['B1','P'],net_kwh=[2,1])),
(ab.f09,frame(variant=['a'],value=[1])),
(sens.f10,frame(flexibility=[.1],efficiency=[.9],value=[1])),
(sched.f13,frame(method=['B1','ORACLE'],station=[0,0],start_h=[0,1],end_h=[1,2])),
(pareto.f15,frame(model=['m'],latency_ms=[1],mae=[.1])),
])
def test_figures(tmp_path,fn,data):
    fn(data,tmp_path/'figure'); assert (tmp_path/'figure.png').is_file(); assert (tmp_path/'figure.pdf').is_file()

def test_missing_inputs_skip(tmp_path,capsys,monkeypatch):
    from regenate.visualization.generate_all_figures import main
    monkeypatch.chdir(tmp_path); monkeypatch.setattr('sys.argv',['figures','--campaign','missing','--out','out']); main(); assert 'SKIP missing' in capsys.readouterr().out

def test_f14_sankey(tmp_path):
    from regenate.visualization.plot_sankey import f14
    f14(frame(source=['source'], target=['sink'], value=[1]), tmp_path/'sankey')
    assert (tmp_path/'sankey.png').is_file()
    assert (tmp_path/'sankey.pdf').is_file()

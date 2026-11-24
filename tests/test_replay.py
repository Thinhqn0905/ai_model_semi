import json

import pandas as pd
import pytest

from regenate.data.generator import fifo_schedule
from regenate.evaluation.oracle_campaign import execute
from regenate.simulation.replay import Replay


@pytest.fixture
def inst():
    return dict(jobs=pd.DataFrame([
        dict(job_id=j, release_h=0., due_h=8., deadline_h=12., dur_nom_h=1., dur_true_h=1.,
             recipe_id='S1', kappa_true=1., eligible_stations=[0]) for j in range(2)]),
        stations=pd.DataFrame([dict(station_id=0, p_rated_kw=1., downtime_json='[]')]),
        recipe=pd.DataFrame([dict(dur_frac=1., p_in_frac=1., p_rec_frac=0., p_aux_kw=0.)]), dt_h=.25)


def test_fifo_matches_executor(inst):
    assign, starts = fifo_schedule(inst)
    result, _ = Replay(inst, {j: (assign[j], starts[j]) for j in assign}).run()
    assert {j: t for j, (_, t) in result.items()} == execute(inst, assign, starts)


def test_frozen_and_partial_trace(inst):
    def planner(obs):
        if obs['running']:
            j = next(iter(obs['running']))
            assert 'dur_true_h' not in str(obs)
            return {j: (0, 9.)}
        return {}
    result, log = Replay(inst, {0: (0, 0), 1: (0, 1)}, planner).run()
    assert result[0] == (0, 0.)
    assert log.reason.str.contains('frozen').any()


@pytest.mark.parametrize('planner,approve,reason', [
    (lambda obs: 1 / 0, None, 'ZeroDivisionError'),
    (lambda obs: {1: (0, 3.)}, lambda old, new, obs: False, 'engineer_reject'),
    (lambda obs: {1: (7, 3.)}, None, 'infeasible'),
])
def test_fallback(inst, planner, approve, reason):
    result, log = Replay(inst, {0: (0, 0), 1: (0, 1)}, planner, approve=approve).run()
    assert result[1] == (0, 1.)
    assert log.reason.str.contains(reason).any()


def test_downtime_and_determinism(inst):
    inst['stations'].loc[0, 'downtime_json'] = json.dumps([[.5, 1.5]])
    plan = {0: (0, 0), 1: (0, 1)}
    one, log = Replay(inst, plan, seed=7).run()
    two, _ = Replay(inst, plan, seed=7).run()
    assert one == two
    assert all(not (t < 1.5 and t + 1 > .5) for _, t in one.values())


def test_events(inst):
    observations = []
    def planner(obs):
        observations.append(obs)
        return {}
    events = [(0, 'sensor_loss', {'station': 0, 'duration_h': .5}),
              (0, 'mes_disconnect', {'duration_h': .25}),
              (0, 'delay', {'job_id': 0, 'duration_h': .5})]
    result, log = Replay(inst, {0: (0, 0), 1: (0, 2)}, planner, events=events).run()
    assert result[0][1] == .5
    assert observations[0]['stations'][0]['stale']
    assert 'mes_disconnect' in set(log.reason)

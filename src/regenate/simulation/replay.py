"""Discrete-event shadow replay; power traces are synthetic simulation observations."""
import copy
import json
import math
import time

import pandas as pd
import simpy

from regenate.data.generator import render
from regenate.evaluation.oracle_campaign import true_dur


class Replay:
    def __init__(self, inst, initial_plan, replanner=None, period_h=0.25,
                 approve=None, seed=0, events=None, max_solve_s=60.0):
        if period_h <= 0 or max_solve_s < 0:
            raise ValueError("invalid period or solve limit")
        self.inst, self.replanner, self.period_h = inst, replanner, float(period_h)
        self.approve = approve or (lambda old, new, obs: True)
        self.seed, self.events, self.max_solve_s = seed, sorted(events or [], key=lambda e: e[0]), max_solve_s
        self.jobs = {r.job_id: r for r in inst['jobs'].itertuples(index=False)}
        self.stations = {r.station_id: sorted(json.loads(r.downtime_json)) for r in inst['stations'].itertuples(index=False)}
        # lead: run on the render grid (true duration in phase steps, starts ceil-ed to dt) so score() can render it
        self.dt = float(inst['dt_h']); self.dur = {j: true_dur(inst, j) for j in self.jobs}
        self.grid = lambda v: math.ceil(float(v) / self.dt - 1e-9) * self.dt
        self.plan = self._validate(initial_plan, {})
        self.log = []

    def _validate(self, proposal, frozen):
        if not isinstance(proposal, dict) or set(proposal) - set(self.jobs):
            raise ValueError('unknown job or invalid plan')
        for j, value in proposal.items():
            if j in frozen and tuple(value) != tuple(frozen[j]):
                raise ValueError('frozen job modification')
        plan = dict(self.plan) if hasattr(self, 'plan') else {}
        plan.update(proposal)
        if set(plan) != set(self.jobs):
            raise ValueError('missing jobs')
        for j, value in plan.items():
            s, start = value
            if s not in self.stations or s not in self.jobs[j].eligible_stations or not math.isfinite(float(start)) or start < 0:
                raise ValueError('infeasible plan')
            plan[j] = (s, float(start))
        return plan

    def run(self):
        env = simpy.Environment()
        done, running, realised = {}, {}, {}
        stale, disconnected, delays = {}, [], {}
        events = iter(self.events)
        next_event = next(events, None)
        next_replan = 0.0
        eps = 1e-10

        def record(event, accepted, reason='', solve_s=0.0):
            self.log.append(dict(t_h=float(env.now), event=event, accepted=accepted, reason=reason, solve_s=solve_s))

        def finish(j, duration):
            yield env.timeout(duration)
            done[j] = running.pop(j)
            record('finish', True)

        def observation():
            active = {}
            for j, (s, start) in running.items():
                one = dict(self.inst, jobs=self.inst['jobs'].loc[self.inst['jobs'].job_id == j])
                trace = render(one, {j: s}, {j: 0.0}, self.inst['dt_h'], truth=True)
                row = list(self.stations).index(s)
                n = max(0, int(math.floor((env.now - start) / self.inst['dt_h'] + eps)))
                active[j] = dict(station=s, start_h=start, elapsed_h=env.now-start,
                                 partial_power_trace={k: a[row, :n].tolist() for k, a in zip(('p_in_kw', 'p_rec_kw', 'p_aux_kw'), trace)})
            queued = {j: {k: getattr(job, k) for k in ('release_h', 'due_h', 'deadline_h', 'dur_nom_h', 'recipe_id')}
                      for j, job in self.jobs.items() if j not in realised}
            availability = {s: dict(available=not any(a <= env.now < b for a, b in windows) and not any(v[0] == s for v in running.values()),
                                    stale=env.now < stale.get(s, -1)) for s, windows in self.stations.items()}
            return dict(t_h=float(env.now), done=copy.deepcopy(done), running=active, queued=queued, stations=availability)

        def process():
            nonlocal next_event, next_replan
            while len(done) < len(self.jobs):
                yield env.timeout(0)  # process completions scheduled at this same timestamp
                if len(done) == len(self.jobs):
                    break
                while next_event is not None and next_event[0] <= env.now + eps:
                    _, kind, payload = next_event
                    if kind == 'sensor_loss':
                        stale[payload['station']] = env.now + float(payload['duration_h'])
                    elif kind == 'mes_disconnect':
                        disconnected.append(env.now + float(payload['duration_h']))
                    elif kind == 'delay':
                        delays[payload['job_id']] = max(delays.get(payload['job_id'], 0), env.now + float(payload['duration_h']))
                    else:
                        raise ValueError('unknown injected event: ' + str(kind))
                    record(kind, True)
                    next_event = next(events, None)
                if env.now + eps >= next_replan:
                    if self.replanner is not None:
                        if any(env.now < end for end in disconnected):
                            record('replan', False, 'mes_disconnect')
                        else:
                            obs = observation(); old = copy.deepcopy(self.plan); t0 = time.monotonic()
                            try:
                                proposal = self.replanner(copy.deepcopy(obs)); elapsed = time.monotonic() - t0
                                if elapsed > self.max_solve_s:
                                    raise TimeoutError('timeout')
                                candidate = self._validate(proposal, realised)
                                if not self.approve(copy.deepcopy(old), copy.deepcopy(candidate), copy.deepcopy(obs)):
                                    record('replan', False, 'engineer_reject', elapsed)
                                else:
                                    self.plan = candidate; record('replan', True, '', elapsed)
                            except Exception as exc:
                                record('replan', False, f'{type(exc).__name__}: {exc}', time.monotonic()-t0)
                    next_replan += self.period_h
                busy = {s for s, _ in running.values()}
                for j in sorted((j for j in self.jobs if j not in realised), key=lambda j: (self.plan[j][1], j)):
                    s, planned = self.plan[j]; job = self.jobs[j]
                    if s in busy or self.grid(max(planned, float(job.release_h), delays.get(j, 0))) > env.now + eps:
                        continue
                    duration = self.dur[j]
                    if any(env.now < b - eps and env.now + duration > a + eps for a, b in self.stations[s]):
                        continue
                    realised[j] = (s, float(env.now)); running[j] = realised[j]; busy.add(s)
                    record('start', True); env.process(finish(j, duration))
                candidates = [next_replan]
                if next_event is not None: candidates.append(float(next_event[0]))
                candidates += [self.grid(v) for j in self.jobs if j not in realised for v in (self.plan[j][1], self.jobs[j].release_h, delays.get(j, 0)) if self.grid(v) > env.now + eps]
                candidates += [self.grid(b) for windows in self.stations.values() for a, b in windows if self.grid(b) > env.now + eps]
                candidates += [start + self.dur[j] for j, (_, start) in running.items() if start + self.dur[j] > env.now + eps]
                yield env.timeout(max(0, min(candidates) - env.now))
        env.process(process()); env.run()
        return realised, pd.DataFrame(self.log, columns=['t_h', 'event', 'accepted', 'reason', 'solve_s'])

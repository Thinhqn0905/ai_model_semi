import argparse
import copy
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset
from regenate.forecasting import eta, ds05_bench as bench


def past_window(arrays, cycle_file, b, lookback):
    assert b > 0 and lookback > 0
    a = arrays[cycle_file]
    assert all(b <= len(x) for x in a)
    start = max(0, b - lookback)
    assert start < b
    result = np.zeros((4, lookback), dtype=np.float32)
    result[:, -(b-start):] = np.asarray([x[start:b] for x in a], dtype=np.float32)
    return np.nan_to_num(result, nan=0., posinf=0., neginf=0.)


def prepare(cyc, arrays):
    d = eta.remaining_samples(cyc, arrays)
    d = d[d.previous_total.notna()].copy()
    d['abnormal'] = eta.abnormal(d.total, d.previous_total)
    d['progress'] = pd.cut(d.elapsed_min / d.total, [0, .25, .5, .75, 1], labels=['0-25','25-50','50-75','75-100'], include_lowest=True).astype(str)
    reference = eta.remaining_samples(cyc, arrays)
    reference = reference[reference.previous_total.notna()]
    keys = ['use_case', 'cycle_file', 'elapsed_min', 'split']
    assert d[keys].reset_index(drop=True).equals(reference[keys].reset_index(drop=True))
    assert not d.duplicated(keys).any()
    return d.reset_index(drop=True)


class Samples(Dataset):
    def __init__(self, d, arrays, lookback, static):
        self.d, self.arrays, self.lookback, self.static = d.reset_index(drop=True), arrays, lookback, static
    def __len__(self): return len(self.d)
    def __getitem__(self, i):
        r = self.d.iloc[i]
        return (torch.from_numpy(past_window(self.arrays, r.cycle_file, int(r.elapsed_min), self.lookback)),
                torch.from_numpy(self.static[i]), torch.tensor(np.log1p(r.true), dtype=torch.float32))


class Net(nn.Module):
    def __init__(self, n_static):
        super().__init__()
        self.conv = nn.Sequential(nn.Conv1d(4, 16, 3, padding=2), nn.ReLU(),
                                  nn.Conv1d(16, 16, 3, dilation=2, padding=4), nn.ReLU())
        self.head = nn.Sequential(nn.Linear(16 + n_static, 32), nn.ReLU(), nn.Linear(32, 3))
    def forward(self, x, static):
        # Both convolutions are causal: discard the right padding after each layer.
        z = torch.relu(self.conv[0](x))[..., :x.shape[-1]]
        z = torch.relu(self.conv[2](z))[..., :x.shape[-1]]
        return self.head(torch.cat((z[..., -1], static), dim=1))


def run(proc, out, device='cpu', lookback=240, epochs=30, seed=0, patience=5):
    proc, out = Path(proc), Path(out)
    out.mkdir(parents=True, exist_ok=True)
    if lookback < 1 or epochs < 1: raise ValueError('lookback and epochs must be positive')
    torch.manual_seed(seed); np.random.seed(seed); torch.set_num_threads(2)
    dev = torch.device(device)
    cyc = pd.read_parquet(proc / 'ds05_cycles.parquet')
    if 'split' not in cyc or 'ord' not in cyc: cyc = bench.order_cycles(cyc)
    else: cyc = cyc[cyc.error.fillna('') == ''].sort_values(['use_case', 'ord']).copy()
    arrays = {}
    for path in sorted((proc / 'ds05_traces').glob('*.parquet')): arrays.update(bench.cycle_arrays(pd.read_parquet(path)))
    d = prepare(cyc, arrays)
    features = list(bench.features_at(*next(iter(arrays.values())), 60, None))
    raw = d[features].replace([np.inf, -np.inf], np.nan).fillna(-1).to_numpy(dtype=np.float32)
    train_mask = (d.split == 'train').to_numpy()
    mean = raw[train_mask].mean(axis=0); scale = raw[train_mask].std(axis=0); scale[scale < 1e-6] = 1
    cats = pd.get_dummies(d.use_case, dtype=np.float32).to_numpy()
    static = np.concatenate(((raw-mean)/scale, cats), axis=1).astype(np.float32)
    loaders = {}
    for split in ('train', 'val', 'test'):
        mask = (d.split == split).to_numpy()
        if not mask.any(): raise ValueError(f'empty {split} split')
        loaders[split] = DataLoader(Samples(d[mask], arrays, lookback, static[mask]), batch_size=128, shuffle=split == 'train')
    model = Net(static.shape[1]).to(dev); opt = torch.optim.Adam(model.parameters(), lr=.001)
    quantiles = torch.tensor(eta.QS, device=dev)
    scaler = torch.amp.GradScaler('cuda', enabled=dev.type == 'cuda')
    best, stale, state = float('inf'), 0, None
    start = time.perf_counter()
    for epoch in range(epochs):
        model.train()
        for x, s, y in loaders['train']:
            x, s, y = x.to(dev), s.to(dev), y.to(dev)
            opt.zero_grad()
            with torch.autocast(device_type=dev.type, enabled=dev.type == 'cuda'):
                err = y[:, None] - model(x, s); loss = torch.maximum(quantiles*err, (quantiles-1)*err).mean()
            scaler.scale(loss).backward(); scaler.step(opt); scaler.update()
        model.eval(); total = 0.; count = 0
        with torch.no_grad():
            for x, s, y in loaders['val']:
                x, s, y = x.to(dev), s.to(dev), y.to(dev)
                err = y[:, None] - model(x, s); total += torch.maximum(quantiles*err, (quantiles-1)*err).mean().item()*len(y); count += len(y)
        val = total / count
        if val < best: best, stale, state = val, 0, copy.deepcopy(model.state_dict())
        else: stale += 1
        if stale >= patience: break
    if dev.type == 'cuda': torch.cuda.synchronize()
    train_s = time.perf_counter()-start; model.load_state_dict(state)
    def predict(split, target):
        model.to(target).eval(); result = []; start = time.perf_counter()
        with torch.no_grad():
            for x, s, _ in loaders[split]: result.append(model(x.to(target), s.to(target)).cpu().numpy())
        if target.type == 'cuda': torch.cuda.synchronize()
        elapsed = (time.perf_counter()-start)*1000/len(loaders[split].dataset)
        p = np.maximum(np.expm1(np.clip(np.concatenate(result), -20, 20)), 0); p.sort(axis=1)
        return p, elapsed
    pv, _ = predict('val', dev); pt, device_ms = predict('test', dev)
    _, cpu_ms = predict('test', torch.device('cpu'))
    va, te = d[d.split == 'val'], d[d.split == 'test']
    offset = eta.cqr_offset(va.true.to_numpy(), pv[:, 0], pv[:, 2]); calibrated = pt.copy()
    calibrated[:, 0] = np.minimum(np.maximum(pt[:, 0]-offset, 0), pt[:, 1]); calibrated[:, 2] = np.maximum(pt[:, 2]+offset, pt[:, 1])
    previous = np.maximum(te.prev_rem_min.to_numpy(), 0); previous = np.repeat(previous[:, None], 3, axis=1)
    preds = {'previous': previous, 'AI11_tcn': pt, 'AI11_tcn_cqr': calibrated}
    metrics = eta._metrics(te, preds, {'previous': 0, 'AI11_tcn': device_ms, 'AI11_tcn_cqr': device_ms})
    metrics[metrics.model != 'previous'].to_csv(out / 'metrics_tcn.csv', index=False)
    frames = []
    for name in ('AI11_tcn', 'AI11_tcn_cqr'):
        frame = te[['cycle_file', 'use_case', 'true', 'elapsed_min']].copy(); frame['model'] = name
        frame[['q10', 'q50', 'q90']] = preds[name]; frames.append(frame)
    pd.concat(frames, ignore_index=True).to_parquet(out / 'predictions_tcn.parquet', index=False)
    (out / 'manifest.json').write_text(json.dumps(dict(proc=str(proc), seed=seed, lookback=lookback, epochs_run=epoch+1, train_s=train_s,
        device=str(dev), gpu_name=torch.cuda.get_device_name(dev) if dev.type == 'cuda' else None,
        inference_ms_per_sample_gpu=device_ms if dev.type == 'cuda' else None, inference_ms_per_sample_cpu=cpu_ms,
        cqr_offset_minutes=offset, static_features=features, use_cases=sorted(d.use_case.unique().tolist()),
        split='eta T2 input chronological per module', boundary='NOT_VERIFIED_INPUT_DATA'), indent=2))


def main():
    p = argparse.ArgumentParser(); p.add_argument('--proc', required=True); p.add_argument('--out', required=True)
    p.add_argument('--device', default='cpu'); p.add_argument('--lookback', type=int, default=240); p.add_argument('--epochs', type=int, default=30); p.add_argument('--seed', type=int, default=0)
    run(**vars(p.parse_args()))


if __name__ == '__main__': main()

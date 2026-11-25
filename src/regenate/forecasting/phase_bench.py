"""AI14 — next phase-transition timing error on DS05 cycles: time-indexed recipe (AI00) vs phase-aligned recipe (AI15a).
  python -m regenate.forecasting.phase_bench --proc data/ds05_proc --split val --out runs/run3/ai14
Decision points every 15 min from minute 60 (same protocol as Branch C). No training: both predictors use only the
previous cycle of the same module + the observed past of the running cycle.
"""
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
from regenate.data.bench_v2 import load_proc
from regenate.forecasting.phase import segments, is_phase_structured, transition_errors


def run(proc, split="val", stride=15, min_hist=60):
    cyc, arrs = load_proc(proc)
    cyc = cyc.sort_values(["use_case", "ord"]); rows = []
    for uc, g in cyc.groupby("use_case"):
        files = g.cycle_file.tolist(); spl = g.split.tolist()
        for i in range(1, len(files)):
            if spl[i] != split:
                continue
            ch, ds = arrs[files[i]][:2]; pch, pds = arrs[files[i - 1]][:2]
            struct = is_phase_structured(segments(pch, pds))
            for b, er, ea in transition_errors(ch, ds, pch, pds, range(min_hist, len(ch), stride)):
                rows.append(dict(use_case=uc, cycle_file=files[i], b=b, structured=struct, err_recipe_min=er, err_aligned_min=ea))
    return pd.DataFrame(rows)


def summarise(d):
    g = d.groupby(["use_case", "structured"])
    out = g.agg(n=("b", "size"), mae_recipe=("err_recipe_min", "mean"), mae_aligned=("err_aligned_min", "mean"),
                med_recipe=("err_recipe_min", "median"), med_aligned=("err_aligned_min", "median"),
                miss_recipe=("err_recipe_min", lambda x: x.isna().mean()), miss_aligned=("err_aligned_min", lambda x: x.isna().mean()))
    out["skill_aligned"] = 1 - out.mae_aligned / out.mae_recipe
    return out.reset_index()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--proc", required=True); ap.add_argument("--split", default="val")
    ap.add_argument("--out", required=True); a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    d = run(a.proc, a.split); d.to_parquet(out / f"ai14_{a.split}.parquet", index=False)
    s = summarise(d); s.to_csv(out / f"ai14_{a.split}_summary.csv", index=False); print(s.round(3).to_string(index=False))
    (out / "manifest.json").write_text(json.dumps(dict(args=vars(a), n=len(d)), indent=1))


if __name__ == "__main__":
    main()

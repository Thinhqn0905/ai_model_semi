"""Sensitivity figures from the completed, paired simulation campaign."""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from .common import save

SWEEPS = ("flex", "eta_afe", "eta_link", "p_link_max", "n_stations", "allow_export")
CAPTION = ("SIM_ASSUMED_PROFILE | B1p-OPT − ORACLE at M0; paired 95% CI. "
           "Solver gaps are not included in CI; see sensitivity report.")


def f10(df, out):
    # Keep the generic heatmap interface used by existing callers.
    if "sweep" not in df.columns:
        table = df.pivot(index="flexibility", columns="efficiency", values="value")
        fig, ax = plt.subplots()
        im = ax.imshow(table, aspect="auto", origin="lower")
        ax.set_xticks(range(len(table.columns)), table.columns)
        ax.set_yticks(range(len(table.index)), table.index)
        ax.set(xlabel="Efficiency", ylabel="Flexibility")
        fig.colorbar(im, ax=ax)
        save(fig, df, out)
        return

    rows = df[df.sweep.isin(SWEEPS) & (df.scenario == "S3") & (df.n > 0)].copy()
    rows["label"] = rows.sweep.astype(str) + " = " + rows.value.astype(str)
    fig, axes = plt.subplots(1, 2, figsize=(13, max(7, len(rows) * .3)), sharey=True)
    positions = list(range(len(rows)))
    for ax, metric, unit in zip(axes, ("gain_kwh", "gain_pct"), ("kWh", "%")):
        ax.barh(positions, rows[metric + "_mean"], color="#467aa5", alpha=.8)
        ax.hlines(positions, rows[metric + "_lo"], rows[metric + "_hi"], color="black", linewidth=1.2)
        ax.axvline(0, color="black", linewidth=.8, label="S1 control ≈ 0")
        ax.set_xlabel("Gain (" + unit + ")")
        ax.legend(loc="lower right", fontsize=8)
    axes[0].set_yticks(positions, rows.label)
    axes[0].invert_yaxis()
    fig.suptitle("One-at-a-time sensitivity: S3 gain and S1 control")
    fig.text(.5, .01, CAPTION, ha="center", fontsize=8)
    fig.tight_layout(rect=(0, .035, 1, .97))
    save(fig, df[df.boundary == "SIM_ASSUMED_PROFILE"], out)


def f10b(df, out):
    rows = df[(df.sweep == "flex") & (df.scenario == "S3") & (df.n > 0)].copy()
    rows["flex_numeric"] = pd.to_numeric(rows.value)
    rows = rows.sort_values("flex_numeric")
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(rows.flex_numeric, rows.gain_kwh_mean, marker="o", color="#467aa5")
    ax.fill_between(rows.flex_numeric.to_numpy(), rows.gain_kwh_lo.to_numpy(), rows.gain_kwh_hi.to_numpy(), alpha=.25, color="#467aa5", label="95% CI")
    ax.axhline(0, color="black", linewidth=.8, label="S1 control ≈ 0")
    ax.set(xlabel="Flexibility", ylabel="S3 gain (kWh)", title="Gain versus flexibility")
    ax.legend()
    fig.text(.5, .01, CAPTION, ha="center", fontsize=7)
    fig.tight_layout(rect=(0, .05, 1, 1))
    save(fig, df[df.boundary == "SIM_ASSUMED_PROFILE"], out)


def f10_grid(df, out):
    rows = df[(df.sweep == "grid") & (df.scenario == "S3") & (df.n > 0)].copy()
    if rows.empty:
        return False
    parts = rows.value.astype(str).str.split("_eta_", n=1, expand=True)
    rows["flex"] = pd.to_numeric(parts[0])
    rows["eta"] = pd.to_numeric(parts[1])
    table = rows.pivot(index="flex", columns="eta", values="gain_kwh_mean").sort_index()
    fig, ax = plt.subplots(figsize=(6, 4.5))
    im = ax.imshow(table, aspect="auto", origin="lower")
    ax.set_xticks(range(len(table.columns)), table.columns)
    ax.set_yticks(range(len(table.index)), table.index)
    ax.set(xlabel="Link efficiency", ylabel="Flexibility", title="S3 gain (kWh)")
    for y in range(len(table.index)):
        for x in range(len(table.columns)):
            value = table.iloc[y, x]
            if pd.notna(value):
                ax.text(x, y, f"{value:.2f}", ha="center", va="center", color="white")
    fig.colorbar(im, ax=ax, label="B1p-OPT − ORACLE (kWh)")
    fig.text(.5, .01, "SIM_ASSUMED_PROFILE | Mean gain; blank cells are missing.", ha="center", fontsize=8)
    fig.tight_layout(rect=(0, .05, 1, 1))
    save(fig, df[df.boundary == "SIM_ASSUMED_PROFILE"], out)
    return True


if __name__ == "__main__":
    data = pd.read_csv("runs/sens_v1/sensitivity_results.csv")
    destination = Path("reports/figures")
    destination.mkdir(parents=True, exist_ok=True)
    f10(data, destination / "F10")
    f10b(data, destination / "F10b")
    f10_grid(data, destination / "F10_grid")


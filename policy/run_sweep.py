# policy/run_sweep.py
"""
Run the elasticity x seed robustness sweep locally.

Same grid as notebooks/05_sweep_colab.ipynb, but writes straight into results/
instead of policy/ (the notebook's outputs were moved by hand afterwards).
Resumable: rerunning skips (elasticity, seed) pairs already in the CSV.

Writes:
  results/sweep_results.csv    one row per (elasticity, seed)
  results/sweep_summary.csv    mean +/- sd across seeds
  results/sweep_headline.csv   formatted robustness table
  results/figures/sweep_robustness.png
  models/sweep/                per-run weights (gitignored)

Run:  python -m policy.run_sweep
"""

from __future__ import annotations

import time
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import policy.sweep as sw

ROOT     = Path(__file__).resolve().parent.parent
RESULTS  = ROOT / "results"
FIGURES  = RESULTS / "figures"
SAVE_DIR = ROOT / "models" / "sweep"
for d in (RESULTS, FIGURES, SAVE_DIR):
    d.mkdir(parents=True, exist_ok=True)

ELASTICITIES    = [0.7, 0.8, 0.9, 1.0]   # above the degenerate boundary (~0.65)
SEEDS           = [0, 1, 2, 3, 4]
TOTAL_TIMESTEPS = 500_000                # same budget as the headline run
EVAL_EPISODES   = 300


def main():
    print(f"Sweep at adoption {sw.ADOPTION}x — "
          f"{len(ELASTICITIES)} elasticities x {len(SEEDS)} seeds "
          f"= {len(ELASTICITIES) * len(SEEDS)} runs")

    t0 = time.time()
    df = sw.run_sweep(
        elasticities=ELASTICITIES,
        seeds=SEEDS,
        total_timesteps=TOTAL_TIMESTEPS,
        eval_episodes=EVAL_EPISODES,
        out_csv=str(RESULTS / "sweep_results.csv"),
        save_dir=str(SAVE_DIR),
        verbose=True,
    )
    print(f"\nDone in {(time.time() - t0) / 60:.1f} min. {len(df)} runs.")

    summary = sw.summarise(df)
    summary.to_csv(RESULTS / "sweep_summary.csv")
    pd.set_option("display.width", 220, "display.max_columns", 40)
    print("\n" + summary.to_string())

    rows = []
    for e, g in df.groupby("elasticity"):
        rows.append({
            "elasticity": e,
            "lambda": round(g["lambda"].iloc[0], 3),
            "PPO": f"{g['PPO_score'].mean():.1f} ± {g['PPO_score'].std():.1f}",
            "ToU": f"{g['ToU_score'].mean():.1f}",
            "ToU3 (3-band)": f"{g['ToU3_score'].mean():.1f}",
            "Flat": f"{g['Flat_score'].mean():.1f}",
            "Congestion (oracle)": f"{g['Congestion_score'].mean():.1f}",
            "PPO - ToU": f"{g['margin_vs_ToU'].mean():+.1f} ± {g['margin_vs_ToU'].std():.1f}",
            "PPO - ToU3": f"{g['margin_vs_ToU3'].mean():+.1f} ± {g['margin_vs_ToU3'].std():.1f}",
        })
    tbl = pd.DataFrame(rows)
    tbl.to_csv(RESULTS / "sweep_headline.csv", index=False)
    print("\n" + tbl.to_string(index=False))

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))
    g = df.groupby("elasticity")

    ax = axes[0]
    ax.errorbar(g["PPO_score"].mean().index, g["PPO_score"].mean(),
                yerr=g["PPO_score"].std(), marker="o", capsize=4,
                label="PPO (±1 sd over seeds)")
    for col, lab, st in [("ToU_score", "ToU (2-band)", "--"),
                         ("ToU3_score", "ToU (3-band)", ":"),
                         ("Flat_score", "Flat £0.30", "-."),
                         ("Congestion_score", "Congestion oracle", "-")]:
        ax.plot(g[col].mean().index, g[col].mean(), st, marker="s", ms=4,
                alpha=0.7, label=lab)
    ax.set_xlabel("price elasticity")
    ax.set_ylabel("score (revenue − λ·wait)")
    ax.set_title("Policy score vs demand elasticity")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[1]
    m, s = g["margin_vs_ToU"].mean(), g["margin_vs_ToU"].std()
    ax.bar(m.index.astype(str), m.values, yerr=s.values, capsize=4, alpha=0.8)
    ax.axhline(0, color="k", lw=1)
    ax.set_xlabel("price elasticity")
    ax.set_ylabel("PPO − ToU (score)")
    ax.set_title("PPO advantage over handcrafted ToU")
    ax.grid(alpha=0.3, axis="y")

    plt.tight_layout()
    plt.savefig(FIGURES / "sweep_robustness.png", dpi=150)
    plt.close(fig)
    print(f"\nsaved {FIGURES / 'sweep_robustness.png'}")


if __name__ == "__main__":
    main()

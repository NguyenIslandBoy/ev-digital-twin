import pandas as pd, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

NAVY, TEAL, AMBER = "#123B5C", "#1B9AAA", "#E4A02A"

CSV = Path("results/ppo_price_by_hour.csv")
OUT = Path("results/figures/ppo_price_by_hour.png")
OUT.parent.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(CSV)
h, p = df["hour"].values, df["price"].values

# handcrafted 2-band ToU: £0.45 peak 07:00-19:00, £0.15 otherwise
tou = np.where((h >= 7) & (h <= 19), 0.45, 0.15)

fig, ax = plt.subplots(figsize=(10, 5.2))

# shade where ToU overcharges relative to the learned policy
ax.fill_between(h, p, tou, where=(tou > p), interpolate=True,
                color=AMBER, alpha=0.13, zorder=1)

for lvl in (0.15, 0.30, 0.45):
    ax.axhline(lvl, color="#D8DFE5", lw=1, zorder=0)

ax.step(h, tou, where="mid", color=NAVY, lw=2.4, ls="--",
        label="Handcrafted ToU (clock-based)", zorder=3)
ax.plot(h, p, color=AMBER, lw=3.4, marker="o", ms=6,
        markerfacecolor="white", markeredgewidth=2.2,
        label="PPO learned policy", zorder=4)

ax.annotate("expensive while\nqueues build", xy=(11, 0.427), xytext=(10.6, 0.492),
            ha="center", fontsize=11, color="#9A6B10", fontweight="bold")
ax.annotate("cheap once the day's\ndemand is largely spent", xy=(19, 0.151),
            xytext=(19.4, 0.212), ha="center", fontsize=11,
            color="#9A6B10", fontweight="bold")
ax.annotate("ToU still charging peak\nwith no queue to manage", xy=(17.2, 0.30),
            xytext=(13.0, 0.335), fontsize=10.5, color=NAVY, style="italic",
            arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.4,
                            connectionstyle="arc3,rad=-0.25"))

ax.set_xlim(-0.6, 23.6)
ax.set_ylim(0.10, 0.545)
ax.set_xticks(range(0, 24, 2))
ax.set_xticklabels([f"{x:02d}" for x in range(0, 24, 2)], fontsize=11)
ax.set_yticks([0.15, 0.30, 0.45])
ax.set_yticklabels(["£0.15", "£0.30", "£0.45"], fontsize=12, fontweight="bold")
ax.set_xlabel("Hour of day", fontsize=12.5)
ax.set_ylabel("Mean price per kWh", fontsize=12.5)
ax.set_title("What the agent learned: price the congestion, not the clock",
             fontsize=14.5, fontweight="bold", color=NAVY, pad=12)

for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color("#B8C4CE")

ax.legend(loc="upper left", frameon=False, fontsize=11.5)
ax.text(0.5, -0.2,
        "Mean across 500 episodes. Intermediate values (e.g. 08:00, 14:00) are hours where the agent "
        "switches tariff\ndepending on live queue state, which a fixed clock schedule cannot produce.",
        transform=ax.transAxes, ha="center", fontsize=10, color="#5A6C78")

plt.tight_layout()
plt.savefig(OUT, dpi=220, bbox_inches="tight")
print(f"saved {OUT}")
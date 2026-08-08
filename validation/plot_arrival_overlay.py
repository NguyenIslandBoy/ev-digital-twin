import duckdb, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

NAVY, TEAL, AMBER = "#123B5C", "#1B9AAA", "#E4A02A"

ROOT = Path(__file__).resolve().parent.parent
OUT  = ROOT / "results" / "figures" / "arrival_vs_tou_window.png"

con = duckdb.connect(str(ROOT / "data" / "ev_twin.duckdb"), read_only=True)
df = con.execute("""
    SELECT EXTRACT(hour FROM session_start) AS hour, COUNT(*) AS n
    FROM charging_sessions GROUP BY 1 ORDER BY 1
""").df()
con.close()

hours = np.arange(24)
counts = np.zeros(24)
counts[df["hour"].astype(int).values] = df["n"].values
top = counts.max()

fig, ax = plt.subplots(figsize=(10, 5))
ax.axvspan(6.5, 19.5, color=NAVY, alpha=0.11, zorder=0)
ax.bar(hours, counts, color=TEAL, width=0.75, zorder=2)
ax.set_ylim(0, top * 1.36)                      # headroom so text clears the bars

ax.text(13, top * 1.27, "ToU 'peak' window  (07:00–19:00)",
        ha="center", fontsize=13, fontweight="bold", color=NAVY)

ax.text(23.5, top * 1.15,
        "all demand sits inside\nthe peak window \na clock-based tariff has\nnothing to discriminate on",
        ha="right", va="top", fontsize=11.5, fontweight="bold",
        color=AMBER, linespacing=1.45, zorder=5)

ax.set_xticks(range(0, 24, 2)); ax.set_xlim(-0.7, 23.7)
ax.set_xlabel("Hour of day", fontsize=13)
ax.set_ylabel("Sessions", fontsize=13)
ax.set_title("Real arrivals vs the ToU peak window", fontsize=15,
             fontweight="bold", color=NAVY, pad=12)
ax.tick_params(labelsize=12)
for s in ("top", "right"): ax.spines[s].set_visible(False)
plt.tight_layout()
plt.savefig(OUT, dpi=220, bbox_inches="tight")
print(f"saved {OUT}")
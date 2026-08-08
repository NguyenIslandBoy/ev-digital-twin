# validation/regenerate_results.py
"""
Regenerate every results/ artefact that does NOT require a trained PPO agent.

Covers the calibration report, the Phase 5 scenario evaluation and the
elasticity boundary scan - i.e. everything notebooks 02 and 03 produce, plus
the arrival-timing gate. The PPO artefacts (eval_*, ppo_*, sweep_*) require
retraining and are listed as stale at the end rather than touched.

Reads the DuckDB read-only; writes only into results/.

Run:  python -m validation.regenerate_results
"""

from __future__ import annotations

import duckdb
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats
from scipy.stats import nbinom

from simulation.model import ChargingNetworkModel
from simulation.agents import _sample_connector, _sample_duration, _sample_energy
from simulation.config import DB_PATH, STEPS_PER_DAY, NB_R, NB_P
from simulation.scenario_engine import ScenarioEngine, SCENARIOS
import policy.sweep as sweep

ROOT     = Path(__file__).resolve().parent.parent
RESULTS  = ROOT / "results"
FIGURES  = RESULTS / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)

N_EPISODES = 500
BASE_SEED  = 42

sns.set_theme(style="whitegrid")


# ── real data ─────────────────────────────────────────────────────────────────
def load_real() -> dict:
    con = duckdb.connect(str(DB_PATH), read_only=True)
    real = {
        "sessions": con.execute(
            "SELECT COUNT(*) AS s FROM charging_sessions "
            "GROUP BY DATE_TRUNC('day', session_start)"
        ).df()["s"].to_numpy(),
        "energies": con.execute(
            "SELECT energy_kwh FROM charging_sessions"
        ).df()["energy_kwh"].to_numpy(),
        "durations": con.execute(
            "SELECT duration_hrs FROM charging_sessions WHERE duration_hrs IS NOT NULL"
        ).df()["duration_hrs"].to_numpy(),
        "hours": con.execute(
            "SELECT EXTRACT(hour FROM session_start)::INT AS h FROM charging_sessions"
        ).df()["h"].to_numpy(),
    }
    con.close()
    return real


def _kde_pair(sim, real, title, xlabel, out, xlim=None):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.kdeplot(sim,  ax=ax, label="Simulated", fill=True, alpha=0.4)
    sns.kdeplot(real, ax=ax, label="Real",      fill=True, alpha=0.4)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    if xlim:
        ax.set_xlim(*xlim)
    ax.legend()
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close(fig)


# ── 1. calibration ────────────────────────────────────────────────────────────
def calibration(real: dict) -> pd.DataFrame:
    print(f"[1/3] Calibration ({N_EPISODES} episodes)...")

    sim, arrival_hours = [], []
    for i in range(N_EPISODES):
        m = ChargingNetworkModel(seed=i)
        prev = 0
        for step in range(STEPS_PER_DAY):
            m.step()
            arrival_hours.extend([(step * 30) // 60] * (m.ev_agent_counter - prev))
            prev = m.ev_agent_counter
        sim.append(m.get_kpis())

    sessions = np.array([r["sessions_completed"] for r in sim])
    arrival_hours = np.array(arrival_hours)

    # Energy and duration are sampled directly: the twin consumes exactly these
    # samplers, so this tests the fitted distributions, not the twin's dynamics.
    rng = np.random.default_rng(0)
    sim_energy = np.array([_sample_energy(_sample_connector(rng), rng)
                           for _ in range(5000)])
    rng = np.random.default_rng(0)
    sim_duration = np.array([_sample_duration(_sample_connector(rng), rng)
                             for _ in range(5000)])

    real_hours = np.repeat(np.arange(24), np.bincount(real["hours"], minlength=24))

    rows = []
    for name, s, r in [
        ("Sessions per day",  sessions,      real["sessions"]),
        ("Energy per session", sim_energy,   real["energies"]),
        ("Session duration",  sim_duration,  real["durations"]),
        ("Arrival hour",      arrival_hours, real_hours),
    ]:
        ks, _ = stats.ks_2samp(s, r)
        rows.append({"distribution": name, "ks_statistic": round(float(ks), 4),
                     "sim_mean": round(float(np.mean(s)), 4),
                     "real_mean": round(float(np.mean(r)), 4)})

    _kde_pair(sessions, real["sessions"], "Sessions per Day - Simulated vs Real",
              "Sessions", FIGURES / "calibration_sessions.png")
    _kde_pair(sim_energy, real["energies"], "Energy per Session - Simulated vs Real",
              "kWh", FIGURES / "calibration_energy.png", xlim=(0, 120))
    _kde_pair(sim_duration, real["durations"], "Session Duration - Simulated vs Real",
              "Hours", FIGURES / "calibration_duration.png", xlim=(0, 4))

    # Negative-Binomial fit against real daily counts (independent of the twin)
    nb = nbinom.rvs(n=NB_R, p=NB_P, size=5000, random_state=42)
    _kde_pair(nb, real["sessions"],
              "Sessions per Day - Negative Binomial Fit vs Real", "Sessions",
              FIGURES / "calibration_nb_fit.png")

    # Arrival-timing gate: the check that a KS on daily counts cannot make.
    fig, ax = plt.subplots(figsize=(10, 5))
    hours = np.arange(24)
    width = 0.42
    ax.bar(hours - width / 2, np.bincount(arrival_hours, minlength=24) / len(arrival_hours),
           width=width, label="Simulated", color="#1B9AAA")
    ax.bar(hours + width / 2, np.bincount(real["hours"], minlength=24) / len(real["hours"]),
           width=width, label="Real", color="#123B5C")
    ax.set_title("Arrival Hour - Simulated vs Real")
    ax.set_xlabel("Hour of day")
    ax.set_ylabel("Share of arrivals")
    ax.set_xticks(range(0, 24, 2))
    ax.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "calibration_arrival.png", dpi=150)
    plt.close(fig)

    df = pd.DataFrame(rows)
    df.to_csv(RESULTS / "calibration_summary.csv", index=False)
    print(df.to_string(index=False))
    return df


# ── 2. Phase 5 scenarios ──────────────────────────────────────────────────────
def scenarios() -> tuple[pd.DataFrame, pd.DataFrame]:
    print(f"\n[2/3] Scenarios ({len(SCENARIOS)} x {N_EPISODES} episodes)...")
    engine  = ScenarioEngine(n_episodes=N_EPISODES, base_seed=BASE_SEED)
    results = engine.run_all()
    summary = engine.compare_kpis(results)

    kpi_cols = ["sessions_completed", "energy_kwh", "revenue_gbp",
                "co2_g", "avg_wait_hrs", "avg_utilisation"]

    sig = pd.concat([engine.wilcoxon_vs_baseline(results, kpi=k) for k in kpi_cols],
                    ignore_index=True)
    sig_out = sig[["scenario", "kpi", "p_value", "significant"]].rename(
        columns={"p_value": "wilcoxon_p_vs_baseline"})
    sig_out.to_csv(RESULTS / "scenario_significance.csv", index=False)

    # headline table: one row per scenario, revenue-significance as the p-value
    rev_p = dict(zip(sig[sig.kpi == "revenue_gbp"]["scenario"],
                     sig[sig.kpi == "revenue_gbp"]["p_value"]))
    head = pd.DataFrame({
        "scenario":        summary["scenario"],
        "sessions_completed": summary["sessions_completed_mean"],
        "revenue_gbp":     summary["revenue_gbp_mean"],
        "co2_g":           summary["co2_g_mean"],
        "avg_wait_hrs":    summary["avg_wait_hrs_mean"],
        "avg_utilisation": summary["avg_utilisation_mean"],
    }).reset_index(drop=True)
    head["wilcoxon_p_vs_baseline"] = head["scenario"].map(rev_p)
    head.to_csv(RESULTS / "scenario_summary.csv", index=False)

    # figures (same three notebook 03 produces)
    fig, ax = plt.subplots(figsize=(12, 5))
    for key, df in results.items():
        sns.kdeplot(df["sessions_completed"], ax=ax, label=SCENARIOS[key].name,
                    fill=False, linewidth=2)
    ax.set_title("Sessions per Day - All Scenarios")
    ax.set_xlabel("Sessions"); ax.set_ylabel("Density"); ax.legend(fontsize=9)
    plt.tight_layout(); plt.savefig(FIGURES / "scenario_sessions.png", dpi=150)
    plt.close(fig)

    kpi_labels = {"sessions_completed_mean": "Sessions/Day",
                  "energy_kwh_mean": "Energy (kWh)", "co2_g_mean": "CO2 (gCO2)",
                  "avg_wait_hrs_mean": "Avg Wait (hrs)",
                  "avg_utilisation_mean": "Utilisation Rate"}
    fig, axes = plt.subplots(1, 5, figsize=(18, 5))
    for ax, (col, label) in zip(axes, kpi_labels.items()):
        vals = summary[col].values
        names = [s[:18] for s in summary["scenario"].values]
        colours = ["steelblue" if v <= vals[0] else "tomato" for v in vals]
        ax.barh(names, vals, color=colours)
        ax.axvline(vals[0], color="black", linestyle="--", linewidth=1)
        ax.set_title(label, fontsize=10); ax.set_xlabel(label, fontsize=8)
    plt.suptitle("KPI Comparison Across Scenarios", fontsize=13, y=1.02)
    plt.tight_layout()
    plt.savefig(FIGURES / "scenario_kpi_comparison.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    for key, df in results.items():
        sns.kdeplot(df["co2_g"], ax=axes[0], label=SCENARIOS[key].name,
                    fill=False, linewidth=2)
    axes[0].set_title("CO2 Emissions per Day - All Scenarios")
    axes[0].set_xlabel("gCO2"); axes[0].legend(fontsize=8)
    axes[1].scatter(summary["co2_g_mean"], summary["revenue_gbp_mean"], s=120, zorder=5)
    for _, row in summary.iterrows():
        axes[1].annotate(row["scenario"][:15],
                         (row["co2_g_mean"], row["revenue_gbp_mean"]),
                         textcoords="offset points", xytext=(5, 5), fontsize=8)
    axes[1].set_title("Revenue vs CO2 - Scenario Trade-offs")
    axes[1].set_xlabel("Mean CO2 (gCO2)"); axes[1].set_ylabel("Mean Revenue (GBP)")
    plt.tight_layout(); plt.savefig(FIGURES / "scenario_co2_revenue.png", dpi=150)
    plt.close(fig)

    print(head.round(4).to_string(index=False))
    return head, sig_out


# ── 3. elasticity boundary ────────────────────────────────────────────────────
def elasticity_boundary() -> pd.DataFrame:
    print(f"\n[3/3] Elasticity boundary (adoption {sweep.ADOPTION}x)...")
    rows = []
    for e in (0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2):
        lam, diag = sweep.derive_lambda(e, n_episodes=200)
        rows.append({"elasticity": e, "lambda": lam,
                     "status": "ok" if lam is not None else "degenerate",
                     "r30": diag["r30"], "w30": diag["w30"],
                     "r45": diag["r45"], "w45": diag["w45"]})
        print(f"  elasticity {e}: "
              + (f"lambda {lam:.3f}" if lam is not None else "DEGENERATE"))
    df = pd.DataFrame(rows)
    df.to_csv(RESULTS / "elasticity_boundary.csv", index=False)
    return df


# Produced by the training pipeline, not by this script. If the simulator or
# the regime changes, these must be REGENERATED BY RETRAINING - rerunning this
# script will not touch them, and leaving them stale silently mixes results
# from two different simulators in one folder.
FROM_TRAINING = {
    "python -m policy.train": [
        "evaluations.npz", "figures/ppo_learning_curve.png",
    ],
    "python -m policy.evaluate": [
        "eval_results.csv", "eval_summary.csv", "ppo_price_by_hour.csv",
    ],
    "python validation/plot_price_by_hour.py": [
        "figures/ppo_price_by_hour.png",
    ],
    "python -m policy.run_sweep": [
        "sweep_results.csv", "sweep_summary.csv", "sweep_headline.csv",
        "figures/sweep_robustness.png",
    ],
}


def main():
    calibration(load_real())
    scenarios()
    elasticity_boundary()
    print("\nRegenerated calibration, scenario and elasticity artefacts.")
    print("\nNOT produced here - these come from the training pipeline:")
    for cmd, files in FROM_TRAINING.items():
        print(f"  {cmd}")
        for f in files:
            print(f"      results/{f}")


if __name__ == "__main__":
    main()

# analysis/distributions.py

import duckdb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pathlib import Path

from ingestion.config import DB_PATH

OUTPUT_DIR = Path("analysis/outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_sessions() -> pd.DataFrame:
    con = duckdb.connect(str(DB_PATH))
    df = con.execute("""
        SELECT
            session_start,
            session_stop,
            energy_kwh,
            duration_hrs,
            connector_type,
            charger_id,
            month,
            season,
            day,
            carbon_intensity_gco2_kwh
        FROM charging_sessions
    """).df()
    con.close()
    df["hour"]       = df["session_start"].dt.hour
    df["is_weekend"] = df["session_start"].dt.dayofweek >= 5
    return df


def fit_distribution(data: np.ndarray, name: str) -> dict:
    """Try lognormal and gamma fits, return the better one by AIC."""
    results = {}
    for dist_name, dist in [("lognormal", stats.lognorm), ("gamma", stats.gamma)]:
        params = dist.fit(data, floc=0)
        log_likelihood = np.sum(dist.logpdf(data, *params))
        k = len(params)
        aic = 2 * k - 2 * log_likelihood
        results[dist_name] = {"params": params, "aic": aic}

    best = min(results, key=lambda x: results[x]["aic"])
    print(f"  {name}: best fit = {best} (AIC={results[best]['aic']:.1f})")
    return {"best": best, **results}


def plot_arrival_distribution(df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Overall hourly arrivals
    df["hour"].value_counts().sort_index().plot(
        kind="bar", ax=axes[0], color="steelblue"
    )
    axes[0].set_title("Arrivals by Hour of Day")
    axes[0].set_xlabel("Hour")
    axes[0].set_ylabel("Number of Sessions")

    # Weekday vs weekend
    for label, group in df.groupby("is_weekend"):
        tag = "Weekend" if label else "Weekday"
        group["hour"].value_counts().sort_index().plot(
            kind="line", ax=axes[1], label=tag
        )
    axes[1].set_title("Arrivals by Hour — Weekday vs Weekend")
    axes[1].set_xlabel("Hour")
    axes[1].set_ylabel("Number of Sessions")
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "arrival_distribution.png", dpi=150)
    plt.show()
    print("Saved: arrival_distribution.png")


def plot_energy_distribution(df: pd.DataFrame, fit: dict) -> None:
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(df["energy_kwh"], bins=60, stat="density", ax=ax, color="steelblue")

    x = np.linspace(df["energy_kwh"].min(), df["energy_kwh"].max(), 200)
    best = fit["best"]
    if best == "lognormal":
        ax.plot(x, stats.lognorm.pdf(x, *fit["lognormal"]["params"]),
                "r-", lw=2, label="Lognormal fit")
    else:
        ax.plot(x, stats.gamma.pdf(x, *fit["gamma"]["params"]),
                "r-", lw=2, label="Gamma fit")

    ax.set_title("Energy Demand Distribution (kWh)")
    ax.set_xlabel("kWh")
    ax.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "energy_distribution.png", dpi=150)
    plt.show()
    print("Saved: energy_distribution.png")


def plot_duration_distribution(df: pd.DataFrame, fit: dict) -> None:
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(df["duration_hrs"], bins=60, stat="density", ax=ax, color="steelblue")

    x = np.linspace(df["duration_hrs"].min(), df["duration_hrs"].max(), 200)
    best = fit["best"]
    if best == "lognormal":
        ax.plot(x, stats.lognorm.pdf(x, *fit["lognormal"]["params"]),
                "r-", lw=2, label="Lognormal fit")
    else:
        ax.plot(x, stats.gamma.pdf(x, *fit["gamma"]["params"]),
                "r-", lw=2, label="Gamma fit")

    ax.set_title("Session Duration Distribution (hrs)")
    ax.set_xlabel("Hours")
    ax.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "duration_distribution.png", dpi=150)
    plt.show()
    print("Saved: duration_distribution.png")


def plot_seasonal_patterns(df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    df.groupby("season")["energy_kwh"].mean().plot(
        kind="bar", ax=axes[0], color="steelblue"
    )
    axes[0].set_title("Average Energy Demand by Season")
    axes[0].set_xlabel("Season")
    axes[0].set_ylabel("Avg kWh")

    df.groupby("day")["energy_kwh"].count().reindex([
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ]).plot(kind="bar", ax=axes[1], color="steelblue")
    axes[1].set_title("Session Count by Day of Week")
    axes[1].set_xlabel("Day")
    axes[1].set_ylabel("Number of Sessions")

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "seasonal_patterns.png", dpi=150)
    plt.show()
    print("Saved: seasonal_patterns.png")


def run_analysis() -> dict:
    print("Loading sessions from DuckDB...")
    df = load_sessions()
    print(f"Loaded {len(df)} sessions\n")

    print("Fitting distributions...")
    energy_fit   = fit_distribution(df["energy_kwh"].values,   "energy_kwh")
    duration_fit = fit_distribution(df["duration_hrs"].values, "duration_hrs")

    print("\nGenerating plots...")
    plot_arrival_distribution(df)
    plot_energy_distribution(df, energy_fit)
    plot_duration_distribution(df, duration_fit)
    plot_seasonal_patterns(df)

    # Summary stats for simulation config
    summary = {
        "n_sessions":         len(df),
        "n_chargers":         df["charger_id"].nunique(),
        "energy_fit":         energy_fit,
        "duration_fit":       duration_fit,
        "arrival_by_hour":    df["hour"].value_counts().sort_index().to_dict(),
        "connector_mix":      df["connector_type"].value_counts(normalize=True).to_dict(),
        "weekday_ratio":      float((~df["is_weekend"]).mean()),
    }

    print("\n=== Summary ===")
    print(f"Chargers        : {summary['n_chargers']}")
    print(f"Connector mix   : {summary['connector_mix']}")
    print(f"Weekday ratio   : {summary['weekday_ratio']:.2%}")

    return summary


if __name__ == "__main__":
    run_analysis()
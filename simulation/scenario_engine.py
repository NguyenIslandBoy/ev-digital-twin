# simulation/scenario_engine.py

import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from simulation.model import ChargingNetworkModel
from simulation.config import (
    RANDOM_SEED,
    WEEKDAY_RATIO,
    STEPS_PER_DAY,
    PRICE_PER_KWH,
)


# ── SCENARIO DEFINITIONS ──────────────────────────────────────────────────────

@dataclass
class Scenario:
    """
    Defines a single simulation scenario with its parameter overrides.
    All parameters not specified default to baseline values.
    """
    name:                str
    adoption_multiplier: float = 1.0
    carbon_penalty:      float = 0.0
    tou_pricing:         bool  = False
    description:         str   = ""

    # ToU price schedule - price per kWh by hour (0-23)
    # Default: flat rate from config
    tou_schedule:        dict  = field(default_factory=dict)

    def get_price(self, hour: int) -> float:
        """Return price per kWh for a given hour."""
        if self.tou_pricing and self.tou_schedule:
            return self.tou_schedule.get(hour, PRICE_PER_KWH)
        return PRICE_PER_KWH


# ── BUILT-IN SCENARIOS ────────────────────────────────────────────────────────

# Two-rate ToU schedule: peak £0.45, off-peak £0.15
_TOU_SCHEDULE = {
    **{h: 0.15 for h in list(range(0, 7)) + list(range(20, 24))},   # off-peak
    **{h: 0.45 for h in range(7, 20)},                               # peak
}

SCENARIOS = {
    "baseline": Scenario(
        name="Baseline",
        description="Current charging network with flat-rate pricing and observed demand."
    ),
    "ev_growth_low": Scenario(
        name="EV Adoption Growth (Low)",
        adoption_multiplier=1.5,
        description="50% increase in daily arrivals representing near-term EV adoption growth."
    ),
    "ev_growth_high": Scenario(
        name="EV Adoption Growth (High)",
        adoption_multiplier=2.0,
        description="100% increase in daily arrivals representing aggressive EV adoption growth."
    ),
    "tou_pricing": Scenario(
        name="Time-of-Use Pricing",
        tou_pricing=True,
        tou_schedule=_TOU_SCHEDULE,
        description="Peak rate £0.45/kWh (07:00-19:00), off-peak £0.15/kWh (20:00-06:00)."
    ),
    "carbon_incentive": Scenario(
        name="Carbon-Aware Incentives",
        carbon_penalty=0.001,
        description="Carbon penalty of £0.001 per gCO2 applied to charging cost."
    ),
    "combined": Scenario(
        name="Combined Policy",
        tou_pricing=True,
        tou_schedule=_TOU_SCHEDULE,
        carbon_penalty=0.001,
        description="ToU pricing combined with carbon-aware incentives."
    ),
}


# ── CARBON INTENSITY SCHEDULE ─────────────────────────────────────────────────
# Hourly carbon intensity (gCO2/kWh) - simplified UK grid profile
# Higher during morning and evening peak, lower overnight and midday (solar)
CARBON_SCHEDULE = {
    0: 45,  1: 42,  2: 40,  3: 38,  4: 38,  5: 40,
    6: 55,  7: 70,  8: 80,  9: 75, 10: 65, 11: 55,
   12: 50, 13: 48, 14: 50, 15: 55, 16: 65, 17: 80,
   18: 85, 19: 80, 20: 70, 21: 60, 22: 55, 23: 50,
}


# ── SCENARIO RUNNER ───────────────────────────────────────────────────────────

class ScenarioEngine:
    """
    Runs multiple simulation scenarios and returns KPI dataframes
    for comparison and analysis.
    """

    def __init__(self, n_episodes: int = 500, base_seed: int = RANDOM_SEED):
        self.n_episodes = n_episodes
        self.base_seed  = base_seed

    def _run_scenario(self, scenario: Scenario) -> pd.DataFrame:
        """Run n_episodes for a single scenario and return KPI dataframe."""
        records = []

        for i in range(self.n_episodes):
            rng        = np.random.default_rng(self.base_seed + i)
            is_weekday = rng.random() < WEEKDAY_RATIO
            hour_seed  = self.base_seed + i

            # Get carbon intensity for this episode
            # Weighted average across hours (simplified)
            carbon_intensity = np.mean(list(CARBON_SCHEDULE.values()))

            model = ChargingNetworkModel(
                seed=hour_seed,
                is_weekday=is_weekday,
                price_per_kwh=PRICE_PER_KWH,
                carbon_penalty=scenario.carbon_penalty,
                adoption_multiplier=scenario.adoption_multiplier,
                carbon_intensity=carbon_intensity,
            )

            # Override price per step if ToU pricing active
            if scenario.tou_pricing:
                model._tou_schedule = scenario.tou_schedule

            # Run episode step by step to apply ToU pricing per step
            for step in range(STEPS_PER_DAY):
                if scenario.tou_pricing:
                    hour = (step * 30) // 60
                    model.price_per_kwh = scenario.get_price(hour)
                model.step()

            kpis = model.get_kpis()
            kpis["scenario"]   = scenario.name
            kpis["is_weekday"] = is_weekday
            kpis["episode"]    = i
            records.append(kpis)

        return pd.DataFrame(records)

    def run_all(
        self,
        scenario_keys: list[str] | None = None
    ) -> dict[str, pd.DataFrame]:
        """
        Run all (or specified) scenarios.
        Returns dict of {scenario_key: DataFrame}.
        """
        keys = scenario_keys or list(SCENARIOS.keys())
        results = {}

        for key in keys:
            scenario = SCENARIOS[key]
            print(f"Running: {scenario.name} ({self.n_episodes} episodes)...")
            results[key] = self._run_scenario(scenario)
            print(f"  Done. Mean sessions: {results[key]['sessions_completed'].mean():.1f}")

        return results

    def compare_kpis(
        self,
        results: dict[str, pd.DataFrame]
    ) -> pd.DataFrame:
        """
        Aggregate KPIs across scenarios for comparison.
        Returns a summary dataframe with mean and std for each KPI.
        """
        rows = []
        kpi_cols = [
            "sessions_completed", "energy_kwh", "revenue_gbp",
            "co2_g", "avg_wait_hrs", "avg_utilisation"
        ]

        for key, df in results.items():
            row = {"scenario": SCENARIOS[key].name, "key": key}
            for col in kpi_cols:
                row[f"{col}_mean"] = df[col].mean()
                row[f"{col}_std"]  = df[col].std()
            rows.append(row)

        return pd.DataFrame(rows).set_index("key")

    def wilcoxon_vs_baseline(
        self,
        results: dict[str, pd.DataFrame],
        kpi: str = "sessions_completed"
    ) -> pd.DataFrame:
        """
        Run Wilcoxon signed-rank test comparing each scenario against baseline.
        Returns p-values and effect direction.
        """
        from scipy.stats import wilcoxon

        baseline = results["baseline"][kpi].values
        rows = []

        for key, df in results.items():
            if key == "baseline":
                continue
            scenario_vals = df[kpi].values
            n = min(len(baseline), len(scenario_vals))

            try:
                stat, p = wilcoxon(baseline[:n], scenario_vals[:n])
                direction = "increase" if scenario_vals.mean() > baseline.mean() else "decrease"
            except Exception:
                stat, p, direction = None, None, "N/A"

            rows.append({
                "scenario":  SCENARIOS[key].name,
                "kpi":       kpi,
                "baseline_mean":  baseline.mean(),
                "scenario_mean":  scenario_vals.mean(),
                "pct_change":     (scenario_vals.mean() - baseline.mean()) / baseline.mean() * 100,
                "direction":      direction,
                "wilcoxon_stat":  stat,
                "p_value":        p,
                "significant":    p < 0.05 if p is not None else False,
            })

        return pd.DataFrame(rows)
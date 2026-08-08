# simulation/config.py

import json
import duckdb
import numpy as np
from pathlib import Path

# ── PATHS ─────────────────────────────────────────────────────────────────────
ROOT_DIR = Path(__file__).resolve().parent.parent
DB_PATH  = ROOT_DIR / "data" / "ev_twin.duckdb"

# ── SIMULATION CONSTANTS ──────────────────────────────────────────────────────
STEP_MINUTES   = 30       # each time step = 30 minutes
STEPS_PER_DAY  = 48       # 24 hours / 0.5 hour
RANDOM_SEED    = 42

# ── LOAD CALIBRATION PARAMETERS FROM DUCKDB ───────────────────────────────────
def load_sim_params() -> dict:
    con = duckdb.connect(str(DB_PATH), read_only=True)
    rows = con.execute("SELECT key, value_json FROM simulation_params").fetchall()
    con.close()
    return {key: json.loads(value) for key, value in rows}

# Load once at import time
_params = load_sim_params()

# ── ARRIVAL RATES ─────────────────────────────────────────────────────────────
# Sessions per day per hour → sessions per 30-min step
_arrival_by_hour: dict = _params["arrival_by_hour"]
ARRIVAL_RATES: dict[int, float] = {
    int(hour): rate / 2
    for hour, rate in _arrival_by_hour.items()
}

# Share of the day's demand arriving in each 30-min step. Each hour spans two
# steps, so normalising the per-step rates over all 48 steps gives a proper
# distribution - the model allocates the daily target across it in one
# multinomial draw, which preserves the empirical arrival profile exactly.
_step_rates = np.array(
    [ARRIVAL_RATES.get((step * 30) // 60, 0.0) for step in range(STEPS_PER_DAY)]
)
STEP_ARRIVAL_P: np.ndarray = _step_rates / _step_rates.sum()

# ── CHARGER CONFIGURATION ─────────────────────────────────────────────────────
CHARGER_IDS: list[int]  = _params["charger_ids"]
N_CHARGERS:  int        = _params["n_chargers"]

# ── CONNECTOR TYPE PARAMETERS ─────────────────────────────────────────────────
# Keys: IEC_62196_T2_COMBO, CHADEMO, IEC_62196_T2
CONNECTOR_PARAMS: dict = _params["connector_params"]

CONNECTOR_SHARES: dict[str, float] = {
    k: v["share"] for k, v in CONNECTOR_PARAMS.items()
}

# Connector draw as a CDF rather than rng.choice(names, p=shares): every driver
# samples one, and searchsorted over a precomputed CDF is ~5x cheaper.
CONNECTOR_NAMES: tuple[str, ...] = tuple(CONNECTOR_SHARES.keys())
CONNECTOR_CDF: np.ndarray = np.cumsum(list(CONNECTOR_SHARES.values()))
CONNECTOR_CDF[-1] = 1.0    # guard the last bin against float drift

CONNECTOR_ENERGY: dict[str, dict] = {
    k: {
        "mean":   v["energy_mean"],
        "std":    v["energy_std"],
        # ndarray, not list: this is the simulation's hottest lookup, and
        # rng.choice() re-converts a list to an array on every single call.
        "values": np.asarray(v["energy_values"], dtype=float),
    }
    for k, v in CONNECTOR_PARAMS.items()
}

CONNECTOR_DURATION: dict[str, dict] = {
    k: {
        "s":     v["duration_lognorm"][0],   # shape (= sigma of the log)
        "loc":   v["duration_lognorm"][1],   # location
        "scale": v["duration_lognorm"][2],   # scale (= exp(mu))
        "mu":    float(np.log(v["duration_lognorm"][2])),   # for rng.lognormal
    }
    for k, v in CONNECTOR_PARAMS.items()
}

# ── SESSION CAPS ──────────────────────────────────────────────────────────────
MAX_DURATION_HRS = 4.0    # 99.9th percentile cap
MIN_ENERGY_KWH   = 5.0    # minimum observed session energy

# ── DAY TYPE ─────────────────────────────────────────────────────────────────
WEEKDAY_RATIO: float = _params["weekday_ratio"]

# Negative Binomial parameters for daily session count
# Fitted from real data: mean=25.11, var=107.69
NB_R: float = 7.6315    # dispersion parameter
NB_P: float = 0.2331    # probability parameter

# ── SCENARIO DEFAULTS (overridden by scenario engine later) ───────────────────
PRICE_PER_KWH:       float = 0.30    # £/kWh baseline ToU price
CARBON_PENALTY:      float = 0.0     # £/gCO2 carbon incentive (off by default)
ADOPTION_MULTIPLIER: float = 1.0     # arrival rate scaling (1.0 = baseline)


if __name__ == "__main__":
    print(f"DB path       : {DB_PATH}")
    print(f"N chargers    : {N_CHARGERS}")
    print(f"Charger IDs   : {CHARGER_IDS}")
    print(f"Steps/day     : {STEPS_PER_DAY}")
    print(f"Weekday ratio : {WEEKDAY_RATIO:.2%}")
    print(f"\nArrival rates (sessions/30-min step):")
    for h, r in sorted(ARRIVAL_RATES.items()):
        bar = "#" * int(r * 20)
        print(f"  {h:02d}:00  {r:.3f}  {bar}")
    print(f"\nConnector shares:")
    for k, v in CONNECTOR_SHARES.items():
        print(f"  {k}: {v:.2%}")
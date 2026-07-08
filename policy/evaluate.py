# policy/evaluate.py
"""
Step 5 — evaluate the trained PPO pricing agent against the handcrafted ToU
schedule and a flat-rate baseline, all under the high-adoption (2x) regime.

Reuses the model's own KPI definitions (model.get_kpis) so the numbers are
directly comparable to Phases 4-5, and runs paired Wilcoxon signed-rank tests
(same as scenario_engine) since every policy is evaluated on identical episode
seeds.

Run:  python policy/evaluate.py                       # uses policy/logs/best_model.zip
      python policy/evaluate.py path/to/model.zip
"""

from __future__ import annotations

import sys
import numpy as np
import pandas as pd
from scipy.stats import wilcoxon

from stable_baselines3 import PPO
from policy.environment import ChargingPricingEnv, PRICE_LEVELS

# ── evaluation config (must match training regime) ────────────────────────────
N_EPISODES       = 500
BASE_SEED        = 20000
ADOPTION         = 2.0
PRICE_ELASTICITY = 0.8
LAMBDA_WAIT      = 0.934      # keep in sync with signal_check.py / training
ENVKW = dict(adoption_multiplier=ADOPTION,
             price_elasticity=PRICE_ELASTICITY,
             lambda_wait=LAMBDA_WAIT)

# price-level indices in PRICE_LEVELS = [0.15, 0.30, 0.45]
IDX_015, IDX_030, IDX_045 = 0, 1, 2


# ── policies: obs, step_index -> action index ─────────────────────────────────
def make_ppo_policy(model):
    def pol(obs, step):
        return int(model.predict(obs, deterministic=True)[0])
    return pol


def flat_policy(obs, step):
    # flat-rate baseline: £0.30 all day
    return IDX_030


def tou_policy(obs, step):
    # handcrafted Time-of-Use: peak £0.45 (07:00-19:00), off-peak £0.15
    hour = (step * 30) // 60
    return IDX_045 if 7 <= hour <= 19 else IDX_015


# ── run one policy over paired seeds, collect full KPIs ───────────────────────
def run_policy(pol, name):
    records = []
    action_counts = np.zeros(len(PRICE_LEVELS), dtype=int)
    hour_price = []                              # (hour, price) per step
    for i in range(N_EPISODES):
        seed = BASE_SEED + i
        env = ChargingPricingEnv(**ENVKW, seed=seed)
        obs, _ = env.reset(seed=seed)
        trunc = False
        step = 0
        while not trunc:
            a = pol(obs, step)
            action_counts[a] += 1
            hour_price.append(((step * 30) // 60, float(PRICE_LEVELS[a])))
            obs, r, term, trunc, info = env.step(a)
            step += 1
        m = env._model
        kpis = m.get_kpis()                     # same KPI defs as Phases 4-5
        wait_steps = sum(c.total_wait_steps for c in m.charger_agents)
        kpis["policy"] = name
        kpis["episode"] = i
        kpis["wait_steps"] = wait_steps
        kpis["score"] = kpis["revenue_gbp"] - LAMBDA_WAIT * wait_steps
        records.append(kpis)
    return pd.DataFrame(records), action_counts, hour_price


def summarise(df):
    kpi_cols = ["revenue_gbp", "avg_wait_hrs", "sessions_completed",
                "energy_kwh", "co2_g", "avg_utilisation", "score"]
    rows = []
    for name, g in df.groupby("policy", sort=False):
        row = {"policy": name}
        for c in kpi_cols:
            row[f"{c}_mean"] = g[c].mean()
            row[f"{c}_std"] = g[c].std()
        rows.append(row)
    return pd.DataFrame(rows).set_index("policy")


def paired_wilcoxon(df, policy_a, policy_b, kpi):
    a = df[df.policy == policy_a].sort_values("episode")[kpi].values
    b = df[df.policy == policy_b].sort_values("episode")[kpi].values
    try:
        stat, p = wilcoxon(a, b)
    except ValueError:
        stat, p = np.nan, np.nan
    pct = (a.mean() - b.mean()) / abs(b.mean()) * 100 if b.mean() != 0 else np.nan
    return {"comparison": f"{policy_a} vs {policy_b}", "kpi": kpi,
            f"{policy_a}_mean": a.mean(), f"{policy_b}_mean": b.mean(),
            "pct_change": pct, "wilcoxon_stat": stat, "p_value": p,
            "significant": (p < 0.05) if p == p else False}


def main(model_path="policy/logs/best_model.zip"):
    print(f"Loading PPO model: {model_path}")
    model = PPO.load(model_path)

    policies = {
        "PPO":          make_ppo_policy(model),
        "ToU":          tou_policy,
        "Flat £0.30":   flat_policy,
    }

    frames = []
    action_mix = {}
    hour_profiles = {}
    for name, pol in policies.items():
        print(f"  evaluating {name} ({N_EPISODES} episodes)...")
        fdf, counts, hp = run_policy(pol, name)
        frames.append(fdf)
        action_mix[name] = counts
        hour_profiles[name] = hp
    df = pd.concat(frames, ignore_index=True)

    summary = summarise(df)
    pd.set_option("display.width", 200, "display.max_columns", 40)
    print("\n=== KPI summary (high-adoption 2x, means) ===")
    show = ["revenue_gbp_mean", "avg_wait_hrs_mean", "sessions_completed_mean",
            "co2_g_mean", "avg_utilisation_mean", "score_mean"]
    print(summary[show].round(2).to_string())

    print("\n=== Paired Wilcoxon: PPO vs ToU (the handcrafted schedule) ===")
    wrows = [paired_wilcoxon(df, "PPO", "ToU", k) for k in
             ["revenue_gbp", "avg_wait_hrs", "score"]]
    wdf = pd.DataFrame(wrows)
    print(wdf[["kpi", "PPO_mean", "ToU_mean", "pct_change", "p_value", "significant"]]
          .round(4).to_string(index=False))

    print("\n=== Paired Wilcoxon: PPO vs Flat £0.30 ===")
    w2 = pd.DataFrame([paired_wilcoxon(df, "PPO", "Flat £0.30", k) for k in
                       ["revenue_gbp", "avg_wait_hrs", "score"]])
    print(w2[["kpi", "PPO_mean", "Flat £0.30_mean", "pct_change", "p_value", "significant"]]
          .round(4).to_string(index=False))

    # price mix per policy — surfaces the ToU-collapse and PPO's real spread
    print("\n=== Price mix (fraction of steps at each level) ===")
    mix_rows = []
    for name, counts in action_mix.items():
        tot = counts.sum()
        mix_rows.append({"policy": name,
                         "£0.15": counts[0] / tot,
                         "£0.30": counts[1] / tot,
                         "£0.45": counts[2] / tot})
    print(pd.DataFrame(mix_rows).set_index("policy").round(3).to_string())

    # PPO price-by-hour profile (interpretability figure: is £0.15 in dead hours?)
    hp = pd.DataFrame(hour_profiles["PPO"], columns=["hour", "price"])
    prof = hp.groupby("hour")["price"].mean()
    prof.to_csv("policy/ppo_price_by_hour.csv")
    print("\nSaved policy/ppo_price_by_hour.csv (mean PPO price per hour)")

    # persist for the writeup
    df.to_csv("policy/eval_results.csv", index=False)
    summary.to_csv("policy/eval_summary.csv")
    print("\nSaved policy/eval_results.csv and policy/eval_summary.csv")
    return df, summary


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "policy/logs/best_model.zip"
    main(path)
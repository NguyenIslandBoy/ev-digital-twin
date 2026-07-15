# policy/sweep.py
"""
Robustness sweep: elasticity x seed.

For each price_elasticity:
  1. Derive lambda_wait from the tie-point between const £0.30 and const £0.45
     (MUST be re-derived per elasticity — the trade-off shifts with it).
  2. For each seed: train PPO at that lambda, evaluate vs ToU / flat / heuristic.
  3. Append one row per (elasticity, seed).

Used by the Colab sweep notebook. Import and call `run_sweep(...)`.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import VecNormalize, VecMonitor

from policy.environment import ChargingPricingEnv, make_env, PRICE_LEVELS

from pathlib import Path

# All generated CSVs go to <repo_root>/results/ (created if missing)
RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)


IDX_015, IDX_030, IDX_045 = 0, 1, 2
ADOPTION = 2.0


# ── policies ──────────────────────────────────────────────────────────────────
def pol_flat(obs, step):
    return IDX_030


def pol_tou(obs, step):
    hour = (step * 30) // 60
    return IDX_045 if 7 <= hour <= 19 else IDX_015


def pol_tou3(obs, step):
    """3-band clock ToU — has the middle gear, still blind to congestion.
    Tests whether PPO's edge is state-conditioning rather than just £0.30."""
    hour = (step * 30) // 60
    if 11 <= hour <= 16:      # demand peak
        return IDX_045
    if 7 <= hour <= 19:       # shoulder
        return IDX_030
    return IDX_015            # overnight


def pol_congestion(obs, step):
    """State-aware non-learned reference.
    obs = [step_frac, occ(6), que(6), price_norm, arrivals_frac]"""
    loaded = (np.sum(obs[7:13]) > 0.001) or (np.sum(obs[1:7]) >= 5)
    return IDX_045 if loaded else IDX_030


def make_ppo_policy(model):
    def pol(obs, step):
        return int(model.predict(obs, deterministic=True)[0])
    return pol


# ── rollout ───────────────────────────────────────────────────────────────────
def rollout(pol, envkw, n_episodes, base_seed):
    revs, waits, sess, co2 = [], [], [], []
    for i in range(n_episodes):
        s = base_seed + i
        env = ChargingPricingEnv(**envkw, seed=s)
        obs, _ = env.reset(seed=s)
        trunc, step = False, 0
        while not trunc:
            obs, r, term, trunc, info = env.step(pol(obs, step))
            step += 1
        m = env._model
        k = m.get_kpis()
        revs.append(k["revenue_gbp"])
        waits.append(sum(c.total_wait_steps for c in m.charger_agents))
        sess.append(k["sessions_completed"])
        co2.append(k["co2_g"])
    return (float(np.mean(revs)), float(np.mean(waits)),
            float(np.mean(sess)), float(np.mean(co2)))


# ── step 1: derive lambda for a given elasticity ──────────────────────────────
def derive_lambda(elasticity, n_episodes=400, base_seed=500):
    """Tie-point lambda where const £0.30 and const £0.45 score equally.

    Returns (lambda, diagnostics). lambda is None when the regime is
    DEGENERATE — i.e. £0.45 dominates £0.30 on BOTH revenue and wait, so no
    trade-off exists and the optimal policy is trivially the static maximum
    price. This happens when price_elasticity is too low for price to shed
    meaningful demand, and is itself a reportable result (adaptive pricing
    requires sufficiently price-responsive demand).
    """
    envkw = dict(adoption_multiplier=ADOPTION,
                 price_elasticity=elasticity,
                 lambda_wait=0.0)          # irrelevant for raw KPI collection
    r30, w30, _, _ = rollout(lambda o, s: IDX_030, envkw, n_episodes, base_seed)
    r45, w45, _, _ = rollout(lambda o, s: IDX_045, envkw, n_episodes, base_seed)
    diag = dict(r30=r30, w30=w30, r45=r45, w45=w45)

    denom = w30 - w45
    if denom <= 0:
        diag["reason"] = "wait did not fall as price rose"
        return None, diag

    lam = (r30 - r45) / denom
    if lam <= 0:
        # £0.45 wins on revenue AND wait -> price strictly dominates.
        diag["reason"] = ("degenerate: £0.45 dominates £0.30 on both revenue "
                          f"and wait (lambda would be {lam:.2f} < 0); demand "
                          "is insufficiently price-responsive for a trade-off")
        diag["degenerate_lambda"] = float(lam)
        return None, diag

    return float(lam), diag


# ── step 2: train one PPO ─────────────────────────────────────────────────────
def train_ppo(elasticity, lam, seed, total_timesteps, n_envs=8,
              ent_coef=0.02, verbose=0):
    envkw = dict(adoption_multiplier=ADOPTION,
                 price_elasticity=elasticity,
                 lambda_wait=lam)
    train_env = VecMonitor(make_vec_env(make_env(**envkw), n_envs=n_envs, seed=seed))
    train_env = VecNormalize(train_env, norm_obs=False, norm_reward=True, clip_reward=50.0)
    model = PPO("MlpPolicy", train_env,
                n_steps=256, batch_size=256, n_epochs=10,
                gamma=0.99, gae_lambda=0.95, ent_coef=ent_coef,
                learning_rate=3e-4, verbose=verbose, seed=seed)
    model.learn(total_timesteps=total_timesteps, progress_bar=False)
    return model


# ── step 3: evaluate one trained model vs all baselines ───────────────────────
def evaluate_all(model, elasticity, lam, n_episodes=300, base_seed=20000):
    envkw = dict(adoption_multiplier=ADOPTION,
                 price_elasticity=elasticity,
                 lambda_wait=lam)
    policies = {
        "PPO":        make_ppo_policy(model),
        "ToU":        pol_tou,
        "ToU3":       pol_tou3,
        "Flat":       pol_flat,
        "Congestion": pol_congestion,
    }
    out = {}
    for name, pol in policies.items():
        rev, wait, sess, co2 = rollout(pol, envkw, n_episodes, base_seed)
        out[name] = dict(revenue=rev, wait_steps=wait, sessions=sess,
                         co2=co2, score=rev - lam * wait)
    return out


# ── one full (elasticity, seed) run ───────────────────────────────────────────
def run_one(elasticity, lam, seed, total_timesteps, eval_episodes=300,
            save_path=None):
    model = train_ppo(elasticity, lam, seed, total_timesteps)
    if save_path:
        model.save(save_path)
    res = evaluate_all(model, elasticity, lam, n_episodes=eval_episodes)
    row = {"elasticity": elasticity, "lambda": lam, "seed": seed}
    for name, d in res.items():
        for k, v in d.items():
            row[f"{name}_{k}"] = v
    row["margin_vs_ToU"] = res["PPO"]["score"] - res["ToU"]["score"]
    row["margin_vs_ToU3"] = res["PPO"]["score"] - res["ToU3"]["score"]
    row["margin_vs_Flat"] = res["PPO"]["score"] - res["Flat"]["score"]
    return row


def run_sweep(elasticities, seeds, total_timesteps, eval_episodes=300,
              out_csv=None, save_dir=None, verbose=True, resume=True):
    """Run the elasticity x seed grid.

    Resumable: if `resume` is True and `out_csv` already exists, any
    (elasticity, seed) pair already present is skipped and its row preserved.
    Rows are flushed to disk after every run, so an interrupted session (e.g.
    a dropped Colab runtime) loses at most the run in progress.
    """
    import os

    if out_csv is None:
        out_csv = str(RESULTS_DIR / "sweep_results.csv")

    rows = []
    done = set()

    if resume and os.path.exists(out_csv):
        prev = pd.read_csv(out_csv)
        rows = prev.to_dict("records")
        done = {(round(float(r["elasticity"]), 4), int(r["seed"])) for r in rows}
        if verbose and done:
            print(f"Resuming: {len(done)} run(s) already complete in {out_csv}")

    for e in elasticities:
        pending = [s for s in seeds if (round(float(e), 4), int(s)) not in done]
        if not pending:
            if verbose:
                print(f"\n=== elasticity {e} | all seeds already done — skipped ===")
            continue

        lam, diag = derive_lambda(e)
        if lam is None:
            if verbose:
                print(f"[elasticity {e}] NO TRADE-OFF — skipped. {diag.get('reason','')}")
            continue
        if verbose:
            print(f"\n=== elasticity {e} | derived lambda = {lam:.3f} "
                  f"| {len(pending)} seed(s) to run ===")

        for s in pending:
            sp = f"{save_dir}/ppo_e{e}_s{s}" if save_dir else None
            row = run_one(e, lam, s, total_timesteps,
                          eval_episodes=eval_episodes, save_path=sp)
            rows.append(row)
            done.add((round(float(e), 4), int(s)))
            if verbose:
                print(f"  seed {s}: PPO={row['PPO_score']:.1f}  ToU={row['ToU_score']:.1f}  "
                      f"ToU3={row['ToU3_score']:.1f}  Flat={row['Flat_score']:.1f}  "
                      f"margin_vs_ToU={row['margin_vs_ToU']:+.1f}")
            pd.DataFrame(rows).to_csv(out_csv, index=False)   # flush after each run

    return pd.DataFrame(rows)


def summarise(df):
    """Mean ± std across seeds, per elasticity."""
    g = df.groupby("elasticity")
    out = pd.DataFrame({
        "lambda": g["lambda"].first(),
        "PPO_score_mean": g["PPO_score"].mean(),
        "PPO_score_std": g["PPO_score"].std(),
        "ToU_score": g["ToU_score"].mean(),
        "ToU3_score": g["ToU3_score"].mean(),
        "Flat_score": g["Flat_score"].mean(),
        "Congestion_score": g["Congestion_score"].mean(),
        "margin_vs_ToU_mean": g["margin_vs_ToU"].mean(),
        "margin_vs_ToU_std": g["margin_vs_ToU"].std(),
    })
    return out.round(2)
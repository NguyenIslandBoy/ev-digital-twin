# policy/train.py
"""
Train the headline PPO pricing agent locally.

Same configuration as notebooks/04_train_ppo_colab.ipynb — that notebook exists
because the simulation used to be slow enough to need a Colab session. It no
longer is (~2,000 env steps/s on CPU, and the MLP policy is tiny), so a full
500k-timestep run finishes in minutes here.

Writes:
  models/best_model.zip       best by periodic evaluation (used by evaluate.py)
  models/ppo_pricing.zip      final weights
  results/evaluations.npz     EvalCallback history
  results/figures/ppo_learning_curve.png

Run:  python -m policy.train
"""

from __future__ import annotations

import shutil
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import VecNormalize, VecMonitor
from stable_baselines3.common.callbacks import EvalCallback

from policy.environment import make_env

ROOT    = Path(__file__).resolve().parent.parent
MODELS  = ROOT / "models"
RESULTS = ROOT / "results"
LOGS    = ROOT / "policy" / "logs"
for d in (MODELS, RESULTS, RESULTS / "figures", LOGS):
    d.mkdir(parents=True, exist_ok=True)

# Keep in sync with policy/evaluate.py and validation/signal_check.py.
ADOPTION         = 3.0
PRICE_ELASTICITY = 0.8
LAMBDA_WAIT      = 1.581
TOTAL_TIMESTEPS  = 500_000
N_ENVS           = 8
SEED             = 0

ENVKW = dict(adoption_multiplier=ADOPTION,
             price_elasticity=PRICE_ELASTICITY,
             lambda_wait=LAMBDA_WAIT)


def main():
    print(f"Training PPO — {ENVKW}, {TOTAL_TIMESTEPS:,} timesteps, {N_ENVS} envs")

    # Observations are already scaled to [0, 1], so normalise the reward only.
    train_env = VecMonitor(make_vec_env(make_env(**ENVKW), n_envs=N_ENVS, seed=SEED))
    train_env = VecNormalize(train_env, norm_obs=False, norm_reward=True,
                             clip_reward=50.0)

    # Eval env matches the wrapper type for stat sync but does not normalise.
    eval_env = VecMonitor(make_vec_env(make_env(**ENVKW), n_envs=1, seed=SEED + 123))
    eval_env = VecNormalize(eval_env, norm_obs=False, norm_reward=False,
                            training=False)

    model = PPO(
        "MlpPolicy", train_env,
        n_steps=256, batch_size=256, n_epochs=10,
        gamma=0.99, gae_lambda=0.95,
        ent_coef=0.02,
        learning_rate=3e-4,
        verbose=1, seed=SEED,
    )

    eval_cb = EvalCallback(
        eval_env, best_model_save_path=str(LOGS), log_path=str(LOGS),
        eval_freq=5_000, n_eval_episodes=50, deterministic=True, verbose=1,
    )

    model.learn(total_timesteps=TOTAL_TIMESTEPS, callback=eval_cb,
                progress_bar=False)

    model.save(MODELS / "ppo_pricing")
    shutil.copy(LOGS / "best_model.zip", MODELS / "best_model.zip")
    shutil.copy(LOGS / "evaluations.npz", RESULTS / "evaluations.npz")

    data = np.load(LOGS / "evaluations.npz")
    x, y = data["timesteps"], data["results"].mean(axis=1)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(x, y, marker="o", ms=3)
    ax.set_xlabel("timesteps")
    ax.set_ylabel("mean eval return (true reward)")
    ax.set_title("PPO learning curve")
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(RESULTS / "figures" / "ppo_learning_curve.png", dpi=150)
    plt.close(fig)

    print(f"\nfinal eval return : {float(y[-1]):.1f}")
    print(f"best eval return  : {float(y.max()):.1f}")
    print(f"saved {MODELS/'best_model.zip'}, {MODELS/'ppo_pricing.zip'}")
    print(f"saved {RESULTS/'evaluations.npz'}, figures/ppo_learning_curve.png")


if __name__ == "__main__":
    main()

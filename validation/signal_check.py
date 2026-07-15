# signal_check.py
# Step 3 gate (run BEFORE training). Answers two questions on YOUR real data:
#   1. At what lambda_wait do the two price constants tie? (the regime where
#      adaptive pricing has the most room)
#   2. At that lambda, does a congestion-state-conditional policy beat both
#      constants? If yes, PPO has learnable signal worth training for.
#
# Run:  python signal_check.py

import numpy as np
from policy.environment import ChargingPricingEnv

N = 400   # episodes per policy


def rollout(policy_fn, seed0=500):
    """Return mean (revenue, wait_steps) over N episodes."""
    revs, waits = [], []
    for ep in range(N):
        env = ChargingPricingEnv(seed=seed0 + ep)
        obs, info = env.reset(seed=seed0 + ep)
        trunc = False
        step = 0
        while not trunc:
            obs, r, term, trunc, info = env.step(policy_fn(step, obs))
            step += 1
        revs.append(info["cum_revenue"])
        waits.append(info["cum_wait_steps"])
    return float(np.mean(revs)), float(np.mean(waits))


def score(rev, wait, lam):
    return rev - lam * wait


const = lambda idx: (lambda s, o: idx)   # 0=£0.15, 1=£0.30, 2=£0.45


def congestion(q_thresh, occ_thresh):
    # obs layout: [step_frac, occ(6), que(6), price_norm, arrivals_frac]
    def pf(s, o):
        total_occ  = float(np.sum(o[1:7]))
        total_qnrm = float(np.sum(o[7:13]))
        if total_qnrm > q_thresh or total_occ >= occ_thresh:
            return 2   # £0.45 when loaded
        return 1       # £0.30 otherwise
    return pf


print(f"Signal check  (N={N} episodes/policy, high-adoption regime)\n")

# --- constants ---
rev30, wait30 = rollout(const(1))
rev45, wait45 = rollout(const(2))
print(f"const £0.30 : revenue {rev30:7.1f} | wait_steps {wait30:6.1f}")
print(f"const £0.45 : revenue {rev45:7.1f} | wait_steps {wait45:6.1f}")

# --- calibrate tie-point lambda: score30 == score45 ---
denom = (wait30 - wait45)
if denom <= 0:
    print("\n[!] wait did not fall as price rose - check price_elasticity > 0.")
    raise SystemExit(1)
lam_tie = (rev30 - rev45) / denom
print(f"\nTie-point lambda_wait = {lam_tie:.3f}  "
      f"(use this as the env's lambda_wait for training)\n")

# --- gate: does state-adaptive beat both constants at lam_tie? ---
s30 = score(rev30, wait30, lam_tie)
s45 = score(rev45, wait45, lam_tie)
best_const = max(s30, s45)

best_heur = -1e18
best_cfg = None
for qt, ot in [(0.001, 4), (0.001, 5), (0.001, 6), (0.07, 5), (0.14, 5)]:
    rh, wh = rollout(congestion(qt, ot))
    sh = score(rh, wh, lam_tie)
    if sh > best_heur:
        best_heur, best_cfg = sh, (qt, ot)

print(f"{'policy':<30}{'score@lam_tie':>14}")
print("-" * 44)
print(f"{'const £0.30':<30}{s30:>14.1f}")
print(f"{'const £0.45':<30}{s45:>14.1f}")
print(f"{f'congestion {best_cfg}':<30}{best_heur:>14.1f}")

margin = best_heur - best_const
print()
if margin > 2:
    print(f"GATE PASS: state-adaptive beats best constant by {margin:.1f}. "
          f"Train PPO with lambda_wait={lam_tie:.3f}.")
else:
    print(f"GATE MARGINAL/FAIL: only +{margin:.1f}. Raise price_elasticity or "
          f"re-examine before spending Colab time.")
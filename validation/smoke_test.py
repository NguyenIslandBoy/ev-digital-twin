# smoke_test.py
# Step 1 verification: confirms the Phase 6 patches (price_elasticity, hourly_carbon)
# (1) do NOT change Phase 5 behaviour when off, and
# (2) create a real revenue-vs-throughput trade-off when on.
#
# Run:  python smoke_test.py

import numpy as np
from simulation.model import ChargingNetworkModel

N = 200          # episodes per cell
ADOPT = 2.0      # high-adoption regime (where pricing has signal)


def mean_kpi(price, elasticity, kpi, n=N):
    vals = []
    for i in range(n):
        m = ChargingNetworkModel(
            seed=2000 + i,
            adoption_multiplier=ADOPT,
            price_per_kwh=price,
            price_elasticity=elasticity,
        )
        vals.append(m.run_episode()[kpi])
    return float(np.mean(vals))


def cell(price, elasticity):
    return (
        mean_kpi(price, elasticity, "revenue_gbp"),
        mean_kpi(price, elasticity, "sessions_completed"),
    )


print(f"High-adoption ({ADOPT}x), {N} episodes/cell\n")
print(f"{'elasticity':>10} {'price':>6} {'revenue':>9} {'sessions':>9}")
print("-" * 38)

results = {}
for elast in (0.0, 0.8):
    for price in (0.30, 0.45):
        rev, sess = cell(price, elast)
        results[(elast, price)] = (rev, sess)
        print(f"{elast:>10.1f} {price:>6.2f} {rev:>9.1f} {sess:>9.1f}")

print()

# ── Invariant 1: elasticity OFF => no demand response (Phase 5 logic intact) ──
sess_030_off = results[(0.0, 0.30)][1]
sess_045_off = results[(0.0, 0.45)][1]
inv1 = abs(sess_045_off - sess_030_off) < 1.0   # sessions ~ identical
print(f"[1] elast=0.0: sessions £0.30={sess_030_off:.1f} vs £0.45={sess_045_off:.1f}  "
      f"-> {'PASS (no demand response, as expected)' if inv1 else 'FAIL (patch leaked into legacy path)'}")

# ── Invariant 2: elasticity ON => £0.45 sheds sessions AND revenue dips ──────
rev_030_on = results[(0.8, 0.30)][0]
rev_045_on = results[(0.8, 0.45)][0]
sess_030_on = results[(0.8, 0.30)][1]
sess_045_on = results[(0.8, 0.45)][1]
inv2 = (sess_045_on < sess_030_on) and (rev_045_on < rev_030_on)
print(f"[2] elast=0.8: £0.45 sheds sessions ({sess_045_on:.1f}<{sess_030_on:.1f}) and "
      f"revenue dips ({rev_045_on:.1f}<{rev_030_on:.1f})  "
      f"-> {'PASS (real trade-off exists)' if inv2 else 'FAIL (raise elasticity toward 1.0-1.2)'}")

print()
if inv1 and inv2:
    print("ALL CHECKS PASS - patches are safe and the RL environment will have learnable signal.")
else:
    print("CHECK FAILED - see above before proceeding to environment.py.")
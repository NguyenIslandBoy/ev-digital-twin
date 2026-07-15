import warnings; warnings.filterwarnings("ignore")
import policy.sweep as sw

print(f"{'elast':>6} {'lambda':>9}  status")
print("-" * 40)
for e in [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2]:
    lam, d = sw.derive_lambda(e, n_episodes=200)
    if lam is None:
        dl = d.get("degenerate_lambda")
        print(f"{e:>6} {'--':>9}  DEGENERATE" + (f" (lam={dl:.2f})" if dl else ""))
    else:
        print(f"{e:>6} {lam:>9.3f}  ok")
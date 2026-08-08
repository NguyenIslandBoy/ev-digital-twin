# results/ — provenance

Every artefact in this folder was produced by the **current** simulator. Two
defects were fixed after the first full run, and everything downstream of them
was regenerated or retrained:

1. **Arrival allocation** — `_spawn_arrivals` applied the per-step share at twice
   its true value and squared the adoption multiplier, compressing the day's
   demand into the morning. At 2x adoption essentially no arrivals occurred
   after 11:30.
2. **Energy delivery** — the session step count was floored while the charge
   rate was derived from the unfloored duration, so ~14% of each session's
   sampled energy was never delivered. Revenue, CO2 and energy were all low.

Fixing (1) removed most of the congestion at 2x adoption (mean wait fell to
~1 minute), so the RL regime moved to **3x**, where the network is congested
enough for a revenue-vs-wait trade-off to exist on defensible terms
(~41% utilisation, ~13 min mean wait, tie-point lambda ~1.6 rather than ~15.6).

## How to regenerate

| Command | Produces |
|---|---|
| `python -m validation.regenerate_results` | `calibration_summary.csv`, `scenario_summary.csv`, `scenario_significance.csv`, `elasticity_boundary.csv`, `figures/calibration_*.png`, `figures/scenario_*.png` |
| `python -m policy.train` | `evaluations.npz`, `figures/ppo_learning_curve.png`, and `models/best_model.zip` |
| `python -m policy.evaluate` | `eval_results.csv`, `eval_summary.csv`, `ppo_price_by_hour.csv` |
| `python validation/plot_price_by_hour.py` | `figures/ppo_price_by_hour.png` |
| `python -m policy.run_sweep` | `sweep_results.csv`, `sweep_summary.csv`, `sweep_headline.csv`, `figures/sweep_robustness.png` |
| `python validation/plot_arrival_overlay.py` | `figures/arrival_vs_tou_window.png` |
| `python validation/combine_calibration.py` | `figures/calibration_3panel.png` |

Derived from the real session log only, and independent of both defects:
`sessions_clean.csv`, `figures/arrival_patterns.png`,
`figures/charger_utilisation.png`, `figures/energy_duration_distributions.png`.

Runtimes on CPU: calibration + scenarios ~40s, headline training ~3 min,
evaluation ~15s, full 20-run sweep ~59 min. No GPU is required — the Colab
notebooks (04, 05) exist because the simulator used to be ~17x slower.

`figures/calibration_arrival.png` is an arrival-timing gate. No such check
existed before, which is why defect 1 went unnoticed: a KS test on daily
session *counts* cannot see a corrupted arrival *profile*.

## Consistency note

`elasticity_boundary.csv` and `sweep_*.csv` both report a tie-point lambda per
elasticity, and the two disagree (e.g. at elasticity 0.8: 1.702 vs 1.581).
This is not an error — lambda is `(r30 - r45) / (w30 - w45)`, a ratio whose
denominator is a small difference between two noisy wait means, so it is
sensitive to the episode count. The boundary scan uses 200 episodes, the sweep
400. Quote the episode count wherever a lambda is reported.

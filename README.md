# An AI-Enabled Digital Twin for EV Charging

**Behavioural Simulation, Policy Evaluation, and Pricing Optimisation**

MSc Data Science Dissertation (CSC8639) · Newcastle University
Hoang Nguyen Lai (250539846)
Supervisor: Dr Jichun Li · Project proposer: Dr Sanchari Deb

---

## Overview

A calibrated agent-based digital twin of the Newcastle University (USB) EV charging network, built from 29,775 real charging sessions, and used to (a) evaluate charging policies under EV-adoption growth and (b) train a reinforcement-learning agent to set charging prices.

The central result: a **PPO agent that conditions on live congestion state** learns a pricing policy that materially outperforms a handcrafted Time-of-Use (ToU) schedule — and the advantage comes specifically from reacting to real-time queue state, which any clock-based rule is structurally blind to.

## Key findings

All figures are for the high-adoption (2×) regime, the setting where pricing has a genuine effect on behaviour. Scores are the objective `revenue − λ·wait`; margins are paired across identical episode seeds.

| Finding | Evidence |
|---|---|
| **PPO beats the handcrafted ToU schedule** | +20% on the objective and +24% on revenue at the headline config (elasticity 0.8, λ 0.934), Wilcoxon *p* < 0.001 over 500 paired episodes |
| **Robust to the demand assumption and to training seed** | PPO − ToU margin stays **+70 to +91** across elasticity 0.7–1.0; standard deviation across 5 training seeds is only **~2–3 points** |
| **The advantage is state-conditioning, not price granularity** | PPO also beats **ToU3** — a 3-band clock schedule with the same middle tariff — by **+54 to +73** everywhere. More price levels do not close the gap; conditioning on live queue state does |
| **A static ToU schedule is worse than doing nothing** | ToU scores **318.8 < 341.7** for flat pricing: indiscriminate peak pricing sheds more revenue than its wait reduction is worth |
| **Adaptive pricing has a critical elasticity (≈ 0.65)** | Below it, the high price dominates on *both* revenue and wait, no trade-off exists, and the optimal policy collapses to a static maximum price |

Headline comparison (2× adoption, 500 episodes, elasticity 0.8):

| Policy | Revenue (£) | Wait (min) | Sessions | Score |
|---|---|---|---|---|
| **PPO** | **400.9** | 9.6 | 41.0 | **383.1** |
| Flat £0.30 | 386.9 | 19.8 | 49.3 | 341.7 |
| ToU (2-band) | 323.9 | 2.9 | 34.3 | 318.8 |

> Note: PPO does **not** minimise waiting time — ToU does, by serving ~30% fewer cars. PPO holds a superior revenue–wait *trade-off* at the chosen λ; it accepts modest congestion to serve more sessions at higher revenue. See *Limitations*.

## Repository structure

```
ev_digital_twin/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/                     # supervisor session CSV, meter ids
│   └── ev_twin.duckdb           # all project data (single source of truth)
├── ingestion/                   # Phase 1 — data pipeline (DuckDB, scraper)
├── simulation/                  # Phases 2–5 — Mesa ABM + scenario engine
│   ├── config.py                #   loads calibration params from DuckDB
│   ├── agents.py                #   EVDriverAgent, ChargerAgent
│   ├── model.py                 #   ChargingNetworkModel (48 × 30-min steps)
│   └── scenario_engine.py       #   scenarios, KPIs, Wilcoxon tests
├── policy/                      # Phase 6 — RL pricing
│   ├── environment.py           #   Gymnasium wrapper (Discrete(3) pricing)
│   ├── evaluate.py              #   PPO vs ToU vs Flat + Wilcoxon
│   └── sweep.py                 #   elasticity × seed robustness sweep
├── validation/                  # pre-training gates (reproducible evidence)
│   ├── smoke_test.py            #   patch invariants + trade-off existence
│   ├── signal_check.py          #   λ tie-point + state-adaptive gate
│   └── scan_elasticity.py       #   degenerate-boundary scan (~0.65)
├── notebooks/
│   ├── 00_metering_investigation.ipynb
│   ├── 01_eda.ipynb             #   EDA + writes simulation_params to DuckDB
│   ├── 02_calibration.ipynb     #   KS-test validation
│   ├── 03_scenarios.ipynb       #   Phase 5 policy evaluation
│   ├── 04_train_ppo_colab.ipynb #   PPO training (Colab GPU)
│   └── 05_sweep_colab.ipynb     #   robustness sweep (Colab GPU)
├── models/                      # trained PPO weights (headline + sweep)
├── results/                     # generated CSVs and figures
└── reports/                     # dissertation, poster, reference material
```

## Data

- **`charging_sessions`** (29,775 rows, 6 chargers, Mar 2021 – Jul 2024) — the supervisor-provided session log. This is the only data used for calibration and simulation.
- **`metering_raw`** (28.7M scraped rows) — half-hourly building-meter data, **investigated and excluded**. It measures whole-building load (correlation with session energy **r = −0.086**) and suffers systematic collection failures (a single flat value repeated across most months). See `notebooks/00_metering_investigation.ipynb`. Grid-load KPIs are therefore derived from the calibrated simulation, not the meters.

## Method

**Simulation (Phases 2–5).** A Mesa agent-based model where each episode is one day (48 × 30-min steps). Drivers arrive from a Negative-Binomial daily target distributed by empirical hourly rates; each samples a connector type, an empirically-resampled energy demand, and a lognormal duration. Chargers manage occupancy and queues. Calibration is validated by two-sample KS tests (see below).

**RL pricing (Phase 6).** A Gymnasium environment wraps the simulation. Each step the agent sets a network-wide price from `{£0.15, £0.30, £0.45}` (`Discrete(3)`) and receives a dense, incremental reward:

```
reward = Δrevenue − λ_wait · Δwait_steps        (λ_co2 = 0 for the headline agent)
```

Training uses PPO (Stable-Baselines3) under the high-adoption (2×) regime with an opt-in **price-abandonment** mechanism — the demand-side downside to high prices that makes pricing a real optimisation problem. `λ_wait` is the tie-point between the two constant-price policies, re-derived per elasticity.

## Calibration

Judged on the **KS statistic (effect size)** and moment agreement, not a fixed p-value threshold — with tens of thousands of real sessions, KS p-values reject on negligible deviations.

| Distribution | Model | KS statistic | Sim / Real mean |
|---|---|---|---|
| Sessions per day | Negative Binomial (r=7.63, p=0.23) | 0.061 | 25.4 / 25.1 |
| Energy per session | Empirical resampling per connector | 0.009 | 30.4 / 30.4 |
| Session duration | Lognormal per connector | 0.037 | 0.76 / 0.74 |

Energy uses empirical resampling, so its agreement is expected by construction; duration (parametric lognormal) and sessions (NB) are the fits that genuinely earn the "calibrated" label.

## Reproducing the results

**Environment**

```bash
python -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**1. Build the database** (loads the session CSV into DuckDB)

```bash
python -m ingestion.run_scraper --load-sessions
```

**2. EDA → calibration → scenarios** (run in order; notebook 01 writes the `simulation_params` the simulation depends on)

```
notebooks/00_metering_investigation.ipynb
notebooks/01_eda.ipynb
notebooks/02_calibration.ipynb
notebooks/03_scenarios.ipynb
```

**3. Phase 6 — validate, then train**

```bash
python validation/smoke_test.py       # patches behave; trade-off exists
python validation/signal_check.py     # derives λ; confirms learnable signal
python validation/scan_elasticity.py  # shows the degenerate boundary (~0.65)
```

Train PPO in `notebooks/04_train_ppo_colab.ipynb` (Colab GPU), download `best_model.zip` into `models/`, then evaluate locally:

```bash
python -m policy.evaluate models/best_model.zip
```

**4. Robustness sweep** — `notebooks/05_sweep_colab.ipynb` (Colab; resumable). Writes `results/sweep_results.csv`.

## Robustness sweep (elasticity × 5 seeds)

| Elasticity | λ | PPO (± sd) | ToU | ToU3 | Flat | Congestion | PPO − ToU |
|---|---|---|---|---|---|---|---|
| 0.7 | 0.23 | 432.3 ± 3.1 | 341.7 | 374.2 | 373.4 | 396.2 | +90.6 |
| 0.8 | 0.93 | 395.2 ± 2.6 | 318.1 | 341.6 | 338.3 | 378.3 | +77.1 |
| 0.9 | 1.59 | 367.1 ± 2.8 | 296.7 | 311.0 | 305.4 | 362.8 | +70.4 |
| 1.0 | 2.20 | 355.5 ± 2.0 | 275.7 | 282.6 | 274.8 | 351.1 | +79.8 |

Elasticities 0.5 and 0.6 are degenerate (no trade-off) and reported as the boundary condition.

## Tech stack

| Layer | Tool | Version |
|---|---|---|
| Storage | DuckDB | ≥ 0.10 |
| Simulation | Mesa | 2.3.4 (pinned) |
| RL | Stable-Baselines3 / Gymnasium | 2.9.0 / ≥ 0.29 |
| Statistics | scipy, numpy | latest |
| Data / plotting | pandas, matplotlib, seaborn | latest |

## Limitations (read honestly)

- **Abandonment is a modelling assumption, not calibrated.** The session data contains only completed sessions, so there is no ground truth for how many drivers leave when prices rise. The elasticity sweep (0.7–1.0) exists precisely to show the result is not an artefact of one assumed value; it should be grounded against a cited price-elasticity-of-demand range.
- **PPO does not dominate ToU on every KPI.** It trades a little more waiting time for substantially more revenue and throughput; the claim is a better weighted objective at the stated λ, not Pareto dominance.
- **PPO's CO₂ is higher than ToU's**, because it serves more energy. CO₂ is a monitored KPI, not an optimised one (λ_co2 = 0); the `hourly_carbon` flag is available for a carbon-aware extension.
- **Results are conditional on the 2× high-adoption regime.** At present (12%) utilisation, pricing produces sub-1% behavioural effects (Phase 5) — adaptive pricing is a lever for a future, more congested network, not today's.
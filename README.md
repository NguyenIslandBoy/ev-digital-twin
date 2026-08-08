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

All figures are for the high-adoption (3×) regime, the setting where pricing has a genuine effect on behaviour. Scores are the objective `revenue − λ·wait`; margins are paired across identical episode seeds.

| Finding | Evidence |
|---|---|
| **PPO beats the handcrafted ToU schedule** | +24% on the objective and +25% on revenue at the headline config (elasticity 0.8, λ 1.581), Wilcoxon *p* < 0.001 over 500 paired episodes |
| **Robust to the demand assumption and to training seed** | PPO − ToU margin stays **+101 to +181** across elasticity 0.7–1.0; standard deviation across 5 training seeds is only **1.4–5.1 points** |
| **The advantage is state-conditioning, not price granularity** | PPO also beats **ToU3** — a 3-band clock schedule with the same middle tariff — by **+94 to +140** everywhere. More price levels do not close the gap; conditioning on live queue state does |
| **A static ToU schedule is worse than doing nothing** | ToU scores **559.5 < 601.9** for flat pricing: indiscriminate peak pricing sheds more revenue than its wait reduction is worth. Holds at elasticity 0.7–0.9; at 1.0 the two are level (480.6 vs 479.5) |
| **Adaptive pricing has a critical elasticity (≈ 0.65)** | Below it, the high price dominates on *both* revenue and wait, no trade-off exists, and the optimal policy collapses to a static maximum price |

Headline comparison (3× adoption, 500 episodes, elasticity 0.8, λ 1.581):

| Policy | Revenue (£) | Wait (min) | Sessions | Score |
|---|---|---|---|---|
| **PPO** | **700.6** | 1.1 | 62.6 | **695.3** |
| Flat £0.30 | 664.5 | 10.0 | 72.6 | 601.9 |
| ToU (2-band) | 562.5 | 0.6 | 48.4 | 559.5 |

> Note: PPO does **not** minimise waiting time — ToU does, by serving ~23% fewer cars. PPO holds a superior revenue–wait *trade-off* at the chosen λ; it accepts modest congestion to serve more sessions at higher revenue. Nor does it dominate the hand-designed congestion heuristic by much (+7 to +12 points) — most of the available state-conditioning value is reachable without learning. See *Limitations*.

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
├── reports/                     # dissertation, poster, reference material
└── pbi-report/                  # visualise data and findings on Power BI
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

Training uses PPO (Stable-Baselines3) under the high-adoption (3×) regime with an opt-in **price-abandonment** mechanism — the demand-side downside to high prices that makes pricing a real optimisation problem. `λ_wait` is the tie-point between the two constant-price policies, re-derived per elasticity. 3× is the lowest multiplier at which the network is congested enough for that trade-off to exist on defensible terms: at 2× mean waiting is ~1 minute and λ rises above 15, which is not a preference any operator would hold.

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

The metering scrape is a separate opt-in step (`--scrape`, needs `NCL_METERING_COOKIE` in `.env`). Its output was investigated and excluded — see *Data* above — so it is not required to reproduce any result.

**2. EDA → calibration → scenarios** (run in order; notebook 01 writes the `simulation_params` the simulation depends on)

```
notebooks/00_metering_investigation.ipynb
notebooks/01_eda.ipynb
notebooks/02_calibration.ipynb
notebooks/03_scenarios.ipynb
```

**3. Phase 6 — validate, then train**

```bash
python -m validation.smoke_test       # patches behave; trade-off exists
python -m validation.signal_check     # derives λ; confirms learnable signal
python -m validation.scan_elasticity  # shows the degenerate boundary (~0.65)
```

Then train and evaluate — **CPU only, no GPU needed**:

```bash
python -m policy.train               # ~3 min; writes models/best_model.zip
python -m policy.evaluate            # ~15 s; defaults to models/best_model.zip
python validation/plot_price_by_hour.py
```

**4. Robustness sweep** (elasticity × seed, ~59 min, resumable — rerun to continue)

```bash
python -m policy.run_sweep
```

**5. Regenerate the non-RL artefacts** (calibration, scenarios, elasticity boundary, ~40 s)

```bash
python -m validation.regenerate_results
```

`notebooks/04_train_ppo_colab.ipynb` and `05_sweep_colab.ipynb` are the Colab equivalents of steps 3–4. They exist because the simulator used to be ~17× slower; both stages now run locally in the times above. See `results/README.md` for which command produces which file.

## Robustness sweep (elasticity × 5 seeds)

| Elasticity | λ | PPO (± sd) | ToU | ToU3 | Flat | Congestion | PPO − ToU |
|---|---|---|---|---|---|---|---|
| 0.7 | 0.271 | 705.0 ± 5.1 | 603.6 | 610.8 | 649.2 | 692.6 | +101.4 |
| 0.8 | 1.581 | 686.4 ± 2.3 | 560.7 | 576.3 | 590.6 | 677.8 | +125.8 |
| 0.9 | 2.871 | 671.2 ± 3.8 | 519.7 | 548.1 | 532.9 | 664.5 | +151.5 |
| 1.0 | 4.065 | 661.7 ± 1.4 | 480.6 | 521.8 | 479.5 | 654.0 | +181.1 |

λ is re-derived per elasticity over 400 episodes. It is a ratio whose denominator is a small difference between two noisy wait means, so it is sensitive to the episode count — `results/elasticity_boundary.csv` uses 200 episodes and reports different values (1.702 at elasticity 0.8). Quote the episode count wherever λ appears.

Elasticities 0.5 and 0.6 are degenerate (no trade-off) and reported as the boundary condition.

## Tech stack

| Layer | Tool | Version |
|---|---|---|
| Storage | DuckDB | ≥ 0.10 |
| Simulation | Mesa | 2.3.4 (pinned) |
| RL | Stable-Baselines3 / Gymnasium | 2.9.0 / 1.3.0 (both pinned) |
| Statistics | scipy, numpy | latest |
| Data / plotting | pandas, matplotlib, seaborn | latest |

## Limitations (read honestly)

- **Abandonment is a modelling assumption, not calibrated.** The session data contains only completed sessions, so there is no ground truth for how many drivers leave when prices rise. The elasticity sweep (0.7–1.0) exists precisely to show the result is not an artefact of one assumed value; it should be grounded against a cited price-elasticity-of-demand range.
- **PPO does not dominate ToU on every KPI.** It trades a little more waiting time for substantially more revenue and throughput; the claim is a better weighted objective at the stated λ, not Pareto dominance.
- **PPO's CO₂ is higher than ToU's**, because it serves more energy. CO₂ is a monitored KPI, not an optimised one (λ_co2 = 0); the `hourly_carbon` flag is available for a carbon-aware extension.
- **Learning adds less than the state-conditioning itself.** The hand-designed congestion heuristic reaches within 7–12 points of PPO at every elasticity. The large margin is over *clock-based* schedules; against a competent state-aware rule the learned policy wins consistently but narrowly.
- **Results are conditional on the 3× high-adoption regime.** At present (~14%) utilisation, pricing produces sub-1% behavioural effects (Phase 5), and even at 2× mean waiting is ~1 minute — adaptive pricing is a lever for a future, substantially more congested network, not today's.

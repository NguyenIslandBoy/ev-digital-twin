# An AI-Enabled Digital Twin for EV Charging
**Progress Report | CSC8639 MSc Dissertation**
Hoang Nguyen Lai (250539846) | Newcastle University | June 2026

---

## 1. Overview

This report summarises progress on the MSc dissertation project, which develops a calibrated agent-based digital twin of the EV charging network at Newcastle University's Urban Sciences Building (USB). The simulation reproduces real historical charging behaviour, evaluates policy interventions, and will incorporate a reinforcement learning pricing agent as a high-distinction extension. Phases 1 through 5 are complete. Phase 6 (RL) is the sole remaining implementation task.

---

## 2. Remaining Deadlines

| Deadline | Item | Status |
|---|---|---|
| 29 July 2026 | Research Poster (10 pts) | Not started |
| 10 August 2026 | Dissertation submission | In progress |
| 10 August 2026 | Source code submission | Ongoing |
| 13 August 2026 | Oral presentation evidence | Not started |

---

## 3. Work Completed

### Phase 1: Data Engineering

A modular Python pipeline scrapes 30-minute interval energy data from Newcastle University's metering portal across 498 USB building meters (598,596 authenticated POST requests with checkpoint-based fault tolerance). All data is stored in a portable DuckDB database (`ev_twin.duckdb`). A systematic data quality investigation of the two EV-relevant meters revealed systemic collection failures in 34 of 40 months (Pearson r = 0.086), leading to the decision to use the supervisor-provided charging session CSV as the sole data source.

| Table | Rows | Purpose |
|---|---|---|
| `charging_sessions` | 29,775 | Primary calibration data (2021-2024) |
| `metering_raw` | 28,728,144 | Building energy data (investigated, not used) |
| `simulation_params` | 7 parameter sets | Agent calibration parameters from EDA |
| `scrape_checkpoint` | 598,596 | Fault-tolerant resume mechanism |

### Phase 2: Exploratory Data Analysis

A comprehensive EDA was conducted on 29,775 charging sessions across 1,186 real days. Key findings informing agent behaviour are summarised below.

| Finding | Detail | Simulation Implication |
|---|---|---|
| Bimodal arrivals | Peaks at 11:00 and 14:00 to 16:00 | Empirical hourly Poisson sampling |
| Weekday split | 68.93% weekday sessions | Separate scaling by day type |
| Connector mix | IEC_62196_T2_COMBO 82.07% | Categorical sampling per agent |
| Energy demand | Mean 30.4 kWh, Gamma fit poor | Empirical sampling per connector |
| Session duration | Gamma fit confirmed, median 0.64 hrs | Gamma sampling, capped at 4 hrs |
| Charger utilisation | 12% average, 6 chargers | Per-charger capacity modelled |

### Phase 3: Mesa Agent-Based Simulation

The simulation implements two agent types running at 30-minute steps (48 steps per day episode):

- **EVDriverAgent:** samples connector type, energy demand (empirical), and session duration (Gamma) on creation; selects charger via greedy shortest-queue with price sensitivity and carbon deferral behaviour
- **ChargerAgent:** manages single-slot occupancy and queue; tracks per-session energy, revenue, CO2, and wait time metrics

Daily session counts are drawn from a Negative Binomial distribution (r = 7.63, p = 0.23) fitted by method of moments to capture real-world overdispersion (variance = 107.69 >> mean = 25.11), which a Poisson model cannot reproduce.

### Phase 4: Calibration Validation

Two-sample Kolmogorov-Smirnov tests at alpha = 0.05 confirm the simulation is calibrated against the real dataset.

| Distribution | KS Statistic | p-value | Result |
|---|---|---|---|
| Sessions per day | 0.0606 | 0.1442 | PASS |
| Energy per session | 0.0087 | 0.8978 | PASS |

Simulated mean within 1.2% of real (25.42 vs 25.11). Simulated std within 4.1% of real (9.95 vs 10.38).

### Phase 5: Scenario Engine and Policy Evaluation

Six scenarios were evaluated across 500 episodes each. Wilcoxon signed-rank tests compare each against the baseline.

| Scenario | Sessions/Day | Revenue (GBP) | CO2 (gCO2) | Avg Wait (hrs) |
|---|---|---|---|---|
| Baseline | 25.60 (SD 10.04) | 201.53 (SD 79.91) | 38,934 (SD 15,438) | 0.005 (SD 0.02) |
| EV Growth 1.5x | 38.16 (SD 15.05) | 297.80 (SD 120.77) | 57,534 (SD 23,332) | 0.095 (SD 0.19) |
| EV Growth 2.0x | 51.20 (SD 20.08) | 402.25 (SD 161.17) | 77,712 (SD 31,138) | 0.354 (SD 0.46) |
| ToU Pricing | 25.60 (SD 10.04) | 277.90 (SD 111.26) | 38,578 (SD 15,238) | 0.005 (SD 0.02) |
| Carbon Incentives | 25.60 (SD 10.04) | 200.13 (SD 81.00) | 38,665 (SD 15,648) | 0.006 (SD 0.03) |
| Combined Policy | 25.60 (SD 10.04) | 278.03 (SD 113.26) | 38,592 (SD 15,547) | 0.007 (SD 0.03) |

**Key finding:** At 12% baseline utilisation, pricing interventions produce sub-1% behavioural effects. EV adoption growth is the dominant policy lever, increasing wait times by up to 6,981% under a 2x multiplier. This indicates infrastructure expansion is more critical than pricing at the current network scale.

---

## 4. Next Steps

### 4.1 Remaining Code: Phase 6 RL Policy Optimisation

The reinforcement learning extension wraps the Mesa simulation as a Gymnasium-compatible environment and trains a PPO agent to autonomously learn a pricing strategy outperforming handcrafted ToU rules.

| File | Purpose | Status |
|---|---|---|
| `policy/environment.py` | Gymnasium wrapper around ChargingNetworkModel | Not started |
| Colab training notebook | PPO training on A100 GPU (500k timesteps) | Not started |
| `policy/evaluate.py` | Compare PPO vs ToU vs baseline via Wilcoxon test | Not started |

Observation space: current hour, per-charger occupancy and queue length, price signal, carbon intensity. Action space: Discrete(3) price levels at GBP 0.15, GBP 0.30, GBP 0.45. Reward: weighted composite of revenue, CO2 reduction, and wait time penalty.

### 4.2 Research Poster

A one-page A1 research poster is required by 29 July 2026. Content: motivation and project gap, simulation architecture diagram, calibration results, scenario KPI comparison plot, and key findings.

### 4.3 Dissertation Writing

Dissertation writing runs in parallel with RL implementation from June onwards. Target submission: 10 August 2026.

| Chapter | Content | Target Draft |
|---|---|---|
| 1. Introduction | EV context, problem statement, novelty, objectives | June 2026 |
| 2. Literature Review | 5 reviewed papers, gap analysis, positioning | June 2026 |
| 3. Methodology | Data pipeline, EDA, simulation design, calibration | July 2026 |
| 4. Results | Scenario evaluation, Wilcoxon tests, RL comparison | Late July 2026 |
| 5. Discussion | Key findings, limitations, future work | Early August 2026 |
| 6. Conclusion | Summary, contributions, recommendations | Early August 2026 |

---

## 5. Tech Stack

| Layer | Tool | Notes |
|---|---|---|
| Storage | DuckDB | Single portable .duckdb file |
| Data ingestion | Python, requests, pandas | Modular pipeline, checkpoint-based resume |
| Simulation | Mesa 2.3.4 | Pinned version |
| Statistics | scipy, numpy | KS tests, Wilcoxon, NB fitting |
| RL training | Stable-Baselines3, Gymnasium | PPO on Google Colab A100 |
| Visualisation | seaborn, matplotlib | EDA, calibration, scenario plots |
| Version control | GitHub | github.com/NguyenIslandBoy/ev-digital-twin |

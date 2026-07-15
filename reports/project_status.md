# EV Digital Twin - Project Status & Action Plan
**CSC8639 Dissertation | Hoang Nguyen Lai | May 2026**

---

## Upcoming Deadlines

| Deadline | Item | Status |
|---|---|---|
| 29 May 16:00 | Ethical Approval Evidence | [URGENT] Not submitted |
| 5 Jun 16:00 | Interim Report (100 pts) | [IN PROGRESS] |
| 29 Jul 16:00 | Poster | [PENDING] |
| 10 Aug 16:00 | Dissertation Submission | [PENDING] |
| 10 Aug 16:00 | Source Code | [PENDING] |
| 13 Aug 16:00 | Oral Presentation Evidence | [PENDING] |

---

## What Has Been Done

### Data Engineering (Phase 1 - Complete)
- Scraped all 498 USB building meters from Newcastle metering portal
- Identified 2 EV-relevant meters: `USB_E_SwitchMA` and `USB_E_SwitchMB` (115,392 rows)
- Stored all data in DuckDB (`ev_twin.duckdb`) with checkpoint/resume mechanism
- Loaded supervisor CSV (`usb_merged_final_data.csv`) - 29,775 charging sessions, 2021–2024
- Modular project structure: `ingestion/config.py`, `storage.py`, `scraper.py`, `run_scraper.py`

### Exploratory Data Analysis (Phase 2 - Complete)
- Arrival patterns: bimodal peaks at 11–12 and 14–16, strong weekday/weekend split
- Energy distribution: flat plateau 5–20 kWh → empirical sampling preferred over lognormal
- Duration distribution: lognormal fits well, capped at 4 hrs (only 0.11% exceed this)
- Connector type analysis: IEC_62196_T2_COMBO dominates at 82%, distinct energy/duration profiles per type
- Charger utilisation: 6 chargers, uneven load (5000198 and 5000199 handle ~48% of sessions)
- Seasonal patterns: Spring highest, Summer lowest (term-time effect)
- All calibration parameters saved to DuckDB `simulation_params` table

### Literature Review (Ongoing)
- Paper 1: Multi-agent game-theoretic pricing model - utility function, SOC urgency model
- Paper 2: Digital twin for EV infrastructure - ABM with PSO optimisation, GIS integration
- Paper 3: Grid-integrated DT framework - CPO incentive optimisation, demand response
- Paper 4: Smart city DT for building energy benchmarking - smart meter analytics
- Paper 5: Edge-AI RL + AHP framework - ongoing

---

## Immediate Actions (This Week)

### 1. Ethics Form - Submit Before 29 May
- Confirm with supervisor: project is low-risk (no human participants, anonymised institutional data)
- Submit online form at: https://www.ncl.ac.uk/research/researchgovernance/ethics/process/
- Download PDF summary after submission
- Upload to Canvas as evidence

### 2. Key questions to calrify

- Confirm integration strategy: CSV only vs. CSV + metering switchboard data (USB_E_SwitchMA/B)
- Confirm what a distinction-level submission looks like for this project
- Clarify role of second supervisor (Jichun Li) - joint meetings or separate?
- Confirm: is RL optimisation expected as a core deliverable or optional extension?

### 3. Meeting with Dr Jichun Li (Supervisor)
- Present about the progress
- Ask for guidance, the first thing is the **Ethics form**

---

## Interim Report - Due 5 June

### Structure
1. **Introduction**
2. **Aim and objectives**
3. **Overview of progress**
4. **Project plan**
5. **References**
6. **Data management plan**

### Key Content to Include
- EDA plots (arrival distribution, energy/duration, seasonal patterns)
- Calibration parameter table (connector mix, lognormal params, arrival rates)
- Project architecture diagram (ingestion → simulation → RL)
- Gantt chart or timeline

---

## Remaining Phases

### Phase 3 - Mesa Simulation (Target: June)
- `simulation/agents.py` - EVDriverAgent, ChargerAgent
- `simulation/model.py` - ChargingNetworkModel
- Calibrate simulation to reproduce real statistics from CSV
- Validate: simulated kWh distribution vs. real, simulated arrivals vs. real

### Phase 4 - Scenario Engine (Target: July)
- EV adoption growth scenario (scale arrival rates)
- Time-of-use pricing scenario (price signal by hour)
- Carbon-aware incentives scenario (nudge toward low-carbon periods)
- Compare KPIs: utilisation, wait time, CO2, grid load

### Phase 5 - RL Policy Optimisation (Target: July, if on schedule)
- Wrap Mesa simulation as Gym-compatible environment
- Train PPO agent via Stable-Baselines3 on Colab
- Compare learned policy vs. handcrafted rules

### Phase 6 - Writing & Submission (Target: Aug)
- Dissertation draft
- Source code cleanup and documentation
- Poster design
- Oral presentation

---

## Project Stack

| Layer | Tools |
|---|---|
| Data storage | DuckDB (`ev_twin.duckdb`) |
| Data engineering | Python, requests, pandas |
| Simulation | Mesa (agent-based modelling) |
| RL training | Stable-Baselines3, Gymnasium (Colab) |
| Analysis | scipy, seaborn, matplotlib |
| Environment | Python 3.13 (school), 3.14 (laptop), venv at `C:\venvs\ev_digital_twin` |


Questions to address:
Create a shared folder to track progress
I will think of this
Data integration strategy

# Project 86: AI-Enabled Digital Twin for Low-Carbon and Grid-Resilient EV Charging Networks

**Supervisor(s):** Sanchari Deb, School of Engineering, Newcastle University  
**Keywords:** AI, Charging, EV, Agent-based modelling, Digital twin  

---

## 📖 Project Description

This project develops an AI-powered digital twin of an EV charging network using historical charging session data (timestamps, kWh, duration, charger/connector type, utilization, location, carbon intensity/emissions, seasonality). 

The digital twin will be implemented as an **agent-based simulation** where EV drivers are modelled as heterogeneous agents making charging decisions (when, where, and how much to charge), and charging stations are treated as resources with capacity constraints.

### "What-If" Policy Evaluation
The digital twin will be used to evaluate “what-if” policies under realistic behavioral dynamics and uncertainty, including:
1. **EV adoption growth:** Increasing arrival rates and demand intensity.
2. **Time-of-use (ToU) pricing:** Price signals varying by hour or day.
3. **Carbon price / carbon-aware incentives:** Nudging charging toward lower-carbon periods.

### Optimisation Stage
A final stage introduces policy optimisation (e.g., Reinforcement Learning or search-based optimisation) to automatically learn incentive and pricing strategies. The goal is to balance:
* Grid load smoothing
* Station utilization
* User waiting times and availability
* CO₂ reduction

---

## 🛠️ Skills & Requirements

### Essential Requirements
* **Strong Python** programming skills.
* **Data science / Machine Learning foundations** (feature engineering, model evaluation).
* **Probability & statistics** (distributions, simulation, uncertainty).

### Preferable (but can be learned)
* Agent-based modelling.
* Reinforcement learning basics (e.g., Q-learning / DQN concepts).
* Optimisation fundamentals (constraints, objective functions).

---

## 🎯 Expected Outcomes & Deliverables

* **Calibrated Digital Twin:** An agent-based simulator that successfully reproduces key statistics from the historical dataset (distributions of kWh, duration, arrival times, utilization patterns).
* **Scenario Engine:** A framework to stress-test policies under EV adoption growth, ToU pricing, and carbon price/incentives.
* **Policy Evaluation Report:** An analysis comparing the baseline against various interventions using multiple Key Performance Indicators (KPIs).
* **Optional (High-Distinction Extension):** A policy optimisation module (RL or heuristic optimisation) that autonomously learns better incentive/pricing strategies than handcrafted rules.
* **Final Project Deliverables:** * Reproducible codebase
  * Comprehensive documentation
  * Final dissertation-level analysis
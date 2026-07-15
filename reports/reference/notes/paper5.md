# Edge-AI based multi-criteria optimization framework for dynamic EV charging with real-time grid load, traffic, and user behavior integration

(https://link.springer.com/article/10.1007/s00607-025-01531-x)

## Abstract

- Managing electric vehicle (EV) charging in real-time while minimising energy cost and maintaining grid stability is challenging
- Existing methods struggle to adapt to rapid influx of heterogeneous data
> Introduce Edge-AI based optimisation framework that enables real-time EV charging with multiple criteria
    > Using a hybrid algorithm: Reinforcement Learning with the Analytic Hierarchy Process (AHP) to evaluate and prioritise conflicting objectives such as reducing wait time, minimising grid strain, lowering electricity costs, and decresing emissions
    > Achieved low-latency reponsiveness and enhanced resilience against connectivity failures
    > Results: 23.5% shorter wait time, 18.2% improvement in grid utilisation, and 21.7% cost reduction compared to conventional approaches

## Introduction

- **Context & Motivation**
    - Rapid EV adoption (projected >1/3 of new US vehicle sales by 2030) demands proportional upgrades to charging infrastructure
    - Current charging systems rely on **static logic or centralised scheduling**, unable to adapt to real-time variations in traffic, energy pricing, grid load, and driver behaviour — leading to suboptimal usage, wait times, and grid instability
- **Limitations of Existing Approaches**
    - Cloud-based AI solutions suffer from **latency, bandwidth limitations**, and failure under intermittent connectivity
    - Most AI-driven systems optimise for a **single outcome** (e.g., cost or time), ignoring the multifactorial nature of real-world EV charging
    - Data sources are used **in isolation** — few systems integrate traffic conditions, dynamic tariffs, grid strain, and driver behaviour simultaneously
- **Proposed Solution: Edge-AI Optimisation Framework**
    - Embeds intelligent algorithms **at the station or vehicle level** for rapid, autonomous, low-latency decision-making without reliance on remote servers
    - Integrates multiple real-time data streams: road and traffic conditions, utility load profiles and time-of-use pricing, vehicle state-of-charge, and driver-specific behavioural patterns
    - Core algorithm combines **Reinforcement Learning (RL)** — which dynamically adapts to environmental feedback — and the **Analytic Hierarchy Process (AHP)** — a structured multi-criteria decision-making technique to balance conflicting objectives
- **Optimisation Objectives**
    - **Queue duration:** minimise wait times at charging stations
    - **Grid load:** reduce peak demand and prevent local grid instability
    - **Electricity cost:** leverage dynamic pricing to lower charging costs
    - **Environmental sustainability:** incorporate carbon intensity and renewable energy availability
- **Key Advantages**
    - **Personalised** charging strategies based on user urgency, cost preference, and environmental priorities
    - **Distributed demand** across station networks to smooth peak usage
    - **Scalable** across urban, suburban, and highway environments without requiring a centralised controller
    - Aligned with US federal priorities under the **Bipartisan Infrastructure Law** and **Inflation Reduction Act**
- **Contributions**
    1. Integrated edge-computing framework combining multiple optimisation methods and data types into a unified EV charging system
    2. Flexible and scalable deployment model for diverse real-world environments
    3. Validated through simulations using real and synthetic data, demonstrating quantitative improvements in operational efficiency and energy usage

## Related Work

### Decentralised processing through edge computing

- **Edge computing:** enables processing data at or near the source rather than relying solely on centralised cloud servers:
    - improved real-time response and autonomy in decision-making at the station level (Al Gafri et al.)
    - analysed the application of edge devices across electric transportation systems and noted the potential for enhanced latency control and resilience, particularly in volatile grid conditions (Arévalo et al.)
- However, edge-oriented systems are 
    - still rudimentary, often serving only as localised data filters or basic execution nodes
    - lack sophisticated predictive capabilities or the capacity to adapt to fast-changing traffic and grid variables
    - without deeper integration of intelligent algorithms, remain underutilised in dynamic urban energy environments
    > decentralized approach supports real-time load balancing, crucial for managing energy demand fluctuations in urban areas (Alghamdi et al.)

### Adaptive Learning Models for EV Charging Decisions
- **Role of AI & RL:** Reinforcement learning (RL) has become central in optimising energy flows within EV charging networks, outperforming static or rule-based schedulers by adapting to evolving demand and infrastructure constraints
- **Key Approaches:**
    - Zhao used deep RL within a **Markov Decision Process (MDP)** framework to regulate charging behaviour in response to congestion, availability, and vehicle movement
    - Mosammam et al. implemented **Q-learning** to manage trade-offs between energy efficiency and battery health in plug-in hybrid EVs
    - Said et al. proposed scheduling protocols for home charging with **time-of-use pricing**, showing how adaptive models can incorporate dynamic electricity prices
- **Remaining Gap:** Even advanced multi-agent RL systems often fail to address **multiple optimisation targets concurrently**, limiting their applicability for holistic system-level control

### Decision Models Based on Multiple Objectives
- **Why MCDM:** Real-world EV charging optimisation involves inherently multi-dimensional trade-offs — economic, technical, and environmental — driving adoption of **Multi-Criteria Decision-Making (MCDM)** methods including AHP, fuzzy logic, and composite scoring
- **Key Studies:**
    - Al Gafri et al. applied **AHP** to select charging station locations based on cost, accessibility, and grid readiness — demonstrating enhanced transparency and reproducibility
    - Kumar et al. combined **AHP with differential search optimisation** for sustainable EV infrastructure planning, adapting to both energy policy and user behaviour
    - Said and Moufah integrated AHP into a **real-time load management protocol** for dynamic load balancing and efficient energy distribution
- **Remaining Gap:** Most MCDM frameworks operate in **static or simulation-only contexts**, rarely ingesting live data — limiting practical value in urban ecosystems that evolve hour by hour

### Real-Time Data Fusion for Charging Optimisation
- **Underutilised Opportunity:** Integration of diverse real-time data sources — road congestion, user travel history, and dynamic electricity prices — remains uncommon despite its potential
- **Key Studies:**
    - Suanpang and Jamjuntr noted that combining mobility, environmental, and grid-layer inputs into a **singular AI model** is rare
    - Radenkovic and Huynh integrated energy state and traffic data in fog and vehicular edge networks to improve system robustness — but fell short of fully synchronising user mobility profiles, traffic density, and live grid load
    - Alghamdi et al. proposed **profit maximisation for EV stations** using renewable energy sources, demonstrating how sustainability and profitability can coexist in real-time optimisation
- **Remaining Gap:** A cohesive control mechanism that combines **traffic behaviour, grid intelligence, and user history** running at the edge has yet to be realised

### Identified Limitations in State-of-the-Art Models
- **Narrow Objective Focus:** Most strategies address isolated goals — time minimisation or cost reduction — without unifying grid sustainability, carbon emissions, and user satisfaction
- **Overreliance on Cloud Computing:** Despite efficiency gains, most RL implementations depend on cloud-hosted environments prone to **latency and connectivity requirements**
- **Insufficient Personalisation:** Many systems overlook user diversity in urgency, energy needs, and behavioural preferences, limiting adaptive, user-centric service delivery
- **Opaque Decision Logic:** Most AI models offer minimal **explainability**, complicating validation, public deployment, and regulatory acceptance
- **Research Response:** This study addresses these gaps by combining **Reinforcement Learning and AHP** into a real-time optimisation engine designed for distributed execution at EV stations or on-vehicle platforms

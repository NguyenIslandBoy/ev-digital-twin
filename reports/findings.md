# EV Charging Network at Urban Sciences Building
## Research Findings Report
**Prepared by:** Hoang Nguyen Lai, MSc Data Science
**Date:** June 2026

---

## What This Project Is Doing

This project is building a virtual replica of the USB EV charging network — a digital twin — that can simulate how drivers use the six chargers on a day-to-day basis. Once the virtual model accurately reproduces real behaviour, it can be used to test policy questions such as: what happens to queues and emissions if EV ownership doubles? Would time-varying prices reduce peak demand? The goal is to answer these questions through simulation rather than by experimenting on the live network.

---

## What the Real Data Showed

The dataset you provided covers 29,775 charging sessions between March 2021 and July 2024. Several patterns emerged that are relevant to infrastructure planning.

**Usage is concentrated in teaching hours.** Arrivals peak sharply between 11:00 and 12:00, and again between 14:00 and 16:00. This matches the USB lecture schedule. Outside of these windows, charger demand drops considerably. Overnight, the network is almost entirely unused.

**The network is lightly loaded at present.** Across the three-year dataset, the average charger utilisation rate is 12%. This means chargers are occupied for roughly three hours out of every 24. At this level of utilisation, drivers almost never queue — the average waiting time in the historical data is negligible.

**EV adoption has grown steadily.** Sessions increased from approximately 4,000 in 2021 to over 11,000 in 2023, representing nearly a threefold increase in three years. If this trend continues, the network will face meaningful capacity pressure within the next few years.

**Two chargers carry a disproportionate share of the load.** Chargers 5000198 and 5000199 together account for approximately 48% of all sessions. This suggests either a location advantage (closer to building entrances or car parks) or a connector type preference among USB users.

**Energy demand varies significantly by connector type.** The dominant connector (IEC 62196 Type 2 Combo, used in 82% of sessions) delivers an average of 34 kWh per session — consistent with DC fast charging. The CHAdeMO connector delivers around 14 kWh per session on average. This distinction matters for grid load calculations.

---

## What the Simulation Found

A simulation was built and validated against the real dataset. It correctly reproduces the number of charging sessions per day and the energy demand per session to a statistically confirmed level of accuracy. Once validated, the simulation was used to test three policy scenarios.

### Scenario 1: EV Adoption Growth

Two growth levels were tested — a 50% increase in daily arrivals (representing near-term growth over two to three years) and a 100% increase (representing a doubling of EV ownership over four to five years).

The results are striking. At 50% growth, average waiting times increase by approximately 1,800% compared to today. At 100% growth, waiting times increase by nearly 7,000%. Put simply, the current six-charger network cannot accommodate a doubling of EV demand without significant queuing. Carbon emissions from charging scale proportionally with demand, increasing by 48% and 100% respectively.

This finding suggests that infrastructure expansion — adding chargers or increasing charging speed — is the most important policy decision facing the USB network over the next five years.

### Scenario 2: Time-of-Use Pricing

A pricing structure was tested in which the cost per kWh is higher during peak hours (07:00 to 19:00) and lower overnight. The specific rates tested were £0.45 per kWh during peak hours and £0.15 per kWh off-peak, compared to a flat baseline rate of £0.30 per kWh.

Revenue from charging increased by approximately 38% under this pricing structure, simply because most charging occurs during peak hours when the higher rate applies. However, the impact on driver behaviour was modest. Total daily sessions and carbon emissions changed by less than 1%. This is consistent with the low-utilisation finding — when chargers are readily available, drivers have little incentive to shift their behaviour in response to price signals.

**Practical implication:** Time-of-use pricing is an effective revenue tool for the USB network but is unlikely to meaningfully reduce peak demand or carbon emissions at current utilisation levels.

### Scenario 3: Carbon-Aware Incentives

A small financial penalty was applied to charging during periods of high grid carbon intensity — typically morning and evening peaks when gas generation dominates the UK grid. Drivers could reduce their charging cost by choosing to charge during low-carbon periods such as midday or overnight.

The effect was small but directionally correct: carbon emissions from USB charging fell by approximately 0.7% and total energy delivered fell slightly. As with pricing, the impact is limited by the fact that chargers are rarely congested, so drivers experience little friction regardless of when they charge.

**Practical implication:** Carbon-aware incentives have limited effectiveness as a standalone measure at current utilisation. Their impact would grow significantly if applied in a higher-utilisation network.

---

## The Central Finding

The most important insight from this analysis is that **the USB EV charging network is currently demand-constrained, not supply-constrained**. Chargers are available when needed, so price signals and carbon incentives have limited ability to change behaviour. The network operates comfortably today, but growth in EV ownership will change this rapidly.

The simulation indicates that even a 50% increase in daily charging sessions — achievable within two to three years at recent growth rates — would push the network into a regime where queuing becomes a regular experience for users. At that point, both pricing and carbon incentive policies become far more effective levers, because drivers face real trade-offs about when and where to charge.

---

## What Comes Next

The final stage of the project will train an artificial intelligence agent to automatically discover the best possible pricing strategy for the USB network. Rather than testing fixed price schedules manually, the AI will learn through repeated simulation which pricing decisions best balance revenue, carbon reduction, and user waiting time simultaneously. This will be compared directly against the handcrafted time-of-use pricing scenario to determine whether an automated approach can outperform a manually designed policy.

The dissertation will be submitted in August 2026 alongside a full reproducible codebase and a research poster summarising the key findings.

---

## Summary Table

| Question | Answer |
|---|---|
| How busy is the USB network today? | 12% average utilisation — lightly loaded |
| When is demand highest? | 11:00 to 12:00 and 14:00 to 16:00 (lecture hours) |
| How fast is demand growing? | Approximately threefold increase from 2021 to 2023 |
| What happens if EV ownership doubles? | Waiting times increase by up to 7,000% — infrastructure expansion needed |
| Does time-of-use pricing reduce peak demand? | No meaningful effect at current utilisation; revenue increases by 38% |
| Does carbon-aware pricing reduce emissions? | Small effect (0.7% reduction) — larger impact expected as utilisation grows |
| What is the most important policy recommendation? | Plan for infrastructure expansion within the next two to three years |

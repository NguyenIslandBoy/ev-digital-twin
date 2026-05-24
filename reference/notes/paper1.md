# 1. Multi-Agent Game-Theoretic Modelling of Electric Vehicle Charging Behavior and Pricing Optimization in Dynamic Ecosystems 

(<https://www.sciencedirect.com/science/article/pii/S1877050925007963>)

(EV: Electric Vehicle) (SOC: State of Charging) (EVCS: Electric Vehicle Charging Station)

## Abstarct

-   Dynamic interactions between electric vehicles (EVs) and electric vehicle charging stations (EVCSs) through a multi-agent simulation
-   Models EV **commuting behavior, charging decisions, and dynamic pricing strategies** to analyze their **impact** on **station utilization and energy distribution**
-   Each vehicle follows a logistic urgency model and a utility function to evaluate trade-offs between charging at home or office stations
-   **RESULT**: \> dynamic pricing **effectively mitigates congestion** at high-demand stations during peak hours while improving resource utilization

> Emphasize the importance of personalized decision-making frameworks and flexible pricing strategies in optimizing EVCS operations.

> integrating real-time pricing and adaptive charging infrastructure in smart cities, with future work exploring real-world traffic patterns, renewable energy integration, and vehicle-to-grid (V2G) interactions to enhance system sustainability

## Objective

This study aims to analyze the charging behavior of electric vehicles (EVs) and the operational performance of electric vehicle charging stations (EVCSs) using a 30-day simulation of 101 EVs.

> Investigates EV decision-making in selecting charging stations based on a utility-based model that considers charging cost, wait time, SOC levels, and station distance.

> Examines dynamic pricing strategies, particularly at office stations, assessing how cost-sensitive EVs minimize expenses while time-sensitive EVs prioritize shorter queues despite higher costs.

> Model EVCS resource management, including slot allocation, queue dynamics, and demand-based utilization. The study evaluates how dynamic pricing reduces congestion, balances station loads, and improves efficiency by redistributing demand between peak and off-peak hours.

> Optimizing EVCS infrastructure, including strategic station placement, load balancing, and adaptive pricing policies.

> Future work may incorporate real-world traffic patterns, renewable energy sources, and vehicle-to-grid (V2G) technologies to further enhance system resilience and sustainability.

## Methodology

-   Employs a simulation-based framework to analyze the charging behavior of electric vehicles (EVs) and the operational management of electric vehicle charging stations (EVCSs)

### EV Commuting and SOC Dynamics

Each EV follows a daily routine, departing from home to reach the office by 8AM and returning home between 4PM and 7PM. SOC depletes during each commute based on travel distance and battery capacity, computed as:

$$
\text{EnergyLoss} (\%) = \frac{\text{DistanceToOffice}}{\text{BatteryCapacity (kWh)}} \times 100
$$

If an EV's SOC falls below a predefined threshold, it evaluates the need to charge using a utility-based decision model

### Charging Decision Model

EVs select charging stations based on a utility function incorporating multiple factors: charging cost $(C)$, total waiting and charging time $(T)$, SOC urgency $(S)$, and distance to the station $(D)$:

$$
U = -(w_c \cdot C + w_T \cdot T - w_S \cdot S - w_D \cdot D)
$$

where $w_c$, $w_T$, $w_S$, and $w_D$ are weight coefiicients reflecting the relative importance of each factor. The SOC urgency factor $(S)$ follows a logistic function:

$$
S = \frac{1}{1 + e^{-k\cdot (\text{SOC} - \text{SOCThresHold})}}
$$

where $k$ is a sentivity parameter controlling the rate at which urgency increases as SOC approaches the threshold. The distance factor $(D)$ is computed using the Euclidean distance:

$$
D = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}
$$

where $(x_1 - x_2)$ and $(y_1 - y_2)$ are the coordinates of the EV and the EVCS, respectively. EVs evaluate all available charging stations and select the one with the highest ultility if a charging slot is available. if no slots are free, the EV defers charging until a later time.

### EVCS Operations and Charging Process

Each EVCS manages a limited number of charging slots. When an EV request charging, it enters a queue if all slots are occupied. The estimated waiting time is determined by the queue length:

$$
\text{TotalWaitingTime} = \frac{\text{EnergyRequired(kWh)}}{\text{ChargingSpeed(kWh/hour)}}
$$

Charging continues until the EV reaches full SOC or completes the estimated charging time. EVCS stations track slot occupancy and manage queues dynamically.

### Dynamic Pricing Mechanism

EVCSs implement dynacmic pricing to balance demand. The price per unit of energy increases when demand is hihg and decreases when utilization is low. Specifically:

-   If occuppancy exceeds a threshold (e.g., monitoring and evening peak hours), the price increases to reduce congestion
-   During low-demand periods, prices decrease to attract more EVs

This pricing adjustment encourages cost-sensitive EVs to charge at off-peak times, reducing waiting times and optimizing station utilization.

### Simulation Execution

The simulation operates over a fixed horizon, divided into hourly increments. At each time steps:

-   EVs update their SOC based on commuting patterns.
-   EVs evaluate charging station options based on their utility function.
-   If required, EVs attempt to charge at an available EVCS.
-   EVCSs allocate slots, manage queues, and dynamically adjust pricing.

Key perfomance metrics, including station utilization, queue lengths, and EV charging preferences, are logged for analysis. The results provide insights into optimizing EVCS infracstructure for efficient distribution and reduced congestion.

## Discussion

Figure 1 shows a pie chart indicating that about 65% of EVs choose to charge at the office ("ChargeOffice") compared to 35% that skip office charging ("SkipOfficeCharge"). Key factors influencing these decisions include state of charge (SOC) thresholds, dynamic pricing, and queue lengths. EVs with higher SOC or lower cost sensitivity may bypass office charging for home stations, while those with urgent needs often charge at the office. This division points to the need for location- and time-based strategies in managing charging demand, suggesting that a well-designed pricing scheme could encourage users to charge during off-peak hours, thus alleviating congestion.

Figures 2 and 3 illustrate how waiting times and queues vary at different Electric Vehicle Charging Stations (EVCS). Waiting time encompasses both the queuing duration and the actual charging duration. Some stations, like the Office station, efficiently manage high queues with sufficient capacity and fast charging rates, resulting in lower total waiting times. Conversely, Home1 and Home2 experience longer waiting times during peak hours due to demand surges, emphasizing the influence of station throughput and timing on the overall waiting experience. The study highlights the need for improved capacity management, charging speeds, and dynamic pricing to mitigate congestion and enhance the efficiency of EV charging operations. Additionally, it discusses how EV charging decisions are affected by the State of Charge (SOC), waiting time, travel distance, and cost, reinforcing the importance of strategic EVCS placement and flexible pricing to cater to diverse user preferences.

## Conclusion

In conclusion, the study highlights the significance of understanding electric vehicle (EV) charging behaviors and improving the operational strategies of charging stations to meet rising demand. Charging choices are driven by factors such as state of charge urgency, cost sensitivity, and location proximity. High-demand stations can face congestion, leading to lower utility during peak times. Implementing dynamic pricing and optimizing capacity can help manage this by incentivizing off-peak charging. Future improvements could include utilizing real-time traffic data and renewable energy to enhance sustainability, alongside using machine learning for better forecasting and scheduling of EV charging. Expanding simulations to consider different vehicle types and user preferences would provide deeper insights into charging behaviors, fostering a more adaptive EV charging ecosystem.

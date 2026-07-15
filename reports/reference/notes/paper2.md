# 2. A Digital Twin Framework for Decision-Support and Optimization of EV Charging Infrastructure in Localized Urban Systems

(<https://arxiv.org/abs/2510.24758>)

## Abstract

-   The model evaluates operational policies, EV station configurations, and renewable energy resources.
-   20% drop in solar efficiency from Oct to Mar, with wind power contributing under 5% of the demand -\> need for adaptive energy management.
-   Newly available charging slots improve user satisfaction, while gasoline bans and idle enhance slot turnover with minimal added complexity.
-   Embedded metaheuristic optimization identifies near-optimal mixes of fast and standard soloar-powered charges, balancing energy performance, profitability, and demand with high computational efficiency.
-   Digital twin provides a flexible, computation-driven platform for EV infrastructure planning that enables scalingfrom localized to city-wide urban contexts

## Introduction

**Questions to address** \> How can a DT with real-time simulation and visualisation support EV infrastructure and energy planning? \> How can dynamic simulations and optimisation algorithms be combined to evaluate policies and station configurations?

-   Existing studies rely on static mathematical and optimization models that oversimplify EV behaviours and interations with infrastructure. Micro-level approaches like agent-based modelling (ABM) using simulation software, have merged to capture EV drivers' daily travel patterns and charging behaviours.
-   Most focusing on station placement and simple capacity sizing often neglect operational policies and energy variability
-   Many simulations frameworks also lack interactive dashboards, limiting pratical application for planners.

> Digital Twin (DT) technology (combining dynamic simulation with decision-support tools) will optimize infrastructure under varying demand conditions

-   Acting as a virtual laboratory, it enables stakeholders to test strategies before implementation, bridging the gap between simulation and real-world deployment
-   Although this study demonstrates the framework in a campus-scale environment, the modular structure and logic of the proposed DT approach are designed to scale effectively for urban system planning.

## Literature review

### Evaluating policy impact on EV Charging Station Operation

-   Agent-based simulations have evaluated policy effectiveness by modelling consumer behaviour and competition between charging and fuel stations
-   Agent-based can access urban policies such as accessing restrictions and shared mobility integration.
-   Need a more flexible and comprehensive framework that integrates policy evaluation, enabling data-driven decision-making insights

### EV charging infrastructure capacity optimisation

-   Charging port numbers directly impact station throughput and user satisfaction. Queuing theory and heuristic algorithms, including Genetic Algorithms (GA), Particle Swarm Optimisation (PSO), and Ant Colony Optimisation (ACO), have been applied to solve complex location and sizing optimisation problems, ensuring cost-effective and efficient EVCS deployment.
-   Potential of real-time inter-agent communication through decentralisedparking coordination, underscoring its value for improving urban nobility efficiency.

### Planning renewable energy integration in EV charging stations

-   Integrating renewable energy enhances grid stability and accommodate more EVs.
-   Nonlinear stochastic programming models, bilevel programming optimize EV charging behaviour to mitigate energy intermittency and minimize costs.
-   Simulation tools such as MATLAB Simulink, HOMER, and GAMS are commonly used to optimize the performance of EV charging stations but lack interactive dashboards

## Methodology

### Description of the Agent-based Simulation Model

-   Using GAMA platform for GIS integration and ability to create visualisations

### Model environment

-   Using GIS layers from OpenStreetMap (OSM) to sketch building footprints from satellite imagery to represent roads, buildings, and infrastructure.
-   The simulation incorporates spatial data to support allocation of agents and activities
-   The environment is conceptualized as an active agent layer interacting with vehicle and energy agents
-   The spatial layer being modified easily makes the model applicable to different areas.
-   About the environemnt: (Figure 1)
    -   Layout: 754m x 631m, extending to nearby area: 1174m x 1131m
    -   Key features: residential buildings, parking areas, and car-accessible roads, pedestrian-only paths, campus boundaries, other campus buildings
-   OSM provides data related to lane count, speed limits, and traffic direction

### Model entities (3 sub-models)

-   Charging station sub-model: campus environment: buildings, roads, and charging areas, with residential buildings as initialisation points for vehicles and road network simulates real-world traffic infrastructure

*Table 1: Variables defining the characteristics of charging areas agent, including the number and type of charging ports available at each location*

| Variable Name | Description | Type | Value Range |
|----|----|----|----|
| `location_CS` | The location of the charging area | string | {"C-Parking", "J-Parking"} |
| `activeCS_11kW` | Number of 11kW CPs | integer | \[0; 50\] |
| `activeCS_30kW` | Number of 30kW CPs | integer | \[0; 10\] |
| `num_CS` | Total number of CPs at each building | integer | \[0; 100\] |

-   The energy sub-model incorporates renewable energy sources into the charging infrastructure, costing of 3 agents: BESS (Battery Energy Storage System), solarEngergy, and windEnergy (computes energy production and system costs of solar irradiation, air temprature, and wind speed)

*Table 2: Key attributes of agents in the energy sub-model, detailing parameters for energy output calculations based on renewable energy sources.*

| Agent Name | Variable Name | Description | Type | Value Range |
|----|----|----|----|----|
| `bess` | `bess_capacity` | BESS storage capacity | float | 80000 kW |
|  | `bess_SoC` | Stored energy in BESS | float | \[0; 80000\] |
| `solarEnergy` | `solar_ghi` | Solar irradiation | float | \[0; 1000\] |
|  | `air_temp` | Air temperature | float | \[0; 40\] |
|  | `nb_solar` | Number of PV panels | integer | \[0; 1000\] |
|  | `unit_panel_area` | Area of a PV panel | float | 2.7 m² |
|  | `total_panel_area` | Total PV area | float | \[0; 2700\] |
|  | `current_panel_tmp` | Actual PV temperature | float | \[0; 40\] |
|  | `solar_generated` | Solar energy generated | float | \[0; +∞\] |
|  | `solar_cost` | Total PV system cost | float | \[0; +∞\] |
| `windEnergy` | `wind_speed` | Actual wind speed | float | \[0; 10\] |
|  | `nb_wind` | Number of turbines | integer | \[0; 15\] |
|  | `wind_generated` | Wind energy generated | float | \[0; +∞\] |
|  | `wind_cost` | Total wind system cost | float | \[0; +∞\] |

-   The traffic sub-model governs vehicle movements, determining parking and charging slot selection: gasoline-powered cars and electric vehicles (agents). These agents make charging decisions based on station availability, energy demand, and individual priority, providing a realistic simulation of real-world constraints.

*Table 3: Attributes for electric vehicles agent, including state of charge, owner satisfaction, charging status, and station preferences.*

| Variable Name | Description | Type | Value Range |
|----|----|----|----|
| `nb_electrical` | Number of EVs per day | integer | \[30; 200\] |
| `is_charging` | EV is charging or not | bool | {true, false} |
| `satisfied` | EV can access a port when needed | bool | {true, false} |
| `SoC` | Battery level (%) assigned daily | float | \[20; 90\] |
| `EV_model` | EV models at VinUni | string | {"VFe34", "VF8", "VF9"} |
| `priority_des` | Preference to stay in the current lot | bool | {true, false} |
| `priority_fast` | Preference for fast/slow charging | bool | {true, false} |

### Model processes

-   Time-stepped approach, 5-minute interval between each step
-   If charging infrastructure includes renewable energy, the energy sub-model is exucuted first to estimate daily energy generation, then traffic and chargign station sub-models are updated sequentially
-   Weather data is retrieved at 5-minute intervals at the beginning of each day.
-   The photovoltaic (PV) power output $(P_PV(t))$ is calculated by:

$$
P_PV(t) = k\cdot \frac{G(t)}{G_{ref}} P_{PV,STC}\cdot \eta_{PV}\cdot [1-\beta_T\cdot (T_c(t)-T_{c,STC})]
$$

where - $k = 1.15$: Bifacial PV panel absorption efficiency - $G(t)$: Solar irradiance at time $t, G_{ref} = 800W$: Reference irradiance - $P_{PV, STC} = 610W$: Rated power of PV panel - $\eta_{PV} = 22.6%$: Solar absorption efficiency - $\beta = 0.0028$: Temprature-dependent power degradation coeficient - $T_{c,STC} = 25$: Panel temprature under standard conditions - $T_c(t)$: Panel temprature computed by air temprature at time $t$

-   Wind power generation $P_W(t)$ is calculated based on wind speed at the hub height:

$$
P_W(t) = \begin{cases}
0, & \text{if } v \leq v_{cut-in} \text{ or } v \geq v_{cut-out} \\
P_{rated} \cdot \dfrac{v^3(t) - v^3_{cut-in}}{v^3_r - v^3_{cut-in}}, & \text{if } v_{cut-in} \leq v \leq v_r \\
P_{rated}, & \text{if } v_r \leq v \leq v_{cut-out}
\end{cases}
$$

where - $v(t)$: Actual wind speed at time $t$, calculated proportionally based on actual wind speed and reference wind speed and turbine height - $P_{rated}= 3000W$: Rated power output - $v_{cut-in} = 3.5 m/s, v_{cut-out} = 45 m/s$: Cut-in and cut-out wind speeds - $v_r = 12 m/s$: Rated wind speed

-   At the start of each cycle, global variables are initialized, and agents are instantiated to represent initial conditions. Each vehicle's behaviour is determined by its state, with decision-making processes trigerring transitions between states based on predefined conditions

*Table 4: Common state variables for electric and gasoline vehicles, outlining their parking and movement behaviors.*

| Variable Name | Description | Type | Value Range |
|----|----|----|----|
| `parking_area` | Targeted parking lot | chargingAreas | {"C-Parking", "J-Parking"} |
| `home` | Initial location | residential | one_of(residential_areas) |
| `start_work` | Start work time | integer | \[8; 9\] or \[12; 14\] |
| `end_work` | End work time | integer | \[17; 19\] |
| `moving_obj` | Car's movement state | string | {"resting", "parking", "working", "leaving"} |
| `parking_slot` | Parking slot type | string | {"active_CS", "inactive_CS"} |
| `in_parkingArea` | Car in parking area? | bool | {true, false} |

``` mermaid
flowchart TD
    Start([Start]) --> WithinTime{Within Time?}
    WithinTime -- No --> StopExit([Stop/Exit])
    WithinTime -- Yes --> Resting[Resting State]

    Resting --> StartWork{Start work time?}
    StartWork -- No --> CheckProb{Check prob move?}
    CheckProb -- Yes --> TimeBtw{Time btw 10am & 15pm?}
    CheckProb -- P --> RandomMove[Random move]

    TimeBtw -- No --> Working[Working State]
    TimeBtw -- Yes --> EndWork{End work time?}
    Working -- 1-p --> Resting

    EndWork -- No --> GetSlot{Get parking slot?}
    EndWork -- Yes --> MoveToGate[Move to Gate]

    GetSlot -- Yes --> DoAssign[Do Assign Slot]
    GetSlot -- No --> Working
    DoAssign --> MoveToGate

    StartWork -- Yes --> MoveToGate
    RandomMove --> MoveToGate

    MoveToGate --> GoInside{Go inside?}
    GoInside -- Yes --> Parking[Parking State]
    GoInside -- No --> Leaving[Leaving State]

    Leaving --> AtGate{At Gate?}
    AtGate -- No --> Reset[Reset]
    AtGate -- Yes --> DoneReset{Done reset?}
    DoneReset -- No --> Reset
    DoneReset -- Yes --> Start
```

*Figure 2: Decision-making process of vehicle agents. Each timestep follows the same loop for gasoline and EVs, except in "Do Assign Slot," where EV parking depends on SoC and station preferences.*

-   Vehicles begin in a Resting State and proceed to the campus gate at the start time of their work.
-   Key distinction between gasoline vehicles and EVs lies in the "Do Assign Slot" function determining parking or charging slots based on the state of charge (SoC) and individual preferences
-   $SoC \leq 35\%$ -\> charging; $35\% \leq  SoC \leq 70\%$ -\> charge based on predefined probability; $SoC \geq 70\%$ -\> sufficiently charged and randomly assigned to inactive charging ports instead
-   Charging and station preferences (`priority_des` and `priority_fast`) influence slot selection
-   The model continuously updates params like enegery production, SoC of EV, and traffic flow, at the end of the day, KPIs are aggregated and visualised to evaluate performance and identify oppotunities and optimisation

### Input data

-   Charging infrasrtucture and vehicle usage patterns in parking areas
-   The number of EVs and gasoline vehicles, classified EV types, and recorded parking locations during peak hours (9AM amd 2PM) were tracked manually over a week.
-   An online survey and qualitative interviews gathered driver behaviour insights, covering demographics, parking, and charging habits, and system improvement suggestions
-   Available engergy consumption data for EV charging total electricity usage (kWh)
-   Historical solar and wind data from Solcat

### Evaluation metrics and objective functions

-   User satisfaction: the percentage of EVs taht successfully complete charging, referred to as the satisfaction score (SS). A higher SS indicated greater system efficiency, while the opposite suggests issues such as energy shortages, congestion, or insufficient charging infrastructure:

$$
\text{Satisfaction Score} = \frac{\text{EVs that completed charging}}{EVs that requested charging}
$$

-   Renewable energy efficiency: Evaluates the relationship between energy generation, storage, and consumption, aiming to maximize self-consumption and reduce dependency on external energy:

$$
\text{Self-Sufficiency} = \frac{\text{Consumed Renewable Energy}}{\text{Total Generated Demand}}
$$

$$
\text{Self-Consumption} = \frac{\text{Consumed Renewable Energy}}{\text{Total Generated Renewable Energy}}
$$

-   Financial performance: cost-savings from renewable energy use and the payback period for investments. A shorter payback indicates greater economic feasibility:

$$
\text{Payback Period} = \frac{Investment in Renewable Energy}{Monthly Profit}
$$

-   To ensure comparability, all values are normalised between 0 and 1. The payback period is normalised using the following function to prioritise profit return time within a predefined threshold of the payback period:

$$
f(x) = \begin{cases}
\frac{x}{\text{threshold}}, x \leq \text{threshold}\\
e^{\frac{\text{threshold} - x}{\text{threshold}}}, x > \text{threshold}
\end{cases}
$$

-   Optimisation metric combines the previous indicators to balance user satisfaction, energy self-sufficiency, and financial viability:

$$
\text{Objective function} = \text{Satisfaction Score} + \text{Normalised Payback Period} + 0.8 \times \text{Self-Sufficiency}
$$

-   The weight of $0.8$ for self-sufficiency highlights the goal of integrating renewable energy as a supplementary, rathen than exclusive, source.

### Experimental and Optimisation Setup Description

#### Dynamic Simulation Experiment Configuartion

-   **Policy Evaluation**:
    -   P1: Ban gasoline vehicles from charging stations
    -   P2: Impose 1,000 VND/min idle fee after 30 minutes of full charge
    -   P3: Relocate fully charged EVs to inactive stations
    -   Real-time notification system of available charging ports

*Table 5: Scenarios for implementing different operational policy combinations to evaluate their impact on EV charging station operations.*

| Policy / Case Level | Case 0 | Case 1 | Case 2 | Case 3 | Case 4 | Case 5 |
|----|----|----|----|----|----|----|
| Policy 1: Restrict gasoline vehicles | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Policy 2: Impose idle fee | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ |
| Policy 3: Relocate fully charged EVs | ✗ | ✗ | ✗ | ✓ | ✗ | ✓ |
| Policy 4: Real-time notification system | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ |

These policies are introduced incrementally across six scenarios in Table 5, with varying EV numbers (50, 100, 150, 200), a fixed charging station setup including C-Parking (20x11kW, 4x30kW), J-Parking (15x11kW, 4x30kW) and 30 gasoline vehicles across all cases.

-   **Infrastructure Planning**:
    -   Tbale 6 outlines the charging station setups and solar panel options, with a fixed BESS and an annual average weather dataset
    -   C-Parking: 280 configurations, J-Parking: 6,440 (6,720 in total) \> Initial simulations focus on C-Parking, with optimisation algorithms extending the analysis to J-Parking

*Table 6: Value ranges for various configurations of charging stations and solar panels, including options for C-Parking and J-Parking.*

| Category     | Configuration Options                               |
|--------------|-----------------------------------------------------|
| C-Parking    | **11kW Charging Ports:** 20, 25, 30, 35, 40, 45, 50 |
|              | **30kW Charging Ports:** 2, 4, 6, 8, 10             |
| J-Parking    | **11kW Charging Ports:** 15, 18, 21, 24, 27, 30     |
|              | **30kW Charging Ports:** 2, 4, 6, 8                 |
| Solar Panels | 200, 300, 400, 500, 600, 700, 800, 900              |
| BESS         | Capacity: 80kW                                      |
| Weather Data | Annual average dataset                              |

#### Statistical Testing for Dynamic Simulation with Wilcoxon Test

-   Limited sample size and non-normally distributed data -\> Wilcoxon signed-rank test: non-parametric and effective in handling skewed data and outliers
-   $H_0$: the median difference between paired observations is 0: ranks absolute differences between paired samples, assigns ranks, then calculates test statistic $W$ based on the sum of ranks:

$$
W = min(R^+, R^-)
$$

where $R^+$ and $R^-$ are the sums of positive and negative ranks, respectively - p-value is used to determine statistical significance \> Employ the `scipy.stats.wilcoxon` function (Python) to computes the test statistic and corresponding p-value for hypothesis testing

#### Optimisation Algorithm Integration Settings

*Table 7: Summary of optimization algorithms embedded in the digital twin, describing their approaches and objectives in exploring the solution space.*

| Algorithm | Source | Description |
|----|----|----|
| Hill Climbing | Pearl, 1984 | A local search that iteratively improves the solution. |
| Simulated Annealing | Kirkpatrick et al., 1983 | A probabilistic technique that avoids local optima. |
| Tabu Search | Glover, 1989, 1990 | Uses memory structures to avoid revisiting solutions. |
| Reactive Tabu Search | Battiti and Tecchiolli, 1994 | Adjusts memory size for improved efficiency. |
| Genetic Algorithm | Holland, 1975; Goldberg and Holland, 1988 | A population-based algorithm inspired by evolution. |
| Particle Swarm Optimization | Kennedy and Eberhart, 1995 | A swarm intelligence method where particles adjust positions based on experience. |

## Results and Discussion

### Dashboard and Seasonal Energy Analysis

#### Seasonal Solar Fluctuations

-   Solar energy output peaks from July–September (Q3), covering **73%** of daily electricity demand (**1,078 kWh/day**)
-   From January–March (Q1), solar output declines by **21%**, meeting only **52% of demand** (**681 kWh/day**)
-   Monthly profit during July–September reaches **100 million VND**, which is **43% higher** than January–March (**70 million VND**) despite similar demand

#### Wind Energy Assessment

-   20 wind turbines at 100m height showed marginal improvement in self-sufficiency from **0.52 (SD=0.09)** to **0.54 (SD=0.11)**
-   Wilcoxon test confirmed this difference was **statistically insignificant** ($p = 0.2801$)
-   Mean daily renewable energy consumption rose only modestly from **681 kWh** to **718 kWh**
-   Wind energy contributes **under 5%** of total energy supply despite a **28% increase** in initial investment
-   Peak wind generation occurs outside primary charging hours (**7:00 PM – 6:00 AM**), limiting effectiveness

### Policy Evaluation and Infrastructure Analysis

#### EV Satisfaction Scores by Policy (50-EV Scenario)

| Scenario | Satisfaction |
|----|----|
| No intervention (baseline) | \< 90% |
| Case 1: Gasoline vehicle ban | Increased accessibility |
| Case 2: Idle fee (1,000 VND/min after 30 min) | **95%** |
| Case 3: EV relocation | \< 1% increase |
| Case 4–5: Real-time notification | Up to **\~100%** (low demand) |
| High demand (200 EVs) + notification | **\~60%** (+10%) |

#### Satisfaction Decline with EV Growth

| EV Count | Satisfaction |
|----------|--------------|
| 50 EVs   | 87%          |
| 100 EVs  | 74%          |
| 150 EVs  | 62%          |
| 200 EVs  | 43%          |

#### Charger Configuration Results (280 configurations tested)

-   Lower demand (50–100 EVs): increasing 11 kW chargers steadily improves satisfaction, reaching nearly **100%** at 30 chargers (50 EVs) and 50 chargers (100 EVs)
-   Higher demand (150–200 EVs): 30 kW fast chargers become more critical
-   Optimal configuration: **20 × 11 kW** and **10 × 30 kW** chargers
-   Beyond **40 × 11 kW units**, diminishing returns emerge due to uneven congestion

#### Solar Panel Integration (50-EV Scenario)

-   Self-consumption remains consistently $\geq$ **80%**, indicating efficient solar utilization
-   Self-sufficiency starts below **30%** but rises to nearly **90%** as panel capacity increases
-   Beyond **500 solar panels**, additional installations offer negligible financial returns (payback threshold: **60 months**)

#### Optimal Configurations by Demand

| Metric             | 50 EVs | 100 EVs | 150 EVs | 200 EVs |
|--------------------|--------|---------|---------|---------|
| 11 kW Ports        | 35     | 50      | 20      | 20      |
| 30 kW Ports        | 4      | 4       | 10      | 10      |
| Solar Panels       | 500    | 900     | 600     | 600     |
| Satisfaction Score | 1.00   | 0.99    | 0.94    | 0.89    |
| Self-Consumption   | 0.99   | 0.98    | 0.95    | 0.93    |
| Self-Sufficiency   | 0.67   | 0.60    | 0.59    | 0.57    |
| Normalized Payback | 0.94   | 0.98    | 0.95    | 0.92    |
| Objective Function | 2.47   | 2.45    | 2.37    | 2.26    |

#### Sensitivity Analysis — Total-Order Sobol Indices ($S_T$)

| Factor              | $S_T$ | Interpretation                    |
|---------------------|-------|-----------------------------------|
| 11 kW chargers      | 0.38  | Highest influence on satisfaction |
| Notification system | 0.37  | Most substantial policy effect    |
| 30 kW chargers      | 0.34  | Comparable to notification system |
| Idle fees           | 0.34  | Moderate influence                |
| Relocation policies | 0.34  | Nearly identical to idle fees     |

### Optimization Algorithm Performance

#### Particle Swarm Optimization (PSO) Results

| Scenario | NED   |
|----------|-------|
| EV50     | 1.000 |
| EV100    | 1.238 |
| EV150    | 1.345 |
| EV200    | 0.656 |

-   NED values range from **0.656 to 1.345**, indicating minimal deviation from brute-force results
-   EV100 and EV150 show slightly higher NED due to solar panel influence
-   **Computational time reduced by 82%**: PSO evaluated \~**50 configurations** vs. **280** in the full-case scenario

#### Dual-Parking Optimization (6,720 combinations)

PSO yields near-optimal results after evaluating only \~**50 configurations**:

| Metric             | 50 EVs | 100 EVs | 150 EVs | 200 EVs |
|--------------------|--------|---------|---------|---------|
| C-Parking 11 kW    | 32     | 50      | 20      | 20      |
| C-Parking 30 kW    | 3      | 3       | 10      | 10      |
| J-Parking 11 kW    | 15     | 15      | 15      | 15      |
| J-Parking 30 kW    | 2      | 8       | 8       | 8       |
| Solar Panels       | 604    | 900     | 543     | 600     |
| Satisfaction Score | 1.00   | 0.97    | 0.93    | 0.95    |
| Self-Sufficiency   | 0.75   | 0.61    | 0.56    | 0.57    |
| Cases Tested       | 52     | 54      | 51      | 53      |

## Discussion

### Key Findings

-   The Digital Twin captures a **21% decrease** in solar efficiency from October–March
-   Wind contribution is **minimal** ($\leq 5\%$ of demand) despite a **28%** investment increase
-   Notification systems improve satisfaction by **\~10%** during high demand
-   Gasoline bans and idle fees increase charger turnover
-   Policy interventions alone are **insufficient** for long-term planning; expanded physical capacity is required

### Computational Efficiency

-   Embedding PSO directly within the simulation eliminates the traditional separation between simulation and post-simulation optimization phases
-   The unified framework achieves **over 80% reduction** in computational overhead

### Model Limitations

-   Assumes ideal user compliance with operational policies
-   May not fully reflect behavioral variability in larger, less controlled environments
-   Focuses on a single site, limiting analysis of inter-station interactions across broader networks

### Future Work

-   Extension to district- and city-scale networks
-   Modeling of interconnected stations across diverse zones
-   Incorporation of real-time operational data

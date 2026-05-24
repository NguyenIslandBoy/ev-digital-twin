# 3. Digital Twin System Framework and Implementation for Grid-Integrated Electric Vehicles

## Abstract

-   DT-based EV system operation framework to address the integration and interoperability between systems
-   Implementing individual EVs, charging stations, and charging station operators (CPOs) as DTs, enabling integrated operation with the power grid
-   DT-based agent supports independent decision-making on power service participation by considering location, distance, charging amount, spare time, and incentives data
-   CPO can establish an optimal incentive strategy to induce EV users to participate in grid power services
-   Enabling analysis and verification of the impact of participants on charging station operation, grid stability, and economic efficiency
-   Incentive-based demand response program verification

## Introduction

-   Integrating EVs into the grid to secure the flexibility and stability
-   Previous research focuses:
    -   Integrated vehicle-to-grid and grid-to-vehicle systems in microgrid (MG) environment
    -   Feed-in tariff and incentives for EV charging stations using stochastic method
    -   Battery degradation management strategies to secure economic feasibility of EVs participating in power system
    -   EV charging forcasting and dynamic energy scheduling using learning-based algorithms (ML and RL)
-   Previous research limitations:
    -   Not reflect actual operating environment accurately because not consider user behaviour (affects EV mobility) and the variability of charging patterns
    -   Limited simulations because of simple modelling and complicated construction scenarios
    -   Agent-based models have been proposed to simulate the driving and charging behaviours of EVs to address this issue, still not fully accounting for the complex interactions between other systems in a smart grid environemnt
-   Digital twin (DT):
    -   Replica of a physical system in a virtual space, providing real-time monitoring, forcasting, operation, and analysis
    -   Observing interactions betwwen systems in a smart grid in more details
    -   Systems recently used: distribution systems and distributed resource operations
-   Papers proposed DT:
    -   Anomoly detection and optimisation solution for hydroelectric power plant systems
    -   Combined with IoT and renewable energy modelling
    -   An engineering approach into grid operation
    -   Multiple energy networks and focus on mechanism-based modelling architecture
    -   Holomorphic embedding-based model of multiple energy networks accomodating various energy types
    -   Distributed energy resources (DERs) in distribution systems including 4 core modules:DER: a distribution system, energy management system, and an electric consumer, analysing the impact if grid interconnection
    -   Hierachical DT architecture supporting grid planning and operation: emulates the actual grid conditions within a real-time simulation and verifies the time delay between the physical grid and its DT
-   While emphasizing the accuracy of individual models, EVs should be considered a part of the entire system from a power service operation perspective because of the complex interactions among the large number of EVs, charging points (CPs), charging station operators (CPOs), and distribution systems
-   Based on advanced DT model (linked with the operation simulation of a distribution system), enables the creation and management of DTs for individual EVs, CPs, and CPOs and integrates these elements with grid operations.
-   DT-based EVs independently make decisions to participate in power services by considering parameters such as driving distance, location, battery status, and spare time, as well as external factors, such as incentives for service based on an advanced elasticity model
-   Contributions to existing literature:
    -   A DT-based e-mobility simulation framework integrated with a distribution system is proposed.
    -   An interaction model that operates independently among EV users, CPOs, and the distribution system
    -   An independent decision-making model for EVs based on an elasticity model, considereing the driving distance, incentives, charging, and time pressure
-   The analysis of various mutual influences: distribution system stability, operational costs, and user utility, is supported based on EV user responses

## Simulation Platform for Grid-Integrated EV Operation

-   Smart Grid Simulator (SGSim) simulating a smart grid environment and is reliable across various power system applications
-   A multi-agent-based modular suctructure, where smart grid components, such as load customers, DERs, and power system, operate independently
-   Enable easy addition or modification of various smart grid components through modularisation, offering advantages in terms of scability and flexibility
-   Support various smart grid agent functions, enabling the analysis of intergrated operatons and interactions between systems, similar to real-world environments

``` mermaid
graph TD
    subgraph CommonPackage["Common Package"]
        GovernorAgent["**Governor Agent**\nAgent_Flow_Management()\nSimulation_Environment_Control()\nEvent_Management()"]
        EventAgent["**Event Agent**\nExternal_Data_Import()\nOperation_Algorithm_Import()\nEvent_Dispatch()"]
    end

    subgraph GridPackage["Grid Package"]
        PowerFlowAgent["**PowerFlow Agent**\nPowerFlow_Analysis()"]
        TopologyAgent["**Topology Agent**\nCustomer_Data_Integrate()\nDS_Device_Management()\n(Switch, Transformer, ETC)\nDL_Grouping()"]
        GridAnalysisAgent["**Grid Analysis Agent**\nDisplay_DS_State()\nResult_Visualization()"]
        FailureAgent["**Failure Agent**\nFailure_Current_Calc()\nProtection_Device_Operation()"]
    end

    subgraph P2PPackage["P2P Package"]
        ProsumeAgent["**Prosumer Agent**\nSelf_Scheduling()\nProsumer_Visualization()"]
        P2PETAnalysisAgent["**P2P-ET Analysis Agent**\nDS_Analysis_on_Prosumer()\nResult_Visualization()"]
        ETOAgent["**ETO Agent**\nP2P_ET_Optimal_Operation()"]
    end

    Databus[["Databus"]]

    subgraph CustomerPackage["Customer Package"]
        LoadAgent["**Load Agent**\nLoad_Generate()\nLoad_Forecasting()\nEvent_Operator()\n(DR, Blackout, ETC Event)"]
        ParticipationAgent["**Participation Agent**\nPower_Service_Participation_Filtering()"]
        DERAgent["**DER Agent**\nDER_Generate()\nRE_Forecasting()\nEvent_Operator()\n(Blackout, Curtailment, ETC Event)"]
    end

    subgraph VPPPackage["VPP Package"]
        ResourceAgent["**Resource Agent**\nResource_Scheduling()\nResource_Visualization()"]
        AggregatorAgent["**Aggregator Agent**\nParticipate_VPPMarket()\nOptimal_Operation_Plan_for_Market()"]
        VPPAnalysisAgent["**VPP Analysis Agent**\nDS_Analysis_on_VPP()\nResult_Visualization()"]
    end

    subgraph EMobilityPackage["E-Mobility Package"]
        EVAgent["**EV Agent**\nLocation_Management()\nEV_User_Response()\nPower_Service_()\nEV_State()\nBattery_Operation()"]
        CPOAgent["**CPO Agent**\nPower_Service_Operation()\nPower_Service_Optimization()"]
        CPAgent["**CP Agent**\nCharging_Control()\nSettlement()"]
        AnalysisAgent["**Analysis Agent**\nDS_Analysis_on_EV()\nResult_Visualization()"]
    end

    CommonPackage --> Databus
    GridPackage --> Databus
    P2PPackage --> Databus
    Databus --> CustomerPackage
    Databus --> VPPPackage
    Databus --> EMobilityPackage
```

**Figure 1.** Class diagram of SGSim

-   In the diagram, the common package manages the overall simulation of the DT, including eah agents's execution order, the message flow coordination, the interaction between agents, and event handling
-   Customer package enables independent operational simulations of load customers and DERs and also supports data generation and forecasting simulations for these components
-   Grid package provides simulation functions for both normal and fault states of the distribution system and can be used to conduct grid impact analysis through integration with other systems
-   2 DT pacakges supporting simulations for peer-to-peer operation and virtual power plant operation
-   In this study, a DT-based e-mobility package framework of previous study was expanded, including integrated operation with the grid system

## E-Mobility Package Framework

### Mobility Pakckage Architecture

*(4 main agents)*

-   EV agent: supports independent decision-making simulation for participation in power services by considering the behavioural dynamics of EV users
-   CP agent: supports individual charging and discharging simulations of charging stations
-   CPO agent: supports simulations for establishing strategies to participate in power services: voltage management and frequency control
-   Analysis agent: do data analysis
-   Share and access data in real time via the databus
-   THe grid package connects with the load agent and DER agent from the customer package to configure loads and DERs within the distribution system
-   Info and signals for power service operation are managed through the event module of the common agent, which interacts with the power service operation module of the CPO agent

``` mermaid
graph TD
    subgraph EMobility["E-Mobility Package"]

        subgraph EVAgent["EV Agent"]
            StateModule["State module"]
            LocationModule["Location management module"]
            BatteryModule["Battery module"]
            UserResponseModule["User response module"]
        end

        subgraph CPAgent["CP Agent"]
            ChargerModule["Charger module"]
            SettlementModule["Settlement module"]
        end

        subgraph CPOAgent["CPO Agent"]
            PowerServiceModule["Power service operation module"]
            OptimizationModule["Optimization module"]
        end

        subgraph AnalysisAgent["Analysis Agent"]
            AnalysisModule["Analysis module"]
            VisualizationModule["Visualization module"]
        end

        %% Within EV Agent
        StateModule --> BatteryModule
        LocationModule --> StateModule
        LocationModule --> UserResponseModule
        BatteryModule --> UserResponseModule

        %% EV Agent to CP Agent (Connect/Disconnect)
        BatteryModule -. "Connect/Disconnect" .-> ChargerModule

        %% Request signal: EV Agent to CP Agent
        StateModule -. "Request signal" .-> ChargerModule

        %% CP Agent internal
        ChargerModule --> SettlementModule

        %% CPO Agent: Power service signal
        PowerServiceModule -. "Power service signal" .-> ChargerModule
        PowerServiceModule --> OptimizationModule

        %% CP Agent to CPO Agent: Control
        ChargerModule -. "Control" .-> PowerServiceModule

        %% Down to Analysis Agent
        UserResponseModule -. " " .-> AnalysisModule
        SettlementModule -. " " .-> VisualizationModule
        OptimizationModule -. " " .-> VisualizationModule

        %% Analysis Agent internal
        AnalysisModule --> VisualizationModule
    end

    subgraph GridPackage["Grid Package"]
        TopologyAgent["Topology Agent"]
        PowerFlowAgent["Power Flow Agent"]
        TopologyAgent --> PowerFlowAgent
    end

    subgraph CommonPackage["Common Package"]
        EventAgent["Event Agent"]
    end

    %% Cross-package communication
    LocationModule -. "Location information" .-> GridPackage
    CommonPackage -. "Power service event" .-> PowerServiceModule
```

**Legend:**
- `——→` Communication within agents
- `- - →` Communication between agents

**Figure 2.** E-mobility package architecture

Fig 2 shows the e-mobility package architecture, highlighting the interactions between the agents within the framework

### Functions of E-Mobility Package

**(A) EV Agent**: independently makes decisions about participating in power services based on details such as EV driving, location, distance, charging, and spare time, and external factors (incentives). The EV agent comprises 4 modules, and the interactions among these ones are shown in Fig 3

``` mermaid
graph TD
    External1(["External agents/modules"])
    External2(["Decision-making\n(Service participation, etc.)"])

    LocationModule["Location management module"]
    StateModule["State module"]
    BatteryModule["Battery module"]
    UserResponseModule["User response module"]

    %% External inputs/outputs
    External2 <-. " " .-> StateModule
    External1 -. "Charge/discharge state" .-> BatteryModule
    LocationModule -. "Location" .-> External1

    %% Location management module connections
    LocationModule -- "Location" --> StateModule
    LocationModule -- "Driving information\n(distance, etc.)" --> StateModule
    LocationModule -- "Location" --> UserResponseModule
    LocationModule -- "Driving distance" --> UserResponseModule

    %% State module connections
    StateModule -- "Charge behavior, etc." --> BatteryModule
    StateModule -- "Utility" --> UserResponseModule

    %% Battery module connections
    BatteryModule -- "Battery state (SOC, etc.)" --> StateModule
    BatteryModule -- "Battery state\n(Capacity, SOC, etc.)" --> UserResponseModule

    %% User response module connections
    UserResponseModule -- "Driving, user char., etc." --> LocationModule
```

**Legend:** - `——→` Communication within agents - `- - →` to external agents or modules

**Figure 3.** EV agent architecture

-   Simulates the behaviour of EV users, supporting independent EV user decision-making regarding activities such as driving, charging, and participating in power services by interacting with other modules within the EV agent
-   User response module
    -   Quantifies the utility of individual EV users based on details like location data, distance to CPs, battery state, spare time, charging price information, and incentives
    -   Interfaces with the location management module, battery module, and state module to obtain the information to calculate the utility
    -   The results are used as key indicators for decision-making in the state module
-   Location managementmodule
    -   Manages the spatial and temporal positioning of individual EVs
    -   Is linked to the battery module to support the calculation of battery consumption according to the distance and is linked to the topology agent of the grid package to facilitate location data mapping for individual EVs based on node units in the power distribution system
-   The battery module
    -   Interacts with the state module, the location module, and the CP agent's charger module to simulate the battery status (state of charge - SOC, degradation, etc.) according to the driving, charging, and discharging details

**(B) CP Agent**: supports simulations at the individual charger level within CPs and performs functions such as charging control and setllement, also supports control simulations of operational strategies for power services involving CPO agents. This agent comprises a charger module and settlement module, of which main functions are: - Interacts with the battery module of the EV agent to provide charging power based on charging behaviour of EV users or supports charger control simulation based on operation strategy by linking with power service operation module of the CPO agent - Is linked with the topology agent of the grid package to provide location and charging/discharging power information for grid simulation - Settlement module performs settlements related to the charging and participation of EVs in power services; reflects changes in the CP's charging prices and the incentive strategies

**(C) CPO Agent**: comprises a power service operation module and an optimisation module, supports the simulation of charging service and power service operations; the main functions are: - Power service operation module manages the overall power service operation and interacts with the EV agent's state module and the event agent of the common package. Also, it considers operating strategies received from the optimisation module to provide power service signals to EV users or charging/discharging control signals to the charger module - Optimisation module establishes the optimal strategy for the power service, which data is provided by the power service operation module and feeded back optimisation results

**(D) Analysis Agent**: analyses the main simulation results from the e-mobility package and provides real-time monitoring and visualisation functions, comprising analysis module and visulisation module, with following functions: - Analysis module filters, sorts, and aggregates the simulation results of each agent of the e-mobility package and grid package in real time using language-integrated queries - Visualisation module visualised the data analysed wiht a dashboard and user interface (UI); to synchronise data with the UI, the Model-View-ViewModel pattern was applied

**Figure 4 — E-Mobility Package Visualization UI/UX**

**(a) EV Package Simulation Results** Displays comprehensive simulation output including incentive rates per station, number of participating EVs, and total charging amounts per CP under power service operation.

**(b) EV Agent Results** Shows EV behavior states **before and after Demand Response (DR)**, covering: - Individual EV states: staying, moving, charging - Battery SOC over time - User utility values per EV number

**(c) CPO Agent Results** Presents the optimization outcomes including: - **Optimization progress** (profit convergence over iterations) - **Optimal incentive** calculation per charging point - **Sensitivity analysis** of CPO profit and EV user utility against average arrival time (AT)

**(d) Distribution System Analysis** Visualizes the grid package state changes resulting from CPO power service operations, shown as an interactive distribution network map.

### Simulation Flow of E-Mobility

``` mermaid
sequenceDiagram
    participant EV as EV Agent
    participant CP as CP Agent
    participant CPO as CPO Agent
    participant Grid as Grid Package
    participant Common as Common Agent<br/>(Event Module)

    loop Normal Operation ①
        EV ->> EV: EV state
        EV ->> CP: Connected to charger
        EV ->> Grid: EV and charger location information
        Grid ->> Grid: Topology mapping
        EV ->> EV: Driving EV
        CP ->> EV: Charging/discharging
        CP ->> CPO: Charger state and power
        CP ->> Grid: Charging/discharging power
        Grid ->> Grid: Power flow
    end

    Common -->> CPO: Power service signal (from utility) ②

    rect rgb(200, 200, 200)
        Note over EV, Grid: Power Service Operation ③
        CPO ->> CPO: Optimization for incentive determination
        CPO ->> EV: Power service signal (service information)
        EV ->> EV: EV user response
        EV ->> CP: Participation signal
        Note over EV, Grid: Same flow as ①
    end

    CP ->> EV: Settlement
```

**Figure 5.** Simulation flow of e-mobility package with grid package.

**(A) Normal Operation** - Operation (1) is the simulation flow without power service request, when the siml=ulation starts, the EV agent's state module updates the EV's spatiotemporal data and status based on the interactions between the modules in the EV agent, the EV state is updated from the EV agent at each simulation step - Next, the battery module is mapped to the charger module of the CP agent based on the charging data; if the EV is driving, its location data is shared with the topology agent of the grid package; then the location data from charger module is updated to this topology agent, which completes the spatiotemporal mapping of the EV and charger - Charger module charges the battery based on the EV user's charging requirement; then the state data is sent to the CPO agent and the power flow agent of the grid package; then the power flow agent performs a power flow analysis by updating the charger state and the data from the topology agent

**(B) Power Service Operation** - When power service signal (2) is transmitted to the CPO from te event module during the simulation, power service operation (3) is simulated - The CPO establishes an optimal operation strategy based on the power service data - Power service targets incentive-based demand response (DR) to solve overvoltage situations in the distribution system; the optimal operation strategy for the CPO is to calculte the optimal incentives to induce EV charging - After the optimal incentive for the CPO is determined, the power service data (incentives,...) is transmitted to the EV agent's state module, then the EV user's responsiveness is calculated in the EV agent's response module, and the EV state, including the decision on whether to participate in the power service, is updated - Then, the power service participation data is transmitted to the CPO's power service operation module, and the next real-time operation sequence is the same as (1) - When the power service ends, a settlement is performed in the EV's agent settlement module, and the result is delivered to the individual EVs that participated in the service

## E-Mobility Function Models

### EV State Model of EV Agent

-   An EV user selects ($u^*_{t,c}$) a CP that maximises their utility by participating in the power service, which can be expressed as Equations (1) and (2). The utility $\sigma _c$ is defined as the energy that the EV user wants to charge
-   Based on the rated charge ($P^{cp}_c$), the charging energy ($E_{t,c}$) of the EV at time slot $t$ can be expressed as Equation (3), while Equation (4) represents the total charging energy ($E^t_{t,c}$) during the participation in the power service
-   Equation (5)-(7) represent the charging start time ($\tau^{st}_c$), time spent at the CP for charging ($\tau^{cs}_c$), and the charging end time ($\tau^{ce}_c$) for the EV, respectively
-   Equation (8) represents the charging state of the EV at a CP, which is determined at a time between ($\tau^{cs}_c$) and $min(\tau^{pe}_c, \tau^{ce}_c)$
-   Equation (9) represents the SOC constant for the EV battery charging

$$u^*_{t,c} = \arg\max_{u_{t,c}} \sigma^t_c \tag{1}$$

$$\sigma^t_c = \sum_{t \in PT} u_{t,c} \cdot \sigma_{t,c}, \quad \forall c \in CT \tag{2}$$

$$E_{t,c} = \min(u_{t,c} \cdot \sigma_{t,c} \ , \ \varepsilon \cdot u_{t,c} P^{cp}_c \cdot \eta^c), \quad \forall t \in PT, \forall c \in CT \tag{3}$$

$$E^t_{t,c} = \sum_{t=\tau^{cs}_c}^{\min(\tau^{pe}_c, \tau^{ce}_c)} E_{t,c}, \quad \forall t, \tau^{cs}_c, \tau^{de}_c \in T, \forall c \in CT \tag{4}$$

$$\tau^{cs}_c = \max(\tau^{ps}_c, \tau^{ar}_c), \quad \forall c \in CT \tag{5}$$

$$\tau^{st}_c = \frac{E^t_{t,c}}{\varepsilon \cdot P^{cp}_c \cdot \eta^c}, \quad \forall c \in CT \tag{6}$$ 

$$\tau^{ce}_c = \tau^{cs}_c + \tau^{st}_c, \quad \forall c \in CT \tag{7}$$

$$u_{t,c} = \begin{cases} 1, & \tau^{cs}_c \leq t \leq \min(\tau^{pe}_c, \tau^{ce}_c) \\ 0, & \text{otherwise} \end{cases}, \quad \forall t \in T, \forall c \in CT \tag{8}$$

$$s^{min}_{t,c} \leq s^{it}_c - \varepsilon \cdot P^{evm}_{t,c} / \eta^d + \sum_{g=1}^{t} E_{t,c} \leq s^{max}_{t,c}, \quad \forall t \in T, \forall c \in CT \tag{9}$$

**Here:**
- $t$ is time slot
- $c$ is a $CP$
- $CT$ is a set of CPs
- \$T is a set of operating times
- $PT$ is a set of power service operations
- $\varepsilon$ is a unit conversion variable (kW to kWh) 
- $\tau^{ps}_c$ and $\tau^{pe}_c$ are the start and end times of the power service, respectively 
- $\tau^{ar}_c$ is the arrival time of the EV at the CP
- $\eta^c$ and $\eta^d$ are the charging and discharging efficiency, respectively
- $s^{min}_{t,c}$ and $s^{max}_{t,c}$ represent the minimum and maximum bettery SOC
- $s^{it}_{c}$ is the battery SOC
- $P^{evm}_{t,c}$ is the energy consumed when driving to a CP

### EV User Response Model of EV Agent

-   EV users decide independently to participate in power services based on their attitudes toward the services ($AT_t$), incentives ($\delta_t$), charging presure ($\lambda_t$), and time pressure ($\gamma_t$)
-   The responsiveness of EV users to participate in power services is quantified as a utility, which is based on the elasticity of price (incentive and charging price) and charging amount
-   Assuming that charging of the EV does not move to another time, the charging amount, including self-elasticity ($E^{et}_t$), with a negative value can be expressed as Equation (10), which is derived through Equations (11) - (13)
-   Equations (11) represents the benefit of participating in the power service for an EV; when the profit mmaximisation condition is considered, Equation (11) can be expressed as Equation (12)
-   Equation (13) representsa quadratic function for the customer benefit ($B(d_t)$); differentiating it and applying Equation (12) yields Equation (10)A

$$d_t = d^o_t \left[1 + E^{et}_t \frac{(\rho_t - \rho^o_t - \delta_t)}{\rho^o_t}\right], \quad E_t = \frac{\Delta d_t}{\Delta \rho_t} \leq 0 \tag{10}$$

$$F(d_t) = B(d_t) - d_t \cdot \rho_t + \delta_t \cdot \Delta d_t \tag{11}$$

$$\frac{\partial B(d_t)}{\partial d_t} = \rho_t - \delta_t \tag{12}$$

$$B(d_t) = B^o_t + \rho^o_t (d_t - d^o_t) \left[1 + \frac{d_t - d^o_t}{2E^{et}_t \cdot d^o_t}\right] \tag{13}$$

**Here:** - $d^o_t$ is the initial charging energy - $\rho^o_t$ is the initial charging price - $E^{et}_t$ is elf-elasticity model, can be expressed as a utility for individual EV users, including charging time and driving time \> more spare times --\> higher possibility of participating in the power service - Charging pressure is expressed as the degree of battery SOC required for EV driving \> lower SOC --\> higher possibility of participating in the power service - Time pressure can be expressed based on the user's time, as in Equation (15), while charging pressure can be expressed based on the remaining battery capacity, as in Equation (16)

$$\sigma_t = d^o_t \left[1 + \frac{E^{et}_t}{\rho^o_t}\left(\rho_t - \rho^o_t - \frac{\gamma_t \cdot \delta_t}{\lambda_t} \cdot \omega\right)\right] \tag{14}$$

$$\gamma_t = \left(\frac{\min(t, \tau^{ts}_t)}{\tau^{ts}_t}\right)^{\frac{1}{AT_t}} \tag{15}$$

$$\lambda_t = \left(\frac{B^S_t}{B^c}\right)^\alpha \tag{16}$$

**Here:** - $\omega$ is the weight variable - $AT_t$ is the EV user's attitude - $\alpha$ is the charging pressure parameter, and $B^S_t$ and $B^c$ are the battery SOC and battery capacity respectively

### Power Service Optimisation Model of CPO

-   The operational goal of CPO is to determine the optimal incentive to induce EV charging
-   When the DR signal is announced, the CPO adjusts incentives to increase the charging capacity of the CP to induce EV charging participation
-   The CPO operates with the goal of maximising the operation profit , which is calculated based on the DR response power, charging price, and incentives, using Equation (17)
-   Equation (18) represents the DR reponse power, which is calculated as the sum of the EV charging amount during the DR operation time
-   THe EV charging is assumed to be the rated charging
-   Equaiton (19) and (20) represent the incentive contraints and the DR contract capacity, respectively

$$\text{maximize} \sum_{t \in PT} \sum_{c \in CT} P^{ps}_{t,c}(\rho^o_{t,c} - \delta_{t,c})\varepsilon \tag{17}$$

$$P^{ps}_{t,c} = \sum_{i \in EV} u^*_{t,c,i} P^{cp}_{c,i}, \quad \forall t \in PT, \forall c \in CT, \forall i \in EV \tag{18}$$

$$\delta_{t,c} \leq \delta^{max}_t, \quad \forall t \in PT, \forall c \in CT \tag{19}$$

$$\varepsilon P^{ps}_{t,c} \geq P^{con}_{t,c}, \quad \forall t \in PT, \forall c \in CT, \forall i \in EV \tag{20}$$

**Here:**
- $i$ denotes en EV
- $EV$ is the EV set
- $P^{ps}_{t,c}$ is the DR response power of the CPs
- $\delta^{max}_t$ is the maximum Incentive
- $P^{con}_{t,c}$ is the DR contract capacity

-   The CPO's optimisation module calculates the optimal incentive by interacting with the EV agent's state module
-   The incentive for the CPO is reflected as an input to the EV response module linked to the EV state module
-   The utility calculated in the EV response module is reflected in the EV state module
-   The results of the EV user's CP selection and charging amount are reflected as inputs to the CPO's optimisation module
-   The particle swarm optimisation model was used to derive the optimal result

## Case Study and Discussion

### Case Study Design

- Targeting 120 EVs
- Approximately 6.5 MWp of PV was introduced
- 3 CPs were placed at 5 km intervals
- Rated power of CP charger was set to 50 kW (fast charging)
- Power service targets at incentive-based DR
- DR data (operating times, contract information, etc) was announced to the CPO 15 min before the DR started; DR operation time and DR contract capacity were set to 30 min and 1.44 MWh
- Charging pace is 18 ₡/kWh, and the maximum incentive was set at 54% of the charging price
- Self-elasticity of the EV reactivity model was set to -1 considering the rated charger
- The $AT$ amd $\alpha$ were set to 0.9-1.1 amd 0.1-0.3
- Simulations were conducted at 1 min intervals, with analyses based on the DR operational times

### Cast Study Results and Discussion

**(A) DR Program Operation Results**
- InFig 8:
  - According to the DR operation, the optimal incentives for CPs 1-3 were 4.46, 3.56, and 3.60 ₡/kWh
  - The optimal incentives converged after 29 iterations of the optimisation progress, and the CPO's profit was approximately $90
  - In the DR service, 68 out of 120 EVs participated, among which 30 EVs had no prior charging plans (due to utility increses through incentives)
  - Average charging power for DR participation across 3 CPs was 1,478 MWh -> ~33.7% increase in profit compared to the charging revenue of CPO
  > Incentive-based operation encourages EV users to participate in DR, which increases CP utilisation and then enhances CPO profit
- In Fig 9 and Fig 10:
  - EV user selects the CP that maximises utility, considering factors like distance, charging price, incentives, spare time, and battery state
  - With provided incentives, the utility of the EVs participating in DR increased by an average of 10.04%
  - Overvoltage up to 1.06 PU (ID 21) before DR reduces to below the limit of 1.04 PU after DR
  > The overvoltage in the distribution system was resolved after DR

**(B) Sensitivity Analysis for EV Users**
- In Fig 11:
  - $AT$ was varied by 50% of its initial value
  - Total 300 Monte Carlo simulations were performed
  - Utility was ditributed between 18.3 and 20.3, depending on the $AT$ change of EV users
  - CPO's profit varied in the range of $74-103
  - Utility incresed when the $AT$ toward DR was positive --> Increase in DR participation and CPO profits

**(C) Expandability and Interoperability**
- Agents interact over a databus-based architecture (Fig 2), as part of the SGSim platform
- Message broker function enables: seamless communication and minimise delays while sharing relatively slow and non-critical data
- Non-time critical agents do not require synchronisation with the core agents by allowing best-effort-based approaches

## Conclusion

This study presents a Digital Twin (DT)-based framework for simulating EV system operation integrated with power grid simulation. Key points:

- Individual EVs, CPs, and CPOs are modelled as DTs to enable integrated grid operation - The EV agent uses an advanced elasticity model for individual user decision-making and behavioural simulation
- Validated through a case study on incentive-based Demand Response (DR), confirming mutual operation of EV users, CPOs, and grids
- Future work includes:
  - Deriving realistic parameter values reflecting regional/environmental characteristics
  - Incorporating EV driving and mobility characteristics into user response models
  - Developing learning-based models (reinforcement/machine learning) for more realistic EV-DT systems
  - Building an integrated framework with distribution system operators and market mechanisms for ancillary service simulation
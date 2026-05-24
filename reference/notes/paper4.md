# 4. Smart City Digital Twin–Enabled Energy Management: Toward Real-Time Urban Building Energy Benchmarking

(https://shorturl.at/KjQO1)

## Abstract

- Although energy benchmarking approaches are useful for identifying overall efficient and poor performers across buildings at a city scale, they are limited in their ability to provide actionable insights
- Concurrently, advances in smart metering data analytics combined with new data streams available via smart metering infrastructure enable top-down building benchmarking analyses
- This paper will:
  - Leverage smart meter electricity data through strategic periods
  - Quantify daily benchmarks from annual, conventional ones
  - Investigate how such metrics can lead to near real-time enery management
- Strategic periods include: occupied and unoccupied periods during the school year, during the summer, and peak summer demand periods
- A building's overall benchmark marks meriods in which a building is over- or underperforming during the day, week, month
> How these temporally segmented energy benchmanrks can provide a more specific and accurate measure for building efficiency
- Discuss how thes findings establish the foundation for digital twin-enabled urban energy management by enabling identification of building retrofit strategies and near-real-time efficiency of the performance of an entire building portfolio

## Introduction

- Prominent challenges such as urbanisation and rising greenhouse gas emmissions have sparked efforts to make cities smarter
- building account for most of energy consumption in cities, and high energy conservation through retrofits or operational improvements --> key focus for smart city initiatives
- Intersection of smart cities and building energy efficiency has opportunity for real-time intelligent planning and urban energy management
- Digital twins are envsioned to improve city mnitoring, control and decision making through enhanced visualisation and interaction with city data
- Digital twins capturing and incorporating streamed building data can be a promising portfolio performance assessment and urban energy management
- In March, 2019, over 90 cities, 10 counties, and 2 states in the US have committed entirely to renewable energy sources by no later than 2050
- Because many buildings require different levels of energy consumption based on the time, temporally segmented benchmarks can provide a more accurate measure for buildings efficiency
> using smart meter data with a digital twin can reveal hidden energy patterns and support more precise, real-time energy management

## Background

### Energy Performance Assessments in Existing Buildings

- **Categories**Energy performance assessment of buildings falls into two main approaches: energy classification (benchmarking) and energy diagnosis.
- **Energy classification** 
    - is a top-down method that standardizes annual energy use across buildings to compare efficiency
    - widely used because it requires minimal data and works well at large scales (e.g., cities)
    - only provides high-level insights and cannot pinpoint specific causes of inefficiency or guide targeted improvements
- **Energy diagnosis**
  - uses bottom-up methods like simulations and audits to identify where and why energy is being wasted
  - While it produces actionable, system-level recommendations, it is data-intensive, time-consuming, costly, and often impractical for large-scale application due to the need for detailed building information and expert analysis
- **Hybrid solution:** 
  - combines the scalability of benchmarking with the actionable insights of diagnosis
  - using smart meter data to create time-segmented energy benchmarks
  - real-time insights without requiring extensive data collection, making it well-suited for integration into digital twin–based energy management systems and improving decision-making at the community or city level

### Temporal Dimension of Building Energy Performance

- **Context:** Smart meter data is increasingly available through advanced metering infrastructure, enabling granular electricity use recording (sub-hourly), which has spurred a wide range of energy analytics applications.
- **Smart Meter Data Analytics**
    - Supports real-time energy load analysis, forecasting, consumer segmentation, and demand response
    - Has been applied to anomaly detection, occupant behaviour analysis, and dynamic pricing optimisation
    - Rarely applied to building benchmarking and performance assessment, especially at scale
- **Traditional Building Energy Benchmarking**
    - Calculated on an annual basis, offering limited insight into *when* or *why* inefficiencies occur
    - Cannot guide targeted efficiency improvements due to lack of temporal granularity
- **Temporally Segmented Benchmarking**
    - Leverages smart meter granularity to segment energy benchmarks by specific periods (e.g., operational vs. non-operational, event vs. non-event)
    - Applied in prior studies to sports arenas and 500 K–12 schools to identify efficiency opportunities
    - However, prior studies assumed temporal differences exist without statistically validating their magnitude, distribution, or significance a gap this paper addresses
- **Research Contribution:**
    - Investigates whether temporally segmented benchmarks *statistically* differ from non-temporally segmented (annual) counterparts
    - Uses 15-minute smart meter electricity data from 38 buildings on the Georgia Tech campus (Sep 2015 – Sep 2016) as a test bed
    - Discusses practical implications through a **digital twin lens**, enabling:
        1. Identification and prioritisation of specific retrofit strategies
        2. Near-real-time building energy management
    - Positions temporally segmented benchmarks as a key input for digital twin–enabled energy management systems at community or city scale

## Methods

- **Study Site:** Georgia Institute of Technology (GT) campus — selected as a representative community-scale test bed due to its diverse building mix (offices, labs, recreation, health,food, retail, classrooms), comparable to a small town.
- **Dataset**
    - 38 campus buildings with building-level electricity consumption data
    - All buildings share a **district water loop** for heating and cooling buildings with individual electric HVAC systems were excluded to avoid bias in efficiency scores
    - Power recorded in **15-minute increments**
    - Data range: **September 26, 2015 – September 25, 2016** (one full year)
- **Analytical Steps:**
    1. Segment building energy consumption by strategic time periods
    2. Compute daily energy benchmarks for each building
    3. Conduct hypothesis tests to statistically evaluate deviations from non-temporally segmented (annual) counterparts

### Data Segmentation by Period

- Segmented periods:
  - (A) Occupied periods during the school year
  - (B) Unoccupied periods during the school year
  - (C) Occupied periods during the summer
  - (D) Unoccupied periods during the summer
  - (E) Peak summer periods
  - (F) Total period
- Reason: High potential to enlighten efficiency opportunitie, supported by
  - Substantial energy waste occurs in buildings during unoccupied periods due to misaligned operational schedules
  > Differentiate efficiency levels between occupied and unoccupied states in targeting efficiency opportunities
  - Annual energy-efficiency scores for university buildings skewed due to significant operational shifts during the summer
  > seprating summer months from annual efficiency scores to uncover actual efficiency levels
  - Peak demand periods lead to utility peak demand charges
  - Retrofit opportunities exist to reduce energy demand during summer peak periods, such as improving air conditioner efficiency

**Table 1. Segmented Period Details**

| Period | Days | Times | Total Number of Days |
|--------|------|-------|----------------------|
| Occupied during school year (A) | 9/26/15–5/7/16, 8/21/16–9/25/16 | 8 a.m.–8 p.m. (M–F) | 174 |
| Unoccupied during school year (B) | 9/26/15–5/7/16, 8/21/16–9/25/16 | 8 p.m.–8 a.m. (M–F) | 174 |
| Occupied during summer (C) | 5/8/16–8/20/16 | 8 a.m.–8 p.m. (M–F) | 75 |
| Unoccupied during summer (D) | 5/8/16–8/20/16 | 8 p.m.–8 a.m. (M–F) | 75 |
| Peak summer (E) | 9/26/15–9/30/15, 6/01/16–9/25/16 | 2 p.m.–7 p.m. (M–F) | 86 |
| **Total** | 9/26/15–9/25/16 | 12 a.m.–11:59 p.m. | **365** |

- **Occupancy Assumptions**
    - Occupied: 8 a.m.–8 p.m. weekdays (building entrances open/unlocked)
    - Unoccupied: 8 p.m.–8 a.m. weekdays (key access required, low to no occupancy)
    - Weekends excluded due to inconsistent occupancy patterns
    - Winter break (Dec 19, 2015 – Jan 3, 2016) removed due to unknown occupancy states
- **Seasonal & Billing Definitions**
    - School year vs. summer divided per GT's 2015–2016 academic calendar
    - Peak summer period (E) aligned with Georgia Power's peak billing demand rate window
- **Data Aggregation**
    - 15-min interval data aggregated to **daily energy use values** for Periods A, B, C, D, and Total
    - Each day's value = average of 15-min readings
    - Period E (peak summer): 30-min running average applied; **maximum daily value** selected (reflecting how peak demand charges are billed)
    - Total period = average electricity use across all 24 hours → used as the **control**
- **Hypothesis Testing**
    - 38 comparisons conducted per period (one per building)
    - Each hypothesis tests whether a building's daily efficiency scores during a segmented period differ from its total (annual) period scores:

| Hypothesis | Comparison |
|------------|------------|
| A (1–38) | Total vs. Occupied school year |
| B (1–38) | Total vs. Unoccupied school year |
| C (1–38) | Total vs. Occupied summer |
| D (1–38) | Total vs. Unoccupied summer |
| E (1–38) | Total vs. Peak summer demand |

### Efficiency Score Development

- **Purpose of Benchmarking**
    - Generate building efficiency scores that enable accurate energy comparisons across buildings
    - Early methods used simple ratios (e.g., energy per area); this study adopts a more robust **regression-based methodology** (Chung et al. 2006), similar to the Energy Star scoring approach

- **Model Variables**
    - **Dependent variable:** Energy Use Intensity (EUI) = energy use divided by building floor area
    - **Independent variables:** Building characteristics outside the control of operators/occupants (e.g., space type areas, floor area) sourced from GT's Capital Planning and Space Management database
    - Space types converted to **Building Use Ratios (BURs)** (0–1 scale) by dividing space type area by total floor area

- **Normalisation Process**
    - EUI and floor area inputs were **log-transformed** to address skewed distributions
    - Explanatory variables rescaled to mean = 0, SD = 1 for interpretability
    - A **multivariate linear regression** model was fitted for each day within each period (e.g., 174 models for Period A):

$$EUI = a + b_1x^*_1 + \cdots + b_kx^*_k + \varepsilon \tag{1}$$

  - **Forward selection** with the **Akaike Information Criterion (AIC)** used for variable selection
    
- **Normalised EUI Calculation**
    - Each building's normalised EUI computed as:

$$EUI_{norm} = EUI_0 - EUI + a \tag{2}$$

  - Where $EUI_0$ = measured $EUI$ , $EUI$ = model-predicted $EUI$ , $a$ = intercept (representing the average building EUI in the dataset)
  - Buildings consuming more than predicted receive a higher $EUI_{norm}$ (less efficient)

- **Efficiency Scores**
    - Normalised EUIs rescaled to **0–1 per day**, where:
        - **0** = least efficient
        - **1** = most efficient
    - Result: a distribution of daily efficiency scores per building per period

- **Statistical Testing**
    - **Wilcoxon signed-rank test** used (non-parametric, suitable for ordinal efficiency scores)
    - Paired comparison: each building's total period score vs. its temporally segmented score on the **same day**
    - Multiple comparison problem addressed using the **Holm procedure** (a less conservative alternative to Bonferroni correction) to control familywise error rates
    - Statistical significance threshold: **95% confidence interval**
    - Analysis conducted in **R version 3.5.1**

## Results

- **Overall Findings**
    - Null hypotheses rejected at 95% confidence interval for the majority of buildings across all five periods, confirming that temporally segmented efficiency scores differ statistically from total (annual) period scores:

| Hypothesis | Period | Buildings with Significant Difference (of 38) |
|------------|--------|-----------------------------------------------|
| A | Occupied school year | 34 |
| B | Unoccupied school year | 32 |
| C | Occupied summer | 31 |
| D | Unoccupied summer | 30 |
| E | Peak summer demand | 32 |

- **Key Statistics**
    - **~75% of buildings (n = 28)** had statistically distinct efficiency scores in **4 or more** of the examined periods vs. the total period
    - **All 38 buildings** showed a statistically significant difference in at least one period
    - P-values of 1 in some cases reflect the Holm procedure's conservative adjustment to control Type I errors

- **Magnitude of Differences (Statistically Significant Buildings)**
    - Period A (Occupied school year):
        - Mean absolute difference: **7.9%**
        - Maximum absolute difference: **48.3%**
    - Differences varied by period (see Fig. 1)
    - Comparisons between two temporally segmented periods (rather than vs. total) yielded **even larger differences**, as the total period represents an average across all periods

## Discussion – Practical Implications & Validation

**Table 3. Adjusted p-values for Hypotheses A, B, C, D, and E**

| Building | A | B | C | D | E | Total Significant Cases |
|----------|---|---|---|---|---|------------------------|
| 1  | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | 5 |
| 2  | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | 5 |
| 3  | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | 0.002ᵇ  | 5 |
| 4  | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | 5 |
| 5  | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | 5 |
| 6  | <0.001ᵃ | 0.005ᵇ  | 0.048ᶜ  | <0.001ᵃ | <0.001ᵃ | 5 |
| 7  | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | 5 |
| 8  | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | 5 |
| 9  | 0.021ᶜ  | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | 0.03ᶜ   | 5 |
| 10 | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | 5 |
| 11 | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | 5 |
| 12 | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | 5 |
| 13 | <0.001ᵃ | 0.034ᶜ  | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | 5 |
| 14 | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | 5 |
| 15 | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | 0.004ᵇ  | <0.001ᵃ | 5 |
| 16 | <0.001ᵃ | <0.001ᵃ | 0.006ᵇ  | <0.001ᵃ | 0.026ᶜ  | 5 |
| 17 | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | 5 |
| 18 | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | 5 |
| 19 | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | 5 |
| 20 | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | 5 |
| 21 | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | 5 |
| 22 | 0.005ᵇ  | 0.005ᵇ  | <0.001ᵃ | <0.001ᵃ | 0.728   | 4 |
| 23 | 1       | <0.001ᵃ | <0.001ᵃ | 0.001ᵇ  | <0.001ᵃ | 4 |
| 24 | <0.001ᵃ | 0.005ᵇ  | <0.001ᵃ | 1       | <0.001ᵃ | 4 |
| 25 | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | 0.085   | <0.001ᵃ | 4 |
| 26 | <0.001ᵃ | 1       | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | 4 |
| 27 | 1       | <0.001ᵃ | <0.001ᵃ | <0.001ᵃ | 0.002ᵇ  | 4 |
| 28 | <0.001ᵃ | <0.001ᵃ | 0.959   | <0.001ᵃ | <0.001ᵃ | 4 |
| 29 | 0.001ᵇ  | 0.309   | 0.959   | 0.001ᵇ  | <0.001ᵃ | 3 |
| 30 | <0.001ᵃ | 0.473   | 0.003ᵇ  | <0.001ᵃ | 0.728   | 3 |
| 31 | <0.001ᵃ | 0.003ᵇ  | 0.009ᵇ  | 1       | 0.728   | 3 |
| 32 | <0.001ᵃ | <0.001ᵃ | 0.312   | 1       | 0.011ᶜ  | 3 |
| 33 | 0.006ᵇ  | <0.001ᵃ | 0.959   | <0.001ᵃ | 1       | 3 |
| 34 | <0.001ᵃ | 0.004ᵇ  | 0.006ᵇ  | 1       | 0.292   | 3 |
| 35 | <0.001ᵃ | 0.075   | <0.001ᵃ | 1       | <0.001ᵃ | 3 |
| 36 | 0.687   | <0.001ᵃ | 0.445   | <0.001ᵃ | 1       | 2 |
| 37 | <0.001ᵃ | 0.063   | 0.443   | 1       | <0.001ᵃ | 2 |
| 38 | 0.773   | 1       | 0.765   | 0.264   | 0.03ᶜ   | 1 |
| **Total significant cases** | **34** | **32** | **31** | **30** | **32** | |

ᵃ p < 0.001 — ᵇ p < 0.01 — ᶜ p < 0.05

- **Core Contribution**
    - Statistically confirmed that temporally segmented building energy benchmarks differ significantly from conventional (total/annual) benchmarks for the vast majority of buildings (30–34 out of 38)
    - Fills a gap in prior work (Francisco et al. 2018; Grolinger et al. 2018; Roth and Jain 2018), which explored temporally segmented benchmarks but never statistically validated their deviation from conventional counterparts

**Fig. 1 – Interpretation: Absolute Efficiency Score Differences by Time Period**

- **Overall Pattern**
    - All five periods show median absolute differences clustered **below 0.1** (i.e., <10%), suggesting that for most buildings on most days, temporally segmented scores are relatively close to total period scores
    - However, the **spread and outliers vary considerably** across periods, revealing important differences in how and when buildings deviate

- **Period-by-Period Insights**

| Period | Description | Median Diff. | Notable Observation |
|--------|-------------|-------------|----------------------|
| A | Occupied school year | ~0.07 | Moderate spread; outliers up to ~0.48 |
| B | Unoccupied school year | ~0.07 | Similar to A but slightly wider box; outliers ~0.50 |
| C | Occupied summer | ~0.06 | Tightest distribution; most consistent performance |
| D | Unoccupied summer | ~0.06 | Similar to C; few outliers above 0.35 |
| E | Peak summer demand | ~0.10 | **Largest** spread and highest outliers (~0.65); most variable |

- **Key Takeaways**
    - **Period E (peak summer)** stands out with the highest median difference and widest distribution, indicating that building efficiency during peak demand hours deviates most dramatically from annual benchmarks — this period is the most critical for targeted energy management intervention
    - **Periods C and D (summer)** show the tightest distributions, suggesting more consistent building behaviour during summer regardless of occupancy state
    - **Periods A and B (school year)** show comparable variability, implying that both occupied and unoccupied hours during the school year produce similarly meaningful deviations from total benchmarks
    - The presence of **high outliers in all periods** confirms that for some buildings, temporally segmented scores can differ from total scores by **up to 48–65%**, reinforcing the practical value of period-specific benchmarking for identifying underperforming buildings

- **Advancement of Smart Meter Analytics**
    - Demonstrates how smart meter data can be integrated with building energy benchmarking
    - Enables detection of performance variations **across time** (daily and seasonal), relative to a community of buildings — critical for urban energy management

- **Practical Implications**
    - Temporally segmented benchmarks support:
        1. **Targeting and prioritising** individual building efficiency opportunities
        2. **Near-real-time monitoring** of building performance deviations at portfolio scale
    - Well-suited for integration into **digital twin–enabled energy management platforms**, which stream smart meter data and require dynamic, real-time metrics to function effectively

- **Digital Twin Vision**
    - A smart city digital twin platform built around temporally segmented benchmarks (Fig. 2) would allow portfolio managers to:
        - Identify and prioritise specific **retrofit strategies**
        - Detect **near-real-time efficiency deviations** in the context of the whole building portfolio
    - Positions temporally segmented benchmarks as a foundational metric for next-generation urban energy management systems

### Prioritisation of Specific Retrofit Strategies

- **Core Idea:** Differences between total and temporally segmented efficiency scores reveal *when* a building underperforms, which directly informs *what type* of retrofit or intervention is most appropriate

- **Building-Level Examples (Fig. 3 – Summer Peak Period):**

| Building | Pattern | Implication |
|----------|---------|-------------|
| 18 | Total scores consistently **higher** than peak scores (differences up to 34.1%) | Masked inefficiency during peak hours → prioritise AC upgrades or peak-load shifting |
| 20 | Peak scores consistently **more efficient** than total | Low priority for peak demand interventions |
| 8  | Shifted from positive to negative scores over time | Sharp operational change → review building management system (BMS) |
| 6  | Mixed, variable deviations day-to-day | Unstable controls → investigate automated systems and actual building conditions |


### Near-Real-Time Energy Management (Fig. 4)

- **Approach:** 30-day moving average of raw efficiency scores tracked across periods within individual buildings to detect performance trends over time

- **Building 14:**
    - Occupied and unoccupied scores aligned with total for first ~2 months
    - From late December onward: occupied scores **improved**, unoccupied scores **declined**
    - Persistent gap suggests an **operational shift** (e.g., BMS misalignment or poor after-hours behaviour) — flags need for automation schedule review and occupant behaviour campaigns

- **Building 4:**
    - Unoccupied scores consistently very high (>0.90) throughout the year
    - Occupied scores ~10% lower, gap widening in the final 2 months
    - Summer peak scores tracked occupied period trends
    - Suggests capital-intensive occupied-hours retrofits are most appropriate: lighting upgrades, AC efficiency, demand-controlled ventilation

### External Validation

- **Model Fit:** Mean adjusted R² values ranged **0.72–0.80** across periods — consistent with regression benchmarking literature
- **Key Drivers of EUI** (significant in >75% of models for ≥3 periods):
    - **Higher EUI:** Laboratory space, mechanical room space, office space, larger floor area, older buildings (less-efficient equipment)
    - **Lower EUI:** Circulation space (hallways, lobbies) — low occupancy loads, no energy-intensive equipment
    - **Notable finding:** Service space (bathrooms, janitorial) positively associated with EUI — a previously undocumented relationship, possibly driven by hot water use, ventilation, and cleaning equipment

### Limitations & Future Directions

- **Benchmark Accuracy:** Difficult to verify that benchmarking scores truly reflect actual efficiency levels, especially at scale
- **Regression Assumptions:** Residuals assumed to reflect only inefficiency, but also contain statistical noise and measurement error
- **Occupancy Estimation:** Measured occupancy data unavailable for all buildings; estimated states may not reflect reality — incorporating occupancy proxies would improve model accuracy
- **Future Work:**
    - Validate benchmarks against real retrofit outcomes and operational changes
    - Test alternative benchmarking methodologies (e.g., weekly, monthly scales)
    - Expand digital twin platform to include gas, heating, cooling, and water data
    - Conduct user-interface testing with facility managers to refine platform utility

**Table 4. Frequency of Regression Coefficient Statistical Significance (%)**

| Variable | Total (n=365) | A (n=174) | B (n=174) | C (n=75) | D (n=75) | E (n=86) |
|----------|:-------------:|:---------:|:---------:|:--------:|:--------:|:--------:|
| BUR: service | 100 | 100 | 100 | 100 | 100 | 100 |
| Floor area | 99 | 98 | 99 | 100 | 100 | 100 |
| BUR: laboratory | 94 | 98 | 96 | 93 | 91 | 95 |
| BUR: circulation | 91 | 67 | 91 | 72 | 100 | 24 |
| BUR: office | 88 | 93 | 84 | 95 | 91 | 90 |
| BUR: mechanical | 85 | 89 | 84 | 97 | 88 | 100 |
| Years since renovation | 83 | 62 | 83 | 99 | 87 | 65 |
| Building age | 39 | 22 | 39 | 57 | 52 | 33 |
| BUR: classroom | 21 | 9 | 15 | 23 | 24 | 8 |
| BUR: supply | 18 | 6 | 16 | 12 | 32 | 10 |
| BUR: general | 11 | 3 | 4 | 12 | 21 | 9 |
| BUR: study | 9 | 2 | 2 | 13 | 19 | 5 |
| BUR: special | 1 | 10 | 1 | 0 | 0 | 14 |
| Number of floors | 1 | 2 | 1 | 0 | 0 | 0 |
| Percent renovated | 0 | 0 | 0 | 0 | 0 | 0 |

*Note: n = number of days in period. BUR = Building Use Ratio.*
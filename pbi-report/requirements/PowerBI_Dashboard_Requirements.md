# Power BI Dashboard - Requirements & Business Rules

**Project:** An AI-Enabled Digital Twin for EV Charging - Results Dashboard
**Purpose of this document:** the single specification Claude Code follows to model the data and author DAX in Power BI. It defines the data model, metric definitions, calculation rules, page content, visuals, and integrity rules. It does **not** contain DAX; write the DAX from these rules.

---

## 1. Purpose and audience

The dashboard makes the dissertation's story legible to viewers who will not read the code or the full document: the supervisor, examiners, and a general technical audience. It is an **explanatory** report - a guided narrative that walks a viewer from the real data through to the findings - not an operational monitoring tool. Density should be low, each page answers one question, and every visual must read in about five seconds.

The dashboard tells one arc across six content pages:

1. **What does the real network look like, and why is the twin built this way?** (EDA)
2. **Is the simulation credible?** (calibration against real data)
3. **Which levers actually move the network?** (scenario evaluation)
4. **Does the learned pricing policy beat the handcrafted schedule, and why?** (policy comparison)
5. **Is the result robust, and when does it stop working?** (elasticity x seed sweep and the boundary)
6. **How does the learned policy actually price?** (behaviour)

The arc is deliberate: **real data -> the twin reproducing it -> experiments on the twin**. The calibration page is the bridge between reality and model, and is more convincing because the viewer has just seen the reality it reproduces.

---

## 2. Data sources

### Repository layout (where the data lives)

```
project_root/
├── data/
│   ├── ev_twin.duckdb              # raw + aggregated project database
│   └── raw/
│       └── usb_merged_final_data.csv   # raw session export (provenance)
└── results/
    ├── <existing summary CSVs>     # pipeline outputs (see below)
    └── <files to be created>       # ALL new CSVs are written here too
```

**Path rules.** The dashboard reads **finished CSV files from `results/` only**. Do not connect Power BI to live DuckDB for calculation, and do not re-run any computation. The raw `data/` sources (`ev_twin.duckdb`, `data/raw/usb_merged_final_data.csv`) are provenance and the origin of the exports below; they are not read directly by Power BI except as a last-resort fallback (see the EDA source note). **Every file to be created is written to `results/`**, alongside the existing summary outputs - nothing new is placed in `data/`. If a listed file is absent, flag it and state the columns it must contain rather than substituting values.

### Session-grain source (EDA layer only)

| File (in `results/`) | Grain | Role |
|---|---|---|
| `results/sessions_clean.csv` (export from `data/ev_twin.duckdb` table `charging_sessions`; last-resort fallback `data/raw/usb_merged_final_data.csv` with section 5 cleaning applied in Power Query) | one session | Provenance layer - feeds the EDA page only |

Required columns (rename in Power Query if the source differs): `session_id`, `session_start` (datetime), `energy_kwh`, `duration_hrs`, `connector_type`, `charger_id`, `carbon_intensity_gco2_kwh` (if present).

### Summary sources (all other pages) - all in `results/`

| File | Grain (one row per...) | Role |
|---|---|---|
| `results/calibration_summary.csv` (create if absent) | distribution | Calibration KS statistics |
| `results/scenario_summary.csv` (export from notebook 03 if absent) | scenario | Scenario evaluation |
| `results/eval_results.csv` | episode x policy (headline config, elasticity 0.8) | Per-episode policy outcomes |
| `results/eval_summary.csv` | policy (wide) | Aggregated headline comparison |
| `results/sweep_results.csv` | elasticity x seed (wide) | Robustness runs |
| `results/sweep_summary.csv` | elasticity | Sweep aggregates with seed std |
| `results/elasticity_boundary.csv` | elasticity | Degenerate-boundary scan |
| `results/ppo_price_by_hour.csv` | hour | Learned policy behaviour |

Files to be created before build - **all written to `results/`**, with required columns:
- `results/sessions_clean.csv`: the session columns above. Source: `data/ev_twin.duckdb` -> `charging_sessions`. A single DuckDB `COPY charging_sessions TO 'results/sessions_clean.csv' (HEADER, DELIMITER ',')`, or a pandas export from notebook 01.
- `results/scenario_summary.csv`: `scenario, sessions_completed, revenue_gbp, co2_g, avg_wait_hrs, avg_utilisation, wilcoxon_p_vs_baseline`. Source: notebook 03 scenario engine output.
- `results/calibration_summary.csv`: `distribution, ks_statistic, sim_mean, real_mean`. Source: notebook 02 calibration output.

---

## 3. Critical reshaping rule (read before modelling)

`sweep_results.csv` and `eval_summary.csv` are **wide**: one column block per policy (e.g. `PPO_score`, `ToU_score`, `ToU3_score`, `Flat_score`, `Congestion_score`, and the same for revenue, wait_steps, sessions, co2). A wide layout cannot support a policy slicer or a single score measure.

**Rule:** unpivot these into **long** format in Power Query so that **Policy becomes a dimension** and each metric (score, revenue, wait_steps, sessions, co2) is a single column. Target grains:

- Sweep fact: one row per **elasticity x seed x policy**.
- Evaluation summary fact: one row per **policy**; episode fact: one row per **episode x policy**.

Drop pre-computed margin columns (`margin_vs_ToU`, etc.) from the facts and recompute them as measures (section 8), so there is one source of truth per metric.

---

## 4. Data model (star schema)

Build a star schema. Facts hold numeric outcomes at a defined grain; dimensions hold descriptive attributes and drive slicers. Avoid fact-to-fact relationships; connect facts only through shared dimensions. The session fact (EDA) stands alone and does **not** join to the results facts.

### Dimension tables

- **DimPolicy** - `PolicyKey`, `PolicyName` (PPO / Flat / ToU 2-band / ToU 3-band / Congestion), `PolicyType` (Learned / Static schedule / Static flat / Heuristic), `IsLearned`, `IsBaseline`, `SortOrder`. Drives a single consistent policy order and colour across every visual.
- **DimElasticity** - `Elasticity`, `LambdaWeight` (waiting-time weight derived at that elasticity, R2), `TradeoffExists`, `RegimeLabel` ("Degenerate" / "Trade-off"). Include degenerate values (0.5, 0.6) and the trained range (0.7-1.0).
- **DimScenario** - `ScenarioName`, `ScenarioType` (Baseline / Adoption growth / Pricing / Carbon / Combined), `AdoptionMultiplier`, `SortOrder`.
- **DimHour** - 0-23, `HourLabel`, `IsToUPeak` (07:00-19:00). Shared by the EDA arrival fact and the price-by-hour fact.
- **DimSeed** - the five training seeds.
- **DimDistribution** - calibration targets (Sessions per day / Energy per session / Session duration), `IsParametricFit` (distinguishes genuine fits from the tautological energy resampling).
- **DimConnector** - three connector types, friendly label, observed share, `SortOrder`.
- **DimCharger** - one row per charger id (optional per-charger slicing).
- **DimDayType** - Weekday / Weekend / All (EDA slicer).

### Fact tables

- **FactSession** - grain: session (from `sessions_clean.csv`). Base: energy_kwh, duration_hrs, carbon_intensity, derived hour and day_type. Links to DimConnector, DimCharger, DimHour, DimDayType. **No** link to results facts.
- **FactCalibration** - grain: distribution. Base: ks_statistic, sim_mean, real_mean. Links to DimDistribution.
- **FactScenario** - grain: scenario. Base: sessions, revenue, co2, avg_wait_hrs, utilisation, wilcoxon_p_vs_baseline. Links to DimScenario.
- **FactEvalEpisode** - grain: episode x policy. Base: revenue, wait_steps, avg_wait_hrs, sessions, co2, utilisation, score. Links to DimPolicy.
- **FactEvalSummary** - grain: policy. Aggregated headline comparison. Links to DimPolicy.
- **FactSweep** - grain: elasticity x seed x policy. Base: revenue, wait_steps, sessions, co2, score. Links to DimPolicy, DimElasticity, DimSeed.
- **FactPriceByHour** - grain: hour. Base: mean price; add a computed ToU reference price per hour (0.45 if peak else 0.15). Links to DimHour.

---

## 5. EDA cleaning rules (Power Query, match the notebook exactly)

The EDA must reproduce the analysis the model was calibrated on. Apply the same rules the pipeline applied, and no others:

- **Duration cap:** cap `duration_hrs` at 4.0 (99.9th percentile). Longer connections are parking overstay and were capped before fitting. **Cap, do not drop.**
- **Energy floor:** exclude sessions below 5 kWh only if notebook 01 did; if unconfirmed, retain and flag.
- Remove rows with null `session_start`, `energy_kwh`, or `duration_hrs`.
- Derive `hour` (0-23) and `day_type` (Weekday / Weekend) from `session_start`.
- Do **not** re-scale, normalise, or resample. Show observed data as-is after the caps above.

Where a cleaning choice cannot be confirmed against notebook 01, apply the conservative option (retain the row) and note the assumption.

---

## 6. EDA consistency rules (prevent the dashboard contradicting the dissertation)

Power BI recomputes distributions live, so it can silently disagree with the fitted figures.

- **C1 - Fixed binning, not automatic.** Do not use auto-binning for the energy and duration histograms. Set explicit bins so shapes match the notebook: energy in 2 kWh bins (0 to ~110); duration in 0.1-hour bins (0 to 4). Auto-bins change the visible shape and contradict the dissertation figure.
- **C2 - Empirical only on the EDA page.** Do not draw fitted lognormal or Negative Binomial curves in DAX. Parametric fits belong to the calibration page. The EDA page shows what was observed; calibration shows the fit reproducing it. Keep them separate.
- **C3 - Observed, not simulated.** Every EDA visual is titled "Observed" and uses the observed-data colour (teal `#1B9AAA`), never simulated styling.
- **C4 - Headline facts are counted, not typed.** Summary numbers (session count, chargers, date range, medians) are measures over FactSession, not hardcoded. The count should equal 29,775; treat a mismatch as a data-load error to investigate, not to hardcode around.

---

## 7. Core business rules and definitions

These govern how every measure is calculated. Incorrect handling here produces plausible-looking but wrong numbers.

- **R1 - Objective score.** `revenue - LambdaWeight * wait_steps`. Primary comparison metric. Prefer a pre-computed `score` column where present; where computed, `LambdaWeight` comes from DimElasticity for the elasticity in context, never a constant.
- **R2 - Lambda is per-elasticity, not global.** The weight differs for every elasticity (~0.23 at 0.7, 0.93 at 0.8, 1.59 at 0.9, 2.27 at 1.0). Any sweep score or margin must use the elasticity-specific weight. Hardcoding one lambda across the sweep is a defect.
- **R3 - Headline configuration.** The default state of the policy-comparison and behaviour pages is **elasticity 0.8, lambda 0.934**. Slicers may change it; the landing state is 0.8.
- **R4 - Margin definition.** Learned-policy advantage over a baseline is `PPO score - baseline score` at matched elasticity, reported both as an absolute point difference and as a percentage of the baseline. Headline: +20.2% on objective, +23.8% on revenue vs ToU 2-band.
- **R5 - Waiting-time display.** Store in hours (`avg_wait_hrs`); **display in minutes** (x60). `wait_steps` is internal to the score only and is never shown.
- **R6 - Seed uncertainty.** Every elasticity has five seeds. Report the **mean** across seeds as the point value and the **standard deviation** as an uncertainty band. Never show a single seed as the result.
- **R7 - Calibration on the KS statistic, not the p-value.** Display the KS statistic. If a p-value appears, caveat that with ~30,000 observations the test rejects on negligible deviations, so the statistic and moment agreement are the criteria. Never present a low p-value as calibration failure.
- **R8 - Percentages.** Utilisation is a 0-1 fraction, displayed as a percentage. Growth figures (e.g. +6,981% waiting time under 2x adoption) are relative to the baseline scenario.
- **R9 - Degenerate regime.** Below the boundary (~0.65) no trade-off and no trained agent exist. These rows are visually distinguished ("Degenerate - pricing collapses to maximum tariff") and must not be plotted as if PPO scores existed there.

---

## 8. Required measures (describe; author the DAX)

Group in a dedicated measure table. Names indicative; keep them human-readable.

**EDA**
- Total sessions; distinct chargers; date range (min/max `session_start`); span in months.
- Median and mean energy; median and mean duration.
- Session count by hour; by hour x day_type.
- Session count and share by connector; mean energy and mean duration by connector.
- Peak-window share: fraction of sessions arriving 07:00-19:00 (quantifies why a clock tariff cannot discriminate; expect it high).

**Evaluation / comparison**
- Mean revenue, score, sessions, CO2 per policy (headline config); mean waiting time in minutes (R5); objective score (R1).
- Margin vs ToU 2-band and vs Flat, absolute and percent (R4).
- Selected-policy score and best-baseline score, for a dynamic advantage card.

**Sweep / robustness**
- Mean PPO score by elasticity across seeds; PPO score std by elasticity (R6).
- Mean score by policy by elasticity.
- PPO advantage over ToU 2-band and over ToU 3-band by elasticity (R2, R4).
- Regime flag for the selected elasticity (R9).

**Scenario**
- Each KPI by scenario; percent change vs baseline (R8).
- Significance indicator from the Wilcoxon p-value: significant / not significant / **undefined**. Handle the undefined case (ToU and combined on session counts, where every paired difference is zero) explicitly - not a blank or an error.

**Behaviour / calibration**
- Mean learned price by hour with the ToU reference overlay.
- KS statistic by distribution; simulated-vs-observed mean difference (R7).

---

## 9. Report pages

One question per page.

**Page 0 - Overview.** Four KPI cards, one per headline finding: calibration quality (max KS, "KS <= 0.061 - validated"); "adoption dominates" (waiting-time rise under 2x adoption); the "+20.2% vs ToU" advantage; the boundary ("no trade-off below elasticity ~0.65"). One sentence each. Stands alone as the elevator pitch.

**Page 1 - The Real Network (EDA).** *What does the real data look like, and why is the twin built this way?* Each visual pairs an observed shape with the modelling decision it drove (state the decision in a subtitle or adjacent text):

| Visual | Data | Insight to state |
|---|---|---|
| Arrivals by hour (column), ToU window shaded, day-type slicer | Count by hour x day_type | "Bimodal, inside the ToU window -> a clock tariff can't tell a busy hour from a quiet one" |
| Energy histogram (fixed 2 kWh bins) | FactSession energy | "Flat 5-20 kWh plateau + heavy tail -> empirical resampling, no parametric fit adequate" |
| Duration histogram (fixed 0.1 hr bins) | FactSession duration | "Clean lognormal shape -> parametric fit, validated next page" |
| Connector mix (share) + mean energy/duration per connector | By connector | "82 / 14 / 4 split, very different profiles -> sample per connector, don't pool" |
| Dataset summary cards | Measures | 29,775 sessions, 6 chargers, date range, median energy, median duration |

**Page 2 - Twin credibility (calibration).** KS statistic by distribution with the parametric-fit flag; simulated-vs-observed means. Note that energy resampling makes its agreement expected by construction (R7). This page shows the twin reproducing the Page 1 distributions.

**Page 3 - Which levers move the network (scenarios).** Scenario KPIs with percent change vs baseline; adoption growth moves everything, pricing moves revenue only. Show the significance indicator including the undefined case.

**Page 4 - Learned pricing beats the clock (headline).** Policy comparison at headline config: revenue, waiting time (minutes), sessions, CO2, score per policy; a prominent +20.2% / +23.8% advantage. Must surface the honest points (section 11): ToU scores below Flat; PPO has higher wait and CO2 than ToU.

**Page 5 - Robustness and boundary.** Score by policy across elasticity with PPO's seed-uncertainty band; PPO-minus-ToU margin by elasticity; degenerate region marked. Carries "not a lucky run" and "state-conditioning not granularity" (PPO also beats ToU 3-band).

**Page 6 - How the policy prices (behaviour).** Learned mean price by hour against the ToU reference, showing the three-phase structure. Note that intermediate hourly means (e.g. 0.353 at 08:00) can only arise from state-dependent switching, which a clock schedule cannot produce.

---

## 10. Visual selection rules

- Policy score/revenue comparison: horizontal bar, sorted, best value emphasised. Not pie, not stacked.
- Score across elasticity: line or clustered column by policy; PPO uncertainty as error bars or shaded band.
- Price by hour: line (learned) with stepped line (ToU reference) overlaid; shade where ToU overcharges relative to PPO.
- EDA histograms: column charts with **fixed bins** (C1); never a smoothed density that hides the plateau/tail.
- Arrivals by hour: column with the ToU window shaded and a day-type slicer.
- Scenario KPIs: small multiples or clustered bars per KPI; do not force incompatible scales onto one axis.
- Single headline numbers: KPI cards, large type.
- Calibration: bar of KS statistics; state "lower is better" in the title.
- Avoid dual axes, 3-D, gauges, decorative chrome. Every chart title states the takeaway, not the mechanic ("PPO holds its advantage as demand grows more elastic", not "Score by elasticity").

---

## 11. Data integrity and honesty rules (mandatory)

This dashboard backs an academic submission; it must not oversell.

- **H1 - Show unfavourable comparisons.** PPO has higher mean waiting time and higher CO2 than ToU. Both visible on Page 4. Framing is a superior weighted trade-off, not dominance.
- **H2 - Show ToU below Flat.** Present, do not smooth over.
- **H3 - Represent uncertainty.** Seed std wherever a sweep mean is shown (R6).
- **H4 - Represent the boundary.** Show and label the degenerate regime (R9); do not truncate the elasticity axis to hide it.
- **H5 - No implied optimality.** Never describe the learned policy as "optimal"; it outperforms tested baselines, it is not proven optimal.
- **H6 - No fabricated values.** Every number traces to a source file. Missing values are shown as missing, never interpolated or invented.
- **H7 - Statistical honesty.** Apply R7; surface the undefined-Wilcoxon case rather than hiding it.
- **H8 - Label observed vs simulated everywhere.** FactSession charts titled "Observed" (teal); model-comparison charts titled "Simulated" or "Calibrated". Visually distinct (C3).
- **H9 - The EDA page is not validation.** It describes the data; validation is the calibration page. EDA titles must not claim the model is "accurate" or "validated".
- **H10 - Excluded metering data stays excluded.** Do not visualise the building-meter readings (r = -0.086, collection failure). If provenance of the exclusion is wanted, a one-line note, not a chart.

---

## 12. Design and theme

- **Palette (institutional):** Newcastle navy `#123B5C` for structure and headers. Reuse the project encoding where colour carries meaning: teal `#1B9AAA` for demand / observed data / state; amber `#E4A02A` for the price signal and the learned policy; navy for supply and static policies; grey `#7B8C99` for measurement and uncertainty. Identical encoding across every page.
- Restrained, high-contrast, no gradients or 3-D; white or light-grey background.
- Consistent policy colour across pages, driven by DimPolicy so it cannot drift.
- Section headers identical in size and weight on every page; labels legible at presentation scale.
- Provide a Power BI theme JSON encoding the palette so styling is applied once.

---

## 13. Modelling conventions for Claude Code

- One source of truth per metric: margins and scores are measures, not stored columns (section 3).
- All aggregation via measures on facts; no pre-aggregation in Power Query except the wide-to-long reshape (section 3) and the EDA cleaning (section 5).
- FactSession is isolated - no relationship to results facts (section 4).
- Only DimPolicy, DimElasticity, DimScenario, DimConnector and DimDayType are slicer sources; do not slice on fact columns.
- Name measures for humans ("PPO advantage over ToU (%)"), columns for the model.
- No calendar/date table is required (the simulation has no calendar); DimHour handles the time axis.

### Validation checks (must hold on current data, or the model is wrong)

**Results layer**
- Headline page reproduces: PPO score 383.1, revenue 400.9, +20.2% vs ToU, KS statistics 0.061 / 0.009 / 0.037. If not, check R1, R2 and the reshape.

**EDA layer**
- Total sessions = 29,775; distinct chargers = 6.
- Connector shares ~82% / 14% / 4% (COMBO / CHADEMO / T2).
- Median duration ~0.64 hr; median energy ~27 kWh (means ~0.74 hr, ~30.4 kWh).
- Peak-window (07:00-19:00) session share is high.
- Arrival-by-hour shape is bimodal (late-morning and mid-afternoon peaks).

If any check fails, fix the source load, the reshape (section 3), or the cleaning (section 5) - never adjust the numbers to match.

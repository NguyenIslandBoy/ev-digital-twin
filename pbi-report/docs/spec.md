# EV Digital Twin - Dashboard Build Spec

**Status: Client-validated** (wireframe + metric table approved 2026-07-27 with no change requests). Drives `/bi-accelerator:02_data-transform`, `/bi-accelerator:03_model-build`, `/bi-accelerator:04_dax-write`.

-   Requirements source: [`pbi-report/requirements/PowerBI_Dashboard_Requirements.md`](../requirements/PowerBI_Dashboard_Requirements.md) (quoted as "§n" below)
-   Validated wireframe: [`docs/wireframe/ev-digital-twin-wireframe.html`](wireframe/ev-digital-twin-wireframe.html) - 7 pages, layout and metric set approved as-is
-   Target `.pbip`: `pbi-report/ev-digital-twin.pbip`

------------------------------------------------------------------------

## 1. Purpose (from §1)

Explanatory dissertation dashboard - "a guided narrative that walks a viewer from the real data through to the findings", one question per page, "every visual must read in about five seconds". Arc: **real data → the twin reproducing it → experiments on the twin**. Not an operational monitor.

Audience: supervisor, examiners, general technical viewers. Academic honesty rules (§11) are mandatory.

## 2. Data sources (verified on disk 2026-07-27)

Power BI reads **finished CSVs from `results/` only** (§2 path rules). Never live DuckDB, never recomputation.

| File | Grain | Status | Verified row count |
|----|----|----|----|
| `results/sessions_clean.csv` | session | **created** - export of `ev_twin.duckdb · charging_sessions` (identical to `data/raw/usb_merged_final_data.csv`, client-confirmed) | 29,775 |
| `results/calibration_summary.csv` | distribution | **created** - extracted from executed notebook 02 outputs | 3 |
| `results/scenario_summary.csv` | scenario | **created** - from DuckDB `scenario_summary` + Wilcoxon revenue p-value (see §2a) | 6 |
| `results/scenario_significance.csv` | scenario × KPI | **created (PROPOSED, client-accepted)** - Wilcoxon p per scenario × KPI, verified against notebook 03 printed values to full precision | 30 |
| `results/eval_results.csv` | episode × policy | pre-existing | 1,500 (500 × 3 policies) |
| `results/eval_summary.csv` | policy (wide) | pre-existing | 3 |
| `results/sweep_results.csv` | elasticity × seed (wide) | pre-existing | 20 (4 × 5) |
| `results/sweep_summary.csv` | elasticity | pre-existing | 4 |
| `results/elasticity_boundary.csv` | elasticity | pre-existing | 6 (0.5–1.0) |
| `results/ppo_price_by_hour.csv` | hour | pre-existing | 24 |

`results/sweep_headline.csv` and `results/evaluations.npz` exist but are **not dashboard sources**; `sweep_headline.csv` may be used as a reconciliation aid for the sweep unpivot.

### 2a. Decisions taken and client-accepted

-   `scenario_summary.csv` column `wilcoxon_p_vs_baseline` carries the **revenue** p-value (the headline KPI); the full per-KPI grid lives in `scenario_significance.csv`. *(§2's single-column schema cannot support §8's per-KPI significance indicator - p-values differ per KPI.)* (inferred, validated)
-   Undefined Wilcoxon cases confirmed in data exactly where §8 predicts: **ToU pricing / sessions_completed** and **Combined / sessions_completed** (every paired difference is zero). Stored as blank p with `significant = False`; must render as "undefined", never blank/error.
-   **Encoding:** `eval_results.csv` / `eval_summary.csv` contain policy value `Flat £0.30` in cp1252. Power Query must load these with **encoding 1252** (or normalize the name); `usb_merged_final_data.csv`-derived files are UTF-8.

## 3. Reshaping rules (§3 - "read before modelling")

`sweep_results.csv` and `eval_summary.csv` are wide (one column block per policy). **Unpivot in Power Query so Policy becomes a dimension**:

-   Sweep fact target grain: **elasticity × seed × policy** (20 rows → 100 rows, 5 policies: PPO, ToU, ToU3, Flat, Congestion).
-   Eval summary fact target grain: **policy** (3 rows); episode fact already long: **episode × policy**.
-   **Drop pre-computed margin columns** (`margin_vs_ToU`, `margin_vs_ToU3`, `margin_vs_Flat`) - margins are measures only (§3, §13: "one source of truth per metric").
-   `sweep_summary.csv` is *not* a fact - its aggregates are reproduced by measures; use it only for reconciliation of the unpivot.

## 4. Star schema (§4)

Facts hold numeric outcomes; dimensions drive slicers. **No fact-to-fact relationships. FactSession is isolated** - no relationship to any results fact (§4, §13).

### Dimensions

| Table | Columns | Source / values (verified) |
|----|----|----|
| DimPolicy | PolicyKey, PolicyName (PPO / Flat / ToU 2-band / ToU 3-band / Congestion), PolicyType (Learned / Static flat / Static schedule / Heuristic), IsLearned, IsBaseline, SortOrder | authored; maps raw names `PPO`, `ToU`, `ToU3`, `Flat`/`Flat £0.30`, `Congestion`. Drives the fixed colour/order everywhere |
| DimElasticity | Elasticity, LambdaWeight, TradeoffExists, RegimeLabel | from `elasticity_boundary.csv`: 0.5/0.6 → "Degenerate - pricing collapses to maximum tariff" (λ null); 0.7→0.233018, 0.8→0.933670, 0.9→1.591571, 1.0→2.201813. **λ at 1.0 is 2.202 in data; §7 R2's "\~2.27" is superseded by data** (client-validated) |
| DimScenario | ScenarioName, ScenarioType, AdoptionMultiplier, SortOrder | 6 scenarios: Baseline / Adoption ×1.5 / Adoption ×2 / ToU pricing / Carbon incentive / Combined |
| DimHour | Hour 0–23, HourLabel, IsToUPeak = hour ∈ [7,18] ("07:00–19:00", §2) | authored; shared by FactSession-derived hour and FactPriceByHour |
| DimSeed | Seed 0–4 | from sweep |
| DimDistribution | DistributionName, IsParametricFit | Sessions per day (TRUE) / Energy per session (**FALSE** - "tautological energy resampling", §4) / Session duration (TRUE) |
| DimConnector | ConnectorKey, FriendlyLabel, ObservedShare, SortOrder | CCS Combo (`IEC_62196_T2_COMBO`, 82.1%) / CHAdeMO (`CHADEMO`, 14.3%) / Type 2 AC (`IEC_62196_T2`, 3.6%) |
| DimCharger | ChargerId (6 values) | optional slicing |
| DimDayType | Weekday / Weekend / All | authored |
| DimKpi *(inferred, for the significance fact)* | KpiName (sessions_completed / energy_kwh / revenue_gbp / co2_g / avg_wait_hrs / avg_utilisation) | supports the §8 per-KPI significance indicator |

### Facts

| Table | Grain | Base columns | Links |
|----|----|----|----|
| FactSession | session | energy_kwh, duration_hrs (capped), carbon_intensity_gco2_kwh, derived hour + day_type | DimConnector, DimCharger, DimHour, DimDayType. **Isolated** |
| FactCalibration | distribution | ks_statistic, sim_mean, real_mean | DimDistribution |
| FactScenario | scenario | sessions, revenue, co2, avg_wait_hrs, utilisation, wilcoxon_p (revenue) | DimScenario |
| FactScenarioSignificance | scenario × KPI | wilcoxon_p, significant | DimScenario, DimKpi |
| FactEvalEpisode | episode × policy | revenue, wait_steps, avg_wait_hrs, sessions, co2, utilisation, score | DimPolicy |
| FactEvalSummary | policy | headline aggregates (means + stds) | DimPolicy |
| FactSweep | elasticity × seed × policy | revenue, wait_steps, sessions, co2, score | DimPolicy, DimElasticity, DimSeed |
| FactPriceByHour | hour | ppo_mean_price, tou_reference_price (0.45 if IsToUPeak else 0.15, §4) | DimHour |

Slicer sources: **only** DimPolicy, DimElasticity, DimScenario, DimConnector, DimDayType (§13).

**⚠ Never mix FactSweep and FactEvalSummary on one visual**: at elasticity 0.8 the sweep gives PPO score 395.2 (30-episode config) while the headline eval gives 383.1 (500 episodes). Different run configurations by design; headline claims come from FactEvalSummary only.

## 5. EDA cleaning (Power Query, §5 - verified against actual data)

-   **Duration cap at 4.0 h** - cap, do not drop. Exactly **33 rows** exceed 4.0 in the source; observed p99.9 = 4.12, spec value 4.0 governs.
-   **Energy floor:** already applied upstream - source minimum is exactly 5.00 kWh, 0 rows below. **No filter step needed** (conservative rule satisfied trivially).
-   **Nulls:** 0 null `session_start` / `energy_kwh` / `duration_hrs` in the export; keep the removal step as a guard.
-   Derive `hour` (0–23) and `day_type` (Weekday = Mon–Fri) from `session_start`.
-   No re-scaling / normalising / resampling (§5); fixed binning is a *visual* setting (§6 C1: energy 2 kWh bins 0–110, duration 0.1 h bins 0–4).

## 6. Validated metric definitions

All feasibility-checked against the actual files; every value below was reproduced during EDA.

### EDA (FactSession - measures, never typed constants; §6 C4)

| Measure | Definition | Verified value |
|----|----|----|
| Total Sessions | COUNTROWS FactSession | **29,775** |
| Distinct Chargers | DISTINCTCOUNT charger_id | **6** |
| Date Range / Span | MIN/MAX session_start | Mar 2021 – Jul 2024 (\~40 months) |
| Median / Mean Energy | over energy_kwh | **27.4 / 30.4 kWh** |
| Median / Mean Duration | over capped duration | **0.644 / 0.740 h** |
| Sessions by Hour (× DayType) | count by derived hour | bimodal; peaks 11:00 (2,346) and 15:00 |
| Connector Share / Profiles | share of sessions; mean kWh, mean h per connector | 82.1 / 14.3 / 3.6%; Combo 34.0 kWh · 0.71 h, CHAdeMO 13.7 · 0.62, Type 2 15.5 · 1.83 |
| Peak-Window Share | fraction arriving 07:00–19:00 | **80.3%** |

### Evaluation / comparison (FactEvalEpisode / FactEvalSummary)

| Measure | Definition | Verified value |
|----|----|----|
| Mean Score per policy | mean of `score` (pre-computed; R1) | PPO **383.1**, Flat 341.7, ToU 318.8 |
| Mean Revenue per policy | mean revenue_gbp | PPO **£400.9**, Flat £386.9, ToU £323.9 |
| Mean Wait (min) | mean avg_wait_hrs × 60 (R5) | PPO 9.4, ToU 2.9, Flat 19.8 |
| Mean Sessions / CO₂ per policy | means | PPO 41.0 / 64.2 kg; ToU 34.3 / 53.9 kg |
| PPO Advantage vs ToU (abs / %) | PPO score − ToU score; ÷ ToU (R4) | **+64.3 / +20.2%** |
| PPO Revenue Advantage vs ToU (%) | same on revenue | **+23.8%** |
| Margin vs Flat (abs / %) | PPO − Flat | +41.3 / +12.1% |
| Selected-policy vs best-baseline score | dynamic advantage card | - |

**Scope limitation (client-accepted):** headline eval contains **PPO, ToU 2-band, Flat only**. `INFEASIBLE:` a 5-policy comparison at the headline 500-episode config - the data does not exist. Per client decision (2026-07-27), Page 4 additionally carries a **five-policy cross-check card sourced from FactSweep at elasticity 0.8** (PPO 395.2, Congestion 378.3, ToU3 341.6, Flat 338.3, ToU 318.1) - a *separate visual*, labelled as a different 30-episode run; it must never be merged into the headline bars.

### Sweep / robustness (FactSweep; every point = mean of 5 seeds, R6)

| Measure | Definition | Verified value |
|----|----|----|
| PPO Score Mean / Std by elasticity | AVERAGEX/STDEVX over seeds | 432.3±3.1 / 395.2±2.6 / 367.1±2.8 / 355.5±2.1 |
| Mean Score by policy × elasticity | after unpivot | matches `sweep_summary.csv` exactly (reconciliation) |
| PPO Margin vs ToU 2-band by elasticity | per-elasticity λ already in `score` (R2) | 90.7 / 77.1 / 70.4 / 79.8 |
| PPO Margin vs ToU 3-band by elasticity | PPO − ToU3 | 58.1 / 53.6 / 56.1 / 72.9 |
| Regime Flag | from DimElasticity.RegimeLabel (R9) | 0.5, 0.6 → Degenerate |

### Scenario (FactScenario / FactScenarioSignificance)

| Measure | Definition | Verified value |
|----|----|----|
| KPI by scenario | base means (500 episodes) | e.g. Baseline £201.5 revenue |
| \% Change vs Baseline | (scenario − baseline) / baseline (R8) | ToU revenue **+37.9%**; Adoption ×2 wait **+6,981%** |
| Significance Indicator | p \< 0.05 → significant; p ≥ 0.05 → not significant; p blank → **"undefined - all paired differences zero"** (§8) | undefined: ToU & Combined on sessions |

### Behaviour / calibration (FactPriceByHour / FactCalibration)

| Measure | Definition | Verified value |
|----|----|----|
| Learned Price by Hour + ToU reference | mean price; 0.45/0.15 overlay | floor £0.150 (15:00–23:00), peak £0.435 (13:00), **£0.353 at 08:00** |
| KS Statistic by distribution | display statistic, never p (R7) | **0.061 / 0.009 / 0.037** |
| Sim − Real mean difference | per distribution | 25.42/25.11 · 30.43/30.44 · 0.763/0.741 |

## 7. Business rules (§7, binding for all DAX)

-   **R1** Score = `revenue − LambdaWeight × wait_steps`; prefer the stored `score` column; computed λ always from DimElasticity in context.
-   **R2** λ is per-elasticity (values in §4 DimGrid above), never a global constant. Hardcoding one λ across the sweep is a defect.
-   **R3** Landing state: elasticity 0.8, λ = 0.934 (data: 0.933670).
-   **R4** Margin = PPO − baseline at matched elasticity, absolute and % of baseline. Headline +20.2% objective / +23.8% revenue vs ToU 2-band.
-   **R5** Wait displayed in **minutes**; `wait_steps` never shown.
-   **R6** Sweep values = mean of 5 seeds ± std band; never a single seed.
-   **R7** Calibration judged on KS **statistic** + moment agreement; p-values caveated ("with \~30,000 observations the test rejects on negligible deviations").
-   **R8** Utilisation 0–1 shown as %; scenario growth is % vs Baseline.
-   **R9** Degenerate rows (elasticity \< \~0.65) labelled "Degenerate - pricing collapses to maximum tariff"; no PPO values plotted there.

## 8. Honesty & consistency rules (§6, §11 - mandatory)

C1 fixed bins · C2 no fitted curves on EDA page · C3 observed = teal, titled "Observed" · C4 headline numbers are measures · H1 PPO's higher wait & CO₂ visible on page 4 · H2 ToU-below-Flat shown · H3 seed std everywhere · H4 boundary shown, axis not truncated · H5 never "optimal" · H6 no fabricated/interpolated values · H7 undefined Wilcoxon surfaced · H8 Observed vs Simulated labelled on every chart · H9 EDA page makes no validation claims · H10 building-meter readings (r = −0.086, collection failure) never visualised.

## 9. Pages (§9; layouts as per validated wireframe)

0 Overview (4 headline KPI tiles + nav) · 1 Real Network / EDA (observed, teal) · 2 Calibration · 3 Scenarios · 4 Policy comparison (headline) · 5 Robustness & boundary · 6 Policy behaviour. Titles state takeaways, not mechanics (§10). Visual selection rules §10 apply (horizontal sorted bars for policy comparison; fixed-bin columns; line + stepped overlay for price; no dual axes / 3-D / gauges).

## 10. Design & theme (§12)

Palette: navy `#123B5C` structure/static policies · teal `#1B9AAA` observed/demand · amber `#E4A02A` learned policy/price · grey `#7B8C99` uncertainty/excluded. Policy colour driven by DimPolicy. White/light-grey background, no gradients. **Client decision (2026-07-27): keep the report's current theme - §12's "provide a Power BI theme JSON" is waived**; apply the palette per-visual/per-dimension where colour carries meaning.

## 11. Reconciliation & validation gates (§13 - all passing on current data)

**Results:** PPO score 383.1 · revenue £400.9 · +20.2% vs ToU · KS 0.061/0.009/0.037. **EDA:** 29,775 sessions · 6 chargers · 82/14/4 split · medians 0.644 h / 27.4 kWh · peak share 80.3% · bimodal arrivals. **Sweep unpivot:** re-aggregated means/stds must equal `sweep_summary.csv`. "If any check fails, fix the source load, the reshape, or the cleaning - never adjust the numbers to match." (§13)

## 12. OPEN items

None. Both former items were closed by client decision on 2026-07-27: - Theme JSON waived - current report theme kept (§10 of this spec). - Page 4 sweep-based five-policy cross-check card **added** (§6 evaluation notes; wireframe updated).

------------------------------------------------------------------------

**Confidence flag: Client-validated** - wireframe and metric set approved without changes; every metric execution-verified against the source files during EDA.

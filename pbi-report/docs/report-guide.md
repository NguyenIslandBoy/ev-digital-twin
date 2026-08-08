---
output:
  pdf_document: default
  html_document: default
---

# EV Digital Twin - Report Build Guide

**Source wireframe:** `docs/wireframe/ev-digital-twin-wireframe.html` (client-validated 2026-07-27; kept as-is per gate decision 2026-07-28) **Model:** `PBIDesktop-ev-digital-twin-61627` (ev-digital-twin.pbip, live Power BI Desktop instance) **Validation:** 44 data visuals - **40 Verified, 1 Needs manual review, 3 Missing measures** (page 6 price tiles → `/bi-accelerator:04_dax-write`)

## How to use

Open `pbi-report/ev-digital-twin.pbip` in Power BI Desktop and build one page at a time. For each visual: add its **Type** from the Visualizations pane, then drag each **Field** into the named **Well**. All value wells take **explicit measures only** - `discourageImplicitMeasures` is on, so a bare numeric column in a value well will not work and is a defect. Text-only elements (narrative tiles, "Reading" cards) are Power BI **text boxes**; page tiles on the Overview are **buttons** with page-navigation actions.

Palette (§12): navy `#123B5C` structure/static policies · teal `#1B9AAA` observed · amber `#E4A02A` learned policy/price · grey `#7B8C99` uncertainty/excluded. Set data colours per DimPolicy member on every policy visual (PPO = amber, ToU 2-band = navy, ToU 3-band/Flat = `#3E6285`, Congestion = grey).

Sort orders: `DimPolicy[PolicyName]`, `DimScenario[ShortLabel]`, `DimConnector[FriendlyLabel]`, `DimDistribution[DistributionName]`, `DimDayType[DayType]` each carry a hidden `SortOrder` column - confirm **Sort by column** is set on each before building (Column tools ▸ Sort by column).

------------------------------------------------------------------------

## Page 0 - Overview

No slicers, no data visuals. Four takeaway tiles and six navigation tiles.

| \# | Visual | Type | Well | Field | Notes |
|----|----|----|----|----|----|
| 0.1 | Takeaway tiles ×4 | Text boxes | - | - | Static narrative. Backing numbers if you prefer cards: `[Max KS Statistic]` (0.061), `[Wait Change vs Baseline (%)]` \@ Adoption ×2 (+6,981%), `[PPO Advantage vs ToU (%)]` (+20.2%), `[PPO Revenue Advantage vs ToU (%)]` (+23.8%) - all Verified |
| 0.2 | Nav tiles 1–6 | Buttons | Action | Page navigation → pages 1–6 | Style per wireframe tiles |

Interactions: none (no data visuals).

------------------------------------------------------------------------

## Page 1 - The Real Network (Observed)

**Slicers:** `DimDayType[DayType]` (dropdown) · `DimConnector[FriendlyLabel]` (dropdown). Both filter FactSession only - every visual on this page is FactSession-backed, so both slicers act on all of them.

| \# | Visual | Type | Well | Field | Notes |
|----|----|----|----|----|----|
| 1.1 | Sessions (observed) | Card | Fields | `[Total Sessions]` | Verified **29,775**. Format `#,0` |
| 1.2 | Chargers | Card | Fields | `[Distinct Chargers]` | Verified **6** |
| 1.3 | Period | Multi-row card | Fields | `[First Session Date]`, `[Last Session Date]`, `[Data Span (Months)]` | Verified Mar 2021 – Jul 2024, 40 months. Format `dd mmm yyyy` |
| 1.4 | Median energy | Card | Fields | `[Median Energy (kWh)]` | Verified **27.4**; put `[Mean Energy (kWh)]` (30.4) in the reference-label/subtitle slot |
| 1.5 | Median duration | Card | Fields | `[Median Duration (h)]` | Verified **0.644**; mean 0.740 as reference label. Cap at 4.0 h confirmed in data (MAX = 4.0) |
| 1.6 | Arrivals by hour | Clustered column chart | X-axis | `DimHour[Hour]` | **Categorical** axis, all 24 hours. Verified rows for every hour (peak band 09:00–15:00, \~2,100–2,350/hr) |
|  |  |  | Y-axis | `[Total Sessions]` | Teal `#1B9AAA` (C3 "Observed") |
|  |  |  | - | - | ToU window shading 07:00–19:00: no native band shading - use a transparent rectangle shape over the plot area, or conditional column colour on `DimHour[IsToUPeak]` (verified column). Title carries the 80.3% takeaway (`[Peak-Window Share (%)]` Verified 80.3%) |
| 1.7 | Connector mix | Horizontal bar chart | Y-axis | `DimConnector[FriendlyLabel]` | Sorted by share |
|  |  |  | X-axis | `[Session Share (%)]` | Verified 82.1 / 14.3 / 3.6%. Format `0.0%`. Teal |
| 1.8 | Connector profiles | Table | Columns | `DimConnector[FriendlyLabel]`, `[Mean Energy (kWh)]`, `[Mean Duration (h)]` | Verified Combo 34.0 kWh · 0.71 h, CHAdeMO 13.7 · 0.62, Type 2 15.5 · 1.83 |
| 1.9 | Energy histogram | Clustered column chart | X-axis | `FactSession[energy_kwh]` **grouped into 2 kWh bins** | Right-click field ▸ New group ▸ Bin size 2 (spec §6 C1: bins 0–110). Report-layer binning - no model change |
|  |  |  | Y-axis | `[Total Sessions]` | Verified by simulated binning: modal bin 10–12 kWh = **1,620** sessions (matches wireframe y-max). Teal. **No fitted curve** (C2) |
| 1.10 | Duration histogram | Clustered column chart | X-axis | `FactSession[duration_hrs]` **grouped into 0.1 h bins** | Bin size 0.1, range 0–4 (C1) |
|  |  |  | Y-axis | `[Total Sessions]` | Verified: modal bin 0.4–0.5 h = **3,345** (matches wireframe). Teal. Annotate "capped at 4.0 h" |

Interactions: default cross-filtering is fine within the page (all one fact). Titles state takeaways per §10; footer carries the H10 exclusion note (building-meter readings never visualised).

------------------------------------------------------------------------

## Page 2 - Twin Credibility (Calibration)

**Slicers:** none.

| \# | Visual | Type | Well | Field | Notes |
|----|----|----|----|----|----|
| 2.1 | Overall status | Card | Fields | `[Max KS Statistic]` | **Needs manual review** - wireframe shows the word "CALIBRATED", but no text-status measure exists. Options: (a) card showing `[Max KS Statistic]` (Verified 0.061) with title "CALIBRATED - all KS ≤ 0.061", or (b) a one-line status measure via `/bi-accelerator:04_dax-write`. Decide at build time |
| 2.2 | Sessions / day KS | Card | Fields | `[KS Statistic]` + visual filter `DimDistribution[DistributionName]` = "Sessions per day" | Verified **0.061**. Subtitle: `[Simulated Mean]` 25.42 vs `[Observed Mean]` 25.11 |
| 2.3 | Session duration KS | Card | Fields | `[KS Statistic]` + filter = "Session duration" | Verified **0.037**; sim 0.763 vs real 0.741 |
| 2.4 | Energy / session KS | Card | Fields | `[KS Statistic]` + filter = "Energy per session" | Verified **0.009**. Must carry the "empirical resampling - agreement by construction" caveat (grey) |
| 2.5 | KS by distribution | Horizontal bar chart | Y-axis | `DimDistribution[DistributionName]` |  |
|  |  |  | X-axis | `[KS Statistic]` | Verified 0.061 / 0.009 / 0.037. Colour: parametric = navy, empirical = grey - conditional on `DimDistribution[IsParametricFit]` (verified column). Footnote: tautological-check caveat |
| 2.6 | Sim vs observed means | Table | Columns | `DimDistribution[DistributionName]`, `[Simulated Mean]`, `[Observed Mean]`, `[Sim vs Obs Difference]`, `DimDistribution[IsParametricFit]` | Verified all three rows. `IsParametricFit` renders the Parametric / By-construction pill; the R7 p-value caveat is a text box below |

Interactions: turn **off** cross-filtering from 2.5/2.6 onto the KS cards (cards are pre-filtered per distribution).

------------------------------------------------------------------------

## Page 3 - Which Levers Move the Network (Scenarios)

**Slicers:** none drawn on the wireframe (DimScenario is an allowed slicer source if wanted later).

| \# | Visual | Type | Well | Field | Notes |
|----|----|----|----|----|----|
| 3.1 | 2× adoption → waiting | Card | Fields | `[Wait Change vs Baseline (%)]` + visual filter `DimScenario[ShortLabel]` = "Adoption ×2" | Verified **+6,981%**. Format `+#,0%` |
| 3.2 | ToU pricing → revenue | Card | Fields | `[Revenue Change vs Baseline (%)]` + filter = "ToU pricing" | Verified **+37.9%** |
| 3.3 | Carbon incentive | Card | Fields | `[Revenue Change vs Baseline (%)]` + filter = "Carbon incentive" | Verified **−0.7%**; subtitle "not significant (p = 0.19)" matches `[Significance Indicator]` = "not significant" (verified) |
| 3.4 | Combined policy | Card | Fields | `[Revenue Change vs Baseline (%)]` + filter = "Combined" | Verified **+38.0%** |
| 3.5 | Revenue vs baseline | Horizontal bar chart | Y-axis | `DimScenario[ShortLabel]` + visual filter ShortLabel ≠ "Baseline" | Verified +47.8 / +99.6 / +37.9 / −0.7 / +38.0%. Sort by `SortOrder`. Adoption ×2 highlighted amber per wireframe |
|  |  |  | X-axis | `[Revenue Change vs Baseline (%)]` |  |
| 3.6 | Sessions vs baseline | Horizontal bar chart | Y-axis / X-axis | `DimScenario[ShortLabel]` / `[Sessions Change vs Baseline (%)]` | Verified +49.1 / +100.0 / 0.0 / −0.0 / 0.0%. Axis **not truncated** (H4) |
| 3.7 | Waiting vs baseline | Horizontal bar chart | Y-axis / X-axis | `DimScenario[ShortLabel]` / `[Wait Change vs Baseline (%)]` | Verified +1,799 / +6,981 / +3.0 / +21.9 / +34.5%. Title notes the scale |
| 3.8 | Significance matrix | Matrix | Rows | `DimScenario[ShortLabel]` |  |
|  |  |  | Columns | `FactScenarioSignificance[kpi]` | `kpi` lives **on the fact** (no DimKpi was built - client-accepted deviation from spec §4). 6 KPI values; wireframe shows 4 columns - filter `kpi` to revenue_gbp, sessions_completed, avg_wait_hrs, co2_g if you want the exact wireframe subset |
|  |  |  | Values | `[Significance Indicator]` | Verified - returns "significant" / "not significant" / **"undefined - all paired differences zero"** exactly where §8 predicts (ToU & Combined on sessions_completed). H7 satisfied; never blank |
| 3.9 | Reading | Text box | - | - | Narrative from wireframe |

Interactions: disable cross-filtering from bars 3.5–3.7 onto the KPI cards (pre-filtered). Bars ↔ matrix cross-highlight on scenario is useful - keep.

------------------------------------------------------------------------

## Page 4 - Learned Pricing Beats the Clock (Policy comparison)

**Slicers:** none (headline page is fixed to the 500-episode eval; elasticity is fixed at 0.8 by construction).

⚠ **Never mix FactSweep and FactEvalSummary/FactEvalEpisode on one visual** (spec §4). Visual 4.7 is the only FactSweep visual here and must stay separate.

| \# | Visual | Type | Well | Field | Notes |
|----|----|----|----|----|----|
| 4.1 | PPO objective score | Card | Fields | `[Mean Score]` + visual filter `DimPolicy[PolicyName]` = "PPO" | Verified **383.1** |
| 4.2 | Advantage vs ToU 2-band | Card | Fields | `[PPO Advantage vs ToU (%)]` | Verified **+20.2%**; `[PPO Advantage vs ToU]` (+64.3) as reference label |
| 4.3 | Revenue advantage | Card | Fields | `[PPO Revenue Advantage vs ToU (%)]` | Verified **+23.8%** (£400.9 vs £323.9) |
| 4.4 | The honest cost | Card | Fields | `[Mean Wait (min)]` + filter PolicyName = "PPO" | Verified **9.4 min** vs ToU 2.9 (H1). Amber/warn styling |
| 4.5 | Objective score by policy | Horizontal bar chart | Y-axis | `DimPolicy[PolicyName]` | Verified: PPO 383.1, Flat 341.7, ToU 2-band 318.8 - only these 3 policies return rows (headline eval scope, client-accepted). Sort **descending by value** |
|  |  |  | X-axis | `[Mean Score]` | Data colours from DimPolicy. Subtitle: "revenue − λ·waiting (R1) · 500 episodes" |
| 4.6 | Revenue per episode | Horizontal bar chart | Y-axis / X-axis | `DimPolicy[PolicyName]` / `[Mean Revenue (£)]` | Verified £400.9 / £386.9 / £323.9. Sorted |
| 4.7 | Cross-check: five policies | Horizontal bar chart | Y-axis | `DimPolicy[PolicyName]` | **FactSweep visual** - visual filter `DimElasticity[Elasticity]` = 0.8 |
|  |  |  | X-axis | `[Sweep Mean Score]` | Verified: PPO 395.2, Congestion 378.3, ToU 3-band 341.6, Flat 338.3, ToU 2-band 318.1. Subtitle must say "separate 30-episode sweep - not comparable with headline bars". Congestion grey (oracle) |
| 4.8 | Mean waiting time | Horizontal bar chart | Y-axis / X-axis | `DimPolicy[PolicyName]` / `[Mean Wait (min)]` | Verified Flat 19.8, PPO 9.4, ToU 2.9. Minutes only - `wait_steps` never shown (R5) |
| 4.9 | CO₂ per episode | Horizontal bar chart | Y-axis / X-axis | `DimPolicy[PolicyName]` / `[Mean CO2 (kg)]` | Verified Flat 77.4, PPO 64.2, ToU 53.9 (H1 - PPO's higher CO₂ visible) |
| 4.10 | How to read this page | Text box | - | - | Includes the ToU-below-Flat point (H2) and the not-comparable caveat |

Interactions: **disable all cross-filtering between 4.7 and every other visual** - a policy click on the cross-check would filter the headline bars via DimPolicy and visually merge the two runs. Cards are pre-filtered; exclude them from interactions too.

Unused-but-built option: `[Selected Policy Score]` / `[Best Baseline Score]` exist for the spec's dynamic advantage card (needs a DimPolicy slicer). Not on the validated wireframe - add only as a client change request.

------------------------------------------------------------------------

## Page 5 - Robustness and the Boundary

**Slicers:** `DimElasticity[Elasticity]` (dropdown, default **0.8** per R3 - set as the saved filter state). Slicer drives the four cards; the two charts show all elasticities (edit interactions: slicer → charts **off**).

| \# | Visual | Type | Well | Field | Notes |
|----|----|----|----|----|----|
| 5.1 | Regime at selection | Card | Fields | `[Regime Label (Selected)]` | Verified: "Trade-off" at 0.7–1.0; "Degenerate - pricing collapses to maximum tariff" at 0.5/0.6 (R9) |
| 5.2 | Seed spread (PPO) | Card | Fields | `[Sweep Score Std (Seeds)]` + visual filter `DimPolicy[PolicyName]` = "PPO" | Verified **±2.61** at 0.8; blank in degenerate regime (correct - no agent trained) |
| 5.3 | Margin vs ToU 2-band | Card | Fields | `[PPO Margin vs ToU 2-band]` | Verified **+77.1** at 0.8; blank at 0.5/0.6 |
| 5.4 | Margin vs ToU 3-band | Card | Fields | `[PPO Margin vs ToU 3-band]` | Verified **+53.6** at 0.8 |
| 5.5 | Score by elasticity × policy | Line chart | X-axis | `DimElasticity[Elasticity]` | **Continuous** axis 0.5–1.0. FactSweep only has rows at 0.7–1.0 - the degenerate zone plots nothing, which is exactly R9. Grey zone shading: rectangle shape over 0.5–0.65 with the "Degenerate" label (no native band shading) |
|  |  |  | Legend | `DimPolicy[PolicyName]` | 5 series (cardinality 5 - fine). Colours per DimPolicy |
|  |  |  | Y-axis | `[Sweep Mean Score]` | Verified all 20 policy × elasticity points (e.g. PPO 432.3 / 395.2 / 367.1 / 355.5) |
|  |  |  | Error bars | `[Sweep Score Band Upper]` / `[Sweep Score Band Lower]` | Analytics ▸ Error bars ▸ By field: upper/lower. Verified (PPO 0.8: 397.8 / 392.6); baselines have zero-width bands (deterministic - correct). Amber band rendering applies to PPO (H3) |
| 5.6 | Margins by elasticity | Clustered column chart | X-axis | `DimElasticity[Elasticity]` | Categorical (four values with data) |
|  |  |  | Y-axis | `[PPO Margin vs ToU 2-band]`, `[PPO Margin vs ToU 3-band]` | Verified 91/58 · 77/54 · 70/56 · 80/73. Amber / `#3E6285` per wireframe legend |

Interactions: slicer → cards **on**, slicer → 5.5/5.6 **off** (charts always show the full range so the boundary stays visible, H4). Chart-to-chart cross-filtering off.

------------------------------------------------------------------------

## Page 6 - How the Policy Prices (Behaviour)

**Slicers:** none.

| \# | Visual | Type | Well | Field | Notes |
|----|----|----|----|----|----|
| 6.1 | Overnight £0.30–0.31 | Card | - | **MISSING** | Needs a min–max-over-window measure (see MISSING table). Interim: text box |
| 6.2 | Peak ramp → £0.435 | Card | - | **MISSING** | Needs `PPO Peak Price` (MAXX over hours). Interim: text box |
| 6.3 | Afternoon release £0.150 | Card | - | **MISSING** | Needs `PPO Floor Price` (MINX over hours). Interim: text box |
| 6.4 | The tell - £0.353 at 08:00 | Card | Fields | `[PPO Mean Price (£/kWh)]` + visual filter `DimHour[Hour]` = 8 | Verified **£0.353** |
| 6.5 | Price by hour vs ToU clock | Line chart | X-axis | `DimHour[Hour]` | **Continuous** axis 0–23 |
|  |  |  | Y-axis | `[PPO Mean Price (£/kWh)]`, `[ToU Reference Price (£/kWh)]` | Verified all 24 hours: PPO overnight \~£0.30–0.31, ramp to peak, floor £0.15 from mid-afternoon; ToU steps 0.15/0.45 on `IsToUPeak`. PPO amber solid + markers; ToU navy **stepped** dashed (line style "stepped" on that series). Y-axis from £0.00 (H4). "Shaded where the clock overcharges" fill: no native between-series shading - use a shape/annotation or drop the fill; note the H8 Simulated label |
| 6.6 | Why this beats a clock | Text box | - | - | Narrative; keep the H5 "not claimed optimal" line in the footer |

Interactions: card 6.4 excluded from chart cross-filtering.

------------------------------------------------------------------------

## Time Intelligence

**Not applicable to this model - nothing to wire up.** The model contains **no calculation group and no date dimension**: it is a results dashboard over simulation outputs (policy / scenario / elasticity / hour grains), and its only timestamp (`FactSession[session_start]`) feeds derived hour and day-type dimensions, not a time series. The usual guidance (bind a Time Intelligence calculation group to a slicer instead of building N×M explicit measures) has no target here, and no wireframe visual asks for YTD/MoM-style variants. If a future change request adds trend-over-time views of the observed sessions, build a DimDate plus calculation group via `/bi-accelerator:03_model-build` first.

## MISSING - visuals with no measure behind them → `/bi-accelerator:04_dax-write`

| Page | Visual | What's needed | Suggested measure(s) |
|----|----|----|----|
| 6 | 6.1 Overnight tile | Min–max of `[PPO Mean Price (£/kWh)]` over hours 0–6, rendered "£0.30–0.31" | `PPO Overnight Price Range` (text: MINX & MAXX over `DimHour[Hour]` ≤ 6, formatted) |
| 6 | 6.2 Peak ramp tile | Daily maximum learned price (£0.435) | `PPO Peak Price (£/kWh)` = MAXX over DimHour of `[PPO Mean Price (£/kWh)]` |
| 6 | 6.3 Afternoon release tile | Daily minimum learned price (£0.150) | `PPO Floor Price (£/kWh)` = MINX over DimHour |
| 2 | 2.1 Overall status (optional) | Text status "CALIBRATED"/"NOT CALIBRATED" from `[Max KS Statistic]` vs threshold | `Calibration Status` - only if the word itself must be data-driven; a static title over the Verified `[Max KS Statistic]` card is acceptable |

All four are cosmetic-tier measures; nothing structural is missing. Until they exist, render 6.1–6.3 as text boxes so no unverified number ships (H6).

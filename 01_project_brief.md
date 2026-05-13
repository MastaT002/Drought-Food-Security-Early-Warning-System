# Project Brief: Drought & Food Security Early Warning System

**Date:** May 2026  
**Analyst:** Trevor Muinde (MastaT)
**Status:** Draft / In Development

---

## 1. Problem Statement

Kenya's Arid and Semi-Arid Lands (ASALs) are experiencing an escalating food security crisis. Following poor short rains in late 2025, approximately **3.7 million people** (over 20% of the analyzed ASAL population) are projected to face IPC Phase 3 "Crisis" level food insecurity between April and June 2026 — a 32% year-on-year increase. Counties such as Wajir, Mandera, and Tana River report 40–60% of their populations in severe acute food insecurity.

Humanitarian agencies and government bodies (NDMA, WFP, Kenya Red Cross) currently operate on **reactive** response models — deploying food aid and cash transfers after IPC reports confirm crisis conditions. There is no publicly available, county-level forecasting tool that predicts food insecurity severity **1–3 months in advance**, enabling pre-positioning of aid before conditions deteriorate.

## 2. Objective

Build a machine learning model that forecasts **IPC food insecurity phase** (Phase 1–5) for Kenya's ASAL counties **30–90 days in advance**, using publicly available climate, vegetation, and market data.

## 3. Success Criteria

| # | Criterion | Target | Measurement |
|---|---|---|---|
| 1 | **Crisis Detection Accuracy** | >70% precision/recall for Phase 3+ | Confusion matrix on holdout test set |
| 2 | **Interpretability** | Stakeholders can identify top 3 drivers per county | SHAP values / feature importance report |
| 3 | **Actionable Output** | Non-technical users can consume forecasts | Interactive risk map + summary table (not raw CSV) |
| 4 | **Reproducibility** | Another analyst can rerun the pipeline | Documented code, pinned dependencies, data dictionary |

## 4. Scope Boundaries

**In Scope:**
- 23 ASAL counties (not all 47 Kenyan counties)
- Forecast horizon: 1–3 months (30–90 days)
- Target variable: IPC Acute Food Insecurity Phase (1–5 scale)
- Predictor categories: rainfall, vegetation health, cereal prices, livestock conditions
- Data sources: Public / open-access only

**Out of Scope:**
- Conflict-driven displacement (Somalia border, pastoral clashes) — data is sparse and politically sensitive
- Long-term climate projections (>6 months)
- Individual household-level predictions (county-level aggregation only)
- Real-time satellite imagery processing (use pre-computed NDVI/rainfall indices)

## 5. Stakeholders

| Stakeholder | Role | How They Use This |
|---|---|---|
| **NDMA** (National Drought Management Authority) | Government coordination | County-level resource allocation and early response activation |
| **WFP Kenya** | Humanitarian food assistance | Pre-positioning food stocks and cash transfer programs |
| **Kenya Red Cross** | Emergency response | Triggering rapid response protocols before peak crisis |
| **County Drought Management Officers** | Local implementation | Justifying budget requests and mobilizing community resources |

## 6. Assumptions & Risks

### Assumptions
- Historical IPC phase classifications are accurate and consistently applied across counties
- CHIRPS rainfall data and MODIS NDVI are reliable proxies for local agricultural conditions
- Market price data from FAO FPMA reflects actual transaction prices in ASAL wholesale markets

### Risks
- **Data sparsity:** Some ASAL counties have limited historical IPC reporting (3–5 years vs. 10+ ideal)
- **Measurement error:** Satellite rainfall estimates have 10–15% error in arid regions with sparse ground stations
- **Confounding variables:** Food insecurity driven by conflict or market shocks (e.g., Middle East fertilizer disruption) may not be captured by climate/vegetation data alone
- **Model drift:** Climate patterns are shifting; a model trained on 2015–2023 data may degrade in accuracy for 2026–2027 forecasts

## 7. Deliverables

1. `01_project_brief.md` — This document
2. `02_data_inventory.md` — Catalog of all data sources with quality assessment
3. `03_notebooks/01_eda.ipynb` — Exploratory data analysis
4. `03_notebooks/02_feature_engineering.ipynb` — Predictor construction
5. `03_notebooks/03_modeling.ipynb` — Model training, validation, and evaluation
6. `04_dashboard/` — Interactive risk map and forecast table
7. `data_dictionary.csv` — Column-level documentation for all datasets

## 8. Timeline (Estimated)

| Phase | Duration | Target Completion |
|---|---|---|
| Data Discovery & Inventory | 3–5 days | Week 1 |
| Data Cleaning & EDA | 5–7 days | Week 2 |
| Feature Engineering | 3–4 days | Week 3 |
| Modeling & Validation | 5–7 days | Week 3–4 |
| Dashboard & Documentation | 3–4 days | Week 4 |
| Portfolio Write-up (LinkedIn) | 1 day | Week 4 |

---

*This brief will be updated as the project evolves. Last updated: May 2026.*

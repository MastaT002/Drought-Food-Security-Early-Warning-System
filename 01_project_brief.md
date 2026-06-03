# Project Brief: Drought & Food Security Early Warning System

**Date:** May 2026

**Last Update:** June 2026

**Analyst:** Trevor Mulundi (MastaT)

**Status:** Baseline and Food Price Enhanced Models Completed / Risk Dashboard Deployed

**Live dashboard:** [Kenya Drought & Food Security Risk Dashboard](https://drought-food-security-early-warning-system-kenya.streamlit.app/)

---

## 1. Problem Statement

Kenya's Arid and Semi-Arid Lands (ASALs) are highly vulnerable to drought, rainfall variability, vegetation stress, and food insecurity.

During severe drought periods, many ASAL counties experience high levels of IPC Phase 3 "Crisis" food insecurity or worse. Counties such as Turkana, Mandera, Marsabit, Wajir, Garissa, Isiolo, Samburu, Tana River, Baringo, and Kwale repeatedly appear as high-risk areas in the current analysis.

Humanitarian agencies and government bodies often respond after food insecurity conditions have already been confirmed through official reports. This creates a need for earlier warning systems that can help identify counties at risk before conditions worsen.

This project explores whether publicly available environmental indicators and market indicators, especially rainfall, vegetation health, and staple food prices, can help identify high-risk food insecurity cases at county level.

---

## 2. Objective

Build an interpretable machine learning early-warning model that classifies whether a Kenya ASAL county-period is at high risk of serious food insecurity.

In the current baseline model, a county-period is classified as **high risk** if:

```text
20% or more of the county population is in IPC Phase 3 or worse
```

The project uses publicly available food security, climate, vegetation, and market price data, including:

* IPC food insecurity outcomes
* CHIRPS rainfall data
* MODIS NDVI vegetation health data
* WFP Kenya food price data

The current models focus on **high-risk classification**, not exact IPC Phase 1–5 prediction. Predicting exact IPC phase can be explored in a later version of the project.

---

## 3. Success Criteria

| # | Criterion                    | Target                                                           | Current Status                                                           |
| - | ---------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------ |
| 1 | **High-Risk Classification** | Build a model that predicts whether a county-period is high risk | ✅ Completed                                                              |
| 2 | **Crisis Detection Recall**  | Identify most true high-risk cases                               | ✅ XGBoost detected 14 out of 16 high-risk test cases                     |
| 3 | **Model Comparison**         | Compare multiple baseline models                                 | ✅ Naive Baseline, Logistic Regression, Random Forest, and XGBoost tested |
| 4 | **Interpretability**         | Identify important predictors                                    | ✅ XGBoost feature importance created                                     |
| 5 | **Actionable Output** | Produce a county-level risk table/map | ✅ Completed — risk table and Streamlit dashboard created |                                                    |
| 6 | **Feature Group Comparison** | Compare rainfall-only, NDVI-only, and combined rainfall + NDVI models | ✅ Completed — combined rainfall + NDVI model performed best |
| 7 | **Reproducibility**          | Documented notebooks and processed datasets                      | ✅ In progress                                                            |
| 8 | **Food Price Feature Engineering** | Add food price indicators as market-pressure predictors | ✅ Completed — maize, beans, and rice features created |
| 9 | **Enhanced Model Comparison** | Compare model performance before and after food price features | ✅ Completed — XGBoost improved overall after food prices |
| 10 | **Dashboard-Ready Food Price Predictions** | Create prediction table for enhanced model dashboard view | ✅ Completed |
---

## 4. Scope Boundaries

### In Scope

* Kenya ASAL counties
* County-level food insecurity analysis
* Target variable: high-risk classification based on Phase 3+ population percentage
* Current high-risk threshold: `phase_3_plus_percentage >= 0.20`
* Predictor categories currently included:

  * Rainfall indicators
  * NDVI vegetation indicators
  * Food price indicators
* Public and open-access data sources
* Baseline machine learning model comparison
* Interpretable model outputs such as feature importance and confusion matrix

### Out of Scope for Current Version

* Exact IPC Phase 1–5 forecasting
* Household-level food insecurity prediction
* Real-time production deployment
* Conflict-driven displacement modeling
* Long-term climate projections beyond the food security early-warning window
* Full humanitarian decision automation
* Full market-system modeling beyond staple food price indicators

---

## 5. Stakeholders

| Stakeholder                            | Role                            | How They Could Use This                                               |
| -------------------------------------- | ------------------------------- | --------------------------------------------------------------------- |
| **NDMA**                               | Government drought coordination | County-level drought and food security risk monitoring                |
| **WFP Kenya**                          | Humanitarian food assistance    | Pre-positioning food support and cash transfer planning               |
| **Kenya Red Cross**                    | Emergency response              | Earlier identification of counties requiring closer monitoring        |
| **County Drought Management Officers** | Local implementation            | Supporting evidence-based county risk reporting                       |
| **Data Analysts / Researchers**        | Analysis and modeling           | Reproducing the workflow and improving the model with additional data |

---

## 6. Data Sources

| Dataset                   | Source                                 | Current Use                                 |
| ------------------------- | -------------------------------------- | ------------------------------------------- |
| IPC Acute Food Insecurity | FEWS NET / HDX                         | Food insecurity outcome and Phase 3+ burden |
| CHIRPS Rainfall           | UCSB Climate Hazards Center            | Rainfall indicators and rolling averages    |
| MODIS NDVI                | NASA/USGS via Google Earth Engine      | Vegetation health indicators and anomalies  |
| Kenya County Boundaries   | Public administrative boundaries / HDX | County-level spatial aggregation            |
| WFP Kenya Food Prices | HDX / WFP food price data | Staple food price indicators for maize, beans, and rice |

---

## 7. Assumptions & Risks

### Assumptions

* IPC food insecurity records are sufficiently reliable for county-level analysis.
* CHIRPS rainfall data is a useful proxy for rainfall conditions in ASAL counties.
* MODIS NDVI is a useful proxy for vegetation health and land response.
* Rainfall and NDVI indicators contain useful early-warning signals for food insecurity risk.
* A 20% Phase 3+ population threshold is a reasonable starting point for defining widespread food insecurity risk.
* WFP food price data provides useful market-pressure signals for food insecurity risk.
* National staple food price averages can be used as proxy indicators where county-level price data is missing.

### Risks

* **Small dataset size:** The current modeling dataset has limited records, so model results should be validated further.
* **Class imbalance:** High-risk cases are fewer than non-high-risk cases, so recall, precision, F1-score, and ROC-AUC are more useful than accuracy alone.
* **Confounding variables:** Food insecurity may also be influenced by food prices, livestock conditions, conflict, income, market access, disease outbreaks, and humanitarian support.
* **Satellite data limitations:** Rainfall and NDVI estimates may not fully capture local ground conditions.
* **Model drift:** Environmental and socioeconomic patterns may change over time, reducing future model performance.
* **Correlation vs causation:** The analysis shows predictive signals and associations, not proof that rainfall or NDVI alone cause food insecurity.
* **Incomplete county-level food price coverage:** Some target counties and periods do not have direct county-level food price records, so national proxy prices are used where needed.

---

## 8. Baseline Modeling Summary

A baseline machine learning notebook was completed using the final master dataset.

The model target was:

```text
high_risk = 1 if phase_3_plus_percentage >= 0.20
high_risk = 0 otherwise
```

A time-aware train-test split was used. Earlier records were used for training, while later records were used for testing.

### Models Compared

* Naive Baseline
* Logistic Regression
* Standardized Logistic Regression
* Random Forest Classifier
* XGBoost Classifier

### Model Results

| Model                            | Accuracy | Precision | Recall | F1-score | ROC-AUC |
| -------------------------------- | -------: | --------: | -----: | -------: | ------: |
| Naive Baseline                   |   0.7538 |    0.0000 | 0.0000 |   0.0000 |  0.5000 |
| Logistic Regression              |   0.7692 |    0.5172 | 0.9375 |   0.6667 |  0.9171 |
| Standardized Logistic Regression |   0.7692 |    0.5172 | 0.9375 |   0.6667 |  0.9298 |
| Random Forest                    |   0.8769 |    0.7222 | 0.8125 |   0.7647 |  0.9286 |
| XGBoost                          |   0.8769 |    0.7000 | 0.8750 |   0.7778 |  0.9362 |

### Selected Baseline Model

XGBoost was selected as the strongest balanced baseline model.

It achieved:

* Strong recall
* Highest F1-score
* Highest ROC-AUC
* Better balance between catching high-risk cases and reducing false alarms

The XGBoost confusion matrix showed:

* 43 correctly predicted non-high-risk cases
* 14 correctly predicted high-risk cases
* 6 false alarms
* 2 missed high-risk cases

This means the model correctly identified **14 out of 16 high-risk cases** in the test set.

### Important Predictors

XGBoost feature importance showed that longer-term vegetation and rainfall indicators were most useful.

Top features included:

* `ndvi_6_month_mean`
* `rainfall_6_month_total`
* `ndvi_3_month_mean`
* `rainfall_6_month_avg`

This suggests that medium-term vegetation health and rainfall conditions contain useful signals for food insecurity risk classification.

### Feature Group Comparison

A separate feature group comparison was completed to test whether rainfall-only, NDVI-only, or combined rainfall + NDVI features provide the strongest prediction performance.

The comparison showed that:

* Rainfall-only features provided useful signal but had the weakest performance.
* NDVI-only features performed much better than rainfall-only features.
* The combined rainfall + NDVI model produced the strongest overall performance.

The main takeaway is that NDVI vegetation indicators are stronger than rainfall indicators alone, but combining rainfall and NDVI gives the best early-warning performance.
---

## 9. Food Price Enhanced Modeling Summary

After the baseline rainfall + NDVI model was completed, WFP Kenya food price data was added as an additional market-pressure indicator.

The first food price feature version focused on three staple food groups:

* maize
* beans
* rice

These were selected because they had the strongest coverage compared with other commodities.

Because county-level food price coverage was incomplete, a hybrid feature strategy was used:

* county-level staple food prices where available
* national staple food price proxy where county-level prices were missing

This allowed every county-period record to receive a food price indicator.

### Enhanced Model Results

The models were tested again using rainfall, NDVI, and food price features.

| Model                             | Accuracy | Precision | Recall | F1-score |
| --------------------------------- | -------: | --------: | -----: | -------: |
| Logistic Regression + Food Prices |   0.7846 |    0.5357 | 0.9375 |   0.6818 |
| Random Forest + Food Prices       |   0.8462 |    0.6500 | 0.8125 |   0.7222 |
| XGBoost + Food Prices             |   0.8923 |    0.7647 | 0.8125 |   0.7879 |

### Enhanced Model Insight

XGBoost with rainfall, NDVI, and food price features achieved the strongest overall result.

Compared with the baseline XGBoost model, the enhanced XGBoost model improved accuracy, F1-score, and high-risk precision. However, recall decreased slightly, meaning the model produced fewer false alarms but missed slightly more high-risk cases.

Feature importance showed that NDVI and rainfall remained the strongest predictors, but the 6-month staple food price average also contributed useful predictive signal.
---
## 10. Deliverables

| Deliverable                                            | Description                                    | Status               |
| ------------------------------------------------------ | ---------------------------------------------- | -------------------- |
| `01_project_brief.md`                                  | Project scope, objective, and progress summary | ✅ Updated            |
| `02_data_inventory.md`                                 | Data source inventory and quality notes        | ✅ Created            |
| `data_dictionary.csv`                                  | Column-level documentation                     | ✅ Created / Updating |
| `03_notebooks/01_ipc_data_cleaning.ipynb`              | IPC data cleaning                              | ✅ Completed          |
| `03_notebooks/02_ipc_eda.ipynb`                        | Initial IPC exploratory analysis               | ✅ Completed          |
| `03_notebooks/03_county_boundaries_check.ipynb`        | County boundary validation                     | ✅ Completed          |
| `03_notebooks/03_rainfall_data_collection.ipynb`       | Rainfall data collection and processing        | ✅ Completed          |
| `03_notebooks/04_ipc_rainfall_merge.ipynb`             | IPC and rainfall merge                         | ✅ Completed          |
| `03_notebooks/05_ipc_rainfall_analysis.ipynb`          | Rainfall and IPC analysis                      | ✅ Completed          |
| `03_notebooks/06_ndvi_data_collection_modis_gee.ipynb` | NDVI extraction using Google Earth Engine      | ✅ Completed          |
| `03_notebooks/07_ipc_rainfall_ndvi_merge.ipynb`        | IPC + rainfall + NDVI merge                    | ✅ Completed          |
| `03_notebooks/08_master_dataset_eda.ipynb`             | Master dataset EDA                             | ✅ Completed          |
| `03_notebooks/09_baseline_model.ipynb`                 | Baseline machine learning model                | ✅ Completed          |
| `03_notebooks/10_model_prediction_risk_table.ipynb`    | County-level prediction risk table             | ✅ Completed          |
| `03_notebooks/11_feature_group_model_comparison.ipynb` | Rainfall-only vs NDVI-only vs combined model comparison | ✅ Completed |
| `03_notebooks/12_food_price_data_collection.ipynb` | Food price data collection, cleaning, and feature creation | ✅ Completed |
| `03_notebooks/13_food_price_merge_with_master_dataset.ipynb` | Food price merge with master dataset | ✅ Completed |
| `03_notebooks/14_model_with_food_price_features.ipynb` | Enhanced model with food price features | ✅ Completed |
| `03_notebooks/15_food_price_model_predictions.ipynb` | Dashboard-ready food price prediction table | ✅ Completed |
| `04_dashboard/`                                        | Streamlit risk dashboard and county-level map  | ✅ Created / Deployed |

---

## 10. Current Project Status

✅ Project brief completed
✅ IPC data cleaned and explored
✅ CHIRPS rainfall features created
✅ MODIS NDVI features created
✅ IPC + rainfall + NDVI master dataset created
✅ Master dataset EDA completed
✅ Correlation analysis completed
✅ High-risk classification target created
✅ Time-aware train-test split completed
✅ Baseline models trained and evaluated
✅ XGBoost selected as strongest balanced baseline model  
✅ Model prediction risk table created  
✅ Streamlit risk dashboard prototype created  
✅ County-level risk map created  
✅ Dashboard deployed publicly using Streamlit Community Cloud  
✅ Rainfall-only, NDVI-only, and combined rainfall + NDVI models compared  
✅ Feature group model comparison completed  
✅ WFP Kenya food price data collected
✅ Food price data cleaned and inspected
✅ Staple food groups selected: maize, beans, and rice
✅ County-level and national-level food price features created
✅ Food price features merged with IPC + rainfall + NDVI master dataset
✅ Enhanced food price model trained and evaluated
✅ Baseline vs enhanced model comparison completed
✅ Food price model dashboard prediction table created

**Current stage:** Baseline model completed, food price enhanced model tested, dashboard-ready prediction tables created, and Streamlit dashboard update in progress.

**Next stage:** Update and deploy the Streamlit dashboard to compare baseline vs enhanced model predictions, then improve validation across future IPC periods.
---

## 11. Next Research Direction

Future improvements can include:

1. Improving the Streamlit dashboard design, filters, map styling, and stakeholder explanations.
2. Expanding the dashboard to include full historical risk periods and future prediction outputs.
3. Improving food price feature coverage and testing additional commodities.
4. Adding livestock and market access indicators.
5. Testing longer rainfall, NDVI, and food price lag features.
6. Tuning XGBoost and Random Forest parameters.
7. Testing model performance on future IPC periods.
8. Exploring exact IPC phase prediction as a later modeling task.

---

## 12. Timeline Status

| Phase                        | Status      |
| ---------------------------- | ----------- |
| Data Discovery & Inventory   | ✅ Completed |
| IPC Cleaning & EDA           | ✅ Completed |
| Rainfall Feature Engineering | ✅ Completed |
| NDVI Feature Engineering     | ✅ Completed |
| Master Dataset EDA           | ✅ Completed |
| Baseline Modeling            | ✅ Completed |
| Dashboard / Risk Map         | ✅ Prototype deployed |
| Feature Group Comparison     | ✅ Completed |
| Food Price Predictors        | ✅ Completed |
| Additional Predictors        | ⬜ Planned — livestock, conflict, market access |

---

*This brief will be updated as the project evolves. Last updated: May 2026.*

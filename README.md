# **Drought & Food Security Early Warning System**

A data analytics and machine learning portfolio project focused on building an early-warning system for food insecurity risk across Kenya's Arid and Semi-Arid Lands (ASAL).

**Data sources:** IPC food insecurity outcomes, CHIRPS rainfall data, MODIS NDVI vegetation indicators, and WFP Kenya food price data.

**Current stage:** Baseline model completed, food price features added, enhanced model tested, and Streamlit dashboard being updated to compare baseline vs food price model predictions.

**Latest enhanced model result:** XGBoost with rainfall, NDVI, and food price features achieved the strongest overall performance after adding market indicators.

**Dashboard output:** County-level prediction risk tables and an interactive map dashboard were created for the baseline XGBoost model and the enhanced food price XGBoost model.

**Live dashboard:** [Kenya Drought & Food Security Risk Dashboard](https://drought-food-security-early-warning-system-kenya.streamlit.app/)

**Next stage:** Improve the dashboard comparison view, test longer time-lag features, tune the enhanced model, and improve validation across future IPC periods.

---

## The Problem

* **3.7 million Kenyans** are projected to face IPC Phase 3 "Crisis" level food insecurity between April–June 2026
* **23 ASAL counties** are particularly vulnerable to drought-driven food crises
* Humanitarian agencies often react to crises **after** they peak, not before
* There is limited publicly available county-level modeling that links food insecurity outcomes with rainfall and vegetation indicators for early-warning analysis

## Objective

Build an interpretable machine learning early-warning model that predicts high-risk food insecurity cases across Kenya ASAL counties using publicly available food security, climate, vegetation, and market price data.

In this project, a county-period is classified as **high risk** if **20% or more of the county population is in IPC Phase 3 or worse**.

The baseline model uses rainfall and NDVI indicators, while the enhanced model also includes staple food price indicators.

Both models classify county-periods as:

* `1` = High Risk
* `0` = Not High Risk

---

## Current Findings

The current analysis combines IPC food insecurity outcomes, CHIRPS rainfall indicators, MODIS NDVI vegetation indicators, and WFP Kenya food price indicators for Kenya ASAL counties.

Key findings from exploratory analysis:

* Counties such as Turkana, Mandera, Marsabit, Wajir, Garissa, Isiolo, Samburu, Tana River, Baringo, and Kwale repeatedly appear as high-risk counties.
* Turkana had the highest average Phase 3+ population percentage, meaning it had the largest average share of people facing crisis-level food insecurity or worse.
* Higher IPC severity is generally associated with lower rainfall and weaker vegetation health.
* NDVI indicators showed stronger negative relationships with Phase 3+ population percentage than rainfall indicators.
* The strongest environmental indicator was the 3-month NDVI mean, with a correlation of about `-0.692` against Phase 3+ population percentage.
* The 6-month rainfall average also showed a meaningful negative relationship with Phase 3+ population percentage, with a correlation of about `-0.585`.

These findings suggest that vegetation health and rainfall are useful environmental indicators for drought and food security early-warning analysis.

**Important note:** These results show association, not proof of causation. Food insecurity may also be influenced by market prices, livestock conditions, conflict, income, market access, humanitarian support, and other local factors.

---
### Food Price Feature Findings

Food price data was added as an additional market-pressure indicator using WFP Kenya food price records.

The first food price feature version focused on maize, beans, and rice because these staple groups had the strongest coverage.

Because county-level food price coverage was incomplete, a hybrid feature strategy was used:

- county-level staple food prices where available
- national staple food price proxy where county prices were missing

This allowed food price features to be included for all county-period records in the final modeling dataset.
---

## Baseline Modeling Results

A baseline classification model was built to predict whether a county-period is high risk.

A county-period was classified as high risk if **20% or more of the population was in IPC Phase 3 or worse**.

A time-aware train-test split was used. Earlier records were used for training, while later records were used for testing. This better reflects a real early-warning situation, where past data is used to predict future risk.

Models compared:

* Naive Baseline
* Logistic Regression
* Standardized Logistic Regression
* Random Forest Classifier
* XGBoost Classifier

### Model Comparison

| Model                            | Accuracy | Precision | Recall | F1-score | ROC-AUC |
| -------------------------------- | -------: | --------: | -----: | -------: | ------: |
| Naive Baseline                   |   0.7538 |    0.0000 | 0.0000 |   0.0000 |  0.5000 |
| Logistic Regression              |   0.7692 |    0.5172 | 0.9375 |   0.6667 |  0.9171 |
| Standardized Logistic Regression |   0.7692 |    0.5172 | 0.9375 |   0.6667 |  0.9298 |
| Random Forest                    |   0.8769 |    0.7222 | 0.8125 |   0.7647 |  0.9286 |
| XGBoost                          |   0.8769 |    0.7000 | 0.8750 |   0.7778 |  0.9362 |

### Key Modeling Insights

* The Naive Baseline achieved reasonable accuracy but failed to identify any high-risk cases. This shows why accuracy alone is misleading.
* Logistic Regression achieved the highest recall, meaning it was very good at catching true high-risk cases. However, it produced more false alarms.
* Random Forest improved precision and overall balance compared with Logistic Regression.
* XGBoost achieved the strongest balanced performance overall. It matched Random Forest on accuracy, improved recall, achieved the highest F1-score, and produced the highest ROC-AUC score.

### Selected Baseline Model

XGBoost was selected as the preferred balanced baseline model.

The XGBoost confusion matrix showed:

* 43 correctly predicted non-high-risk cases
* 14 correctly predicted high-risk cases
* 6 false alarms
* 2 missed high-risk cases

This means XGBoost correctly identified **14 out of 16 high-risk cases** in the test set while keeping false alarms lower than Logistic Regression.

### Feature Importance

XGBoost feature importance showed that longer-term vegetation and rainfall indicators were important for prediction.

The most important features were:

* `ndvi_6_month_mean`
* `rainfall_6_month_total`
* `ndvi_3_month_mean`
* `rainfall_6_month_avg`

These results suggest that medium-term vegetation health and rainfall patterns contain useful signals for identifying food insecurity risk.

### Feature Group Comparison

A separate feature group comparison was completed to test whether rainfall-only, NDVI-only, or combined rainfall + NDVI features produced the strongest model performance.

The comparison showed that:

* Rainfall-only features provided useful signal but had the weakest performance.
* NDVI-only features performed much better than rainfall-only features.
* The combined rainfall + NDVI model achieved the strongest overall performance.

The key takeaway is that NDVI vegetation indicators are stronger than rainfall indicators alone, but combining rainfall and NDVI gives the best early-warning performance.
---

## Food Price Enhanced Modeling Results

After the baseline model was completed, WFP Kenya food price data was added as an additional market-pressure indicator.

The food price feature version focused on three staple food groups:

* maize
* beans
* rice

These staples were selected because they had the strongest record counts, useful time coverage, and broad market coverage compared with other commodities.

Because county-level food price coverage was incomplete, a hybrid food price strategy was used:

* county-level staple food prices where available
* national staple food price proxy where county-level prices were missing

This allowed food price features to be included for all county-period records in the final modeling dataset.

### Enhanced Model Comparison

The models were tested again using rainfall, NDVI, and food price features.

| Model                             | Accuracy | Precision | Recall | F1-score |
| --------------------------------- | -------: | --------: | -----: | -------: |
| Logistic Regression + Food Prices |   0.7846 |    0.5357 | 0.9375 |   0.6818 |
| Random Forest + Food Prices       |   0.8462 |    0.6500 | 0.8125 |   0.7222 |
| XGBoost + Food Prices             |   0.8923 |    0.7647 | 0.8125 |   0.7879 |

### Food Price Model Insights

XGBoost with rainfall, NDVI, and food price features achieved the strongest overall result.

Compared with the baseline XGBoost model, the enhanced XGBoost model improved:

* accuracy
* F1-score
* high-risk precision

However, high-risk recall decreased slightly. This means the enhanced model produced fewer false alarms, but it missed slightly more high-risk cases than the baseline XGBoost model.

The final result shows that food price features added useful predictive signal, especially when used with XGBoost.

### Food Price Feature Importance

The XGBoost feature importance results showed that NDVI and rainfall remained the strongest predictors.

The most important features included:

* `ndvi_6_month_mean`
* `ndvi_3_month_mean`
* `rainfall_6_month_total`
* `rainfall_6_month_avg`
* `final_staple_price_per_kg_6_month_avg`

The appearance of `final_staple_price_per_kg_6_month_avg` among the top features shows that longer-term staple food price pressure contributed useful information to the model.

Overall, the enhanced model suggests that food insecurity risk is linked not only to rainfall and vegetation conditions, but also to market price pressure.

---

## Success Criteria

* [x] Build a baseline model to classify high-risk food insecurity cases
* [x] Evaluate performance using accuracy, precision, recall, F1-score, ROC-AUC, and confusion matrix
* [x] Compare baseline machine learning models
* [x] Identify important rainfall and NDVI predictors
* [x] Compare rainfall-only, NDVI-only, and combined rainfall + NDVI models
* [x] Output must be interpretable — stakeholders can see why a county is flagged
* [x] Deliver a simple risk map + table, not a raw CSV
* [x] Add food price indicators as an additional predictor
* [x] Create county-level and national-level food price features
* [x] Compare baseline model performance before and after food price features
* [x] Create dashboard-ready prediction table for the food price model

---

## Data Sources

| Dataset                   | Source                                       | Type                             | Current Status |
| ------------------------- | -------------------------------------------- | -------------------------------- | -------------- |
| IPC Acute Food Insecurity | FEWS NET / HDX                               | Food insecurity outcome data     | ✅ Added        |
| CHIRPS Rainfall           | UCSB Climate Hazards Center                  | Monthly rainfall / climate data  | ✅ Added        |
| MODIS NDVI Vegetation     | NASA/USGS MODIS via Google Earth Engine      | Satellite vegetation health data | ✅ Added        |
| Kenya County Boundaries   | HDX / administrative boundaries              | County shapefile / GeoJSON       | ✅ Added        |
| WFP Kenya Food Prices | HDX / WFP food price data | Market price data for staple foods | ✅ Added |

---

## Tech Stack

* **Python:** pandas, matplotlib, scikit-learn, XGBoost
* **Machine Learning:** Logistic Regression, Random Forest, XGBoost
* **Model Evaluation:** accuracy, precision, recall, F1-score, ROC-AUC, confusion matrix
* **Geospatial / Remote Sensing:** Google Earth Engine, MODIS NDVI, CHIRPS rainfall, GeoJSON county boundaries
* **Notebook Environment:** JupyterLab, Google Colab
* **Dashboard / Visualization:** Streamlit, Plotly, GeoJSON county boundaries, interactive risk map

---

## Project Structure

```text
Drought-Food-Security-Early-Warning-System/
├── 01_project_brief.md
├── 02_data/
│   ├── raw/
│   │   └── Original downloaded datasets
│   └── processed/
│       ├── ipc_max_phase_per_county.csv
│       ├── county_rainfall.csv
│       ├── county_rainfall_features.csv
│       ├── ipc_rainfall_modeling_dataset.csv
│       ├── Kenya_ASAL_NDVI_Clean_2019_2026.csv
│       ├── ipc_rainfall_ndvi_master_dataset.csv
│       ├── phase3_environment_correlation_summary.csv
│       ├── feature_group_model_comparison.csv
│       ├── model_prediction_risk_table.csv
│       ├── kenya_target_counties.geojson
│       ├── wfp_food_prices_ken.csv
│       ├── county_food_price_monthly_features.csv
│       ├── national_food_price_monthly_features.csv
│       ├── ipc_rainfall_ndvi_food_price_master_dataset.csv
│       ├── model_results_food_prices.csv
│       ├── food_price_model_improvement_comparison.csv
│       ├── xgboost_food_price_feature_importance.csv
│       └── model_prediction_risk_table_food_prices.csv
├── 03_notebooks/
│   ├── 01_ipc_data_cleaning.ipynb
│   ├── 02_ipc_eda.ipynb
│   ├── 03_county_boundaries_check.ipynb
│   ├── 03_rainfall_data_collection.ipynb
│   ├── 04_ipc_rainfall_merge.ipynb
│   ├── 05_ipc_rainfall_analysis.ipynb
│   ├── 06_ndvi_data_collection_modis_gee.ipynb
│   ├── 07_ipc_rainfall_ndvi_merge.ipynb
│   ├── 08_master_dataset_eda.ipynb
│   ├── 09_baseline_model.ipynb
│   ├── 10_model_prediction_risk_table.ipynb
│   ├── 11_feature_group_model_comparison.ipynb
│   ├── 12_food_price_data_collection.ipynb
│   ├── 13_food_price_merge_with_master_dataset.ipynb
│   ├── 14_model_with_food_price_features.ipynb
│   └── 15_food_price_model_predictions.ipynb
├── 04_dashboard/
│   ├── app.py
│   ├── README.md
│   └── requirements.txt
├── 02_data_inventory.md
├── data_dictionary.csv
├── README.md
└── LICENSE
```

---

## Project Status

* ✅ Project brief completed
* ✅ IPC raw dataset uploaded
* ✅ IPC data inventory documented
* ✅ IPC data cleaning completed
* ✅ Modeling-ready IPC dataset created
* ✅ Initial IPC EDA completed
* ✅ Kenya ASAL county boundary check completed
* ✅ CHIRPS rainfall data collected and processed
* ✅ IPC + rainfall dataset merged
* ✅ Initial rainfall and IPC relationship analysis completed
* ✅ MODIS NDVI data collected using Google Earth Engine
* ✅ NDVI rolling averages and anomaly features created
* ✅ IPC + rainfall + NDVI master dataset created
* ✅ Master dataset EDA completed
* ✅ Correlation analysis completed
* ✅ Baseline classification target created
* ✅ Time-aware train-test split completed
* ✅ Naive baseline tested
* ✅ Logistic Regression model trained and evaluated
* ✅ Standardized Logistic Regression model trained and evaluated
* ✅ Random Forest model trained and evaluated
* ✅ XGBoost model trained and evaluated
* ✅ Model comparison completed
* ✅ XGBoost selected as strongest balanced baseline model
* ✅ Model prediction risk table created
* ✅ Streamlit dashboard prototype created
* ✅ County-level risk map/dashboard prototype created
* ✅ Streamlit dashboard deployed publicly
* ✅ Rainfall-only, NDVI-only, and combined rainfall + NDVI models compared
* ✅ Feature group model comparison completed
* ✅ WFP Kenya food price data collected
* ✅ Food price data inspected and cleaned
* ✅ Staple food groups selected: maize, beans, and rice
* ✅ Food price unit standardization completed
* ✅ County-level and national-level food price features created
* ✅ Food price features merged with rainfall + NDVI master dataset
* ✅ Enhanced model with food price features trained and evaluated
* ✅ Baseline vs food price model comparison completed
* ✅ XGBoost food price feature importance reviewed
* ✅ Food price dashboard prediction table created

**Current stage:** Food price features added, enhanced model tested, dashboard-ready food price prediction table created, and Streamlit dashboard updated to compare baseline vs enhanced model predictions.

**Live dashboard:** [Kenya Drought & Food Security Risk Dashboard](https://drought-food-security-early-warning-system-kenya.streamlit.app/)

**Next stage:**

* ⬜ Improve Streamlit dashboard comparison between baseline and enhanced models
* ⬜ Tune XGBoost and Random Forest hyperparameters
* ⬜ Test longer rainfall, NDVI, and food price lag features
* ⬜ Improve validation across future IPC periods
* ⬜ Add livestock, conflict, market access, or humanitarian response indicators

---

## Limitations

This project is an early-stage portfolio model and should not be used as a production humanitarian decision system without further validation.

Current limitations include:

* The dataset is relatively small.
* The baseline model uses rainfall and NDVI indicators. The enhanced model also includes food price indicators.
* Food prices have been added, but conflict, livestock conditions, market access, and humanitarian response data are not yet included.
* The current target is based on a 20% Phase 3+ population threshold.
* Results show predictive signals, not proof of causation.
* County-level food price data is incomplete for some counties and periods, so national food price proxy values were used where county-level prices were missing.

---

## Next Research Direction

Future improvements can include:

1. Improve food price feature coverage and test more staple commodities.
2. Add livestock, conflict, market access, and humanitarian response indicators.
3. Tune XGBoost and Random Forest parameters.
4. Test the model on future IPC periods.
5. Improve Streamlit dashboard design, filters, map styling, and stakeholder explanations.

---

## License

This project is open-sourced under the [MIT License](LICENSE).

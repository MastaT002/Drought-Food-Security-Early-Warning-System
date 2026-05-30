# Drought & Food Security Early Warning System

A data analytics and machine learning portfolio project focused on building an early-warning system for food insecurity risk across Kenya's Arid and Semi-Arid Lands (ASAL).

**Data sources:** IPC food insecurity outcomes, CHIRPS rainfall data, and MODIS NDVI vegetation indicators.

**Current stage:** Baseline machine learning model completed and interactive Streamlit risk dashboard prototype created. 

**Latest model result:** XGBoost was selected as the strongest balanced baseline model based on recall, F1-score, and ROC-AUC. 

**Dashboard output:** A county-level prediction risk table and interactive map dashboard were created using the selected XGBoost model. 

**Next stage:** Improve the dashboard, compare rainfall-only vs NDVI-only vs combined models, and test additional predictors such as food prices, market indicators, and longer time-lag features.

---

## The Problem

* **3.7 million Kenyans** are projected to face IPC Phase 3 "Crisis" level food insecurity between April–June 2026
* **23 ASAL counties** are particularly vulnerable to drought-driven food crises
* Humanitarian agencies often react to crises **after** they peak, not before
* There is limited publicly available county-level modeling that links food insecurity outcomes with rainfall and vegetation indicators for early-warning analysis

## Objective

Build an interpretable machine learning early-warning model that predicts high-risk food insecurity cases across Kenya ASAL counties using publicly available environmental and food security data.

In this project, a county-period is classified as **high risk** if **20% or more of the county population is in IPC Phase 3 or worse**.

The current model uses rainfall and NDVI indicators to classify county-periods as:

* `1` = High Risk
* `0` = Not High Risk

---

## Current Findings

The current analysis combines IPC food insecurity outcomes, CHIRPS rainfall indicators, and MODIS NDVI vegetation indicators for Kenya ASAL counties.

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

---

## Success Criteria

* [x] Build a baseline model to classify high-risk food insecurity cases
* [x] Evaluate performance using accuracy, precision, recall, F1-score, ROC-AUC, and confusion matrix
* [x] Compare baseline machine learning models
* [x] Identify important rainfall and NDVI predictors
* [ ] Compare rainfall-only, NDVI-only, and combined rainfall + NDVI models
* [ ] Output must be interpretable — stakeholders can see why a county is flagged
* [ ] Deliver a simple risk map + table, not a raw CSV

---

## Data Sources

| Dataset                   | Source                                       | Type                             | Current Status |
| ------------------------- | -------------------------------------------- | -------------------------------- | -------------- |
| IPC Acute Food Insecurity | FEWS NET / HDX                               | Food insecurity outcome data     | ✅ Added        |
| CHIRPS Rainfall           | UCSB Climate Hazards Center                  | Monthly rainfall / climate data  | ✅ Added        |
| MODIS NDVI Vegetation     | NASA/USGS MODIS via Google Earth Engine      | Satellite vegetation health data | ✅ Added        |
| Kenya County Boundaries   | HDX / administrative boundaries              | County shapefile / GeoJSON       | ✅ Added        |
| Cereal Market Prices      | FAO FPMA or other public market price source | Time-series market data          | ⬜ Planned      |

---

## Tech Stack

* **Python:** pandas, matplotlib, scikit-learn, XGBoost
* **Machine Learning:** Logistic Regression, Random Forest, XGBoost
* **Model Evaluation:** accuracy, precision, recall, F1-score, ROC-AUC, confusion matrix
* **Geospatial / Remote Sensing:** Google Earth Engine, MODIS NDVI, CHIRPS rainfall, GeoJSON county boundaries
* **Notebook Environment:** JupyterLab, Google Colab
* **Planned Dashboard / Visualization:** Streamlit, Power BI, Plotly, or geospatial risk maps

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
│       ├── model_prediction_risk_table.csv
│       └── kenya_target_counties.geojson
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
│   └── 09_baseline_model.ipynb
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

✅ Project brief completed
✅ IPC raw dataset uploaded
✅ IPC data inventory documented
✅ IPC data cleaning completed
✅ Modeling-ready IPC dataset created
✅ Initial IPC EDA completed
✅ Kenya ASAL county boundary check completed
✅ CHIRPS rainfall data collected and processed
✅ IPC + rainfall dataset merged
✅ Initial rainfall and IPC relationship analysis completed
✅ MODIS NDVI data collected using Google Earth Engine
✅ NDVI rolling averages and anomaly features created
✅ IPC + rainfall + NDVI master dataset created
✅ Master dataset EDA completed
✅ Correlation analysis completed
✅ Baseline classification target created
✅ Time-aware train-test split completed
✅ Naive baseline tested
✅ Logistic Regression model trained and evaluated
✅ Standardized Logistic Regression model trained and evaluated
✅ Random Forest model trained and evaluated
✅ XGBoost model trained and evaluated
✅ Model comparison completed
✅ XGBoost selected as strongest balanced baseline model
✅ Model prediction risk table created 
✅ Streamlit dashboard prototype created 
✅ County-level risk map/dashboard prototype started

**Current stage:** Baseline model completed and dashboard prototype created.

**Next stage:**

✅ Create model prediction risk table 
✅ Build county-level risk map/dashboard prototype
⬜ Compare rainfall-only, NDVI-only, and combined rainfall + NDVI models
⬜ Add food price or market data as an additional predictor
⬜ Improve model validation across future IPC periods

---

## Limitations

This project is an early-stage portfolio model and should not be used as a production humanitarian decision system without further validation.

Current limitations include:

* The dataset is relatively small.
* The model currently uses rainfall and NDVI indicators only.
* Food prices, conflict, livestock conditions, market access, and humanitarian response data are not yet included.
* The current target is based on a 20% Phase 3+ population threshold.
* Results show predictive signals, not proof of causation.

---

## Next Research Direction

Future improvements can include:

1. Adding cereal market price indicators.
2. Adding livestock and vegetation stress indicators.
3. Testing rainfall-only, NDVI-only, and combined feature models.
4. Tuning XGBoost and Random Forest parameters.
5. Testing the model on future IPC periods.
6. Creating a county-level risk dashboard.
7. Building an interactive map showing predicted high-risk counties.

---

## License

This project is open-sourced under the [MIT License](LICENSE).

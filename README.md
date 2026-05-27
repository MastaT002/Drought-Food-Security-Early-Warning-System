# Drought & Food Security Early Warning System

A data analytics and machine learning portfolio project focused on building an early-warning system for food insecurity risk across Kenya's Arid and Semi-Arid Lands (ASAL).

**Data sources:** IPC food insecurity outcomes, CHIRPS rainfall data, and MODIS NDVI vegetation indicators.

**Current stage:** Data preparation, feature engineering, and exploratory analysis of the relationship between environmental stress and food insecurity severity.

**Next stage:** Build a baseline classification model to predict high-risk food insecurity cases 1–3 months in advance.

---

## The Problem

- **3.7 million Kenyans** are projected to face IPC Phase 3 "Crisis" level food insecurity between April–June 2026
- **23 ASAL counties** are particularly vulnerable to drought-driven food crises
- Humanitarian agencies currently react to crises **after** they peak, not before
- There is no publicly available, county-level forecasting tool that predicts food insecurity 30–90 days ahead

## Objective

Build an interpretable ML model that forecasts **IPC food insecurity phase** (Phase 1–5) per county, **30–90 days in advance**, using only publicly available data sources.

## Current Findings

The current analysis combines IPC food insecurity outcomes, CHIRPS rainfall indicators, and MODIS NDVI vegetation indicators for Kenya ASAL counties.

Key findings so far:

- Counties such as Turkana, Mandera, Marsabit, Wajir, Garissa, Isiolo, Samburu, Tana River, Baringo, and Kwale repeatedly appear as high-risk counties.
- Turkana had the highest average Phase 3+ population percentage, meaning it had the largest average share of people facing crisis-level food insecurity or worse.
- Higher IPC severity is generally associated with lower rainfall and weaker vegetation health.
- NDVI indicators showed stronger negative relationships with Phase 3+ population percentage than rainfall indicators.
- The strongest environmental indicator was the 3-month NDVI mean, with a correlation of about `-0.692` against Phase 3+ population percentage.
- The 6-month rainfall average also showed a meaningful negative relationship with Phase 3+ population percentage, with a correlation of about `-0.585`.

These findings suggest that vegetation health and rainfall are useful environmental indicators for drought and food security early-warning analysis.

**Important note:** These results show association, not proof of causation. Food insecurity may also be influenced by market prices, livestock conditions, conflict, income, market access, and humanitarian support.

## Success Criteria

- [ ] Build a baseline model to classify high-risk food insecurity cases
- [ ] Evaluate performance using accuracy, precision, recall, and confusion matrix
- [ ] Compare rainfall-only, NDVI-only, and combined rainfall + NDVI models
- [ ] Output must be interpretable — stakeholders can see why a county is flagged
- [ ] Deliver a simple risk map + table, not a raw CSV

## Data Sources

| Dataset | Source | Type | Current Status |
|---|---|---|---|
| IPC Acute Food Insecurity | FEWS NET / HDX | Food insecurity outcome data | ✅ Added |
| CHIRPS Rainfall | UCSB Climate Hazards Center | Monthly rainfall / climate data | ✅ Added |
| MODIS NDVI Vegetation | NASA/USGS MODIS via Google Earth Engine | Satellite vegetation health data | ✅ Added |
| Kenya County Boundaries | HDX / administrative boundaries | County shapefile / GeoJSON | ✅ Added |
| Cereal Market Prices | FAO FPMA or other public market price source | Time-series market data | ⬜ Planned |

## Tech Stack

- **Python:** pandas, matplotlib
- **Geospatial / Remote Sensing:** Google Earth Engine, MODIS NDVI, CHIRPS rainfall, GeoJSON county boundaries
- **Notebook Environment:** JupyterLab, Google Colab
- **Planned Modeling:** scikit-learn
- **Planned Dashboard / Visualization:** Streamlit, Power BI, or Plotly
  
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
│       └── phase3_environment_correlation_summary.csv
├── 03_notebooks/
│   ├── 01_ipc_data_cleaning.ipynb
│   ├── 02_ipc_eda.ipynb
│   ├── 03_county_boundaries_check.ipynb
│   ├── 03_rainfall_data_collection.ipynb
│   ├── 04_ipc_rainfall_merge.ipynb
│   ├── 05_ipc_rainfall_analysis.ipynb
│   ├── 06_ndvi_data_collection_modis_gee.ipynb
│   ├── 07_ipc_rainfall_ndvi_merge.ipynb
│   └── 08_master_dataset_eda.ipynb
├── 04_dashboard/
├── 02_data_inventory.md
├── data_dictionary.csv
├── README.md
└── LICENSE
```

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

Current stage: Preparing for baseline machine learning model.

Next stage:
⬜ Build baseline classification model  
⬜ Predict high-risk food insecurity cases using rainfall and NDVI features  
⬜ Evaluate model performance  
⬜ Create simple risk table and map/dashboard  
⬜ Add food price or market data as an additional predictor

## License

This project is open-sourced under the [MIT License](LICENSE).

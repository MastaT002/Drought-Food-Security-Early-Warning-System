# Drought & Food Security Early Warning System

A machine learning project that forecasts food insecurity severity across Kenya's Arid and Semi-Arid Lands (ASAL) **1–3 months in advance**. By combining satellite rainfall data, vegetation health indices, and local cereal market prices, this model aims to support NGOs and government agencies in shifting from **reactive food aid distribution to predictive, early humanitarian response**.

---

## The Problem

- **3.7 million Kenyans** are projected to face IPC Phase 3 "Crisis" level food insecurity between April–June 2026
- **23 ASAL counties** are particularly vulnerable to drought-driven food crises
- Humanitarian agencies currently react to crises **after** they peak, not before
- There is no publicly available, county-level forecasting tool that predicts food insecurity 30–90 days ahead

## Objective

Build an interpretable ML model that forecasts **IPC food insecurity phase** (Phase 1–5) per county, **30–90 days in advance**, using only publicly available data sources.

## Success Criteria

- [ ] Achieve >70% accuracy at predicting "Crisis" (Phase 3) or worse conditions
- [ ] Output must be interpretable — stakeholders can see **why** a county is flagged
- [ ] Deliver a simple risk map + table, not a raw CSV

## Data Sources

| Dataset | Source | Type |
|---|---|---|
| IPC Acute Food Insecurity | [FEWS NET](https://fews.net/) | Categorical (Phase 1–5) |
| CHIRPS Rainfall | [UCSB Climate Hazards Center](https://www.chc.ucsb.edu/data/chirps) | Time-series / Geo |
| NDVI Vegetation | [NASA/USGS MODIS](https://modis.gsfc.nasa.gov/) | Satellite imagery |
| Cereal Market Prices | [FAO FPMA](https://www.fao.org/giews/food-prices/tool/public/#/home) | Time-series |
| Kenya County Boundaries | [GADM / HDX](https://data.humdata.org/) | Shapefile |

## Tech Stack

- **Python:** pandas, scikit-learn, XGBoost, Prophet
- **Geospatial:** geopandas, kepler.gl
- **Visualization:** Plotly, Power BI / Streamlit
- **Notebook Environment:** Jupyter Lab

## Project Structure

```text
Drought-Food-Security-Early-Warning-System/
├── 01_project_brief.md              # Problem definition & scope
├── 02_data/
│   ├── raw/                         # Original downloaded datasets
│   └── processed/                   # Cleaned & merged datasets
├── 03_notebooks/
│   ├── 01_eda.ipynb                 # Exploratory Data Analysis
│   ├── 02_feature_engineering.ipynb # Feature creation & preparation
│   └── 03_modeling.ipynb            # Model training & evaluation
├── 04_dashboard/                    # Final output: maps + risk tables
├── data_dictionary.csv              # Column definitions
└── README.md                        # Project overview
```

## Status

🚧 **In Development** — Currently in data discovery & project scoping phase.

## License

This project is open-sourced under the [MIT License](LICENSE).

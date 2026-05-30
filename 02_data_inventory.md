# Data Inventory & Quality Assessment

**Project:** Drought & Food Security Early Warning System  
**Date:** May 2026  
**Status:** IPC, CHIRPS rainfall, MODIS NDVI, master dataset EDA, baseline modeling, prediction risk table, and Streamlit dashboard completed
---

### IPC Acute Food Insecurity Phase Classifications

| Attribute | Detail |
|---|---|
| **Source** | Integrated Food Security Phase Classification (IPC) via Humanitarian Data Exchange (HDX) |
| **Dataset URL** | https://data.humdata.org/dataset/kenya-acute-food-insecurity-country-data |
| **File Downloaded** | `ipc_ken_area_long.csv` |
| **File Size** | ~414 KB |
| **Raw Shape** | 5,047 rows × 11 columns |
| **Format** | CSV — long format |
| **Coverage Period** | Jul 2019–Feb 2026 |
| **Analysis Dates** | 15 analysis dates |
| **Validity Types** | `current` and `first projection` |
| **Granularity** | Area/county-level IPC Phase 1–5, Phase 3+ aggregate, total population, and percentage |
| **Access** | Free, public dataset |
| **Use in Project** | Target variable for county-level food insecurity severity modeling |

**Important Structure Notes:**
- Each area/date/validity-period combination has multiple phase rows:
  - `all` = total population
  - `3+` = population in IPC Phase 3 or worse
  - `1`, `2`, `3`, `4`, `5` = population in each IPC phase
- For the first modeling-ready dataset, `current` records will be used as the observed target.
- `first projection` records may later be used for comparison, validation, or future forecast benchmarking.

**Initial Data Quality Findings:**
- The raw dataset contains 5,047 rows and 11 columns.
- Main modeling columns are complete: `Date of analysis`, `Area`, `Validity period`, `Phase`, `Number`, and `Percentage`.
- The `Level 1` column has missing values, but it is not required for the first processed output.
- Date columns are currently stored as text and need to be converted into proper date format.
- The dataset includes both county-level records and non-county analysis areas.

**Data Cleaning Performed:**
- Standardized county names:
  - `TANA RIVER`, `Tana river` → `Tana River`
  - `Taita`, `Taita taveta` → `Taita Taveta`
  - `Tharaka`, `Tharaka-nithi` → `Tharaka Nithi`
  - `West pokot` → `West Pokot`
  - `Lamu county` → `Lamu`
  - `Embu (Mbeere)` → `Embu`
- Aggregated sub-county/sub-area records:
  - `Marsabit - moyale`, `Marsabit - laisamis`, `Marsabit - saku`, `Marsabit - north horr` → `Marsabit`
  - `Turkana west`, `Turkana south`, `Turkana central`, `Turkana north`, `Turkana east-kibish-loima` → `Turkana`
- Removed non-target analysis areas such as urban settlements, refugee/camp areas, and Non-ASAL/Diaspora records.
- Filtered to `current` IPC records only.
- Filtered to the 23 target counties.
- Created one modeling-ready row per county per analysis period.

**Known Data Gaps / Inconsistencies:**
- `Apr 2022` appears only as `first projection`; it does not have `current` observations.
- `Machakos` appears only in Jan 2023 and is classified under `Non-ASAL (Diaspora)`, so it will be excluded from modeling.
- `Jul 2024` reports Marsabit and Turkana as sub-areas instead of direct county totals, so these must be aggregated.
- County naming is inconsistent across years and must be standardized before merging with rainfall, price, or boundary datasets.
- The dataset includes extra non-county areas such as urban settlements and refugee/camp locations, which are not part of the county-level model.

**Modeling-Ready Output Created:**
`02_data/processed/ipc_max_phase_per_county.csv`

Final shape:
- 322 rows
- 7 columns

The final dataset contains 14 current IPC analysis periods across 23 target counties.

Final columns:
- `date`
- `analysis_period`
- `county`
- `max_ipc_phase`
- `phase_3_plus_population`
- `total_population`
- `phase_3_plus_percentage`

---

---

## Master Modeling Dataset Created

The project now includes a master dataset combining IPC food insecurity outcomes, CHIRPS rainfall indicators, and MODIS NDVI vegetation indicators.

**Master dataset:**
`02_data/processed/ipc_rainfall_ndvi_master_dataset.csv`

Final shape:

* 322 rows
* 19 columns

This dataset is the main modeling dataset used for baseline machine learning.

Main column groups:

* IPC outcome columns:

  * `ipc_date`
  * `analysis_period`
  * `county`
  * `max_ipc_phase`
  * `phase_3_plus_population`
  * `total_population`
  * `phase_3_plus_percentage`

* Rainfall feature columns:

  * `rainfall_date`
  * `mean_rainfall_mm`
  * `rainfall_3_month_total`
  * `rainfall_6_month_total`
  * `rainfall_3_month_avg`
  * `rainfall_6_month_avg`

* NDVI feature columns:

  * `date`
  * `mean_ndvi`
  * `ndvi_1_month_mean`
  * `ndvi_3_month_mean`
  * `ndvi_6_month_mean`
  * `ndvi_anomaly`

A correlation summary file was also created:

`02_data/processed/phase3_environment_correlation_summary.csv`

This file summarizes the strongest relationships between environmental indicators and Phase 3+ food insecurity population percentage.

A model prediction risk table was also created:

`02_data/processed/model_prediction_risk_table.csv`

Final shape:

* 65 rows
* 12 columns

This file contains county-level model predictions for the test period. It includes actual risk status, predicted risk status, predicted risk probability, and dashboard-friendly risk labels.

Main output columns include:

* `ipc_date`
* `analysis_period`
* `county`
* `actual_high_risk`
* `predicted_high_risk`
* `predicted_risk_probability`
* `predicted_risk_probability_pct`
* `risk_level`

The `risk_level` column groups county-periods into:

* `Low Risk`
* `Moderate Risk`
* `High Risk`

This file is used as the main input for the Streamlit dashboard.

---

## 2. Climate Predictors

### CHIRPS Rainfall Estimates
| Attribute | Detail |
|---|---|
| **Source** | Climate Hazards Center, UC Santa Barbara |
| **URL** | https://www.chc.ucsb.edu/data/chirps |
| **Format** | NetCDF (geospatial raster) or CSV via Google Earth Engine / CHC API |
| **Coverage** | Global, 1981–present, 0.05° resolution (~5.5 km) |
| **Update Frequency** | Daily (5-day lag) |
| **Granularity** | Pixel-level → aggregate to county means |
| **Access** | Free, public |
| **Quality** | ⭐⭐⭐⭐ High for seasonal trends; ⭐⭐⭐ Moderate in arid areas with sparse ground stations |
| **Notes** | For this project, use **CHIRPS Pentad (5-day)** or **Monthly** aggregates. You'll need to spatially aggregate pixel data to county boundaries using Python (`rasterio` + `geopandas`). |

**Best access method for beginners:**  
Use Google Earth Engine Python API to extract mean rainfall per county per month.  
Tutorial: https://developers.google.com/earth-engine/tutorials/community/chirps

---

## 3. Vegetation Health Predictors

### MODIS NDVI (Normalized Difference Vegetation Index)
| Attribute | Detail |
|---|---|
| **Source** | NASA/USGS MODIS (MOD13Q1 product) |
| **URL** | https://modis.gsfc.nasa.gov/data/dataprod/mod13.php |
| **Format** | HDF / GeoTIFF (250m resolution) |
| **Coverage** | Global, 2000–present |
| **Update Frequency** | 16-day composites |
| **Granularity** | 250m pixel → aggregate to county means |
| **Access** | Free via NASA Earthdata or Google Earth Engine |
| **Quality** | ⭐⭐⭐⭐ High; occasional cloud contamination in rainy seasons |
| **Notes** | NDVI measures vegetation "greenness" — a direct proxy for pasture quality and crop health. Low NDVI + low rainfall = strong food insecurity predictor. Use the **16-day composite** and average to monthly values per county. |

**Recommended access:** Google Earth Engine (much easier than downloading raw HDFs)  
**Alternative:** https://appeears.usgs.gov/ for point/area extraction

---

## 4. Market & Economic Predictors

### FAO Food Price Monitoring and Analysis (FPMA)
| Attribute | Detail |
|---|---|
| **Source** | FAO Global Information and Early Warning System (GIEWS) |
| **URL** | https://www.fao.org/giews/food-prices/tool/public/#/home |
| **Format** | Excel / CSV download |
| **Coverage** | Kenya, major wholesale markets (Nairobi, Mombasa, Kisumu, Eldoret), 2000–present |
| **Update Frequency** | Monthly |
| **Granularity** | Market-level prices for maize, beans, sorghum, rice, wheat |
| **Access** | Free, public |
| **Quality** | ⭐⭐⭐⭐ High for formal markets; ⭐⭐⭐ Moderate for remote ASAL markets |
| **Notes** | Focus on **wholesale maize and bean prices** — these are the staple foods in ASAL counties. You'll need to decide: use Nairobi prices as proxy for all counties, or try to find ASAL-specific market data (harder to find). |

**Direct tool:** https://www.fao.org/giews/food-prices/tool/public/#/dataset/domestic  
Select "Kenya" → download CSV.

---

## 5. Geospatial Boundaries

### Kenya County Boundaries (ASALs)
| Attribute | Detail |
|---|---|
| **Source** | GADM (Database of Global Administrative Areas) or Humanitarian Data Exchange (HDX) |
| **URL** | https://gadm.org/download_country.html or https://data.humdata.org/dataset/kenya-administrative-boundaries |
| **Format** | Shapefile (.shp) or GeoJSON |
| **Coverage** | All 47 counties, Level 1 (county) |
| **Access** | Free, public |
| **Quality** | ⭐⭐⭐⭐⭐ High |
| **Notes** | You'll use this to: (1) aggregate CHIRPS/NDVI pixels to county means, (2) create choropleth risk maps. Filter to the 23 ASAL counties only. |

**Target county list used in processed IPC dataset (23):** Baringo, Embu, Garissa, Isiolo, Kajiado, Kilifi, Kitui, Kwale, Laikipia, Lamu, Makueni, Mandera, Marsabit, Meru, Narok, Nyeri, Samburu, Taita Taveta, Tana River, Tharaka Nithi, Turkana, Wajir, West Pokot

---

## 6. Supplementary / Optional Data

### NDMA Early Warning Bulletins
| Attribute | Detail |
|---|---|
| **Source** | National Drought Management Authority (Kenya) |
| **URL** | https://www.ndma.go.ke/ |
| **Format** | PDF reports |
| **Coverage** | ASAL counties, monthly |
| **Access** | Free, public |
| **Quality** | ⭐⭐⭐⭐ High for ground-truth validation |
| **Notes** | Use these to **validate** your model outputs, not as primary training data. NDMA bulletins include qualitative assessments (pasture, water, livestock body condition) that can confirm whether your model's predictions align with ground reality. |

### World Bank Kenya Economic Indicators
| Attribute | Detail |
|---|---|
| **Source** | World Bank Open Data |
| **URL** | https://data.worldbank.org/country/kenya |
| **Format** | CSV / API |
| **Notes** | Macro indicators (GDP, inflation, fuel prices) as optional economic context. Lower priority than climate/vegetation data. |

---

## 7. Data Quality Summary Matrix

| Dataset | Coverage | Granularity | Update Lag | Accessibility | Priority |
|---|---|---|---|---|---|
| IPC Phase (FEWS NET) | ⭐⭐⭐⭐⭐ | County | ~1 month | Easy | **Critical** |
| CHIRPS Rainfall | ⭐⭐⭐⭐⭐ | 5.5km pixel | ~5 days | Medium (needs GEE) | **Critical** |
| MODIS NDVI | ⭐⭐⭐⭐⭐ | 250m pixel | ~16 days | Medium (needs GEE) | **Critical** |
| FAO FPMA Prices | ⭐⭐⭐⭐ | Market | ~1 month | Easy | **High** |
| Kenya Boundaries | ⭐⭐⭐⭐⭐ | County | Static | Easy | **Required** |
| NDMA Bulletins | ⭐⭐⭐⭐ | County | ~1 month | Easy | **Validation** |

---

## 8. Identified Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| **IPC data is quarterly, not monthly** | Limits time-series granularity to 4 points/year | Use quarterly models; interpolate only if justified |
| **CHIRPS/NDVI require spatial aggregation** | Adds preprocessing complexity | Use Google Earth Engine Python API; write reusable county-aggregation function |
| **FAO prices only cover major markets** | May not reflect remote ASAL prices | Acknowledge limitation in project brief; use Nairobi wholesale as proxy with caveat |
| **Cloud gaps in NDVI during rainy season** | Missing vegetation data when it's most needed | Use 16-day composites with cloud masking; flag missing periods in data dictionary |
| **Different date formats across sources** | Merge errors | Standardize all dates to `YYYY-MM-01` (monthly) or `YYYY-QX` (quarterly) |

---
## 9. Dashboard Output

A Streamlit dashboard was created to display county-level food insecurity risk predictions.

**Dashboard folder:**
`04_dashboard/`

Main files:

* `04_dashboard/app.py`
* `04_dashboard/requirements.txt`
* `04_dashboard/README.md`

The dashboard uses:

* `02_data/processed/model_prediction_risk_table.csv`
* `02_data/processed/kenya_target_counties.geojson`

Dashboard features include:

* Analysis period filter
* Risk level filter
* County-level risk map
* Risk summary cards
* High-risk county table
* Risk level distribution chart

**Live dashboard:**
[Kenya Drought & Food Security Risk Dashboard](https://drought-food-security-early-warning-system-kenya.streamlit.app/)

The dashboard is a prototype portfolio output and should not be used as a production humanitarian decision system without further validation.

---
## 10. Current Project Progress

1. [x] **Download IPC historical data** from HDX
2. [x] **Create IPC cleaning notebook**
3. [x] **Create processed IPC county-level dataset**
4. [x] **Create data dictionary**
5. [x] **Complete IPC exploratory data analysis**
6. [x] **Download and prepare Kenya county boundaries**
7. [x] **Use Google Earth Engine for CHIRPS rainfall extraction**
8. [x] **Create rainfall rolling average features**
9. [x] **Use Google Earth Engine for MODIS NDVI extraction**
10. [x] **Create NDVI rolling averages and anomaly features**
11. [x] **Merge IPC, rainfall, and NDVI into master dataset**
12. [x] **Complete master dataset EDA**
13. [x] **Create Phase 3+ environmental correlation summary**
14. [x] **Build baseline classification model**
15. [x] **Compare Naive Baseline, Logistic Regression, Random Forest, and XGBoost**
16. [x] **Select XGBoost as strongest balanced baseline model**
17. 17. [x] **Create model prediction risk table**
18. [x] **Build Streamlit county-level risk dashboard**
19. [x] **Create interactive county risk map**
20. [x] **Deploy dashboard publicly using Streamlit Community Cloud**

---

## 11. Next Steps

1. [x] **Create model prediction risk table**
2. [x] **Build county-level risk map or dashboard**
3. [x] **Deploy Streamlit dashboard publicly**
4. [ ] **Compare rainfall-only, NDVI-only, and combined rainfall + NDVI models**
5. [ ] **Add FAO FPMA cereal market price data**
6. [ ] **Update data dictionary as new features are added**
7. [ ] **Improve validation using future IPC periods**
8. [ ] **Expand dashboard to include full historical periods and future prediction outputs**
9. [ ] **Improve dashboard design, filters, map styling, and stakeholder explanations**

---

*This inventory will be updated as new datasets, features, and model outputs are added.*


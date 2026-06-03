# Data Inventory & Quality Assessment

**Project:** Drought & Food Security Early Warning System  
**Date:** May 2026  
**Status:** IPC, CHIRPS rainfall, MODIS NDVI, WFP food price features, master dataset EDA, baseline modeling, enhanced food price modeling, prediction risk tables, Streamlit dashboard, and feature group comparison completed
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

A feature group model comparison file was also created:

`02_data/processed/feature_group_model_comparison.csv`

This file compares model performance across three environmental feature groups:

* Rainfall-only features
* NDVI-only features
* Combined rainfall + NDVI features

The comparison showed that rainfall-only features provided useful signal but had the weakest performance. NDVI-only features performed much better, while the combined rainfall + NDVI model produced the strongest overall performance.

The main takeaway is that NDVI vegetation indicators are stronger than rainfall indicators alone, but combining rainfall and NDVI gives the best early-warning performance.

## Food Price Enhanced Master Dataset Created

The project now includes an enhanced master dataset combining IPC food insecurity outcomes, CHIRPS rainfall indicators, MODIS NDVI vegetation indicators, and WFP Kenya food price indicators.

**Enhanced master dataset:**
`02_data/processed/ipc_rainfall_ndvi_food_price_master_dataset.csv`

This dataset was created by merging the rainfall + NDVI master dataset with county-level and national-level food price features.

Food price feature files created:

* `02_data/processed/county_food_price_monthly_features.csv`
* `02_data/processed/national_food_price_monthly_features.csv`

The enhanced dataset includes:

* IPC outcome columns
* Rainfall feature columns
* NDVI feature columns
* County-level food price features where available
* National food price proxy features
* Final hybrid food price features
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

### WFP Kenya Food Prices

| Attribute | Detail |
|---|---|
| **Source** | World Food Programme food price data via Humanitarian Data Exchange (HDX) |
| **Dataset** | WFP Food Prices for Kenya |
| **Format** | CSV |
| **Coverage** | Kenya market-level food price records |
| **Granularity** | Market-level prices aggregated to county-month and national-month features |
| **Access** | Free, public |
| **Use in Project** | Food price / market-pressure predictor |
| **Selected Commodities** | Maize, beans, and rice |
| **Processed Output** | `county_food_price_monthly_features.csv`, `national_food_price_monthly_features.csv` |
| **Quality Notes** | Useful market signal, but county-level coverage is incomplete for some ASAL counties and periods |

**Processing performed:**

* Downloaded WFP Kenya food price data.
* Inspected markets, commodities, units, and dates.
* Mapped market names to target ASAL counties where possible.
* Grouped commodity variants into staple groups:
  * maize
  * beans
  * rice
* Standardized units to price per kilogram.
* Created county-level monthly price features.
* Created national-level monthly price features.
* Created hybrid food price features using county prices where available and national prices as fallback.

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
| WFP Kenya Food Prices | ⭐⭐⭐⭐ | Market | Monthly | Easy | **High** |
| Kenya Boundaries | ⭐⭐⭐⭐⭐ | County | Static | Easy | **Required** |
| NDMA Bulletins | ⭐⭐⭐⭐ | County | ~1 month | Easy | **Validation** |

---

## 8. Identified Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| **IPC data is quarterly, not monthly** | Limits time-series granularity to 4 points/year | Use quarterly models; interpolate only if justified |
| **CHIRPS/NDVI require spatial aggregation** | Adds preprocessing complexity | Use Google Earth Engine Python API; write reusable county-aggregation function |
| **Incomplete county-level food price coverage** | Some counties or periods do not have direct market price records | Use county-level prices where available and national staple price proxy where county prices are missing |
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
* `02_data/processed/model_prediction_risk_table_food_prices.csv`
* `02_data/processed/kenya_target_counties.geojson`

The dashboard allows users to switch between:

* Baseline model: rainfall + NDVI
* Enhanced model: rainfall + NDVI + food prices

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
17. [x] **Create model prediction risk table**
18. [x] **Build Streamlit county-level risk dashboard**
19. [x] **Create interactive county risk map**
20. [x] **Deploy dashboard publicly using Streamlit Community Cloud**
21. [x] **Compare rainfall-only, NDVI-only, and combined rainfall + NDVI models**
22. [x] **Create feature group model comparison output**
23. [x] **Download WFP Kenya food price data**
24. [x] **Inspect and clean food price data**
25. [x] **Select staple food groups: maize, beans, and rice**
26. [x] **Standardize food prices to price per kilogram**
27. [x] **Create county-level and national-level monthly food price features**
28. [x] **Merge food price features with IPC + rainfall + NDVI master dataset**
29. [x] **Train and evaluate enhanced models with food price features**
30. [x] **Compare baseline vs food price enhanced model performance**
31. [x] **Create dashboard-ready food price prediction table**

---

## 11. Next Steps

1. [x] **Create model prediction risk table**
2. [x] **Build county-level risk map or dashboard**
3. [x] **Deploy Streamlit dashboard publicly**
4. [x] **Compare rainfall-only, NDVI-only, and combined rainfall + NDVI models**
5. [x] **Add food price / market price data**
6. [ ] **Improve food price feature coverage and test additional commodities**
7. [ ] **Update data dictionary as new food price features are added**
8. [ ] **Improve validation using future IPC periods**
9. [ ] **Expand dashboard to compare baseline and enhanced food price model predictions**
10. [ ] **Improve dashboard design, filters, map styling, and stakeholder explanations**

---

*This inventory will be updated as new datasets, features, and model outputs are added.*


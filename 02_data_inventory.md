# Data Inventory & Quality Assessment

**Project:** Drought & Food Security Early Warning System  
**Date:** May 2026  
**Status:** Discovery Phase — URLs verified, download in progress

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
- For modeling, `current` records will be used as the main observed target.
- `first projection` records may later be used for comparison or validation.

**Data Cleaning Required:**
- Standardize county names:
  - `TANA RIVER`, `Tana river` → `Tana River`
  - `Taita`, `Taita taveta` → `Taita Taveta`
  - `Tharaka`, `Tharaka-nithi` → `Tharaka Nithi`
  - `West pokot` → `West Pokot`
  - `Lamu county` → `Lamu`
  - `Embu (Mbeere)` → `Embu`
- Aggregate sub-county/sub-area records:
  - `Marsabit - moyale`, `Marsabit - laisamis`, `Marsabit - saku`, `Marsabit - north horr` → `Marsabit`
  - `Turkana west`, `Turkana south`, `Turkana central`, `Turkana north`, `Turkana east-kibish-loima` → `Turkana`
- Remove non-target analysis areas such as urban settlements, refugee/camp areas, and Non-ASAL/Diaspora records.
- Filter to modeling-ready county-level observations.

**Known Data Gaps / Inconsistencies:**
- `Apr 2022` appears only as `first projection`; it does not have `current` observations.
- `Machakos` appears only in Jan 2023 and is classified under `Non-ASAL (Diaspora)`, so it will be excluded from modeling.
- `Jul 2024` reports Marsabit and Turkana as sub-areas instead of direct county totals, so these must be aggregated.
- County naming is inconsistent across years and must be standardized before merging with rainfall, price, or boundary datasets.

**Planned Modeling-Ready Output:**
`ipc_max_phase_per_county.csv`

Expected columns:
- `date`
- `county`
- `max_ipc_phase`
- `phase_3_plus_population`
- `total_population`
- `phase_3_plus_percentage`

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

**ASAL county list (23):** Baringo, Garissa, Isiolo, Kajiado, Kilifi, Kitui, Kwale, Lakipia, Lamu, Machakos, Makueni, Mandera, Marsabit, Meru, Mombasa, Narok, Samburu, Taita Taveta, Tana River, Tharaka Nithi, Turkana, Wajir, West Pokot

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

## 9. Next Steps

1. [ ] **Register for Google Earth Engine** (needed for CHIRPS + NDVI extraction)
2. [ ] **Download IPC historical data** from FEWS NET (Excel format)
3. [ ] **Download FAO FPMA price data** for Kenya (CSV format)
4. [ ] **Download Kenya county shapefile** from GADM or HDX
5. [ ] **Create `data_dictionary.csv`** documenting every column from every source
6. [ ] **Begin EDA notebook** — first step: plot IPC phase trends by county over time

---

*This inventory will be updated as data is downloaded and quality-checked.*

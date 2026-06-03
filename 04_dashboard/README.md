# Kenya Food Insecurity Risk Dashboard

This folder contains the Streamlit dashboard for the Kenya Drought and Food Security Early Warning System.

The dashboard displays county-level food insecurity risk predictions for Kenya ASAL counties.

## Dashboard Purpose

The dashboard helps users explore predicted food insecurity risk by county and analysis period.

It shows:

- predicted risk level
- predicted high-risk probability
- actual high-risk status
- predicted high-risk status
- IPC Phase 3+ percentage
- maximum IPC phase
- rainfall and NDVI context
- food price context when the enhanced model is selected

## Model Versions

The dashboard supports two model versions:

### 1. Baseline Model: Rainfall + NDVI

This model uses climate and vegetation indicators only.

Main feature groups:

- rainfall indicators
- NDVI vegetation indicators

### 2. Enhanced Model: Rainfall + NDVI + Food Prices

This model adds staple food price indicators to the baseline feature set.

Main feature groups:

- rainfall indicators
- NDVI vegetation indicators
- food price indicators

The food price features focus on maize, beans, and rice.

Where county-level food price data is missing, national staple food price proxy values are used.

## Dashboard Input Files

The dashboard uses the following processed data files:

```text
02_data/processed/model_prediction_risk_table.csv
02_data/processed/model_prediction_risk_table_food_prices.csv
02_data/processed/kenya_target_counties.geojson
```

## File Descriptions

| File                                          | Description                                                         |
| --------------------------------------------- | ------------------------------------------------------------------- |
| `model_prediction_risk_table.csv`             | Baseline model prediction table using rainfall + NDVI               |
| `model_prediction_risk_table_food_prices.csv` | Enhanced model prediction table using rainfall + NDVI + food prices |
| `kenya_target_counties.geojson`               | GeoJSON boundary file for the target Kenya ASAL counties            |

## Main Dashboard File

```text
04_dashboard/app.py
```

This file contains the Streamlit dashboard code.

## Requirements File

```text
04_dashboard/requirements.txt
```

This file lists the Python packages needed to run the dashboard.

## Dashboard Features

The dashboard includes:

* model version selector
* analysis period filter
* risk level filter
* county-level risk map
* risk summary cards
* top predicted risk counties table
* risk level distribution chart
* food price source summary for the enhanced model

## Risk Level Definitions

Risk levels are based on predicted probability.

| Risk Level    | Predicted Probability |
| ------------- | --------------------: |
| Low Risk      |             Below 40% |
| Moderate Risk |      40% to below 60% |
| High Risk     |         60% and above |

## Running the Dashboard Locally

From the project root folder, run:

```bash
streamlit run 04_dashboard/app.py
```

## Live Dashboard

The dashboard is deployed using Streamlit Community Cloud:

```text
https://drought-food-security-early-warning-system-kenya.streamlit.app/
```

## Important Note

This dashboard is an early-stage portfolio prototype.

It should not be used as a production humanitarian decision system without further validation, expert review, and operational testing.

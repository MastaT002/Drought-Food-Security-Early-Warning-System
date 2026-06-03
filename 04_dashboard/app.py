import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
from pathlib import Path

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(
    page_title="Kenya Food Insecurity Risk Dashboard",
    layout="wide"
)

st.title("Kenya Food Insecurity Risk Dashboard")

st.markdown(
    """
    This dashboard shows predicted food insecurity risk for Kenya ASAL counties.

    Users can compare two model versions:

    - **Baseline model:** rainfall + NDVI vegetation indicators
    - **Enhanced model:** rainfall + NDVI + food price indicators

    The dashboard classifies county-periods as **Low Risk**, **Moderate Risk**, or **High Risk**
    based on predicted food insecurity risk probability.
    """
)

# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_data():
    base_dir = Path(__file__).resolve().parents[1]

    baseline_risk_path = (
        base_dir / "02_data" / "processed" / "model_prediction_risk_table.csv"
    )

    food_price_risk_path = (
        base_dir / "02_data" / "processed" / "model_prediction_risk_table_food_prices.csv"
    )

    counties_path = (
        base_dir / "02_data" / "processed" / "kenya_target_counties.geojson"
    )

    baseline_risk_table = pd.read_csv(baseline_risk_path)
    baseline_risk_table["ipc_date"] = pd.to_datetime(
        baseline_risk_table["ipc_date"],
        errors="coerce"
    )

    food_price_risk_table = None

    if food_price_risk_path.exists():
        food_price_risk_table = pd.read_csv(food_price_risk_path)
        food_price_risk_table["ipc_date"] = pd.to_datetime(
            food_price_risk_table["ipc_date"],
            errors="coerce"
        )

    counties = gpd.read_file(counties_path)

    return baseline_risk_table, food_price_risk_table, counties


baseline_risk_table, food_price_risk_table, counties = load_data()

# -----------------------------
# Sidebar model selector
# -----------------------------
st.sidebar.header("Model Selection")

model_options = {
    "Baseline: Rainfall + NDVI": "baseline"
}

if food_price_risk_table is not None:
    model_options["Enhanced: Rainfall + NDVI + Food Prices"] = "food_prices"

selected_model_label = st.sidebar.selectbox(
    "Select model version",
    list(model_options.keys())
)

selected_model_key = model_options[selected_model_label]

if selected_model_key == "baseline":
    risk_table = baseline_risk_table.copy()
    model_description = (
        "This model uses rainfall and NDVI vegetation indicators only."
    )
    model_performance = {
        "Accuracy": "87.7%",
        "F1 Score": "77.8%",
        "High-Risk Precision": "70.0%",
        "High-Risk Recall": "87.5%"
    }
else:
    risk_table = food_price_risk_table.copy()
    model_description = (
        "This model uses rainfall, NDVI vegetation indicators, and staple food price features."
    )
    model_performance = {
        "Accuracy": "89.2%",
        "F1 Score": "78.8%",
        "High-Risk Precision": "76.5%",
        "High-Risk Recall": "81.3%"
    }

st.sidebar.info(model_description)

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.header("Filters")

period_options = sorted(risk_table["analysis_period"].dropna().unique())

selected_period = st.sidebar.selectbox(
    "Select analysis period",
    period_options,
    index=len(period_options) - 1
)

risk_options = ["Low Risk", "Moderate Risk", "High Risk"]

selected_risk_levels = st.sidebar.multiselect(
    "Select risk levels",
    risk_options,
    default=risk_options
)

# Filter risk table
filtered_risk = risk_table[
    (risk_table["analysis_period"] == selected_period)
    & (risk_table["risk_level"].isin(selected_risk_levels))
].copy()

# -----------------------------
# Model information
# -----------------------------
st.subheader("Selected Model")

st.write(f"**Model version:** {selected_model_label}")
st.write(model_description)

perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)

perf_col1.metric("Accuracy", model_performance["Accuracy"])
perf_col2.metric("F1 Score", model_performance["F1 Score"])
perf_col3.metric("High-Risk Precision", model_performance["High-Risk Precision"])
perf_col4.metric("High-Risk Recall", model_performance["High-Risk Recall"])

if selected_model_key == "food_prices":
    st.info(
        """
        The enhanced model includes food price features. Some counties do not have direct
        county-level food price records for every period. Where county prices were missing,
        national staple food price indicators were used as a proxy.
        """
    )

# -----------------------------
# Merge risk data with county map
# -----------------------------
map_data = counties.merge(
    filtered_risk,
    on="county",
    how="left"
)

# -----------------------------
# KPI cards
# -----------------------------
st.subheader(f"Risk Summary for {selected_period}")

col1, col2, col3, col4 = st.columns(4)

total_counties = filtered_risk["county"].nunique()
high_risk_counties = (filtered_risk["risk_level"] == "High Risk").sum()
moderate_risk_counties = (filtered_risk["risk_level"] == "Moderate Risk").sum()
low_risk_counties = (filtered_risk["risk_level"] == "Low Risk").sum()

col1.metric("Counties shown", total_counties)
col2.metric("High Risk", high_risk_counties)
col3.metric("Moderate Risk", moderate_risk_counties)
col4.metric("Low Risk", low_risk_counties)

# -----------------------------
# Map
# -----------------------------
st.subheader("County Risk Map")

hover_data = {
    "analysis_period": True,
    "predicted_risk_probability_pct": ":.2f",
    "actual_high_risk": True,
    "predicted_high_risk": True,
    "phase_3_plus_percentage": ":.2f",
    "max_ipc_phase": True
}

if selected_model_key == "food_prices":
    food_price_hover_cols = [
        "final_staple_price_per_kg",
        "final_staple_price_per_kg_3_month_avg",
        "final_staple_price_per_kg_6_month_avg",
        "food_price_source",
        "county_food_price_matched"
    ]

    for col in food_price_hover_cols:
        if col in map_data.columns:
            hover_data[col] = True

fig = px.choropleth_mapbox(
    map_data,
    geojson=map_data.geometry,
    locations=map_data.index,
    color="risk_level",
    hover_name="county",
    hover_data=hover_data,
    mapbox_style="carto-positron",
    center={"lat": 0.5, "lon": 37.8},
    zoom=5,
    opacity=0.65,
    category_orders={
        "risk_level": ["Low Risk", "Moderate Risk", "High Risk"]
    },
    title=f"Predicted Food Insecurity Risk - {selected_period}"
)

fig.update_layout(
    margin={"r": 0, "t": 40, "l": 0, "b": 0},
    height=650
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Top risk counties table
# -----------------------------
st.subheader("Top Predicted Risk Counties")

top_risk = filtered_risk.sort_values(
    "predicted_risk_probability_pct",
    ascending=False
)

display_cols = [
    "analysis_period",
    "county",
    "risk_level",
    "predicted_risk_probability_pct",
    "actual_high_risk",
    "predicted_high_risk",
    "phase_3_plus_percentage",
    "max_ipc_phase"
]

if selected_model_key == "food_prices":
    extra_food_cols = [
        "final_staple_price_per_kg",
        "final_staple_price_per_kg_3_month_avg",
        "final_staple_price_per_kg_6_month_avg",
        "food_price_source",
        "county_food_price_matched"
    ]

    display_cols.extend([
        col for col in extra_food_cols if col in top_risk.columns
    ])

available_display_cols = [
    col for col in display_cols if col in top_risk.columns
]

st.dataframe(
    top_risk[available_display_cols],
    use_container_width=True
)

# -----------------------------
# Food price source summary
# -----------------------------
if selected_model_key == "food_prices" and "food_price_source" in filtered_risk.columns:
    st.subheader("Food Price Source Summary")

    food_source_summary = (
        filtered_risk["food_price_source"]
        .value_counts()
        .reset_index()
    )

    food_source_summary.columns = ["food_price_source", "count"]

    source_fig = px.bar(
        food_source_summary,
        x="food_price_source",
        y="count",
        title=f"Food Price Source Counts - {selected_period}",
        labels={
            "food_price_source": "Food Price Source",
            "count": "Number of County-Periods"
        }
    )

    st.plotly_chart(source_fig, use_container_width=True)

# -----------------------------
# Risk level summary chart
# -----------------------------
st.subheader("Risk Level Distribution")

risk_summary = (
    filtered_risk["risk_level"]
    .value_counts()
    .reindex(["Low Risk", "Moderate Risk", "High Risk"])
    .fillna(0)
    .reset_index()
)

risk_summary.columns = ["risk_level", "count"]

bar_fig = px.bar(
    risk_summary,
    x="risk_level",
    y="count",
    title=f"Risk Level Counts - {selected_period}",
    labels={
        "risk_level": "Risk Level",
        "count": "Number of County-Periods"
    }
)

st.plotly_chart(bar_fig, use_container_width=True)

# -----------------------------
# Notes
# -----------------------------
st.markdown(
    """
    ### Notes

    - **Low Risk**: predicted probability below 40%.
    - **Moderate Risk**: predicted probability from 40% to below 60%.
    - **High Risk**: predicted probability of 60% and above.

    The baseline model uses rainfall and NDVI features.

    The enhanced model uses rainfall, NDVI, and food price features.

    This dashboard is an early-stage portfolio prototype and should not be used
    as a production humanitarian decision system without further validation.
    """
)

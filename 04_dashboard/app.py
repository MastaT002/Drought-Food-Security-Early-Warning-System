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
    This dashboard shows predicted food insecurity risk for Kenya ASAL counties
    using the selected XGBoost baseline model.

    The model uses rainfall and NDVI vegetation indicators to classify county-periods
    as Low Risk, Moderate Risk, or High Risk.
    """
)

# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_data():
    base_dir = Path(__file__).resolve().parents[1]

    risk_path = base_dir / "02_data" / "processed" / "model_prediction_risk_table.csv"
    counties_path = base_dir / "02_data" / "processed" / "kenya_target_counties.geojson"

    risk_table = pd.read_csv(risk_path)
    counties = gpd.read_file(counties_path)

    risk_table["ipc_date"] = pd.to_datetime(risk_table["ipc_date"])

    return risk_table, counties

risk_table, counties = load_data()

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.header("Filters")

period_options = sorted(risk_table["analysis_period"].unique())

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

fig = px.choropleth_mapbox(
    map_data,
    geojson=map_data.geometry,
    locations=map_data.index,
    color="risk_level",
    hover_name="county",
    hover_data={
        "analysis_period": True,
        "predicted_risk_probability_pct": ":.2f",
        "actual_high_risk": True,
        "predicted_high_risk": True,
        "phase_3_plus_percentage": ":.2f"
    },
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

st.dataframe(
    top_risk[display_cols],
    use_container_width=True
)

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

    This dashboard is an early-stage portfolio prototype and should not be used
    as a production humanitarian decision system without further validation.
    """
)
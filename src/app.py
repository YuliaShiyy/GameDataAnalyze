# @Author : Yulia
# @File   : app.py
# @Time   : 2025/9/6

import streamlit as st
from data_loader import load_data, filter_data
from overview import render_overview
from retention import render_retention_funnel
from simulation_trend import render_trend
from correlation import render_correlation
from clustering import render_clustering
from prediction import render_prediction
from report_export import export_full_report

# page setting
st.set_page_config(page_title="Player behavior analysis dashboard", layout="wide")

# load data
df, df_europe = load_data()

# Sidebar filters
st.sidebar.header("🌍 Filters")
all_regions = df['Location'].unique().tolist()
selected_region = st.sidebar.selectbox("Select Region", ["Global"] + all_regions)
genres = st.sidebar.multiselect("Select Game Type", df["GameGenre"].unique())
genders = st.sidebar.multiselect("Select Gender", df["Gender"].unique())
purchase_filter = st.sidebar.selectbox("Paid or Not", ["All", "Paid players", "Not-paid players"])

# Module Navigation
section = st.sidebar.radio(
    "📑 Module Navigation",
    ["Overview",
     "Retention & Funnel",
     "Simulated Trend",
     "Correlation Analysis",
     "Cluster Analysis",
     "Predictive Modeling"],
    index=0
)

# filter global data
filtered_data = filter_data(df, selected_region, genres, genders, purchase_filter)
if len(filtered_data) == 0:
    st.warning("There is no data under the current filter conditions. Please adjust the filter conditions.")
    st.stop()

# --- Run selected module ---
metrics, figs_overview = render_overview(filtered_data, selected_region) if section == "Overview" else (None, {})
fig_retention, fig_funnel = render_retention_funnel(filtered_data) if section == "Retention & Funnel" else (None, None)
fig_new, fig_purchase_trend, fig_sessions_trend = render_trend(filtered_data) if section == "Simulated Trend" else (None, None, None)
results_df, fig_corr, fig_scatter, fig_box = render_correlation(filtered_data) if section == "Correlation Analysis" else (None, None, None, None)
fig_cluster, fig_summary = render_clustering(filtered_data) if section == "Cluster Analysis" else (None, None)
model_acc, fig_cm = render_prediction(filtered_data) if section == "Predictive Modeling" else (None, None)

# --- Export Report ---
st.sidebar.header("📑 Export Report")

# Collect all charts
all_figs = {}
all_figs.update(figs_overview or {})
if fig_retention: all_figs["Retention Rate"] = fig_retention
if fig_funnel: all_figs["Funnel Analysis"] = fig_funnel
if fig_corr: all_figs["Correlation Heatmap"] = fig_corr
if fig_scatter: all_figs["Correlation Scatter"] = fig_scatter
if fig_box: all_figs["Correlation Boxplot"] = fig_box
if fig_cluster: all_figs["Clustering Result"] = fig_cluster
if fig_cm: all_figs["Prediction Confusion Matrix"] = fig_cm
if fig_new: all_figs["New Players Trend"] = fig_new
if fig_purchase_trend: all_figs["Purchase Trend"] = fig_purchase_trend
if fig_sessions_trend: all_figs["Average Sessions Trend"] = fig_sessions_trend

# select charts(default: all)
selected_charts = st.sidebar.multiselect(
    "Select charts to include in the report",
    list(all_figs.keys()),
    default=list(all_figs.keys())
)

if st.sidebar.button("⬇️ Download Report"):
    with st.spinner("Generating report... please wait..."):
        pdf = export_full_report(metrics, results_df, all_figs, model_acc, selected_charts)
    st.sidebar.download_button(
        "Save Report",
        pdf,
        file_name=f"{section}_report.pdf",
        mime="application/pdf"
    )

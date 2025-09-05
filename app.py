# @Author : Yulia
# @File   : app.py
# @Time   : 2025/9/3

import streamlit as st
from data_loader import load_data, filter_data
from overview import render_overview
from retention import render_retention_funnel
from simulation_trend import render_trend
from correlation import render_correlation
from clustering import render_clustering
from prediction import render_prediction
from report_export import export_full_report

# =====================
# 页面设置
# =====================
st.set_page_config(page_title="🎮 Player Behavior Analysis Dashboard", layout="wide")

# =====================
# 加载数据
# =====================
df, df_europe = load_data()

# =====================
# 筛选器
# =====================
st.sidebar.header("🌍 Filters")
all_regions = df['Location'].unique().tolist()
selected_region = st.sidebar.selectbox("Select Region", ["Global"] + all_regions)
genres = st.sidebar.multiselect("Select Game Type", df["GameGenre"].unique())
genders = st.sidebar.multiselect("Select Gender", df["Gender"].unique())
purchase_filter = st.sidebar.selectbox("Paid or Not", ["All", "Paid players", "Not-paid players"])

# =====================
# 模块导航
# =====================
section = st.sidebar.radio(
    "📑 Module Navigation",
    ["Overview", "Retention & Funnel", "Simulated Trend", "Correlation Analysis", "Cluster Analysis", "Predictive Modeling"],
    index=0
)

# =====================
# 数据筛选
# =====================
filtered_data = filter_data(df, selected_region, genres, genders, purchase_filter)
if len(filtered_data) == 0:
    st.warning("⚠️ There is no data under the current filter conditions. Please adjust the filter conditions.")
    st.stop()

# =====================
# 模块渲染
# =====================
metrics, figs_overview = (None, None)
retention, fig_retention, fig_funnel = (None, None, None)
results_df, fig_corr, fig_scatter, fig_box = (None, None, None, None)
fig_cluster, cluster_summary = (None, None)
model_acc, fig_cm = (None, None)
fig_new, fig_purchase_trend, fig_sessions_trend, trend = (None, None, None, None)

if section == "Overview":
    metrics, figs_overview = render_overview(filtered_data, selected_region, render=True)

elif section == "Retention & Funnel":
    retention, fig_retention, fig_funnel = render_retention_funnel(filtered_data, render=True)

elif section == "Simulated Trend":
    fig_new, fig_purchase_trend, fig_sessions_trend, trend = render_trend(filtered_data, render=True)

elif section == "Correlation Analysis":
    results_df, fig_corr, fig_scatter, fig_box = render_correlation(filtered_data, render=True)

elif section == "Cluster Analysis":
    fig_cluster, cluster_summary = render_clustering(filtered_data, render=True)

elif section == "Predictive Modeling":
    model_acc, fig_cm = render_prediction(filtered_data, render=True)

# =====================
# 导出报告
# =====================
st.sidebar.header("📑 Export Report")
if st.sidebar.button("⬇️ Download Full Report"):
    # ⚡ 调用各模块 (render=False) 获取所有数据 & 图表
    metrics, figs_overview = render_overview(filtered_data, selected_region, render=False)
    retention, fig_retention, fig_funnel = render_retention_funnel(filtered_data, render=False)
    results_df, fig_corr, fig_scatter, fig_box = render_correlation(filtered_data, render=False)
    fig_cluster, cluster_summary = render_clustering(filtered_data, render=False)
    model_acc, fig_cm = render_prediction(filtered_data, render=False)
    fig_new, fig_purchase_trend, fig_sessions_trend, trend = render_trend(filtered_data, render=False)

    figs_all = {
        **figs_overview,
        "Retention Rate": fig_retention,
        "Funnel Analysis": fig_funnel,
        "Correlation Heatmap": fig_corr,
        "Correlation Scatter": fig_scatter,
        "Correlation Boxplot": fig_box,
        "Clustering Result": fig_cluster,
        "Prediction Confusion Matrix": fig_cm,
        "New Players Trend": fig_new,
        "Purchase Trend": fig_purchase_trend,
        "Average Sessions Trend": fig_sessions_trend,
    }

    pdf = export_full_report(metrics, results_df, figs_all, model_acc, cluster_summary, trend)

    st.sidebar.download_button(
        "💾 Save Report",
        pdf,
        file_name="player_behavior_report.pdf",
        mime="application/pdf"
    )

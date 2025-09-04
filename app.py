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
st.set_page_config(page_title="Player behavior analysis dashboard", layout="wide")

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
    [
        "Overview",
        "Retention & Funnel",
        "Simulated Trend",
        "Correlation Analysis",
        "Cluster Analysis",
        "Predictive Modeling"
    ],
    index=0
)

# =====================
# 筛选数据
# =====================
filtered_data = filter_data(df, selected_region, genres, genders, purchase_filter)
if len(filtered_data) == 0:
    st.warning("There is no data under the current filter conditions. Please adjust the filter conditions.")
    st.stop()

# =====================
# 模块路由
# =====================
metrics, figs = {}, {}

if section == "Overview":
    metrics, figs = render_overview(filtered_data, selected_region)
elif section == "Retention & Funnel":
    figs["Retention Rate"], figs["Funnel Analysis"] = render_retention_funnel(filtered_data)
elif section == "Simulated Trend":
    figs["New Players Trend"], figs["Purchase Trend"], figs["Average Sessions Trend"] = render_trend(filtered_data)
elif section == "Correlation Analysis":
    results_df, figs["Correlation Heatmap"], figs["Correlation Scatter"], figs["Correlation Boxplot"] = render_correlation(filtered_data)
elif section == "Cluster Analysis":
    figs["Clustering Result"] = render_clustering(filtered_data)
elif section == "Predictive Modeling":
    model_acc, figs["Prediction Confusion Matrix"] = render_prediction(filtered_data)

# =====================
# 导出报告 
# =====================
with st.sidebar.expander("📑 Export Report"):
    if st.button("⬇️ Download Report"):
        # 👉 再跑一遍，收集所有模块的返回值（不会渲染 UI）
        all_metrics, overview_figs = render_overview(filtered_data, selected_region)
        fig_retention, fig_funnel = render_retention_funnel(filtered_data)
        fig_new, fig_purchase_trend, fig_sessions_trend = render_trend(filtered_data)
        results_df, fig_corr, fig_scatter, fig_box = render_correlation(filtered_data)
        fig_cluster = render_clustering(filtered_data)
        model_acc, fig_cm = render_prediction(filtered_data)

        figs_all = {
            **overview_figs,
            "Retention Rate": fig_retention,
            "Funnel Analysis": fig_funnel,
            "Correlation Heatmap": fig_corr,
            "Correlation Scatter": fig_scatter,
            "Correlation Boxplot": fig_box,
            "Clustering Result": fig_cluster,
            "Prediction Confusion Matrix": fig_cm,
            "New Players Trend": fig_new,
            "Purchase Trend": fig_purchase_trend,
            "Average Sessions Trend": fig_sessions_trend
        }

        pdf = export_full_report(all_metrics, results_df, figs_all, model_acc)
        st.download_button(
            "Save Report",
            pdf,
            file_name="full_report.pdf",
            mime="application/pdf"
        )

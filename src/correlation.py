# @Author : Yulia
# @File   : correlation.py
# @Time   : 2025/9/3

import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import pearsonr


def render_correlation(filtered_data, render=True):
    numeric_cols = ["Age", "SessionsPerWeek", "PlayerLevel", "InGamePurchases"]
    if not all(col in filtered_data.columns for col in numeric_cols):
        if render:
            st.warning("The current data is missing the necessary numeric columns to calculate correlations.")
        return None, None, None, None

    # Calculate r & p
    results = []
    for i in range(len(numeric_cols)):
        for j in range(i + 1, len(numeric_cols)):
            col1, col2 = numeric_cols[i], numeric_cols[j]
            series = filtered_data[[col1, col2]].dropna()
            if len(series) < 3:
                continue
            r, p = pearsonr(series[col1], series[col2])
            results.append({
                "Variable Pairs": f"{col1} vs {col2}",
                "Correlation Coefficient (r)": round(r, 3),
                "Significance Level (p)": round(p, 4),
                "Significant Correlation?": "✅ YES" if p < 0.05 else "❌ NO"
            })

    results_df = pd.DataFrame(results).sort_values(
        by=["Significance Level (p)", "Correlation Coefficient (r)"],
        ascending=[True, False],
        key=lambda col: col.abs() if col.name == "Correlation Coefficient (r)" else col
    ).reset_index(drop=True) if results else pd.DataFrame()

    # Heatmap
    corr_matrix = filtered_data[numeric_cols].corr()
    fig_corr = px.imshow(
        corr_matrix, text_auto=True, color_continuous_scale="RdBu_r",
        title="Numerical Variable Correlation Heatmap"
    )

    # Scatter
    fig_scatter = px.scatter(
        filtered_data, x="Age", y="SessionsPerWeek",
        color=filtered_data["InGamePurchases"].map({1: "Paid", 0: "Not-paid"}),
        size="PlayerLevel", hover_data=["GameGenre"],
        title="Age vs. Sessions Per Week"
    ) if "Age" in filtered_data.columns else None

    # Boxplot
    fig_box = px.box(
        filtered_data, x="GameGenre", y="SessionsPerWeek", color="GameGenre",
        title="Sessions by Game Type"
    ) if "GameGenre" in filtered_data.columns else None

    if render:
        st.subheader("🔗 Correlation Analysis")
        if not results_df.empty:
            st.dataframe(results_df)
        st.plotly_chart(fig_corr, use_container_width=True)
        if fig_scatter:
            st.plotly_chart(fig_scatter, use_container_width=True)
        if fig_box:
            st.plotly_chart(fig_box, use_container_width=True)

    return results_df, fig_corr, fig_scatter, fig_box

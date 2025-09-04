# @Author : Yulia
# @File   : correlation.py
# @Time   : 2025/9/3 0:37

import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import pearsonr


def render_correlation(filtered_data):
    st.subheader("🔗 Correlation Analysis")

    numeric_cols = ["Age", "SessionsPerWeek", "PlayerLevel", "InGamePurchases"]
    if not all(col in filtered_data.columns for col in numeric_cols):
        st.warning("The current data is missing the necessary numeric columns to calculate correlations.")
        return None, None, None, None

    # Calculate r & p
    results = []
    for i in range(len(numeric_cols)):
        for j in range(i + 1, len(numeric_cols)):
            col1, col2 = numeric_cols[i], numeric_cols[j]
            try:
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
            except Exception:
                continue

    if len(results) == 0:
        st.info("Insufficient data to calculate pairwise correlations.")
        return

    # Sort by: first ascending by p-value, then descending by |r|
    results_df = pd.DataFrame(results).sort_values(
        by=["Significance Level (p)", "Correlation Coefficient (r)"],
        ascending=[True, False],
        key=lambda col: col.abs() if col.name == "Correlation Coefficient (r)" else col
    ).reset_index(drop=True)

    # Highlight
    def highlight_sig(val):
        return "background-color: lightgreen" if val == "✅ YES" else "background-color: lightcoral"

    st.markdown("**📊 Correlation significance test results (sorted by p-value + correlation strength)**")
    # Supporting Styler with st.write
    st.write(results_df.style.applymap(highlight_sig, subset=["Significant Correlation?"]))

    # Heatmap
    corr_matrix = filtered_data[numeric_cols].corr()
    fig_corr = px.imshow(
        corr_matrix, text_auto=True, color_continuous_scale="RdBu_r",
        title="Numerical Variable Correlation Heatmap"
    )
    st.plotly_chart(fig_corr, use_container_width=True)

    st.divider()
    # Visualization: Scatter & Boxplot
    st.markdown("**👥 Age vs. Sessions Per Week (By Paid/Not-paid)**")
    fig_scatter, fig_box = None, None
    if "Age" in filtered_data.columns and "SessionsPerWeek" in filtered_data.columns:
        fig_scatter = px.scatter(
            filtered_data,
            x="Age", y="SessionsPerWeek",
            color=filtered_data["InGamePurchases"].map({1: "Paid", 0: "Not-paid"}),
            size="PlayerLevel",
            hover_data=["GameGenre"],
            title="Relationship between Age and Number of Sessions"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("**🎮 Game Type vs. Sessions (Boxplot)**")
    if "GameGenre" in filtered_data.columns:
        fig_box = px.box(
            filtered_data,
            x="GameGenre", y="SessionsPerWeek",
            color="GameGenre",
            title="Distribution of Sessions by Game Type"
        )
        st.plotly_chart(fig_box, use_container_width=True)
    return results_df, fig_corr, fig_scatter, fig_box
# @Author : Yulia
# @File   : correlation.py
# @Time   : 2025/9/6

import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import pearsonr, spearmanr


def render_correlation(filtered_data, render=True):
    numeric_cols = ["Age", "SessionsPerWeek", "PlayerLevel", "InGamePurchases"]
    if not all(col in filtered_data.columns for col in numeric_cols):
        if render:
            st.warning("⚠️ The current data is missing the necessary numeric columns to calculate correlations.")
        return None, None, None, None

    # calculate Pearson & Spearman
    results = []
    for i in range(len(numeric_cols)):
        for j in range(i + 1, len(numeric_cols)):
            col1, col2 = numeric_cols[i], numeric_cols[j]
            try:
                series = filtered_data[[col1, col2]].dropna()
                if len(series) < 5:
                    continue
                r_p, p_p = pearsonr(series[col1], series[col2])
                r_s, p_s = spearmanr(series[col1], series[col2])
                results.append({
                    "Variable Pairs": f"{col1} vs {col2}",
                    "Pearson r": round(r_p, 3),
                    "Pearson p": round(p_p, 4),
                    "Spearman ρ": round(r_s, 3),
                    "Spearman p": round(p_s, 4),
                    "Significant?": "✅ YES" if (p_p < 0.05 or p_s < 0.05) else "❌ NO"
                })
            except Exception:
                continue

    if len(results) == 0:
        if render:
            st.info("Insufficient data to calculate correlations.")
        return None, None, None, None

    results_df = pd.DataFrame(results).reset_index(drop=True)

    # highlight
    def highlight_sig(val):
        return "background-color: lightgreen" if val == "✅ YES" else "background-color: lightcoral"

    if render:
        st.subheader("🔗 Correlation Analysis (Pearson & Spearman)")
        st.markdown("**📊 Correlation test results** (at least one significant method is marked as ✅)")
        st.write(results_df.style.applymap(highlight_sig, subset=["Significant?"]))

        # Heatmap
        corr_matrix = filtered_data[numeric_cols].corr()
        fig_corr = px.imshow(
            corr_matrix, text_auto=True, color_continuous_scale="RdBu_r",
            title="Numerical Variable Correlation Heatmap (Pearson)"
        )
        st.plotly_chart(fig_corr, use_container_width=True)

        # Visualization: Scatter & Boxplot
        fig_scatter, fig_box = None, None
        if "Age" in filtered_data.columns and "SessionsPerWeek" in filtered_data.columns:
            fig_scatter = px.scatter(
                filtered_data,
                x="Age", y="SessionsPerWeek",
                color=filtered_data["InGamePurchases"].map({1: "Paid", 0: "Not-paid"}),
                size="PlayerLevel",
                hover_data=["GameGenre"] if "GameGenre" in filtered_data.columns else None,
                title="Age vs. Sessions Per Week (By Paid/Not-paid)"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

        if "GameGenre" in filtered_data.columns:
            fig_box = px.box(
                filtered_data,
                x="GameGenre", y="SessionsPerWeek",
                color="GameGenre",
                title="Sessions Distribution by Game Type"
            )
            st.plotly_chart(fig_box, use_container_width=True)

        return results_df, fig_corr, fig_scatter, fig_box

    return results_df, None, None, None

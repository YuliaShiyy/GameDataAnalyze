# @Author : Yulia
# @File   : simulation_trend.py
# @Time   : 2025/9/3

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


def render_trend(filtered_data, render=True):
    # Make a copy of the data to avoid contaminating the original data
    tmp = filtered_data.copy()

    if "JoinDate" not in tmp.columns:
        np.random.seed(42)
        tmp["JoinDate"] = pd.to_datetime(
            np.random.choice(pd.date_range("2024-01-01", "2024-12-31"), size=len(tmp))
        )

    tmp["Month"] = tmp["JoinDate"].dt.to_period("M").astype(str)
    if "PlayerID" not in tmp.columns:
        tmp["PlayerID"] = range(1, len(tmp) + 1)

    # Generate trend data
    trend = tmp.groupby("Month").agg({
        "PlayerID": "count",
        "InGamePurchases": "sum",
        "SessionsPerWeek": "mean"
    }).reset_index()

    trend.rename(columns={
        "PlayerID": "New Players",
        "InGamePurchases": "Paying Players",
        "SessionsPerWeek": "Average Sessions"
    }, inplace=True)

    fig_new = px.line(trend, x="Month", y="New Players", markers=True,
                      title="📈 New Players per Month")
    fig_purchase_trend = px.line(trend, x="Month", y="Paying Players", markers=True,
                                 title="💰 Paying Players per Month")
    fig_sessions_trend = px.line(trend, x="Month", y="Average Sessions", markers=True,
                                 title="🕹️ Average Sessions per Month")

    if render:
        st.subheader("📊 Simulation Trend Analysis")
        col10, col11 = st.columns(2)
        with col10:
            st.plotly_chart(fig_new, use_container_width=True)
        with col11:
            st.plotly_chart(fig_purchase_trend, use_container_width=True)
        st.plotly_chart(fig_sessions_trend, use_container_width=True)

    return fig_new, fig_purchase_trend, fig_sessions_trend

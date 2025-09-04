# @Author : Yulia
# @File   : simulation_trend.py
# @Time   : 2025/9/3 0:35

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def render_trend(filtered_data):
    st.subheader("📊 Simulation Trend Analysis")
    # Do not modify the original data, just make a copy
    tmp = filtered_data.copy()
    if "JoinDate" not in tmp.columns:
        np.random.seed(42)
        tmp["JoinDate"] = pd.to_datetime(
            np.random.choice(pd.date_range("2024-01-01", "2024-12-31"), size=len(tmp))
        )
    tmp["Month"] = tmp["JoinDate"].dt.to_period("M").astype(str)
    if "PlayerID" not in tmp.columns:
        tmp["PlayerID"] = range(1, len(tmp) + 1)

    trend = tmp.groupby("Month").agg({
        "PlayerID": "count",
        "InGamePurchases": "sum",
        "SessionsPerWeek": "mean"
    }).reset_index()

    trend.rename(columns={
        "PlayerID": "Number of new players",
        "InGamePurchases": "Number of paid players",
        "SessionsPerWeek": "Average number of sessions"
    }, inplace=True)

    col10, col11 = st.columns(2)
    with col10:
        fig_new = px.line(trend, x="Month", y="Number of new players", markers=True, title="📈 Number of New Players Per Month")
        st.plotly_chart(fig_new, use_container_width=True)
    with col11:
        fig_purchase_trend = px.line(trend, x="Month", y="Number of paid players", markers=True, title="💰 Number of Paid Players Per Month")
        st.plotly_chart(fig_purchase_trend, use_container_width=True)

    fig_sessions_trend = px.line(trend, x="Month", y="Average number of sessions", markers=True, title="🕹️ Average Number of Sessions Per Month")
    st.plotly_chart(fig_sessions_trend, use_container_width=True)
    return fig_sessions_trend
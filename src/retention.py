# @Author : Yulia
# @File   : retention.py
# @Time   : 2025/9/3 0:29

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render_retention_funnel(filtered_data, render=True):
    total_players = len(filtered_data)
    day1_retained = (filtered_data['SessionsPerWeek'] >= 1).sum() / total_players if total_players else 0
    day7_retained = (filtered_data['SessionsPerWeek'] >= 2).sum() / total_players if total_players else 0
    day30_retained = (filtered_data['SessionsPerWeek'] >= 4).sum() / total_players if total_players else 0

    retention = pd.DataFrame({
        "Day": ["Day1", "Day7", "Day30"],
        "RetentionRate": [day1_retained, day7_retained, day30_retained]
    })
    fig_retention = px.bar(retention, x="Day", y="RetentionRate",
                           text=[f"{x:.1%}" for x in retention["RetentionRate"]],
                           title="Player Retention Rate")

    funnel_stages = {
        "All Players": total_players,
        "Active (≥2/wk)": (filtered_data['SessionsPerWeek'] >= 2).sum(),
        "Highly Engaged": (filtered_data['EngagementLevel'] == "High").sum(),
        "Paying Players": filtered_data['InGamePurchases'].sum()
    }
    fig_funnel = go.Figure(go.Funnel(
        y=list(funnel_stages.keys()),
        x=list(funnel_stages.values()),
        textinfo="value+percent initial"
    ))

    if render:
        st.subheader("📈 Retention & Funnel")
        st.plotly_chart(fig_retention, use_container_width=True)
        st.plotly_chart(fig_funnel, use_container_width=True)

    return fig_retention, fig_funnel

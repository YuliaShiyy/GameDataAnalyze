# @Author : Yulia
# @File   : retention.py
# @Time   : 2025/9/3 0:29

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def render_retention_funnel(filtered_data):
    st.subheader("📈 Retention analysis (based on SessionsPerWeek)")
    total_players = len(filtered_data)
    if total_players > 0:
        day1_retained = (filtered_data['SessionsPerWeek'] >= 1).sum() / total_players
        day7_retained = (filtered_data['SessionsPerWeek'] >= 2).sum() / total_players
        day30_retained = (filtered_data['SessionsPerWeek'] >= 4).sum() / total_players

        retention = pd.DataFrame({
            "Day": ["Day1", "Day7", "Day30"],
            "RetentionRate": [day1_retained, day7_retained, day30_retained]
        })

        fig_retention = px.bar(
            retention, x="Day", y="RetentionRate",
            text=[f"{x:.1%}" for x in retention["RetentionRate"]],
            title="Player Retention Rate"
        )
        st.plotly_chart(fig_retention, use_container_width=True)
    else:
        st.warning("There is no player data under the current filter conditions, so retention rate cannot be calculated.")

    st.divider()
    st.subheader("🔻 Funnel Analysis: Player → Active → High Engagement → Paying")
    funnel_stages = {
        "All Players": total_players,
        "Active Players (≥2 times/week)": (filtered_data['SessionsPerWeek'] >= 2).sum(),
        "Highly Engaged Players": (filtered_data['EngagementLevel'] == "High").sum(),
        "Paying Players": filtered_data['InGamePurchases'].sum()
    }
    fig_funnel = go.Figure(go.Funnel(
        y=list(funnel_stages.keys()),
        x=list(funnel_stages.values()),
        textinfo="value+percent initial"
    ))
    st.plotly_chart(fig_funnel, use_container_width=True)
    return fig_retention, fig_funnel
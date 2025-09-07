# @Author : Yulia
# @File   : overview.py
# @Time   : 2025/9/3 0:28

import streamlit as st
import plotly.express as px

def render_overview(filtered_data, selected_region, render=True):
    metrics = {
        "Total number of players": len(filtered_data),
        "Average age": round(filtered_data["Age"].mean(), 1),
        "Proportion of paying players": f"{filtered_data['InGamePurchases'].mean()*100:.1f}%",
        "Average number of sessions": round(filtered_data["SessionsPerWeek"].mean(), 1),
        "Proportion of highly engaged players": f"{(filtered_data['EngagementLevel'] == 'High').mean()*100:.1f}%"
    }

    # figs
    fig_location = px.histogram(filtered_data, x="Location", title=f"Geography ({selected_region})", text_auto=True)
    fig_age = px.histogram(filtered_data, x="Age", nbins=20, title="Age Distribution")
    fig_gender = px.pie(filtered_data, names="Gender", title="Gender Distribution")
    fig_sessions = px.histogram(filtered_data, x="SessionsPerWeek", title="Weekly Sessions")
    fig_engagement = px.pie(filtered_data, names="EngagementLevel", title="Engagement Level")
    fig_purchase = px.histogram(filtered_data, x="PlayerLevel", color="InGamePurchases",
                                barmode="group", title="Paying Players by Level")
    fig_genre_purchase = px.histogram(filtered_data, x="GameGenre", color="InGamePurchases",
                                      barmode="group", title="Paying Players by Game Type")

    figs = {
        "Geography": fig_location,
        "Age": fig_age,
        "Gender": fig_gender,
        "Weekly Sessions": fig_sessions,
        "Engagement Level": fig_engagement,
        "Level vs Payment": fig_purchase,
        "Genre vs Payment": fig_genre_purchase
    }

    if render:
        st.subheader("🧭 Overview")
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total number of players", metrics["Total number of players"])
        col2.metric("Average age", metrics["Average age"])
        col3.metric("Proportion of paying players", metrics["Proportion of paying players"])
        col4.metric("Average number of sessions", metrics["Average number of sessions"])
        col5.metric("Proportion of highly engaged players", metrics["Proportion of highly engaged players"])

        st.divider()
        st.plotly_chart(fig_location, use_container_width=True)
        st.plotly_chart(fig_age, use_container_width=True)
        st.plotly_chart(fig_gender, use_container_width=True)
        st.plotly_chart(fig_sessions, use_container_width=True)
        st.plotly_chart(fig_engagement, use_container_width=True)
        st.plotly_chart(fig_purchase, use_container_width=True)
        st.plotly_chart(fig_genre_purchase, use_container_width=True)

    return metrics, figs


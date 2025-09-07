# @Author : Yulia
# @File   : clustering.py
# @Time   : 2025/9/3

import streamlit as st
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


def render_clustering(filtered_data, render=True):
    needed = ["Age", "SessionsPerWeek", "PlayerLevel"]
    if not all(c in filtered_data.columns for c in needed):
        if render:
            st.warning("❌ Cluster analysis cannot be performed because the columns required for clustering are missing.")
        return None, None

    data_clu = filtered_data[needed].dropna()
    if len(data_clu) <= 10:
        if render:
            st.warning("⚠️ The amount of data is insufficient to perform cluster analysis.")
        return None, None

    # Standardization + KMeans
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(data_clu)

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)

    data_show = data_clu.copy()
    data_show["Cluster"] = labels

    # 3D clustering results
    fig_cluster = px.scatter_3d(
        data_show, x="Age", y="SessionsPerWeek", z="PlayerLevel",
        color="Cluster", title="Player Clustering (3D Results)"
    )

    # Cluster mean
    cluster_summary = data_show.groupby("Cluster").mean(numeric_only=True).round(2)

    if render:
        st.subheader("🧩 Player Cluster Analysis (KMeans)")
        st.plotly_chart(fig_cluster, use_container_width=True)
        st.write("**📊 Average Value of Each Cluster:**")
        st.dataframe(cluster_summary, use_container_width=True)

    return fig_cluster, cluster_summary

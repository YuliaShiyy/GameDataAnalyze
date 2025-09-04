# @Author : Yulia
# @File   : clustering.py
# @Time   : 2025/9/3 0:39

import streamlit as st
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def render_clustering(filtered_data):
    st.subheader("🧩 Player Cluster Analysis (KMeans)")

    # Numerical features
    needed = ["Age", "SessionsPerWeek", "PlayerLevel"]
    if not all(c in filtered_data.columns for c in needed):
        st.warning("Cluster analysis cannot be performed because the columns required for clustering are missing.")
        return

    data_clu = filtered_data[needed].dropna()
    if len(data_clu) <= 10:
        st.warning("The amount of data is insufficient to perform cluster analysis.")
        return

    # Standardization + KMeans
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(data_clu)

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)

    data_show = data_clu.copy()
    data_show["Cluster"] = labels

    fig_cluster = px.scatter_3d(
        data_show, x="Age", y="SessionsPerWeek", z="PlayerLevel",
        color="Cluster", title="Player Clustering (3D Clustering Results)"
    )
    st.plotly_chart(fig_cluster, use_container_width=True)

    st.write("**The Average Eigenvalue of Each Cluster：**")
    st.dataframe(data_show.groupby("Cluster").mean(numeric_only=True).round(2), use_container_width=True)
    return fig_cluster

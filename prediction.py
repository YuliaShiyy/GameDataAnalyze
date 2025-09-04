# @Author : Yulia
# @File   : prediction.py
# @Time   : 2025/9/3 0:41

import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix

def render_prediction(filtered_data):
    st.subheader("🤖 Player Spending Prediction Model (Logistic Regression)")

    needed = ["Age", "SessionsPerWeek", "PlayerLevel", "InGamePurchases"]
    if not all(c in filtered_data.columns for c in needed):
        st.warning("The columns required for modeling are missing and the predictive model cannot be trained.")
        return None, None

    model_data = filtered_data[needed].dropna()
    if len(model_data) <= 50:
        st.warning("There is insufficient data under the current filtering conditions to train a prediction model.")
        return None, None

    X = model_data[["Age", "SessionsPerWeek", "PlayerLevel"]]
    y = model_data["InGamePurchases"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    st.metric("Model Accuracy", f"{acc*100:.2f}%")

    # Confusion matrix (fix label order to avoid errors when there is only one class)
    cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
    cm_df = pd.DataFrame(cm, index=["Actual: Not-paid", "Actual: Paid"], columns=["Prediction: Not-paid", "Prediction: Paid"])

    fig_cm = px.imshow(cm_df, text_auto=True, color_continuous_scale="Blues", title="Confusion Matrix")
    st.plotly_chart(fig_cm, use_container_width=True)
    return acc, fig_cm
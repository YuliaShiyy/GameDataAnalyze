# @Author : Yulia
# @File   : data_loader.py
# @Time   : 2025/9/1 22:33

import pandas as pd

def load_data():
    df = pd.read_csv("gaming_data_cleaned.csv")
    df_europe = pd.read_csv("gaming_data_europe.csv")
    return df, df_europe

def filter_data(df, selected_region, genres, genders, purchase_filter):
    if selected_region == "Global":
        filtered_data = df.copy()
    else:
        filtered_data = df[df['Location'] == selected_region].copy()

    if genres:
        filtered_data = filtered_data[filtered_data["GameGenre"].isin(genres)].copy()

    if genders:
        filtered_data = filtered_data[filtered_data["Gender"].isin(genders)].copy()

    if purchase_filter == "Paid players":
        filtered_data = filtered_data[filtered_data["InGamePurchases"] == 1].copy()
    elif purchase_filter == "Not-paid players":
        filtered_data = filtered_data[filtered_data["InGamePurchases"] == 0].copy()

    return filtered_data

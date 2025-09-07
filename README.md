# 🎮 Player Behavior Analysis Dashboard

An interactive dashboard built with **Streamlit** and **Plotly** for analyzing online gaming behavior data.  
This project is part of my portfolio and demonstrates skills in **data engineering, data analysis, and visualization**.

---

## 🚀 Features

✅ **Overview**: Core metrics (players, age, sessions, engagement, payment) and demographic distribution  
✅ **Retention & Funnel Analysis**: Simulated day-1, day-7, day-30 retention; conversion funnel  
✅ **Trend Simulation**: Monthly new players, paying players, average sessions  
✅ **Correlation Analysis**: Pearson correlation, heatmap, scatter plots, boxplots  
✅ **Cluster Analysis (KMeans)**: Player segmentation by Age / Sessions / Level  
✅ **Predictive Modeling (Logistic Regression)**: Predicting paying players  
✅ **Export Report (PDF)**: Export current page’s metrics, charts, and analysis  

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) – Interactive UI
- [Pandas](https://pandas.pydata.org/) – Data manipulation
- [Plotly](https://plotly.com/python/) – Interactive charts
- [Scikit-learn](https://scikit-learn.org/) – Clustering & prediction
- [SciPy](https://scipy.org/) – Statistical tests
- [ReportLab](https://www.reportlab.com/) – PDF export
- [Kaleido](https://github.com/plotly/Kaleido) – Save Plotly charts as images

---

## 📂 Project Structure
    Game_Data_Analyze/
    │── data/ # Datasets
    │ ├── gaming_data_cleaned.csv
    │ ├── gaming_data_europe.csv
    │ └── online_gaming_behavior_dataset.csv
    │
    │── notebooks/ # Jupyter notebooks
    │ └── data_clean.ipynb
    │
    │── src/ # Source code
    │ ├── app.py # Main dashboard entry
    │ ├── clustering.py # Cluster analysis module
    │ ├── correlation.py # Correlation analysis module
    │ ├── data_loader.py # Data loading & preprocessing
    │ ├── overview.py # Overview module
    │ ├── prediction.py # Predictive modeling
    │ ├── report_export.py # Export to PDF
    │ ├── retention.py # Retention & funnel analysis
    │ └── simulation_trend.py # Trend simulation
    │
    │── requirements.txt # Dependencies
    │── README.md # Project documentation

---

## 📊 Example Dashboard
### Overview
![overview](assets/overview.png)

### Retention & Funnel
![retention](assets/retention&funnel.png)

### Simulation Trend
![correlation](assets/simulation_trend.png)


---

## ⚡ Installation

Clone this repo and install dependencies:

    ```bash
    git clone https://github.com/YuliaShiyy/Game_Data_Analyze.git
    cd Game_Data_Analyze
    pip install -r requirements.txt
---

## ▶️ Usage

Run the Streamlit app:

    streamlit run app.py

--- 

## 📂 Data

Dataset used: Kaggle - Predict Online Gaming Behaviour Dataset
.
For demo purposes, pre-cleaned datasets are placed in the data/ folder.

## 📌 To Do / Possible Extensions

    · Add time-series forecasting for player retention
    
    · Deploy the dashboard online (e.g., Streamlit Cloud / Heroku)
    
    · Add more machine learning models (e.g., Random Forest, XGBoost)
    
    · Multi-language support 

# Sales Forecasting & Demand Intelligence System

Internship Project - Week 3 & 4

Live Deployment - https://salesforcast-rishabh.streamlit.app/

---

## What This Project Does

This project builds an end-to-end sales forecasting and demand intelligence system
using 4 years of superstore sales data. It predicts future product demand, detects
unusual sales patterns, segments products by demand behavior and presents everything
through a live interactive dashboard.

---

## Folder Structure

```
SalesForecasting_RishabhPatidar/
│
├── analysis.ipynb        # Main notebook with all 8 tasks
├── train.csv             # Superstore sales dataset (2015-2018)
├── app.py                # Streamlit dashboard code
├── requirements.txt      # Python libraries for deployment
├── summary.pdf           # 2-page executive business report
├── README.md             # This file
│
└── charts/
    ├── revenue_by_category.png
    ├── region_yearly_growth.png
    ├── shipping_by_region.png
    ├── monthly_seasonality.png
    ├── monthly_trend.png
    ├── decomposition.png
    ├── acf_pacf.png
    ├── sarima_forecast.png
    ├── prophet_forecast.png
    ├── xgboost_forecast.png
    ├── stacking_forecast.png
    ├── segment_forecasts.png
    ├── anomaly_isolation_forest.png
    ├── anomaly_zscore.png
    ├── anomaly_comparison.png
    ├── elbow_method.png
    └── clustering_pca.png
```

---

## How to Run the Notebook

1. Install required libraries:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn xgboost prophet statsmodels pmdarima imbalanced-learn
```

2. Place train.csv in the same folder as the notebook

3. Open analysis.ipynb in Jupyter Notebook or Google Colab

4. Run all cells from top to bottom

---

## How to Run the Dashboard Locally

```bash
pip install streamlit pandas numpy plotly scikit-learn
streamlit run app.py
```

Make sure train.csv is in the same folder as app.py

---

## Live Dashboard

The dashboard is deployed on Streamlit Community Cloud with 4 pages:

- Overview - total revenue, monthly trend, category and region breakdown
- Forecast - 3 month sales forecast using our best Stacking model
- Anomaly Report - unusual sales weeks detected by Isolation Forest and Z-Score
- Segments - product demand clusters with stocking recommendations

---

## What Each Task Does

| Task | What it covers |
|------|---------------|
| Task 1 | Load data, parse dates, extract time features, answer 4 business questions |
| Task 2 | Time series decomposition, stationarity test, differencing |
| Task 3 | SARIMA, Prophet, XGBoost, Weighted Ensemble, Stacking model |
| Task 4 | Best model applied to 5 segments (3 categories + 2 regions) |
| Task 5 | Anomaly detection using Isolation Forest and Z-Score |
| Task 6 | KMeans clustering, elbow method, PCA visualization |
| Task 7 | Streamlit dashboard with 4 pages deployed on Streamlit Cloud |
| Task 8 | 2-page executive business report in plain English |

---

## Final Model - Stacking Ensemble

We tested 5 approaches and the Stacking model came out best:

| Model | MAPE |
|-------|------|
| SARIMA | 21.94% |
| Prophet | 21.89% |
| XGBoost | 18.01% |
| Weighted Ensemble | 15.85% |
| Stacking (Final) | 4.70% |

The Stacking model combines SARIMA, Prophet and XGBoost predictions using
a Linear Regression meta model that learns the optimal weights automatically.
A MAPE of 4.70% puts this in the excellent range for monthly retail forecasting.

---

## Key Findings

- Technology generates the highest total revenue across all categories
- West region has the most consistent year over year growth
- November and December consistently drive the highest monthly sales
- Copiers grew 479% over 4 years and is the highest growth product
- Machines declined 29% and is the biggest stocking risk
- Isolation Forest detected 10 anomalous sales weeks across 4 years

---

## Dataset Source

Superstore Sales Dataset
https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting
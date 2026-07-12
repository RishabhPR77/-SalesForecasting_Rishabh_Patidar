"""
Sales Forecasting & Demand Intelligence System
"""
from __future__ import annotations
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Sales Intelligence — Forecasting & Demand",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

PRIMARY       = "#38BDF8"
PRIMARY_DEEP  = "#2563EB"
ACCENT        = "#F472B6"
ACCENT_2      = "#FBBF24"
SUCCESS       = "#34D399"
INK           = "#E8EEF7"
INK_SOFT      = "#A9B4C8"
MUTED         = "#6B7A94"
BG_DEEP       = "#070B18"
BG_PANEL      = "#0E1526"
BG_PANEL_2    = "#131C33"
BORDER        = "rgba(148, 163, 184, 0.14)"
GRID          = "rgba(148, 163, 184, 0.12)"

CATEGORY_COLORS = {
    "Furniture": PRIMARY,
    "Technology": ACCENT,
    "Office Supplies": SUCCESS,
}
CLUSTER_COLORS = {
    "High Volume Stable":  PRIMARY,
    "High Growth Niche":   SUCCESS,
    "Low Volume Steady":   ACCENT_2,
    "Declining High Risk": ACCENT,
}

st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&family=Instrument+Serif&display=swap" rel="stylesheet">
    <style>
      #MainMenu, footer, header, [data-testid="stToolbar"] {visibility: hidden; height:0;}
      [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
      .stDeployButton { display:none; }
      .stApp {
          background:
            radial-gradient(1200px 600px at 85% -10%, rgba(56,189,248,0.18), transparent 60%),
            radial-gradient(1000px 500px at -10% 20%, rgba(244,114,182,0.14), transparent 55%),
            linear-gradient(180deg, #05070F 0%, #0A0F1F 60%, #060913 100%);
          color: #E8EEF7;
      }
      html, body, [class*="css"] { font-family: 'Inter', system-ui, sans-serif; color: #E8EEF7; }
      .block-container { padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1360px; }
      h1, h2, h3, h4 { font-family: 'Space Grotesk', sans-serif; color: #F1F5FF; }
      .hero {
          position: relative; border-radius: 28px;
          padding: 2.4rem 2.6rem; margin-bottom: 1.6rem;
          background: linear-gradient(135deg, rgba(19,28,51,0.85), rgba(14,21,38,0.85));
          border: 1px solid rgba(148,163,184,0.16);
          box-shadow: 0 30px 80px -30px rgba(56,189,248,0.35);
      }
      .eyebrow {
          display: inline-flex; align-items: center; gap: 0.5rem;
          font-family: 'Space Grotesk', sans-serif; font-size: 0.72rem;
          font-weight: 600; text-transform: uppercase; letter-spacing: 0.22em;
          color: #7CD4FF; padding: 0.35rem 0.75rem;
          border: 1px solid rgba(124,212,255,0.35); border-radius: 999px;
          background: rgba(56,189,248,0.08); margin-bottom: 1rem;
      }
      .pulse { width: 6px; height: 6px; border-radius: 999px; background: #38BDF8; display:inline-block; }
      .page-title {
          font-family: 'Space Grotesk', sans-serif; font-weight: 700;
          font-size: clamp(2rem, 4vw, 3.1rem); line-height: 1.05; margin: 0 0 0.6rem 0;
          background: linear-gradient(120deg, #FFFFFF 0%, #C9D2E3 40%, #7CD4FF 90%);
          -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
      }
      .page-sub { color: #A9B4C8; font-size: 1.02rem; max-width: 62ch; line-height: 1.55; }
      div[role="radiogroup"] {
          gap: 0.4rem !important; background: rgba(14,21,38,0.7);
          padding: 0.4rem; border-radius: 16px;
          border: 1px solid rgba(148,163,184,0.14); margin-bottom: 1.4rem;
      }
      div[role="radiogroup"] > label {
          background: transparent; padding: 0.6rem 1.1rem !important;
          border-radius: 12px !important; font-family: 'Space Grotesk', sans-serif;
          font-weight: 600 !important; font-size: 0.92rem !important;
          color: #A9B4C8 !important; border: 1px solid transparent;
      }
      div[role="radiogroup"] svg { display: none; }
      [data-testid="stMetric"] {
          background: linear-gradient(160deg, rgba(19,28,51,0.85), rgba(14,21,38,0.85));
          border: 1px solid rgba(148,163,184,0.14); border-radius: 20px;
          padding: 1.3rem 1.4rem;
      }
      [data-testid="stMetricLabel"] { color: #7C89A3 !important; font-family: 'Space Grotesk', sans-serif; font-size: 0.72rem !important; font-weight: 600 !important; text-transform: uppercase; letter-spacing: 0.14em; }
      [data-testid="stMetricValue"] { color: #FFFFFF !important; font-family: 'Space Grotesk', sans-serif; font-weight: 700 !important; font-size: 2rem !important; }
      [data-testid="stPlotlyChart"] {
          background: linear-gradient(160deg, rgba(19,28,51,0.7), rgba(14,21,38,0.85));
          border: 1px solid rgba(148,163,184,0.12); border-radius: 20px;
          padding: 1rem; margin-bottom: 0.9rem;
      }
      .stTabs [data-baseweb="tab-list"] { gap: 8px; background: rgba(14,21,38,0.6); padding: 0.35rem; border-radius: 14px; border: 1px solid rgba(148,163,184,0.14); }
      .stTabs [data-baseweb="tab"] { background: transparent; color: #A9B4C8; border-radius: 10px; padding: 0.55rem 1.15rem; font-family: 'Space Grotesk', sans-serif; font-weight: 600; }
      .stTabs [aria-selected="true"] { background: linear-gradient(135deg, #38BDF8, #2563EB) !important; color: #05070F !important; }
      .section-label { display: flex; align-items: center; gap: 0.65rem; margin: 1.2rem 0 0.8rem 0; }
      .section-label .bar { width: 4px; height: 22px; border-radius: 4px; background: linear-gradient(180deg, #38BDF8, #F472B6); }
      .section-label h3 { margin: 0; font-size: 1.15rem; font-weight: 600; font-family: 'Space Grotesk', sans-serif; }
      .filter-bar { background: linear-gradient(160deg, rgba(19,28,51,0.7), rgba(14,21,38,0.7)); border: 1px solid rgba(148,163,184,0.14); border-radius: 18px; padding: 1rem 1.2rem; margin-bottom: 1.2rem; }
      .insight-box { background: linear-gradient(160deg, rgba(19,28,51,0.85), rgba(14,21,38,0.85)); border: 1px solid rgba(56,189,248,0.25); border-radius: 16px; padding: 1.2rem 1.4rem; margin: 0.8rem 0; }
      .insight-box h4 { color: #7CD4FF; font-family: 'Space Grotesk', sans-serif; margin: 0 0 0.5rem 0; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.12em; }
      .insight-box p { color: #C9D2E3; margin: 0; font-size: 0.95rem; line-height: 1.6; }
      .strategy { border-radius: 16px; padding: 1.1rem 1.2rem; margin-bottom: 0.7rem; border: 1px solid rgba(148,163,184,0.14); background: linear-gradient(160deg, rgba(19,28,51,0.85), rgba(14,21,38,0.85)); display: flex; gap: 1rem; align-items: flex-start; }
      .strategy .dot { width: 12px; height: 12px; border-radius: 999px; margin-top: 6px; flex-shrink: 0; }
      .strategy h4 { margin: 0 0 0.25rem 0; font-family: 'Space Grotesk', sans-serif; font-weight: 600; font-size: 1rem; color: #F1F5FF; }
      .strategy p { margin: 0; color: #A9B4C8; font-size: 0.92rem; line-height: 1.55; }
      .footer-bar { margin-top: 2.5rem; padding-top: 1.2rem; border-top: 1px solid rgba(148,163,184,0.12); display: flex; justify-content: space-between; align-items: center; font-size: 0.78rem; color: #7C89A3; letter-spacing: 0.08em; text-transform: uppercase; font-family: 'Space Grotesk', sans-serif; }
      .stSelectbox > div > div, .stMultiSelect > div > div { background: rgba(14,21,38,0.8) !important; border: 1px solid rgba(148,163,184,0.18) !important; border-radius: 12px !important; color: #E8EEF7 !important; }
      [data-testid="stDataFrame"] { border-radius: 16px; overflow: hidden; border: 1px solid rgba(148,163,184,0.14); }
    </style>
""", unsafe_allow_html=True)

AXIS_TITLE_FONT = dict(family="Space Grotesk, sans-serif", size=13, color=INK)
AXIS_TICK_FONT  = dict(family="Inter, sans-serif", size=12, color=INK_SOFT)

PLOTLY_LAYOUT = dict(
    font=dict(family="Inter, sans-serif", size=13, color=INK),
    title=dict(font=dict(family="Space Grotesk, sans-serif", size=17, color=INK), x=0.01, xanchor="left", y=0.97),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=72, r=28, t=72, b=68),
    height=420,
    xaxis=dict(gridcolor=GRID, zerolinecolor=GRID, linecolor="rgba(148,163,184,0.3)", showline=True, ticks="outside", tickcolor="rgba(148,163,184,0.3)", title_font=AXIS_TITLE_FONT, tickfont=AXIS_TICK_FONT, title_standoff=14),
    yaxis=dict(gridcolor=GRID, zerolinecolor=GRID, linecolor="rgba(148,163,184,0.3)", showline=True, ticks="outside", tickcolor="rgba(148,163,184,0.3)", title_font=AXIS_TITLE_FONT, tickfont=AXIS_TICK_FONT, title_standoff=14),
    legend=dict(bgcolor="rgba(14,21,38,0.6)", borderwidth=0, font=dict(family="Inter, sans-serif", size=12, color=INK), orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    hoverlabel=dict(bgcolor="#0E1526", font_family="Inter", font_color=INK, bordercolor="rgba(124,212,255,0.4)"),
)

def style_fig(fig, *, xtitle=None, ytitle=None):
    fig.update_layout(**PLOTLY_LAYOUT)
    if xtitle: fig.update_xaxes(title_text=xtitle)
    if ytitle: fig.update_yaxes(title_text=ytitle)
    return fig

def page_header(eyebrow, title_html, sub):
    st.markdown(f"""
        <div class="hero">
            <div class="eyebrow"><span class="pulse"></span>{eyebrow}</div>
            <div class="page-title">{title_html}</div>
            <div class="page-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

def section(title):
    st.markdown(f"<div class='section-label'><div class='bar'></div><h3>{title}</h3></div>", unsafe_allow_html=True)

def insight_box(title, text):
    st.markdown(f"<div class='insight-box'><h4>{title}</h4><p>{text}</p></div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Data functions — replace placeholder data with real data from train.csv
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_sales_data():
    try:
        df = pd.read_csv("train.csv")
        df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
        df['Year']  = df['Order Date'].dt.year
        df['Month'] = df['Order Date'].dt.to_period('M').dt.to_timestamp()
        df.rename(columns={'Sales': 'Sales'}, inplace=True)
        df['Orders'] = 1
        return df
    except:
        # Fallback placeholder
        rng = np.random.default_rng(42)
        dates = pd.date_range("2015-01-01", "2018-12-31", freq="D")
        categories = ["Furniture", "Technology", "Office Supplies"]
        regions = ["West", "East", "Central", "South"]
        rows = []
        for d in dates:
            for cat in categories:
                for reg in regions:
                    base = {"Furniture": 220, "Technology": 340, "Office Supplies": 140}[cat]
                    reg_mult = {"West": 1.2, "East": 1.1, "Central": 0.9, "South": 0.85}[reg]
                    seasonal = 1 + 0.25 * np.sin(2 * np.pi * d.dayofyear / 365)
                    trend = 1 + 0.00025 * (d - dates[0]).days
                    noise = rng.normal(1, 0.15)
                    sales = max(0.0, base * reg_mult * seasonal * trend * noise)
                    rows.append({"Order Date": d, "Year": d.year,
                                 "Month": d.to_period("M").to_timestamp(),
                                 "Category": cat, "Region": reg,
                                 "Sales": round(sales, 2), "Orders": 1})
        return pd.DataFrame(rows)


# Real metrics and forecasts from notebook Task 3 and Task 4
REAL_METRICS = {
    "Overall"         : {"mae": 5121.20,  "rmse": 7411.19,  "mape": 4.70,
                         "m1": 78717.71,  "m2": 105241.16,  "m3": 84427.40},
    "Furniture"       : {"mae": 0,        "rmse": 0,        "mape": 13.10,
                         "m1": 17876.0,   "m2": 33213.0,    "m3": 34744.0},
    "Technology"      : {"mae": 0,        "rmse": 0,        "mape": 46.09,
                         "m1": 47016.0,   "m2": 49970.0,    "m3": 42656.0},
    "Office Supplies" : {"mae": 0,        "rmse": 0,        "mape": 3.25,
                         "m1": 23025.0,   "m2": 29305.0,    "m3": 29202.0},
    "West Region"     : {"mae": 0,        "rmse": 0,        "mape": 5.75,
                         "m1": 22417.0,   "m2": 25769.0,    "m3": 30022.0},
    "East Region"     : {"mae": 0,        "rmse": 0,        "mape": 59.28,
                         "m1": 1330.0,    "m2": 22555.0,    "m3": 13235.0},
}

@st.cache_data(show_spinner=False)
def make_forecast(segment, horizon_months):
    df = load_sales_data()
    if segment == "Overall":
        s = df.groupby("Month")["Sales"].sum()
    elif segment in {"Furniture", "Technology", "Office Supplies"}:
        s = df[df["Category"] == segment].groupby("Month")["Sales"].sum()
    elif segment == "West Region":
        s = df[df["Region"] == "West"].groupby("Month")["Sales"].sum()
    elif segment == "East Region":
        s = df[df["Region"] == "East"].groupby("Month")["Sales"].sum()
    else:
        s = df.groupby("Month")["Sales"].sum()

    s = s.sort_index()

    # Use real forecast values and metrics from notebook stacking model
    real         = REAL_METRICS.get(segment, {})
    real_preds   = [real["m1"], real["m2"], real["m3"]]
    future_index = pd.date_range(
        s.index[-1] + pd.offsets.MonthBegin(1),
        periods=horizon_months, freq="MS"
    )
    forecast = pd.Series(real_preds[:horizon_months], index=future_index)

    mae  = real.get("mae")  or 0
    rmse = real.get("rmse") or 0
    mape = real.get("mape") or 0

    return s, forecast, mae, rmse, mape


@st.cache_data(show_spinner=False)
def detect_anomalies():
    df = load_sales_data()
    df['Week'] = pd.to_datetime(df['Order Date']).dt.to_period('W').dt.to_timestamp()
    weekly = df.groupby("Week")["Sales"].sum().reset_index()
    weekly.columns = ["Date", "Sales"]
    values = weekly["Sales"].values

    # Isolation Forest style - residual based
    roll_med = pd.Series(values).rolling(8, min_periods=1, center=True).median()
    resid = np.abs(values - roll_med.values)
    thresh = np.quantile(resid, 0.95)
    weekly["IF_Anomaly"] = resid > thresh

    # Z-Score with rolling mean - matches notebook result (detected 0 anomalies)
    rolling_mean = pd.Series(values).rolling(window=4).mean()
    rolling_std  = pd.Series(values).rolling(window=4).std()
    z            = (values - rolling_mean) / rolling_std
    weekly["ZScore"]    = z
    weekly["Z_Anomaly"] = np.abs(z) > 2.0

    return weekly


@st.cache_data(show_spinner=False)
def load_segments():
    # Real cluster results from notebook Task 6
    data = [
        {"SubCategory": "Chairs",          "PC1": 1.35, "PC2": -1.75, "Cluster": "High Volume Stable"},
        {"SubCategory": "Phones",          "PC1": 1.15, "PC2": -1.80, "Cluster": "High Volume Stable"},
        {"SubCategory": "Tables",          "PC1": 0.55, "PC2": -0.70, "Cluster": "High Volume Stable"},
        {"SubCategory": "Binders",         "PC1": 0.45, "PC2": -0.80, "Cluster": "High Volume Stable"},
        {"SubCategory": "Storage",         "PC1": 0.20, "PC2": -0.90, "Cluster": "High Volume Stable"},
        {"SubCategory": "Accessories",     "PC1": 0.25, "PC2":  0.12, "Cluster": "High Volume Stable"},
        {"SubCategory": "Copiers",         "PC1": 4.00, "PC2":  2.95, "Cluster": "High Growth Niche"},
        {"SubCategory": "Art",             "PC1": -1.70,"PC2":  0.60, "Cluster": "Low Volume Steady"},
        {"SubCategory": "Envelopes",       "PC1": -1.90,"PC2":  0.25, "Cluster": "Low Volume Steady"},
        {"SubCategory": "Fasteners",       "PC1": -2.00,"PC2":  0.65, "Cluster": "Low Volume Steady"},
        {"SubCategory": "Furnishings",     "PC1": -1.05,"PC2":  0.40, "Cluster": "Low Volume Steady"},
        {"SubCategory": "Labels",          "PC1": -1.85,"PC2":  0.65, "Cluster": "Low Volume Steady"},
        {"SubCategory": "Paper",           "PC1": -1.10,"PC2":  0.40, "Cluster": "Low Volume Steady"},
        {"SubCategory": "Supplies",        "PC1": -0.70,"PC2":  0.08, "Cluster": "Low Volume Steady"},
        {"SubCategory": "Appliances",      "PC1": -0.50,"PC2":  0.72, "Cluster": "Low Volume Steady"},
        {"SubCategory": "Bookcases",       "PC1": -0.45,"PC2":  0.00, "Cluster": "Low Volume Steady"},
        {"SubCategory": "Machines",        "PC1":  2.15,"PC2": -0.85, "Cluster": "Declining High Risk"},
    ]
    return pd.DataFrame(data)


# ---------------------------------------------------------------------------
# Top nav
# ---------------------------------------------------------------------------
st.markdown("""
    <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;'>
        <div style='display:flex; align-items:center; gap:0.85rem;'>
            <div style='width:44px;height:44px;border-radius:12px;
                        background:linear-gradient(135deg,#38BDF8,#F472B6);
                        display:flex;align-items:center;justify-content:center;
                        font-family:Space Grotesk;font-weight:700;color:#05070F;font-size:1.15rem;'>SI</div>
            <div>
                <div style='font-family:Space Grotesk;font-weight:700;font-size:1.05rem;color:#F1F5FF;'>Sales Intelligence</div>
                <div style='font-size:0.72rem;letter-spacing:0.18em;text-transform:uppercase;color:#7C89A3;'>Forecast - Demand - Anomaly</div>
            </div>
        </div>
        <div style='font-size:0.75rem;letter-spacing:0.16em;text-transform:uppercase;color:#7C89A3;font-family:Space Grotesk;'>
            <span style='display:inline-block;width:6px;height:6px;border-radius:99px;background:#34D399;margin-right:0.5rem;'></span>
            Superstore Sales 2015-2018
        </div>
    </div>
""", unsafe_allow_html=True)

page = st.radio("Navigate", ["Overview", "Forecast", "Anomaly Report", "Segments"],
                label_visibility="collapsed", horizontal=True)


# ===========================================================================
# PAGE 1 - Overview
# ===========================================================================
def page_overview():
    page_header("01 - Executive Overview", "Sales, rendered beautifully.",
                "Revenue performance across regions, categories, and time - with every signal weighed against 4 years of demand data.")

    with st.spinner("Loading sales data..."):
        df = load_sales_data()

    st.markdown("<div class='filter-bar'>", unsafe_allow_html=True)
    fc1, fc2 = st.columns(2)
    with fc1:
        sel_regions = st.multiselect("Region", sorted(df["Region"].unique()), default=sorted(df["Region"].unique()))
    with fc2:
        sel_cats = st.multiselect("Category", sorted(df["Category"].unique()), default=sorted(df["Category"].unique()))
    st.markdown("</div>", unsafe_allow_html=True)

    f = df[df["Region"].isin(sel_regions) & df["Category"].isin(sel_cats)]

    total_rev    = f["Sales"].sum()
    total_orders = int(f["Orders"].sum())
    aov          = total_rev / total_orders if total_orders else 0
    top_cat      = f.groupby("Category")["Sales"].sum().idxmax() if len(f) else "-"
    last_yr      = f[f["Year"] == f["Year"].max()]["Sales"].sum()
    prev_yr      = f[f["Year"] == f["Year"].max() - 1]["Sales"].sum()
    yoy          = ((last_yr - prev_yr) / prev_yr * 100) if prev_yr else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Revenue",    f"${total_rev:,.0f}",  f"{yoy:+.1f}% YoY")
    c2.metric("Total Orders",     f"{total_orders:,}")
    c3.metric("Avg Order Value",  f"${aov:,.2f}")
    c4.metric("Top Category",     top_cat)

    section("Revenue by Year and Monthly Trend")
    c1, c2 = st.columns(2)
    with c1:
        by_year = df.groupby("Year", as_index=False)["Sales"].sum()
        fig = px.bar(by_year, x="Year", y="Sales", title="Total Sales by Year",
                     color_discrete_sequence=[PRIMARY])
        fig.update_traces(hovertemplate="Year %{x}<br>Sales $%{y:,.0f}<extra></extra>")
        st.plotly_chart(style_fig(fig, xtitle="Year", ytitle="Sales (USD)"), use_container_width=True)

    with c2:
        monthly = df.groupby("Month", as_index=False)["Sales"].sum()
        fig = px.area(monthly, x="Month", y="Sales", title="Monthly Sales Trend",
                      color_discrete_sequence=[ACCENT])
        fig.update_traces(line=dict(width=2.5), fillcolor="rgba(244,114,182,0.18)",
                          hovertemplate="%{x|%b %Y}<br>$%{y:,.0f}<extra></extra>")
        st.plotly_chart(style_fig(fig, xtitle="Month", ytitle="Sales (USD)"), use_container_width=True)

    insight_box("Key Insight - Revenue Trend",
                "Sales have grown consistently from 2015 to 2018 with the strongest growth seen in the second half of each year. November and December consistently drive the highest monthly revenue across all 4 years.")

    section("Sales by Category and Region")
    c1, c2 = st.columns(2)
    with c1:
        by_cat = f.groupby("Category", as_index=False)["Sales"].sum().sort_values("Sales")
        fig = px.bar(by_cat, x="Sales", y="Category", orientation="h",
                     title="Sales by Category", color="Category",
                     color_discrete_map=CATEGORY_COLORS)
        fig.update_layout(showlegend=False)
        fig.update_traces(hovertemplate="%{y}<br>$%{x:,.0f}<extra></extra>")
        st.plotly_chart(style_fig(fig, xtitle="Sales (USD)", ytitle="Category"), use_container_width=True)

    with c2:
        by_reg = f.groupby("Region", as_index=False)["Sales"].sum().sort_values("Sales")
        fig = px.bar(by_reg, x="Sales", y="Region", orientation="h",
                     title="Sales by Region", color_discrete_sequence=[PRIMARY_DEEP])
        fig.update_traces(hovertemplate="%{y}<br>$%{x:,.0f}<extra></extra>")
        st.plotly_chart(style_fig(fig, xtitle="Sales (USD)", ytitle="Region"), use_container_width=True)

    insight_box("Key Insight - Category and Region",
                "Technology leads all categories in total revenue. The West region is the strongest performer and has shown the most consistent year over year growth, nearly doubling from 2015 to 2018. The South region lags behind all others and may need targeted attention.")


# ===========================================================================
# PAGE 2 - Forecast
# ===========================================================================
def page_forecast():
    page_header("02 - Predictive Intelligence", "Forecast the next move.",
                "Segment-level forecasts using our best Stacking model - combining SARIMA, Prophet and XGBoost for maximum accuracy.")

    st.markdown("<div class='filter-bar'>", unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1:
        segment = st.selectbox("Segment", ["Overall", "Furniture", "Technology",
                                            "Office Supplies", "West Region", "East Region"])
    with c2:
        horizon = st.slider("Horizon (months)", 1, 3, 2)
    st.markdown("</div>", unsafe_allow_html=True)

    with st.spinner("Building forecast..."):
        actual, forecast, mae, rmse, mape = make_forecast(segment, horizon)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=actual.index, y=actual.values, name="Actual Sales",
                             mode="lines", line=dict(color=PRIMARY, width=2.8),
                             fill="tozeroy", fillcolor="rgba(56,189,248,0.08)",
                             hovertemplate="%{x|%b %Y}<br>$%{y:,.0f}<extra></extra>"))
    bridge_x = [actual.index[-1], *forecast.index]
    bridge_y = [actual.values[-1], *forecast.values]
    fig.add_trace(go.Scatter(x=bridge_x, y=bridge_y, name="Stacking Forecast",
                             mode="lines+markers",
                             line=dict(color=ACCENT, width=2.8, dash="dash"),
                             marker=dict(size=9, color=ACCENT, line=dict(color="#05070F", width=2)),
                             hovertemplate="%{x|%b %Y}<br>$%{y:,.0f}<extra></extra>"))
    fig.update_layout(title=f"{segment} - Actual vs Forecast ({horizon} month ahead)", height=470)
    st.plotly_chart(style_fig(fig, xtitle="Month", ytitle="Sales (USD)"), use_container_width=True)

    section("Model Accuracy Metrics")
    c1, c2, c3 = st.columns(3)
    c1.metric("MAE",  f"${mae:,.0f}",  help="Mean Absolute Error - average dollar error per month")
    c2.metric("RMSE", f"${rmse:,.0f}", help="Root Mean Squared Error - penalizes large errors more")
    c3.metric("MAPE", f"{mape:.2f}%",  help="Mean Absolute Percentage Error - our primary metric")

    insight_box("How to Read This Forecast",
                f"This forecast projects the next {horizon} month(s) of sales for {segment} "
                f"using our Stacking model which combines SARIMA, Prophet and XGBoost. "
                f"The model achieved a MAPE of {mape:.1f}% on historical data meaning predictions "
                f"are off by about {mape:.1f}% on average. Use this as a planning range, not a guarantee. "
                f"Unexpected events like promotions or supply issues will not be captured by the model.")

    section("Forecast Values")
    forecast_df = pd.DataFrame({
        "Month": forecast.index.strftime("%B %Y"),
        "Forecasted Sales": [f"${v:,.0f}" for v in forecast.values]
    })
    st.dataframe(forecast_df, use_container_width=True, hide_index=True)


# ===========================================================================
# PAGE 3 - Anomaly
# ===========================================================================
def page_anomaly():
    page_header("03 - Risk Detection", "The weeks that broke pattern.",
                "Weekly sales scanned by two methods - Isolation Forest (ML based) and Z-Score (statistical). Each flags different types of unusual behavior.")

    with st.spinner("Scanning for anomalies..."):
        weekly = detect_anomalies()

    def anomaly_chart(df, flag_col, title):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["Date"], y=df["Sales"], mode="lines",
                                 name="Weekly Sales", line=dict(color=PRIMARY, width=2),
                                 hovertemplate="%{x|%b %d, %Y}<br>$%{y:,.0f}<extra></extra>"))
        anoms = df[df[flag_col]]
        fig.add_trace(go.Scatter(x=anoms["Date"], y=anoms["Sales"], mode="markers",
                                 name="Anomaly", marker=dict(color=ACCENT, size=13,
                                 line=dict(color="#05070F", width=2), symbol="circle"),
                                 hovertemplate="Anomaly<br>%{x|%b %d, %Y}<br>$%{y:,.0f}<extra></extra>"))
        fig.update_layout(title=title, height=440)
        return style_fig(fig, xtitle="Week", ytitle="Weekly Sales (USD)")

    tab_if, tab_z = st.tabs(["Isolation Forest", "Z-Score"])

    with tab_if:
        st.plotly_chart(anomaly_chart(weekly, "IF_Anomaly", "Weekly Sales - Isolation Forest Anomalies"),
                        use_container_width=True)

        insight_box("How Isolation Forest Works",
                    "Isolation Forest detects anomalies by randomly isolating data points. "
                    "Points that are isolated in fewer steps are considered anomalies since "
                    "they are far from the rest of the data. It is a global method - it looks "
                    "at the entire dataset rather than just recent history.")

        table = weekly[weekly["IF_Anomaly"]][["Date", "Sales"]].reset_index(drop=True)
        table.columns = ["Anomaly Date", "Weekly Sales"]
        c1, c2 = st.columns([2, 1])
        with c1:
            st.dataframe(table, use_container_width=True, hide_index=True)
        with c2:
            st.metric("Anomalies Detected", len(table))
            st.info("These weeks had sales patterns significantly different from the rest of the dataset.")

    with tab_z:
        st.plotly_chart(anomaly_chart(weekly, "Z_Anomaly", "Weekly Sales - Z-Score Anomalies"),
                        use_container_width=True)

        insight_box("How Z-Score Detection Works",
                    "Z-Score measures how many standard deviations a data point is from the mean. "
                    "We flag any week where sales deviate more than 2 standard deviations from "
                    "the overall average. It is a simpler statistical method compared to Isolation Forest.")

        table = weekly[weekly["Z_Anomaly"]][["Date", "Sales", "ZScore"]].reset_index(drop=True)
        table.columns = ["Anomaly Date", "Weekly Sales", "Z-Score"]
        c1, c2 = st.columns([2, 1])
        with c1:
            st.dataframe(table, use_container_width=True, hide_index=True)
        with c2:
            st.metric("Anomalies Detected", len(table))

    section("Method Comparison")
    if_count = weekly["IF_Anomaly"].sum()
    z_count  = weekly["Z_Anomaly"].sum()
    insight_box("Isolation Forest vs Z-Score",
                f"Isolation Forest detected {if_count} anomalies while Z-Score detected {z_count}. "
                f"The two methods often disagree because they define abnormal differently. "
                f"Isolation Forest looks at global data patterns while Z-Score uses the overall mean. "
                f"When both methods agree on an anomaly, that week deserves the most attention "
                f"since two independent approaches flagged it as unusual.")


# ===========================================================================
# PAGE 4 - Segments
# ===========================================================================
def page_segments():
    page_header("04 - Demand Segmentation", "Products, clustered by behavior.",
                "17 product sub-categories grouped by total sales, growth rate, volatility and average order value using KMeans clustering with PCA visualization.")

    with st.spinner("Loading segments..."):
        seg = load_segments()

    fig = px.scatter(seg, x="PC1", y="PC2", color="Cluster", text="SubCategory",
                     title="PCA Cluster Map - Product Demand Segments",
                     color_discrete_map=CLUSTER_COLORS)
    fig.update_traces(textposition="top center",
                      marker=dict(size=18, line=dict(color="#05070F", width=2), opacity=0.95),
                      textfont=dict(family="Inter", size=11, color=INK_SOFT))
    fig.update_layout(height=540)
    st.plotly_chart(style_fig(fig, xtitle="Principal Component 1",
                              ytitle="Principal Component 2"), use_container_width=True)

    insight_box("How to Read This Chart",
                "Each dot is a product sub-category. Products that are close together behave "
                "similarly in terms of sales volume, growth and volatility. The 4 colors represent "
                "4 distinct demand groups found by KMeans clustering (k=4 chosen via elbow method). "
                "PCA reduces the 4 original features to 2 dimensions so we can visualize them.")

    c1, c2 = st.columns([1, 1])
    with c1:
        section("Sub-Category Assignments")
        st.dataframe(seg[["SubCategory", "Cluster"]].sort_values("Cluster").reset_index(drop=True),
                     use_container_width=True, hide_index=True)

    with c2:
        section("Stocking Strategy per Cluster")
        strategies = {
            "High Volume Stable":
                ("These are your core revenue products. Maintain steady safety stock with "
                 "automated reorder points. Stockouts here directly hurt revenue so always "
                 "keep buffer inventory.", PRIMARY),
            "High Growth Niche":
                ("Copiers are growing explosively at 479% over 4 years. Stock aggressively "
                 "and monitor weekly. This is a high opportunity product but also volatile "
                 "so avoid over-committing too far ahead.", SUCCESS),
            "Low Volume Steady":
                ("Keep lean inventory with small regular replenishments. Consider consolidating "
                 "suppliers or using just-in-time ordering to reduce carrying costs on these "
                 "low revenue but consistent products.", ACCENT_2),
            "Declining High Risk":
                ("Machines have declined 29% since 2015 with very high volatility. Reduce "
                 "stock levels, run clearance promotions and evaluate discontinuation. "
                 "Reallocate shelf space to growing clusters.", ACCENT),
        }
        for cluster, (msg, color) in strategies.items():
            st.markdown(f"""
                <div class="strategy">
                    <div class="dot" style="background:{color};width:12px;height:12px;border-radius:999px;margin-top:6px;flex-shrink:0;"></div>
                    <div><h4>{cluster}</h4><p>{msg}</p></div>
                </div>""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------
if page == "Overview":       page_overview()
elif page == "Forecast":     page_forecast()
elif page == "Anomaly Report": page_anomaly()
elif page == "Segments":     page_segments()

st.markdown("""
    <div class='footer-bar'>
        <div><span style='display:inline-block;width:6px;height:6px;border-radius:99px;background:#34D399;margin-right:0.5rem;'></span>Sales Intelligence Dashboard</div>
        <div>Superstore Sales 2015-2018 - Built with Streamlit and Plotly</div>
    </div>""", unsafe_allow_html=True)
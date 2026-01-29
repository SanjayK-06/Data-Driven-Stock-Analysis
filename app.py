import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import plotly.express as px
from datetime import timedelta
from streamlit_option_menu import option_menu

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Stock Market Analytics Dashboard",
    layout="wide"
)

# ==================================================
# THEME +  SIDEBAR STYLE
# ==================================================
st.markdown("""
<style>
/* Main App Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg,#efe9fb,#d9ccf2);
}

/* ---  SIDEBAR --- */
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(15px);
    border-right: 1px solid rgba(106, 13, 173, 0.1);
}

/* Sidebar Branding Section */
.sidebar-brand-container {
    padding: 20px 10px;
    text-align: center;
    background: linear-gradient(145deg, #ffffff, #f3e8ff);
    border-radius: 15px;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

.sidebar-header {
    font-size: 24px;
    font-weight: 800;
    color: #4b2d6e;
    letter-spacing: -0.5px;
}

.sidebar-sub {
    font-size: 13px;
    color: #8a70ba;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Sidebar Footer Section */
.sidebar-footer {
    padding: 15px;
    background: rgba(106, 13, 173, 0.05);
    border-radius: 12px;
    margin-top: 20px;
    border: 1px dashed rgba(106, 13, 173, 0.2);
}

.sidebar-footer-title { 
    font-size: 16px; 
    font-weight: 700; 
    color: #4b2d6e; 
    text-align: center; 
}

.sidebar-footer-sub { 
    font-size: 12px; 
    text-align: center; 
    color: #6b5a93; 
    margin-top: 5px;
}

/* TITLES */
.main-title{
    font-size:42px;font-weight:800;text-align:center;color:#4b2d6e;
}
.sub-title{
    text-align:center;font-size:16px;color:#6b5a93;margin-bottom:30px;
}

/* CARDS */
.card{
    background:#faf7ff;border-radius:18px;padding:22px;
    box-shadow:0 10px 28px rgba(0,0,0,0.08);
}

/* KPI */
.kpi-card{
    background:linear-gradient(135deg,#b087e3,#d9b4f5);
    border-radius:20px;padding:20px;color:white;
}
.kpi-value{font-size:32px;font-weight:800;}
.kpi-label{font-size:15px;}
</style>
""", unsafe_allow_html=True)


# ==================================================
# LOAD DATA
# ==================================================
CSV_PATH = r"C:\Users\Amirtha\OneDrive\Desktop\Project\Data-Driven Stock Analysis\Data\CLEANED DATA\Cleaned_nifty_50.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(CSV_PATH)

    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    date_col = next(col for col in df.columns if "date" in col)
    df.rename(columns={date_col: "date"}, inplace=True)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    return df.sort_values(["ticker", "date"])

df_master = load_data()

# ==================================================
# HEADER
# ==================================================
st.markdown("<div class='main-title'>📈 Stock Market Analytics Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>NIFTY-50 Data Driven Insights</div>", unsafe_allow_html=True)

# ==================================================
# SIDEBAR NAVIGATION
# ==================================================

with st.sidebar:
    # Enhanced Top Branding
    st.markdown('''
        <div class="sidebar-brand-container">
            <div class="sidebar-header">📊 Stock Analytics</div>
            <div class="sidebar-sub">NIFTY-50 Insight Engine</div>
        </div>
    ''', unsafe_allow_html=True)

    # Navigation Menu with Enhanced Styling
    selected_label = option_menu(
        menu_title=None, 
        options=["Home", "Volatility", "Returns", "Sectors", "Correlation", "Gainers"],
        icons=['house-door-fill', 'cpu-fill', 'graph-up-arrow', 'pie-chart-fill', 'share-fill', 'award-fill'], 
        default_index=0,
        styles={
            "container": {
                "padding": "5px!important", 
                "background-color": "rgba(255,255,255,0.5)", 
                "border": "1px solid rgba(106, 13, 173, 0.1)",
                "border-radius": "15px"
            },
            "icon": {"color": "#6A0DAD", "font-size": "18px"}, 
            "nav-link": {
                "font-size": "15px", 
                "text-align": "left", 
                "margin":"5px", 
                "padding": "12px 20px",
                "border-radius": "10px",
                "color": "#4b2d6e",
                "--hover-color": "#f3e8ff",
            },
            "nav-link-selected": {
                "background": "linear-gradient(90deg, #AF80D1 0%, #9d4edd 100%)", 
                "font-weight": "600",
                "color": "white",
                "box-shadow": "0 4px 12px rgba(157, 78, 221, 0.3)"
            },
        }
    )

    # Enhanced Footer
    st.markdown('''
        <div class="sidebar-footer">
            <div class="sidebar-footer-title">⚙️ Data-Driven Analysis</div>
            <div class="sidebar-footer-sub">Built with ❤️ by Sanjay Kannan</div>
        </div>
    ''', unsafe_allow_html=True)

nav_map = {
    "Home": "Overview",
    "Volatility": "Q1",
    "Returns": "Q2",
    "Sectors": "Q3",
    "Correlation": "Q4",
    "Gainers": "Q5"
}
page = nav_map[selected_label]


# ==================================================
# FILTERS (HIDE ON HOME)
# ==================================================
if page != "Overview":

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🔍 Filters")

    c1, c2, c3 = st.columns(3)
    max_date = df_master["date"].max()

    with c1:
        date_option = st.selectbox(
            "Date Range",
            ["All Time","Last 1 Year","Last 6 Months","Last 3 Months"]
        )

    with c2:
        sector_choice = st.selectbox(
            "Sector",
            ["All Sectors"] + sorted(df_master["sector"].dropna().unique())
        )

    with c3:
        stock_choice = st.multiselect(
            "Stock",
            sorted(df_master["ticker"].unique())
        )

    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# APPLY FILTERS
# ==================================================
if page != "Overview":
    df = df_master.copy()
    
    # Apply date filter
    if date_option == "Last 1 Year":
        df = df[df["date"] >= max_date - timedelta(days=365)]
    elif date_option == "Last 6 Months":
        df = df[df["date"] >= max_date - timedelta(days=180)]
    elif date_option == "Last 3 Months":
        df = df[df["date"] >= max_date - timedelta(days=90)]
    
    # Apply sector filter
    if sector_choice != "All Sectors":
        df = df[df["sector"] == sector_choice]
    
    # Apply stock filter
    if stock_choice:
        df = df[df["ticker"].isin(stock_choice)]

# ==================================================
# KPI CARDS (HIDE ON HOME)
# ==================================================
if page != "Overview":

    avg_return = df["daily_return"].mean() * 100

    cum_return = (
        df.groupby("ticker")["daily_return"]
        .apply(lambda x: (1+x).cumprod().iloc[-1]-1)
        .dropna()
    )

    k1, k2, k3 = st.columns(3)

    with k1:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>📊 Avg Market Return</div>
            <div class='kpi-value'>{avg_return:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>🏆 Best Stock</div>
            <div class='kpi-value'>{cum_return.idxmax()}</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>📉 Worst Stock</div>
            <div class='kpi-value'>{cum_return.idxmin()}</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()


# ==================================================
# OVERVIEW PAGE (NEW – SAFE)
# ==================================================
if page == "Overview":

    # Increased overall proportions and used small gap to allow containers to expand
    left, center, right = st.columns([1.2, 3.2, 1.2], gap="small")

    with left:
        st.markdown("""<div class="card">
        <h4>🟢 Green vs Red Stocks</h4>
        <p>See the percentage of stocks moving up vs down.</p>
        </div>""", unsafe_allow_html=True)

        st.markdown("""<div class="card" style="margin-top:20px;">
        <h4>🚀 Top Gainers & Losers</h4>
        <p>Identify today’s biggest movers.</p>
        </div>""", unsafe_allow_html=True)

        st.markdown("""<div class="card" style="margin-top:20px;">
        <h4>📉 Volatility by Ticker</h4>
        <p>Understand stock stability.</p>
        </div>""", unsafe_allow_html=True)

    with center:
        st.markdown("<div class='hero-card'>", unsafe_allow_html=True)
        st.image(
            "https://raw.githubusercontent.com/SanjayK-06/Project-assests/main/hero.jpg.jpg",
            width='stretch'
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("""<div class="card">
        <h4>🏦 Sector Performance</h4>
        <p>Compare IT, Banking & Pharm.</p>
        </div>""", unsafe_allow_html=True)

        st.markdown("""<div class="card" style="margin-top:20px;">
        <h4>📈 Cumulative Return</h4>
        <p>Track returns over time.</p>
        </div>""", unsafe_allow_html=True)

        st.markdown("""<div class="card" style="margin-top:20px;">
        <h4>🔗 Stock Correlation</h4>
        <p>Understand relationships.</p>
        </div>""", unsafe_allow_html=True)

# ==================================================
# Q1 – VOLATILITY
# ==================================================
elif page == "Q1":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🔥 Top 10 Volatile Stocks")

    vol = (
        df.groupby("ticker")["daily_return"]
        .std().dropna()
        .sort_values(ascending=False)
        .head(10) * 100
    )

    fig, ax = plt.subplots(figsize=(10,5))
    ax.barh(vol.index[::-1], vol.values[::-1], color="#c9afe1")
    ax.set_xlabel("Volatility (%)")
    st.pyplot(fig)

# ==================================================
# Q2 – CUMULATIVE RETURN
# ==================================================
elif page == "Q2":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📈 Cumulative Return")

    df["cumulative_return"] = (
        df.groupby("ticker")["daily_return"]
        .transform(lambda x: (1+x).cumprod()-1)
    )

    top5 = (
        df.groupby("ticker")["cumulative_return"]
        .last().sort_values(ascending=False)
        .head(5).index
    )

    fig, ax = plt.subplots(figsize=(12,6))
    for t in top5:
        ax.plot(df[df["ticker"]==t]["date"],
                df[df["ticker"]==t]["cumulative_return"], label=t)

    ax.legend()
    st.pyplot(fig)

# ==================================================
# Q3 – SECTOR PERFORMANCE
# ==================================================
elif page == "Q3":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🏭 Sector-wise Performance")

    yearly = (
        df.groupby(["ticker", df["date"].dt.year])
        .agg(first=("close","first"),
             last=("close","last"),
             sector=("sector","first"))
        .reset_index()
    )

    yearly["return"] = (yearly["last"] - yearly["first"]) / yearly["first"]

    sector_perf = yearly.groupby("sector")["return"].mean()

    fig, ax = plt.subplots(figsize=(10,5))
    sector_perf.sort_values().plot(kind="bar", ax=ax, color="#9d4edd")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
    st.pyplot(fig)

# ==================================================
# Q4 – CORRELATION
# ==================================================
elif page == "Q4":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🔗 Stock Correlation")

    pivot = df.pivot(index="date", columns="ticker", values="daily_return")
    corr = pivot.corr()

    fig = px.imshow(corr, color_continuous_scale="RdBu", zmin=-1, zmax=1)
    st.plotly_chart(fig, width='stretch')

# ==================================================
# Q5 – MONTHLY GAINERS & LOSERS
# ==================================================
elif page == "Q5":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📅 Monthly Gainers & Losers")

    df["month"] = df["date"].dt.strftime("%Y-%m")
    month = st.selectbox("Select Month", sorted(df["month"].unique()))

    monthly = (
        df[df["month"] == month]
        .groupby("ticker")["close"]
        .agg(first="first", last="last")
        .reset_index()
    )

    monthly["return"] = (monthly["last"] - monthly["first"]) / monthly["first"] * 100

    top5 = monthly.sort_values("return", ascending=False).head(5)
    bottom5 = monthly.sort_values("return").head(5)

    fig, ax = plt.subplots(figsize=(12,6))
    ax.bar(top5["ticker"], top5["return"], color="#2ecc71", label="Gainers")
    ax.bar(bottom5["ticker"], bottom5["return"], color="#e74c3c", label="Losers")
    ax.axhline(0, linestyle="--", color="black")
    ax.legend()
    plt.xticks(rotation=30)
    st.pyplot(fig)

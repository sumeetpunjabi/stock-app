import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Stock Brain", layout="wide")

st.title("📊 Zero-Install Stock Brain Dashboard")

API_KEY = st.secrets.get("FMP_API_KEY", "")

TICKERS = ["AAPL","MSFT","NVDA","AMZN","GOOGL","TSLA","META","JPM","V","SPY","QQQ"]

BASE = "https://financialmodelingprep.com/api/v3"

def get_profile(ticker):
    url = f"{BASE}/profile/{ticker}?apikey={API_KEY}"
    return requests.get(url).json()[0]

def get_metrics(ticker):
    url = f"{BASE}/key-metrics-ttm/{ticker}?apikey={API_KEY}"
    data = requests.get(url).json()
    return data[0] if isinstance(data, list) and len(data) > 0 else {}

rows = []

for t in TICKERS:
    try:
        p = get_profile(t)
        m = get_metrics(t)

        price = p.get("price", 0)
        eps = p.get("eps", 0)

        mcap = p.get("mktCap", 0)
        cash = m.get("cashAndCashEquivalents", 0)
        debt = m.get("totalDebt", 0)
        fcf = m.get("freeCashFlow", 0)
        ebitda = m.get("ebitda", 0)

        ev = mcap + debt - cash

        rows.append({
            "Ticker": t,
            "Sector": p.get("sector"),
            "Market Cap": mcap,
            "FCF": fcf,
            "Cash": cash,
            "Debt": debt,
            "P/E": price/eps if eps else None,
            "EV/EBITDA": ev/ebitda if ebitda else None
        })

    except:
        pass

df = pd.DataFrame(rows)

sector = st.selectbox("Filter Sector", ["All"] + list(df["Sector"].dropna().unique()))

if sector != "All":
    df = df[df["Sector"] == sector]

st.dataframe(df, use_container_width=True)

st.subheader("📊 Market Cap View")
st.bar_chart(df.set_index("Ticker")["Market Cap"])

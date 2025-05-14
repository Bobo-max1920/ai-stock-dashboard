
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Wall Street AI Pro Dashboard", layout="wide")

st.title("📈 Wall Street AI Pro Stock Picks Dashboard")

csv_file = "daily_stock_picks.csv"
if not os.path.exists(csv_file):
    st.warning("No stock picks file found yet. Run the analysis script first.")
else:
    df = pd.read_csv(csv_file)
    st.subheader("Top Stock Picks (Today)")
    st.dataframe(df, use_container_width=True)

    top_pick = st.selectbox("Select a ticker to analyze:", df["Ticker"].values)
    if top_pick:
        import requests
        API_KEY = "N78SB7UXE4GNEMY"
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": top_pick,
            "interval": "60min",
            "apikey": API_KEY
        }
        r = requests.get(url, params=params)
        data = r.json()
        key = "Time Series (60min)"
        if key in data:
            df_hist = pd.DataFrame(data[key]).T
            df_hist = df_hist.astype(float)
            df_hist.index = pd.to_datetime(df_hist.index)
            df_hist.sort_index(inplace=True)
            st.line_chart(df_hist["4. close"], use_container_width=True)
            st.caption("60-minute close price chart")
        else:
            st.error("Could not fetch chart data for this ticker.")

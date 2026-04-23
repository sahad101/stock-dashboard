import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date

# Page settings
st.set_page_config(
    page_title="📈 Stock Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📈 Stock Market Dashboard")
st.markdown("### Analyze stocks in real-time")

# Sidebar
st.sidebar.header("⚙️ Settings")

stock_options = ["AAPL", "TSLA", "GOOGL", "MSFT", "RELIANCE.NS", "TCS.NS"]
selected_stocks = st.sidebar.multiselect(
    "Select Stocks",
    stock_options,
    default=["AAPL"]
)

start_date = st.sidebar.date_input("Start Date", date(2023, 1, 1))
end_date = st.sidebar.date_input("End Date", date.today())

# Main content
for stock_symbol in selected_stocks:
    st.markdown(f"## 📊 {stock_symbol}")

    stock = yf.Ticker(stock_symbol)
    df = stock.history(start=start_date, end=end_date)

    if df.empty:
        st.warning("No data found")
        continue

    # Metrics row
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Open", round(df["Open"].iloc[-1], 2))
    col2.metric("High", round(df["High"].iloc[-1], 2))
    col3.metric("Low", round(df["Low"].iloc[-1], 2))
    col4.metric("Close", round(df["Close"].iloc[-1], 2))

    # Moving Average
    df["MA20"] = df["Close"].rolling(20).mean()

    # Chart section
    st.markdown("### 📉 Price Trend")
    st.line_chart(df[["Close", "MA20"]])

    # Table section
    with st.expander("📄 View Raw Data"):
        st.dataframe(df)

    # Download
    csv = df.to_csv().encode("utf-8")
    st.download_button(
        "⬇️ Download CSV",
        csv,
        f"{stock_symbol}.csv",
        "text/csv"
    )

    st.markdown("---")
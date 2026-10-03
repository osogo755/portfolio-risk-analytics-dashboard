import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Portfolio Risk Analytics", layout="wide")

st.title("📈 Financial Portfolio & Risk Analytics Dashboard")
st.markdown("Interactive portfolio risk profiling, return distributions, and performance analytics.")

st.sidebar.header("Dashboard Parameters")
tickers_input = st.sidebar.text_input("Stock Tickers (comma separated)", "AAPL, MSFT, GOOGL, AMZN")
period = st.sidebar.selectbox("Time Horizon", ["6mo", "1y", "2y", "5y"], index=1)

tickers = [t.strip().upper() for t in tickers_input.split(",")]

def generate_fallback_data(symbols, horizon):
    days_map = {"6mo": 126, "1y": 252, "2y": 504, "5y": 1260}
    n_days = days_map.get(horizon, 252)
    dates = pd.date_range(end=pd.Timestamp.today(), periods=n_days, freq="B")
    
    np.random.seed(42)
    df_dict = {}
    for sym in symbols:
        price = 100.0
        prices = []
        for _ in range(n_days):
            price *= (1 + np.random.normal(0.0005, 0.015))
            prices.append(price)
        df_dict[sym] = prices
        
    return pd.DataFrame(df_dict, index=dates)

@st.cache_data
def load_data(symbols, horizon):
    try:
        df = yf.download(symbols, period=horizon, progress=False)
        
        # Handle multi-index or single-index Close columns
        if isinstance(df.columns, pd.MultiIndex):
            if 'Close' in df.columns.levels[0]:
                df = df['Close']
        elif 'Close' in df.columns:
            df = df[['Close']]

        if df.empty or df.dropna(how='all').empty:
            st.warning("⚠️ Live market data unavailable. Using simulated data.")
            return generate_fallback_data(symbols, horizon)
            
        return df
    except Exception:
        st.warning("⚠️ Connection issue detected. Using simulated data.")
        return generate_fallback_data(symbols, horizon)

try:
    data = load_data(tickers, period)
    returns = data.pct_change().dropna()

    if returns.empty:
        data = generate_fallback_data(tickers, period)
        returns = data.pct_change().dropna()

    st.subheader("📊 Asset Risk & Return Summary")
    valid_tickers = [t for t in tickers if t in returns.columns]
    
    if valid_tickers:
        cols = st.columns(len(valid_tickers))
        rf_rate = 0.04  # 4% Risk-Free Rate Assumption
        
        for i, ticker in enumerate(valid_tickers):
            asset_returns = returns[ticker]
            ann_return = asset_returns.mean() * 252
            ann_vol = asset_returns.std() * np.sqrt(252)
            sharpe = (ann_return - rf_rate) / ann_vol if ann_vol != 0 else 0
            var_95 = np.percentile(asset_returns, 5)

            with cols[i]:
                st.metric(label=f"{ticker} Return (Ann.)", value=f"{ann_return:.2%}")
                st.write(f"**Volatility:** {ann_vol:.2%}")
                st.write(f"**Sharpe Ratio:** {sharpe:.2f}")
                st.write(f"**95% Daily VaR:** {var_95:.2%}")

    st.markdown("---")

    # Interactive Chart 1: Cumulative Returns Plotly Line Chart
    st.subheader("🚀 Cumulative Returns Comparison")
    cum_returns = (1 + returns).cumprod() - 1
    fig_cum = px.line(cum_returns, labels={'value': 'Cumulative Return', 'index': 'Date'},
                      title="Normalized Cumulative Performance")
    st.plotly_chart(fig_cum, use_container_width=True)

    # Interactive Chart 2: Daily Returns Histogram
    st.subheader("🎲 Return Distribution & Volatility Profile")
    selected_asset = st.selectbox("Select Asset for Histogram", valid_tickers if valid_tickers else tickers)
    if selected_asset in returns.columns:
        fig_hist = px.histogram(returns, x=selected_asset, nbins=50, marginal="box",
                                 title=f"Daily Return Distribution for {selected_asset}")
        st.plotly_chart(fig_hist, use_container_width=True)

except Exception as e:
    st.error(f"Error rendering dashboard analytics: {e}")
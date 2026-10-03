# Financial Risk & Portfolio Analytics Dashboard

An interactive Streamlit and Plotly dashboard for analyzing multi-asset portfolio returns, volatility, risk-adjusted performance, and Value at Risk (VaR).

## Business Problem
Portfolio managers and individual investors need dynamic risk monitoring tools to evaluate asset allocations, downside risk, and performance metrics beyond basic price charts.

## Technical Stack
* **Dashboard Framework:** Streamlit
* **Visualization:** Plotly Express & Plotly Graph Objects
* **Data Ingestion & Calculation:** Python (`pandas`, `numpy`, `yfinance`)

## Key Metrics & Features
* **Cumulative Return Tracking:** Interactive historical performance comparisons across assets.
* **Risk Metrics:** Annualized Volatility, Sharpe Ratio, and 95% Historical Value at Risk (VaR).
* **Drawdown Analysis:** Visualizing peak-to-trough decline metrics over selected time horizons.

## Project Structure
```text
portfolio-risk-analytics-dashboard/
├── README.md
├── requirements.txt
└── src/
    └── dashboard.py
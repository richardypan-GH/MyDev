

print("Hello from tickerscreen1.py!")

import yfinance as yf
import pandas as pd

def get_price(ticker, date):
    """Fetch the adjusted close price on or nearest after a given date."""
    data = yf.download(ticker, start=date, end=date, progress=False)
    if data.empty:
        # If the market was closed, fetch next available trading day
        data = yf.download(ticker, start=date, progress=False)
    return data['Adj Close'].iloc[0] if not data.empty else None


def performance_screen(tickers, date1, date2, date3, drop_pct, rise_pct):
    results = []

    for ticker in tickers:
        p1 = get_price(ticker, date1)
        p2 = get_price(ticker, date2)
        p3 = get_price(ticker, date3)

        if None in (p1, p2, p3):
            continue

        # Percent change calculations
        pct_drop   = (p2 - p1) / p1 * 100
        pct_rebound = (p3 - p2) / p2 * 100

        # Check conditions
        if pct_drop <= -abs(drop_pct) and pct_rebound >= rise_pct:
            results.append({
                "Ticker": ticker,
                "Drop % (date1→date2)": pct_drop,
                "Rise % (date2→date3)": pct_rebound,
                "Price1": p1,
                "Price2": p2,
                "Price3": p3,
            })

    return pd.DataFrame(results)


# ------------------------------
# Example use
# ------------------------------
tickers = ["AAPL", "MSFT", "NVDA", "TSLA", "AMZN"]

date1 = "2024-01-01"
date2 = "2024-06-01"
date3 = "2024-12-01"

drop_threshold = 10   # Must fall at least 10%
rise_threshold = 20   # Must rise at least 20%

df = performance_screen(tickers, date1, date2, date3, drop_threshold, rise_threshold)
print(df)


from .threshold_finder import get_rsi_thresholds
from .data_loader import download_ticker_data
from .feature_engineer import compute_features
import pandas as pd
from ta.momentum import RSIIndicator



def recommend_signals(tickers, thresholds, date=None):
    # thresholds = get_rsi_thresholds(date)
    if thresholds is None:
        return {ticker: "Unknown" for ticker in tickers}

    # Need to extract data for the tickers
    start = pd.to_datetime(date) - pd.Timedelta(days=45)
    end = pd.to_datetime(date) + pd.Timedelta(days=1)
    data = download_ticker_data(tickers, start=start, end=end)

    #print(data, "AAPL" in data)
    signals = {}
    # Iterate through each ticker and get RSI
    for ticker in tickers:
        if ticker not in data:
            signals[ticker] = "Unknown"
            continue

        #df = compute_features(pd.DataFrame({"Close": data[ticker].dropna()}))
        #print(data[ticker])
        RSI = RSIIndicator(data[ticker], window=14).rsi()

        #print(RSI)
        # If RSI could not be determined, signal is unknown
        if RSI.empty:
            signals[ticker] = "Unknown"
            continue

        latest_rsi = RSI.iloc[-1]
        
        # Recommend signals based on threshold
        if latest_rsi < thresholds["Buy"]:
            signals[ticker] = "Buy"
        elif latest_rsi > thresholds["Sell"]:
            signals[ticker] = "Sell"
        else:
            signals[ticker] = "Hold"

        print("===%s=== RSI: %.1f, signal: %s" % (ticker, latest_rsi, signals[ticker]))
    return signals
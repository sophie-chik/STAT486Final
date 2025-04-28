import pandas as pd
from ta.momentum import RSIIndicator


def compute_features(df, rsi_window=14):
    df["RSI"] = RSIIndicator(df["Close"], window=rsi_window).rsi()
    df["RSI_Delta"] = df["RSI"].diff()
    df["Return_3D"] = df["Close"].pct_change(3)
    df["Return_5D"] = df["Close"].pct_change(5)
    df["SMA_20"] = df["Close"].rolling(20).mean()
    df["SMA_Dist"] = (df["Close"] - df["SMA_20"]) / df["SMA_20"]
    df["Volatility"] = df["Close"].rolling(10).std()
    return df.dropna()
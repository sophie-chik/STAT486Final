import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from .data_loader import download_market_data
from .feature_engineer import compute_features
from .model import RSIDynamicModel
from datetime import datetime, timedelta


scaler = StandardScaler()


def get_rsi_thresholds(date=None):
    """
    Calculates RSI Thresholds for the given date. If date is not given, 
    today is used
    Inputs:
        - Date: A date in a string or datetime format
    Outputs: Buy and Sell Thresholds, 
             Probabilities generated, 
             Features.
    """
    # If date is not given, today is used
    if date is None:
        date = datetime.today().date()
    if isinstance(date, str):
        date = pd.to_datetime(date).date()

    start = pd.to_datetime(date) - pd.Timedelta(days=60)
    end = pd.to_datetime(date) + pd.Timedelta(days=1)

    #print(f"Fetching market data from {start.date()} to {end.date()}")
    # Download the data
    market_px = download_market_data(start=start, end=end)

    # Combine all the data
    combined = []
    for ticker in market_px.columns:
        df = pd.DataFrame({"Close": market_px[ticker].copy()})
        features = compute_features(df)
        if not features.empty:
            features = features.copy()
            features["Ticker"] = ticker
            combined.append(features)

    if not combined:
        print(f"No data available for {date} — likely a weekend or holiday.")
        return None

    market_df = pd.concat(combined)
    daily_rows = market_df.loc[market_df.index.normalize() == pd.to_datetime(date)]
    if daily_rows.empty or len(daily_rows) < 2:
        print(f"Not enough data on {date} to compute thresholds.")
        return None

    avg_features = daily_rows[["RSI_Delta", "Return_3D", "Return_5D", "SMA_Dist", "Volatility"]].mean()
    if avg_features.isna().any():
        print(f"NaNs in features for {date}")
        return None

    market_return = avg_features["Return_3D"]
    volatility = avg_features["Volatility"]

    # Adjust the RSI range depending on market conditions
    if market_return > 0.005 and volatility < 0.01:
        rsi_range = np.arange(30, 90, 0.5)
    elif market_return < -0.005 and volatility > 0.01:
        rsi_range = np.arange(10, 70, 0.5)
    else:
        rsi_range = np.arange(10, 90, 0.5)

    probe = pd.DataFrame({
        "RSI": rsi_range,
        "RSI_Delta": avg_features["RSI_Delta"],
        "Return_3D": avg_features["Return_3D"],
        "Return_5D": avg_features["Return_5D"],
        "SMA_Dist": avg_features["SMA_Dist"],
        "Volatility": avg_features["Volatility"]
    })

    # Probe all the values and generate probabilities
    X_probe_scaled = scaler.fit_transform(probe)
    model = RSIDynamicModel()
    proba = model.predict_proba(X_probe_scaled)

    # Pick thresholds based on max and min probabilities
    buy_t = probe.loc[np.argmax(proba), "RSI"]
    sell_t = probe.loc[np.argmin(proba), "RSI"]

    return {
        "Buy": float(buy_t),
        "Sell": float(sell_t),
        "Proba": proba.tolist(),
        "Features": avg_features.to_dict()
    }

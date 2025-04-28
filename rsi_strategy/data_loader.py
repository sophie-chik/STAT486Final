import yfinance as yf
import pandas as pd
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="yfinance")
MARKET_TICKERS = ["SPY", "QQQ", "DIA", "IWM", "TLT", "VIXY", "XLK", "HYG", "GLD"]

# Download market data for the model
def download_market_data(start, end):
    return yf.download(MARKET_TICKERS, start=start, end=end, progress=False)["Close"]

# Download ticker data for inference
def download_ticker_data(tickers, start, end):
    return yf.download(tickers, start=start, end=end, progress=False)["Close"]
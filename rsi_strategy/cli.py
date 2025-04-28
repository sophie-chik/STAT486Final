import argparse
from .threshold_finder import get_rsi_thresholds
from .signal_generator import recommend_signals


def main():
    # Take in date and ticker arguments in the command line
    parser = argparse.ArgumentParser(description="RSI Strategy CLI")
    parser.add_argument(
        "--date", type=str,
        help="Date to analyze (YYYY-MM-DD). Defaults to today.", default=None
    )
    parser.add_argument(
        "--tickers", nargs="*", help="List of tickers to evaluate", default=[]
    )
    args = parser.parse_args()

    # If no ticker argument is provided, only return the threshold
    if args.date or not args.tickers:
        thresholds = get_rsi_thresholds(args.date)
        print("RSI Thresholds: \nBuy:", thresholds["Buy"], "\nSell:", thresholds["Sell"])

    # Calculate signal for each ticker
    if args.tickers:
        signals = recommend_signals(args.tickers, thresholds, args.date)
        #print("Signals:", signals)

if __name__ == "__main__":
    main()

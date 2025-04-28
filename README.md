# STAT486Final
Dynamic RSI is a machine learning-based Python library that dynamically adjusts the traditional RSI (Relative Strength Index) thresholds based on real-time market conditions. Instead of using static values (like 30/70), it intelligently adapts the "Buy" and "Sell" levels depending on market volatility and momentum.

## Setup Instructions

1. **Clone the repository**:

2. **Install dependencies** using the provided `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

3. **(Optional)** Install the package locally:
    ```bash
    pip install -e .
    ```

---

## How to Use

You can use the library **programmatically** or through the **command line interface (CLI)**.

### Programmatic Usage

```python
from rsi_strategy.threshold_finder import get_rsi_thresholds
from rsi_strategy.signal_generator import recommend_signals

# Example: Get optimal RSI thresholds for a date
thresholds = get_rsi_thresholds(date="2024-04-15")

# Example: Generate Buy/Sell/Hold signals
signals = recommend_signals(["AAPL", "MSFT", "GOOGL"], date="2024-04-15")
```

### CLI Usage
```bash
rsi-strategy --date 2024-10-17 --tickers AAPL NVDA NFLX
```
### Sample Output
```bash
RSI Thresholds: 
Buy: 42.0 
Sell: 87.5
===AAPL=== RSI: 58.9, signal: Hold
===NVDA=== RSI: 68.4, signal: Hold
===NFLX=== RSI: 41.3, signal: Buy
```


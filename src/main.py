from pathlib import Path
import json
from analytics import *
import yfinance as yf
from providers.yahoo_provider import *

DATA_DIR = Path("data/sample")

LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"
YAHOO_PERIOD = "1mo"
YAHOO_INTERVAL = "1d"

# Canonical MarketPulse ticker -> Yahoo Finance symbol
YAHOO_SYMBOLS = {
    "AAPL": "AAPL",
    "SP500": "^GSPC",
}


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def load_bloomberg():
    with open(DATA_DIR / "bloomberg_reference_sample.json", encoding="utf-8") as file:
        return json.load(file)


def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def normalize_price_row(row):
    return {
        "date": row["date"],
        "ticker": row["ticker"],
        "open": float(row["open"]),
        "high": float(row["high"]),
        "low": float(row["low"]),
        "close": float(row["close"]),
        "volume": int(row["volume"]),
    }


def filter_prices(prices, ticker):
    return [row for row in prices if row["ticker"] == ticker]

def get_first_close(prices):
    return float(prices[0]["close"])

def get_last_close(prices):
    return float(prices[-1]["close"])

def display_market_summary(asset, prices, show_currency=True):
    print(f"{asset["ticker"]} - {asset["name"]}")
    print(f"Observations : {len(prices)}")
    if (show_currency==False):
        print(f"First Close : {get_first_close(prices)}")
        print(f"Last Close : {get_last_close(prices)}")
    else:
        print(f"First Close : {get_first_close(prices)} USD")
        print(f"Last Close : {get_last_close(prices)} USD")
    

def get_first_date(prices):
    return prices[0]["date"]

def get_last_date(prices):
    return prices[-1]["date"]

def min_close(prices):
    min=float(prices[0]["close"])
    for i in range(1,len(prices)):
        if(min>float(prices[i]["close"])):
            min=float(prices[i]["close"])
    return min

def max_close(prices):
    max=float(prices[0]["close"])
    for i in range(1,len(prices)):
        if(max<float(prices[i]["close"])):
            max=float(prices[i]["close"])
    return max

def normalize_price_row(row):
    return {
        "date": row["date"],
        "ticker": row["ticker"],
        "open": float(row["open"]),
        "high": float(row["high"]),
        "low": float(row["low"]),
        "close": float(row["close"]),
        "volume": int(row["volume"]),
    }
YAHOO_SYMBOLS = {
    "AAPL": "AAPL",
    "SP500": "^GSPC",
}
def main():
    instrument_prices = fetch_yahoo_prices(
        symbol=YAHOO_SYMBOLS["AAPL"],
        canonical_ticker="AAPL",
        period="1mo",
        interval="1d",
    )

    benchmark_prices = fetch_yahoo_prices(
        symbol=YAHOO_SYMBOLS["SP500"],
        canonical_ticker="SP500",
        period="1mo",
        interval="1d",
    )
    instruments = load_instruments()

    normalized_prices = [normalize_price_row(row) for row in prices]

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_latest = instrument_prices[-1]
    benchmark_latest = benchmark_prices[-1]
    
    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices,
        benchmark_prices,
    )
    instrument_return = calculate_period_return(
        aligned_instrument
    )

    print("=== MarketPulse ===")
    print()
    print("Provider")
    print("Yahoo Finance via yfinance")
    print()
    print("Market configuration")
    print(f"Period: {LOOKBACK_LABEL}")
    print(f"Interval: {INTERVAL_LABEL}")
    print()
    print("Market configuration")
    print(f"Instrument : {instrument['ticker']} - {instrument['name']}")
    print(f"Benchmark  : {benchmark['ticker']} - {benchmark['name']}")
    print(f"Period     : {LOOKBACK_LABEL}")
    print(f"Interval   : {INTERVAL_LABEL}")
    print(f"Common observations : {len(aligned_instrument)}")
    print(f"From {aligned_instrument[0]['date']} to {aligned_instrument[-1]['date']}")
    print()
    print(f"Instrument return : {instrument_return:.2f}%")
    print(f"Benchmark return  : {benchmark_return:.2f}%")
    print()
    print("Relative performance")
    print(
        f"{instrument['ticker']} vs {benchmark['ticker']} : "
        f"{relative_performance:+.2f} percentage points"
    )
    print()
    print("Base 100")
    print(
        f"{instrument['ticker']:<5} : "
        f"{instrument_base_100[0]['value']:.2f} -> {instrument_base_100[-1]['value']:.2f}"
    )
    print(
        f"{benchmark['ticker']:<5} : "
        f"{benchmark_base_100[0]['value']:.2f} -> {benchmark_base_100[-1]['value']:.2f}"
    )


if __name__ == "__main__":
    main()

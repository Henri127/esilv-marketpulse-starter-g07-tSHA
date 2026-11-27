from pathlib import Path
import json
from analytics import *
import yfinance as yf
from providers.yahoo_provider import *
from providers.bloomberg_provider import *
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

def build_market_snapshot(instrument_ticker="AAPL",
    benchmark_ticker="SP500",
    lookback=LOOKBACK_LABEL,
    interval=INTERVAL_LABEL,):
    instruments = load_instruments()
    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = fetch_bloomberg_prices(instrument_ticker)
    benchmark_prices = fetch_bloomberg_prices(benchmark_ticker)

    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices,
        benchmark_prices,
    )

    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)
    relative_performance = calculate_relative_performance(
        instrument_return,
        benchmark_return,
    )

    instrument_base_100 = calculate_base_100(aligned_instrument)
    benchmark_base_100 = calculate_base_100(aligned_benchmark)

    provider_label = (
        "Bloomberg"
        if ACCESS_MODE == "LIVE"
        else "Bloomberg stage"
    )
    return {
        "provider": provider_label,
        "access_mode": ACCESS_MODE,
        "lookback": lookback,
        "interval": interval,
        "instrument": instrument,
        "benchmark": benchmark,
        "instrument_prices": aligned_instrument,
        "benchmark_prices": aligned_benchmark,
        "instrument_return": instrument_return,
        "benchmark_return": benchmark_return,
        "relative_performance": relative_performance,
        "instrument_base_100": instrument_base_100,
        "benchmark_base_100": benchmark_base_100,
    }

def main():
    snapshot = build_market_snapshot()

    aligned_instrument = snapshot["instrument_prices"]
    aligned_benchmark = snapshot["benchmark_prices"]
    instrument = snapshot["instrument"]
    benchmark = snapshot["benchmark"]
    instrument_return = snapshot["instrument_return"]
    benchmark_return = snapshot["benchmark_return"]
    relative_perf = snapshot["relative_performance"]
    instrument_base = snapshot["instrument_base_100"][-1]["value"]
    benchmark_base = snapshot["benchmark_base_100"][-1]["value"]

    print("=== MarketPulse ===")
    print()
    print("Provider")
    print(snapshot["provider"])
    print()
    print("Access mode")
    print(snapshot["access_mode"])
    print()
    print("Market configuration")
    print(f"Period: {snapshot['lookback']}")
    print(f"Interval: {snapshot['interval']}")
    print()
    print("Instruments")
    display_market_summary(instrument, aligned_instrument)
    print(f"Max instrument : {max_close(aligned_instrument)}")
    print(f"Min instrument : {min_close(aligned_instrument)}")
    print(f"Period return : {instrument_return:+.2f}%")
    print()
    print("Benchmark")
    display_market_summary(benchmark, aligned_benchmark, False)
    print(f"Max benchmark : {max_close(aligned_benchmark)}")
    print(f"Min benchmark : {min_close(aligned_benchmark)}")
    print(f"Period return : {benchmark_return:+.2f}%")
    print()
    print("Relative performance")
    print(
        f"{instrument['ticker']} vs {benchmark['ticker']}  = "
        f"{relative_perf:+.2f} percentage points"
    )
    print()
    print("Base 100")
    print(f"{instrument['ticker']}  : 100.00 -> {instrument_base:.2f}")
    print(f"{benchmark['ticker']} : 100.00 -> {benchmark_base:.2f}")
    

if __name__ == "__main__":
    main()

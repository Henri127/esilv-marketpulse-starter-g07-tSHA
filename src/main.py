from pathlib import Path
import csv
import json
from analytics import *
import yfinance as yf

from providers.yahoo_provider import *
from providers.bloomberg_provider import (
    fetch_approved_sample_prices,
    BLOOMBERG_IDENTIFIERS,
)

DATA_DIR = Path("data/sample")

# These starter values mirror config/settings.yml.
# settings.yml is a human-readable configuration contract in the CORE.
# Parsing YAML is optional and is not required by the 18-hour lab sequence.
LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def filter_prices(prices, ticker):
    return [row for row in prices if row["ticker"] == ticker]



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


def get_first_date(prices):
    return prices[0]["date"]

def get_last_date(prices):
    return prices[-1]["date"]



def build_market_snapshot():

    # Load market configuration
    instruments = load_instruments()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    # Fetch Bloomberg prices
    instrument_prices = fetch_approved_sample_prices(
        BLOOMBERG_IDENTIFIERS[instrument["ticker"]]
    )

    benchmark_prices = fetch_approved_sample_prices(
        BLOOMBERG_IDENTIFIERS[benchmark["ticker"]]
    )

    # Align both series
    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices,
        benchmark_prices,
    )

    assert len(aligned_instrument) > 0
    assert len(aligned_benchmark) > 0
    assert len(aligned_instrument) == len(aligned_benchmark)

    # Calculate returns
    instrument_return = calculate_period_return(
        aligned_instrument
    )

    benchmark_return = calculate_period_return(
        aligned_benchmark
    )

    relative_performance = calculate_relative_performance(
        instrument_return,
        benchmark_return,
    )

    # Calculate Base 100
    instrument_base_100 = calculate_base_100(
        aligned_instrument
    )

    benchmark_base_100 = calculate_base_100(
        aligned_benchmark
    )

    # Return the application snapshot
    return {
        "provider": "Bloomberg stage - APPROVED_SAMPLE",
        "lookback": LOOKBACK_LABEL,
        "interval": INTERVAL_LABEL,

        "instrument": {
            "ticker": instrument["ticker"],
            "name": instrument["name"],
        },

        "benchmark": {
            "ticker": benchmark["ticker"],
            "name": benchmark["name"],
        },

        "instrument_return": instrument_return,
        "benchmark_return": benchmark_return,
        "relative_performance": relative_performance,

        "instrument_base_100": instrument_base_100,
        "benchmark_base_100": benchmark_base_100,
    }


    
def print_market_snapshot(snapshot):
    instrument = snapshot["instrument"]
    benchmark = snapshot["benchmark"]
    instrument_base_100 = snapshot["instrument_base_100"]
    benchmark_base_100 = snapshot["benchmark_base_100"]

    print("=== MarketPulse ===")
    print()
    print("Provider")
    print(snapshot["provider"])
    print()
    print("Market configuration")
    print(f"Instrument : {instrument['ticker']} - {instrument['name']}")
    print(f"Benchmark  : {benchmark['ticker']} - {benchmark['name']}")
    print(f"Period     : {snapshot['lookback']}")
    print(f"Interval   : {snapshot['interval']}")
    print(f"Common observations : {len(instrument_base_100)}")
    print(
        f"From {instrument_base_100[0]['date']} "
        f"to {instrument_base_100[-1]['date']}"
    )
    print()
    print(f"Instrument return : {snapshot['instrument_return']:.2f}%")
    print(f"Benchmark return  : {snapshot['benchmark_return']:.2f}%")
    print()
    print("Relative performance")
    print(
        f"{instrument['ticker']} vs {benchmark['ticker']} : "
        f"{snapshot['relative_performance']:+.2f} percentage points"
    )
    print()
    print("Base 100")
    print(
        f"{instrument['ticker']:<5} : "
        f"{instrument_base_100[0]['value']:.2f} -> "
        f"{instrument_base_100[-1]['value']:.2f}"
    )
    print(
        f"{benchmark['ticker']:<5} : "
        f"{benchmark_base_100[0]['value']:.2f} -> "
        f"{benchmark_base_100[-1]['value']:.2f}"
    )



def main():
    snapshot = build_market_snapshot()
    print_market_snapshot(snapshot)


if __name__ == "__main__":
    main()



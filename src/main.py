from pathlib import Path
import csv
import json
from analytics import *
import yfinance as yf

from providers.yahoo_provider import *

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



def main():
    
    instruments = load_instruments()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    YAHOO_SYMBOLS = {
        "AAPL": "AAPL",
        "SP500": "^GSPC",
    }

    instrument_prices = fetch_yahoo_prices(
        symbol=YAHOO_SYMBOLS[instrument["ticker"]],
        canonical_ticker=instrument["ticker"],
        period="1mo",
        interval="1d",
    )

    benchmark_prices = fetch_yahoo_prices(
        symbol=YAHOO_SYMBOLS[benchmark["ticker"]],
        canonical_ticker=benchmark["ticker"],
        period="1mo",
        interval="1d",
    )

  

    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices,
        benchmark_prices,
    )

    

    assert len(aligned_instrument) > 0, "Instrument series is empty"
    assert len(aligned_benchmark) > 0, "Benchmark series is empty"

    assert len(aligned_instrument) == len(aligned_benchmark), \
        "Aligned series have different lengths"

    same_dates = all(
        instrument_row["date"] == benchmark_row["date"]
        for instrument_row, benchmark_row in zip(
            aligned_instrument,
            aligned_benchmark,
        )
    )

    assert same_dates, "Dates do not match"

    


    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)

    relative_performance = calculate_relative_performance(
        instrument_return,
        benchmark_return,
    )

    

    instrument_base_100 = calculate_base_100(aligned_instrument)
    benchmark_base_100 = calculate_base_100(aligned_benchmark)

    instrument_base_100_final = instrument_base_100[-1]["value"]
    benchmark_base_100_final = benchmark_base_100[-1]["value"]

    
    
    print("=== MarketPulse ===")
    print()

    print("Provider")
    print("Yahoo Finance via yfinance")
    print()

    print("Market configuration")
    print(f"Instrument : {instrument['ticker']} - {instrument['name']}")
    print(f"Benchmark  : {benchmark['name']}")
    print(f"Period     : {LOOKBACK_LABEL}")
    print(f"Interval   : {INTERVAL_LABEL}")
    print()
 
    print("Instrument return")
    print(f"{instrument['ticker']} : {instrument_return:+.2f}%")
    print()

    print("Benchmark return")
    print(f"{benchmark['ticker']} : {benchmark_return:+.2f}%")
    print()

    print("Relative performance")
    print(
        f"{instrument['ticker']} vs {benchmark['ticker']} : "
        f"{relative_performance:+.2f} percentage points"
    )
    print()

    print("Base 100")
    print(
        f"{instrument['ticker']} : "
        f"100.00 -> {instrument_base_100_final:.2f}"
    )
    print(
        f"{benchmark['ticker']} : "
        f"100.00 -> {benchmark_base_100_final:.2f}"
    )
    print()

  


if __name__ == "__main__":
    main()

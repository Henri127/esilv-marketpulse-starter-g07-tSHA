from pathlib import Path
import csv
import json
from analytics import *

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
    prices = load_prices()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = filter_prices(prices, instrument["ticker"])
    benchmark_prices = filter_prices(prices, benchmark["ticker"])

    instrument_latest = instrument_prices[-1]
    benchmark_latest = benchmark_prices[-1]


    normalized_prices = [
    normalize_price_row(row)
    for row in prices
    ]



    aligned_instrument, aligned_benchmark = align_series(
    instrument_prices,
    benchmark_prices,
    )
    
    


    instrument_return = calculate_period_return(
    aligned_instrument
    )

    benchmark_return = calculate_period_return(
        aligned_benchmark
    )

    instrument_base_100 = calculate_base_100(instrument_prices)[-1]["value"]
    benchmark_base_100 = calculate_base_100(benchmark_prices)[-1]["value"]


    relative_performance = calculate_relative_performance(
        instrument_return,
        benchmark_return
    )



        
    print("=== MarketPulse ===")
    print()

    print("Market configuration")
    print(f"Period   : {LOOKBACK_LABEL}")
    print(f"Interval : {INTERVAL_LABEL}")
    print()

    print("Instrument")
    print(f"{instrument['ticker']} - {instrument['name']}")
    print(f"Period return : {instrument_return:+.2f}%")
    print()

    print("Benchmark")
    print(f"{benchmark['ticker']} - {benchmark['name']}")
    print(f"Period return : {benchmark_return:+.2f}%")
    print()

    print("Relative performance")
    print(
        f"{instrument['ticker']} vs {benchmark['ticker']} : "
        f"{relative_performance:+.2f} %"
    )
    print()

    print("Base 100")
    print(
        f"{instrument['ticker']}  : "
        f"100.00 -> {instrument_base_100:.2f}"
    )
    print(
        f"{benchmark['ticker']} : "
        f"100.00 -> {benchmark_base_100:.2f}"
    )



  

    assert len(aligned_instrument) > 0
    assert len(aligned_benchmark) > 0
    assert len(aligned_instrument) == len(aligned_benchmark)






    


if __name__ == "__main__":
    main()

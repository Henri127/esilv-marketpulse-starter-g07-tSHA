from pathlib import Path
import json

from analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)
from providers.bloomberg_provider import fetch_bloomberg_prices


DATA_DIR = Path("data/sample")

LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"
BLOOMBERG_MODE = "APPROVED_SAMPLE"


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def build_market_snapshot():
    instruments = load_instruments()
    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = fetch_bloomberg_prices(
        instrument["ticker"],
        BLOOMBERG_MODE,
    )
    benchmark_prices = fetch_bloomberg_prices(
        benchmark["ticker"],
        BLOOMBERG_MODE,
    )

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
    relative_performance = calculate_relative_performance(
        instrument_return,
        benchmark_return,
    )

    return {
        "provider": f"Bloomberg stage - {BLOOMBERG_MODE}",
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
        "instrument_base_100": calculate_base_100(aligned_instrument),
        "benchmark_base_100": calculate_base_100(aligned_benchmark),
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
    print("Access mode")
    print(BLOOMBERG_MODE)
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
        f"{instrument_base_100[0]['value']:.2f} -> {instrument_base_100[-1]['value']:.2f}"
    )
    print(
        f"{benchmark['ticker']:<5} : "
        f"{benchmark_base_100[0]['value']:.2f} -> {benchmark_base_100[-1]['value']:.2f}"
    )


def main():
    snapshot = build_market_snapshot()
    print_market_snapshot(snapshot)


if __name__ == "__main__":
    main()

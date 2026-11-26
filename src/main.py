from pathlib import Path
import json

from analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)
from providers.yahoo_provider import fetch_yahoo_prices


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


def main():
    instruments = load_instruments()
    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = fetch_yahoo_prices(
        symbol=YAHOO_SYMBOLS[instrument["ticker"]],
        canonical_ticker=instrument["ticker"],
        period=YAHOO_PERIOD,
        interval=YAHOO_INTERVAL,
    )
    benchmark_prices = fetch_yahoo_prices(
        symbol=YAHOO_SYMBOLS[benchmark["ticker"]],
        canonical_ticker=benchmark["ticker"],
        period=YAHOO_PERIOD,
        interval=YAHOO_INTERVAL,
    )

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

    print("=== MarketPulse ===")
    print()
    print("Provider")
    print("Yahoo Finance via yfinance")
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

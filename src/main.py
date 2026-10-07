from pathlib import Path
import csv
import json


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

def main():
    instruments = load_instruments()
    prices = load_prices()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = filter_prices(prices, instrument["ticker"])
    benchmark_prices = filter_prices(prices, benchmark["ticker"])

    instrument_latest = instrument_prices[-1]
    benchmark_latest = benchmark_prices[-1]

    print("=== MarketPulse ===")
    print()
    print("Market configuration")
    print(f"Period: {LOOKBACK_LABEL}")
    print(f"Interval: {INTERVAL_LABEL}")
    print()
    print("Instruments")
    display_market_summary(instrument,instrument_prices)
    print()
    print("Benchmark")
    display_market_summary(benchmark,benchmark_prices,False)
    print()
    print(get_first_date(prices))
    print(get_last_date(prices))
    print()
    print(f"Max instrument : {max_close(instrument_prices)}")
    print(f"Min instrument : {min_close(instrument_prices)}")
    print()
    print(f"Max benchmark : {max_close(benchmark_prices)}")
    print(f"Min benchmark : {min_close(benchmark_prices)}")

if __name__ == "__main__":
    main()

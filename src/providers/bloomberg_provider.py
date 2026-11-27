import json
from pathlib import Path
from analytics import align_series

BLOOMBERG_IDENTIFIERS = {
    "AAPL": "AAPL US Equity",
    "SP500": "SPX Index",
}



REFERENCE_SAMPLE = Path(
    "data/sample/bloomberg_reference_sample.json"
)


def load_bloomberg_reference_sample(
    path=REFERENCE_SAMPLE,
):
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def find_reference_series(
    payload,
    provider_identifier,
):
    for series in payload["series"]:
        if (
            series["provider_identifier"]
            == provider_identifier
        ):
            return series

    raise ValueError(
        "Approved Bloomberg-stage series not found: "
        f"{provider_identifier}"
    )


def normalize_reference_series(series):
    canonical_ticker = series["canonical_ticker"]
    rows = []

    for observation in series["observations"]:
        rows.append({
            "date": observation["observation_date"],
            "ticker": canonical_ticker,
            "open": float(observation["open_value"]),
            "high": float(observation["high_value"]),
            "low": float(observation["low_value"]),
            "close": float(observation["close_value"]),
            "volume": int(observation["volume_value"]),
        })

    return rows


def fetch_approved_sample_prices(
    provider_identifier,
):
    payload = load_bloomberg_reference_sample()

    series = find_reference_series(
        payload,
        provider_identifier,
    )

    return normalize_reference_series(series)


if __name__ == "__main__":

    apple_prices = fetch_approved_sample_prices(
        BLOOMBERG_IDENTIFIERS["AAPL"]
    )

    sp500_prices = fetch_approved_sample_prices(
        BLOOMBERG_IDENTIFIERS["SP500"]
    )

    print("AAPL:")
    print(apple_prices[:2])

    print("\nSP500:")
    print(sp500_prices[:2])


        # Part 8 - comparaison

    EXPECTED_FILE = Path(
        "data/sample/bloomberg_reference_expected.json"
    )

    with open(EXPECTED_FILE, encoding="utf-8") as file:
        expected_data = json.load(file)

    expected_rows = expected_data["rows"]

    actual_rows = apple_prices + sp500_prices

    print("\nPart 8 - Expected result comparison:")
    print("Actual rows:", len(actual_rows))
    print("Expected rows:", len(expected_rows))

    assert actual_rows == expected_rows

    print("SUCCESS: normalized rows match expected result.")


        # Part 9 

    aligned_apple, aligned_sp500 = align_series(
        apple_prices,
        sp500_prices,
    )

    print("\nPart 9 - Alignment:")
    print("AAPL rows:", len(aligned_apple))
    print("SP500 rows:", len(aligned_sp500))

    assert len(aligned_apple) == len(aligned_sp500)

    assert [
        row["date"] for row in aligned_apple
    ] == [
        row["date"] for row in aligned_sp500
    ]

    print("SUCCESS: Bloomberg series are aligned.")



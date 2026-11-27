import json
from pathlib import Path


# Canonical MarketPulse ticker -> Bloomberg identifier (TD09 mapping)
BLOOMBERG_IDENTIFIERS = {
    "AAPL": "AAPL US Equity",
    "SP500": "SPX Index",
}

REFERENCE_SAMPLE = Path(
    "data/sample/bloomberg_reference_sample.json"
)


# ---------- APPROVED_SAMPLE path ----------

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
    # Teaching wrapper keys, not Bloomberg field mnemonics
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


# ---------- LIVE boundary (not available in this environment) ----------

def fetch_raw_bloomberg_history(
    identifier,
    start_date,
    end_date,
):
    # The instructor supplies or demonstrates
    # the environment-specific implementation.
    raise NotImplementedError


def normalize_bloomberg_history(
    raw_data,
    canonical_ticker,
):
    # LIVE field names must come from docs/BLOOMBERG_FIELD_MAPPING.md
    raise NotImplementedError


# ---------- Provider entry point ----------

def fetch_bloomberg_prices(
    canonical_ticker,
    mode="APPROVED_SAMPLE",
):
    identifier = BLOOMBERG_IDENTIFIERS[canonical_ticker]

    if mode == "APPROVED_SAMPLE":
        return fetch_approved_sample_prices(identifier)

    raise ValueError(
        f"Bloomberg access mode not available: {mode}"
    )

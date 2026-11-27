# Bloomberg Field Mapping

## Access mode

APPROVED_SAMPLE

- Source: `data/sample/bloomberg_reference_sample.json`
- Reference: `docs/10_BLOOMBERG_INSTRUCTOR_REFERENCE.md` (instructor reference mapping)
- Sample provenance: instructor fallback fixture
- Expected canonical reference: `data/sample/bloomberg_reference_expected.json`
- Live connectivity: not demonstrated

The fixture declares `"access_mode": "approved_sample"` and
`"is_live_bloomberg_output": false`. Its values are illustrative teaching
values reused from `data/sample/prices.csv`, not certified Bloomberg
historical observations.

## Market instruments

| Role | Canonical ticker | Bloomberg identifier |
|---|---|---|
| Instrument | AAPL | AAPL US Equity |
| Benchmark | SP500 | SPX Index |

## Inspected inputs

| Series | provider_identifier | canonical_ticker | Observations | First date | Last date |
|---|---|---|---|---|---|
| instrument | AAPL US Equity | AAPL | 21 | 2026-09-01 | 2026-09-30 |
| benchmark | SPX Index | SP500 | 21 | 2026-09-01 | 2026-09-30 |

Each observation contains the keys `observation_date`, `open_value`,
`high_value`, `low_value`, `close_value` and `volume_value`.
No missing value was found in either series.

## Field mapping

| MarketPulse field | Source field or mapping | Status / notes |
|---|---|---|
| date | `observation_date` | teaching wrapper key, ISO string `YYYY-MM-DD` |
| ticker | application mapping from `canonical_ticker` | AAPL or SP500, never the Bloomberg identifier |
| open | `open_value` | teaching wrapper key, convert to float |
| high | `high_value` | teaching wrapper key, convert to float |
| low | `low_value` | teaching wrapper key, convert to float |
| close | `close_value` | teaching wrapper key, convert to float |
| volume | `volume_value` | teaching wrapper key, convert to int (0 for SPX Index) |

Teaching wrapper key != Bloomberg LIVE field mnemonic.

The keys above come from the approved fallback fixture. They are not
Bloomberg field mnemonics, and no LIVE Bloomberg field name is claimed
in this document.

## TD10 handoff

- Access mode: APPROVED_SAMPLE
- Instrument identifier: AAPL US Equity -> canonical ticker AAPL
- Benchmark identifier: SPX Index -> canonical ticker SP500
- Date representation: ISO string `YYYY-MM-DD` in `observation_date`
- Input structure: JSON object with metadata and a `series` list;
  each series has `role`, `canonical_ticker`, `provider_identifier`
  and an `observations` list
- Missing fields: none in the sample
- Special normalization notes:
  - SPX Index prices are stored as integers (for example 6600):
    convert open/high/low/close to float
  - SPX Index `volume_value` is 0 (an index has no traded volume)
  - the output ticker must be the canonical ticker, not the
    Bloomberg identifier
  - Bloomberg identifiers stay inside the provider, analytics.py
    remains unchanged
- Expected canonical reference: `data/sample/bloomberg_reference_expected.json`

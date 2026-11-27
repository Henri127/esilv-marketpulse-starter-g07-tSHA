# Bloomberg Field Mapping

## Access mode

APPROVED_SAMPLE

Source:
data/sample/bloomberg_reference_sample.json

Reference:
docs/10_BLOOMBERG_INSTRUCTOR_REFERENCE.md

Live connectivity:
not demonstrated

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
| date | observation_date | string |
| ticker | application mapping | AAPL or SP500 |
| open | open_value | float |
| high | high_value | float |
| low | low_value | float |
| close | close_value | float |
| volume | volume_value | int |


## TD10 handoff

- Access mode:approved_sample
- Instrument identifier:AAPL US Equity
- Benchmark identifier:SPX Index
- Date representation: YYYY-MM-DD
- Input structure: 
- Missing fields: none
- Special normalization notes:
- Expected canonical reference : data/sample/bloomberg_reference_expected.json

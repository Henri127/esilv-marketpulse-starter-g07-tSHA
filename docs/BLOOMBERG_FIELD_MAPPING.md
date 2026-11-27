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

- Access mode: APPROVED_SAMPLE
- Instrument identifier: AAPL US Equity
- Benchmark identifier:SPX Index
- Date representation: YYYY-MM-DD
- Input structure:  JSON file containing metadata and a series array
- Missing fields: None in the provided sample structure
- Special normalization notes:
observation_date -> date
open_value -> open
high_value -> high
low_value -> low
close_value -> close
volume_value -> volume
Expected canonical reference:  
data/sample/bloomberg_reference_expected.json
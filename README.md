# Solar Performance Analytics

A beginner-friendly Python project for analysing daily solar plant performance using generation, plane-of-array (POA) irradiation, and installed DC capacity.

## Features

- Calculates daily Performance Ratio (PR)
- Calculates daily Capacity Utilisation Factor (CUF)
- Estimates expected generation from POA irradiation and installed DC capacity
- Calculates generation deviation against expected generation
- Produces a monthly summary CSV
- Includes synthetic sample data and basic automated tests

## Important assumptions

This is an illustrative screening tool, not a bankable energy assessment or contractual performance guarantee.

- `energy_kwh` is daily AC energy generated, in kWh.
- `poa_kwh_m2` is daily plane-of-array irradiation, in kWh/m².
- `installed_capacity_kwp` is installed DC capacity, in kWp.
- Expected generation is approximated as `POA irradiation × installed DC capacity`.
- PR is `actual energy / expected generation × 100`.
- CUF is `actual energy / (installed capacity × 24 hours) × 100`.

The calculation assumes consistent reporting boundaries and does not independently correct for clipping, availability, curtailment, meter losses, or capacity changes.

## Project structure

```text
solar-performance-analytics/
├── sample_data/
│   └── daily_plant_data.csv
├── src/
│   └── solar_analytics.py
├── tests/
│   └── test_solar_analytics.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Requirements

- Python 3.10 or newer
- pandas

## Setup

### Windows

```bash
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Run the analysis

From the repository's root folder:

```bash
python -m src.solar_analytics --input sample_data/daily_plant_data.csv --output output
```

The program creates:

- `output/daily_analysis.csv`
- `output/monthly_summary.csv`

## Input CSV format

| Column | Description | Unit |
|---|---|---|
| date | Reporting date | YYYY-MM-DD |
| energy_kwh | Daily AC energy | kWh |
| poa_kwh_m2 | Daily POA irradiation | kWh/m² |
| installed_capacity_kwp | Installed DC capacity | kWp |

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Disclaimer

Sample data is synthetic and for learning purposes only. Validate data quality, measurement boundaries, and engineering assumptions before using any calculation for operational or commercial decisions.

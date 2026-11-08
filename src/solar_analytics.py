"""Daily solar plant performance calculations.

Run from the repository root:
python -m src.solar_analytics --input sample_data/daily_plant_data.csv --output output
"""
from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = {
    "date",
    "energy_kwh",
    "poa_kwh_m2",
    "installed_capacity_kwp",
}


def analyse_daily_data(data: pd.DataFrame) -> pd.DataFrame:
    """Validate input and calculate daily PR, CUF, and generation deviation."""
    missing = REQUIRED_COLUMNS - set(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

    result = data.copy()
    result["date"] = pd.to_datetime(result["date"], errors="raise")
    numeric_cols = ["energy_kwh", "poa_kwh_m2", "installed_capacity_kwp"]

    for column in numeric_cols:
        result[column] = pd.to_numeric(result[column], errors="raise")

    if (result[numeric_cols] < 0).any().any():
        raise ValueError("Energy, irradiation, and capacity cannot be negative.")
    if (result["installed_capacity_kwp"] <= 0).any():
        raise ValueError("Installed DC capacity must be greater than zero.")

    result["expected_generation_kwh"] = (
        result["poa_kwh_m2"] * result["installed_capacity_kwp"]
    )
    result["pr_pct"] = (
        result["energy_kwh"] / result["expected_generation_kwh"] * 100
    ).where(result["expected_generation_kwh"] > 0)

    result["cuf_pct"] = (
        result["energy_kwh"]
        / (result["installed_capacity_kwp"] * 24)
        * 100
    )
    result["generation_deviation_kwh"] = (
        result["energy_kwh"] - result["expected_generation_kwh"]
    )
    result["month"] = result["date"].dt.to_period("M").astype(str)

    return result.sort_values("date").reset_index(drop=True)


def create_monthly_summary(daily: pd.DataFrame) -> pd.DataFrame:
    """Aggregate daily data and calculate energy-weighted monthly PR and CUF."""
    grouped = daily.groupby("month", as_index=False).agg(
        actual_generation_kwh=("energy_kwh", "sum"),
        expected_generation_kwh=("expected_generation_kwh", "sum"),
        installed_capacity_kwp=("installed_capacity_kwp", "last"),
        days_reported=("date", "nunique"),
    )
    grouped["pr_pct"] = (
        grouped["actual_generation_kwh"]
        / grouped["expected_generation_kwh"] * 100
    ).where(grouped["expected_generation_kwh"] > 0)

    grouped["cuf_pct"] = (
        grouped["actual_generation_kwh"]
        / (
            grouped["installed_capacity_kwp"]
            * grouped["days_reported"]
            * 24
        )
        * 100
    )
    grouped["generation_deviation_kwh"] = (
        grouped["actual_generation_kwh"]
        - grouped["expected_generation_kwh"]
    )
    return grouped


def main() -> None:
    parser = argparse.ArgumentParser(description="Solar plant performance analytics")
    parser.add_argument("--input", required=True, help="Path to input daily CSV")
    parser.add_argument("--output", default="output", help="Output folder")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    raw = pd.read_csv(input_path)
    daily = analyse_daily_data(raw)
    monthly = create_monthly_summary(daily)

    daily_path = output_dir / "daily_analysis.csv"
    monthly_path = output_dir / "monthly_summary.csv"
    daily.to_csv(daily_path, index=False, float_format="%.2f")
    monthly.to_csv(monthly_path, index=False, float_format="%.2f")

    print(f"Analysis completed. Daily results: {daily_path}")
    print(f"Monthly summary: {monthly_path}")


if __name__ == "__main__":
    main()

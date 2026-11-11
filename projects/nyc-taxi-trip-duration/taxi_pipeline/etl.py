"""Clean NYC TLC January 2025 Yellow Taxi trips for weekday analytics.

CLI: python -m taxi_pipeline.etl --input INPUT --output OUTPUT
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

REQUIRED = ("tpep_pickup_datetime", "tpep_dropoff_datetime", "trip_distance")


def clean_taxi_trips(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    """Return a weekday-only analytic dataset and transparent quality counts.

    Uses local NYC pickup timestamps as recorded by the TLC file (no timezone inference).
    """
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    data = df.loc[:, REQUIRED].copy()
    counts: dict[str, int] = {"source_rows": len(data)}
    data["tpep_pickup_datetime"] = pd.to_datetime(data["tpep_pickup_datetime"], errors="coerce")
    data["tpep_dropoff_datetime"] = pd.to_datetime(data["tpep_dropoff_datetime"], errors="coerce")
    data["trip_distance"] = pd.to_numeric(data["trip_distance"], errors="coerce")
    counts["invalid_or_missing_values"] = int(data.isna().any(axis=1).sum())
    data = data.dropna(subset=list(REQUIRED)).copy()

    january = (data["tpep_pickup_datetime"] >= "2025-01-01") & (data["tpep_pickup_datetime"] < "2025-02-01")
    counts["outside_january"] = int((~january).sum())
    data = data.loc[january].copy()

    duration_min = (data["tpep_dropoff_datetime"] - data["tpep_pickup_datetime"]).dt.total_seconds() / 60
    valid_duration = duration_min.between(1, 120, inclusive="both")
    counts["invalid_duration"] = int((~valid_duration).sum())
    data = data.loc[valid_duration].copy()
    data["trip_duration_min"] = duration_min.loc[valid_duration]

    valid_distance = data["trip_distance"].between(0.1, 30, inclusive="both")
    counts["invalid_distance"] = int((~valid_distance).sum())
    data = data.loc[valid_distance].copy()
    counts["cleaned_all_days"] = len(data)

    data["day_of_week"] = data["tpep_pickup_datetime"].dt.day_of_week
    weekdays = data["day_of_week"] < 5
    counts["weekend_excluded"] = int((~weekdays).sum())
    data = data.loc[weekdays].copy()
    pickup_hour = data["tpep_pickup_datetime"].dt.hour
    data["peak_hour"] = ((pickup_hour.between(7, 9)) | (pickup_hour.between(16, 18))).astype("int8")
    counts["weekday_analysis_rows"] = len(data)
    return data.reset_index(drop=True), counts


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True, type=Path, help="CSV or Parquet source")
    p.add_argument("--output", required=True, type=Path, help="Parquet destination")
    args = p.parse_args()
    if args.input.suffix.lower() == ".parquet":
        source = pd.read_parquet(args.input, columns=list(REQUIRED))
    elif args.input.suffix.lower() == ".csv":
        source = pd.read_csv(args.input)
    else:
        p.error("Input must end in .csv or .parquet")
    cleaned, counts = clean_taxi_trips(source)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_parquet(args.output, index=False)
    print("Wrote:", args.output)
    for key, value in counts.items():
        print(f"{key}: {value:,}")


if __name__ == "__main__":
    main()

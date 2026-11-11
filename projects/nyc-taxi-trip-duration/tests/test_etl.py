import pandas as pd
import pytest

from taxi_pipeline.etl import clean_taxi_trips


def test_peak_flags_and_filters():
    df = pd.DataFrame({
        "tpep_pickup_datetime": [
            "2025-01-06 08:00", "2025-01-06 11:00", "2025-01-11 08:00",
            "2025-02-01 08:00", "2025-01-07 17:00"
        ],
        "tpep_dropoff_datetime": [
            "2025-01-06 08:15", "2025-01-06 11:10", "2025-01-11 08:10",
            "2025-02-01 08:15", "2025-01-07 17:25"
        ],
        "trip_distance": [2.5, 2.5, 2.0, 2.0, 4.0],
    })
    cleaned, counts = clean_taxi_trips(df)
    assert counts["source_rows"] == 5
    assert counts["cleaned_all_days"] == 4
    assert counts["weekend_excluded"] == 1
    assert counts["weekday_analysis_rows"] == 3
    assert cleaned["peak_hour"].tolist() == [1, 0, 1]
    assert cleaned["trip_duration_min"].tolist() == [15.0, 10.0, 25.0]


def test_missing_column_fails():
    with pytest.raises(ValueError, match="Missing required columns"):
        clean_taxi_trips(pd.DataFrame({"trip_distance": [1]}))

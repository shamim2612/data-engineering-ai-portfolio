-- Athena / AWS Glue Data Catalog: run after uploading curated Parquet.
-- Replace YOUR_BUCKET with your own bucket name.
CREATE DATABASE IF NOT EXISTS d610_taxi;

CREATE EXTERNAL TABLE IF NOT EXISTS d610_taxi.yellow_taxi_weekday_curated (
    tpep_pickup_datetime TIMESTAMP,
    tpep_dropoff_datetime TIMESTAMP,
    trip_distance DOUBLE,
    trip_duration_min DOUBLE,
    day_of_week BIGINT,
    peak_hour TINYINT
)
STORED AS PARQUET
LOCATION 's3://YOUR_BUCKET/curated/yellow_taxi_2025_01/';

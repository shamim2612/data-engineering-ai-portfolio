# NYC Yellow Taxi Trip Duration Analysis

**Status:** Work in progress. This is a portfolio implementation of a WGU D610 data engineering capstone. The research topic has instructor approval; the final analysis and report are still in progress.

## Question

For New York City yellow taxi trips in January 2025, is trip duration associated with weekday rush-hour pickup status after controlling for trip distance and day of week?

A two-sided statistical test will assess whether the adjusted rush-hour association is distinguishable from zero. This is **observational**, not a causal measure of traffic delays.

## Pipeline

```text
NYC TLC public January 2025 Yellow Taxi Parquet
    -> Python validation & cleaning
    -> analysis-ready Parquet
    -> Amazon S3 (raw/ and curated/)
    -> Athena SQL summaries
    -> statistical analysis, documentation, visualizations
```

AWS Glue is an optional ETL execution path if permissions permit. A restricted training account did **not** successfully execute Glue because of its role trust policy; personal AWS or local Python is the fallback.

## What is implemented in this repository?

- [x] Standalone Python data-preparation module with CLI and quality checks
- [x] Small synthetic test dataset and unit tests
- [x] Example Athena external-table DDL and analysis query
- [ ] Run the pipeline on the full January 2025 public Parquet file in this repository version
- [ ] Load the curated Parquet into S3 and verify full-record Athena queries
- [ ] Final adjusted regression, diagnostic checks, plots, and validated findings

Preliminary local exploratory work was performed separately; those numbers are not presented as validated final results here.

## Run locally

From this project folder:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python -m taxi_pipeline.etl --input data/sample_taxi.csv --output outputs/demo_clean.parquet
```

**Source data:** Download `yellow_tripdata_2025-01.parquet` from the [NYC TLC trip records page](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page), put it under `data/raw/`, then run:

```bash
python -m taxi_pipeline.etl --input data/raw/yellow_tripdata_2025-01.parquet --output data/curated/nyc_taxi_2025_01.parquet
```

The output includes weekday trips with flags and durations, ready for aggregates and downstream modeling. Raw data is **not** published to GitHub. The code processes in memory using Pandas; memory capacity must be checked on the full dataset. For larger workloads use a chunked or Spark-based ETL.

## Data rules (initial, subject to documentation and review)

- Only pickups during January 2025, using the pickup timestamp.
- Valid positive trip duration up to 120 minutes.
- Trip distance between 0.1 and 30 miles, inclusive.
- Analysis sample restricted to Monday–Friday.
- Peak hours: 07:00–09:59 and 16:00–18:59, based on pickup local hour.

These rules exclude outliers and may affect representativeness; the final report will disclose counts excluded by each condition.

## Data quality and limitations

The published dataset may contain anomalies or incomplete fields. Trip distances and timestamps are recorded observations; pickup times alone do not measure actual congestion. Location, route, weather, and events can confound observed associations. The project will report model assumptions and the distinction between statistical and practical significance.

## Athena

See `sql/01_create_curated_table.sql` and `sql/02_peak_summary.sql`. Replace the placeholder S3 bucket in the DDL with your own bucket. Run only after uploading the curated Parquet to the matching location. Choose a query-output location in Athena beforehand. Athena queries may incur charges.

## AWS cost / security

Use one region (for example `us-east-1`), private S3 buckets, IAM least privilege, AWS budget notifications, and clean up unused resources. Never commit access keys, account IDs, confidential screenshots, or student identifiers.

## Future work

- Extend analysis to additional months.
- Examine spatial variation using pickup/drop-off taxi zones.
- Compare alternative duration models and robustness checks.

## References

New York City Taxi and Limousine Commission. *TLC Trip Record Data*. https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

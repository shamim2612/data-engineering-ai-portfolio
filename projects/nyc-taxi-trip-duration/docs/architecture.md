# Architecture decisions

## Scope
January 2025 public NYC yellow taxi trip records, weekday rush-hour comparison.

## Cloud services
- **S3** is the raw/curated object store; verify bucket permissions and persistence.
- **Athena** provides SQL over the curated Parquet data using a catalog table.
- **Glue ETL** is optional. Training-account Glue execution was blocked by a role trust-policy error, not a processing-code issue.
- **Python** performs fallback ETL and later regression analysis.

## Evidence to collect for the capstone report
1. Data source/download information and original schema/row count.
2. Data quality counts, missing values, exclusions, and final schema.
3. S3 upload and curated prefix.
4. Athena DDL, successful row-count query, group statistics.
5. Regression code/results, model assumptions, plots, and limitations.

> Do not publish screenshots revealing AWS account identities, signatures, student IDs, or graded submission files.

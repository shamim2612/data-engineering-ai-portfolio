# Workstation Setup & Project Continuity Guide

**Project:** Data Engineering & AI Portfolio — NYC Yellow Taxi Trip Duration Analysis  
**Last updated:** November 11, 2026  
**Purpose:** Reproduce the development setup on a different Windows workstation, keep progress synchronized through GitHub, and resume the WGU D610 capstone without relying on files on one PC.

> **Source of truth:** GitHub repository `https://github.com/shamim2612/data-engineering-ai-portfolio`. This guide is versioned in Git. It describes confirmed work and explicitly separates planned steps.

## 1. Current verified status

| Area | Verified progress | Next action |
| --- | --- | --- |
| GitHub | Public portfolio repo exists; local `main` pushed successfully. Pandas deprecation fix committed as `d689ca3`. | Pull this guide/other remote updates before new work. |
| Local Python | Python 3.13.9, virtual environment, pytest, pandas and pyarrow installed. | Rebuild virtual environment separately on any new PC. |
| Unit tests | `python -m pytest` yielded **2 passed, 0 warnings** after the date-accessor fix. | Repeat on new workstation. |
| Dataset | Original January 2025 NYC TLC Yellow Taxi Parquet downloaded; metadata verified: **3,475,226 rows, 20 columns**, size **59,158,238 bytes**. | Put a local copy under project `data/raw/` on each PC, or retrieve from public source. |
| AWS training account | Private S3 bucket created; CSV upload and Athena external-table query succeeded. | Validate full Parquet pipeline; training-account persistence not guaranteed. |
| AWS Glue | Test job was created, but execution **failed**: `voclabs` role does not trust AWS Glue. | Use Python ETL or separately configure a permitted Glue execution role in a personal account. |
| WGU D610 Task 1 | Instructor approved topic on Nov 6, 2026; a signed nonrestricted-data release form was reviewed in chat. | Confirm Task 1 submission and **pass** status in WGU (not yet independently verified). |
| WGU D610 Task 2 | Design and preliminary exploration completed separately; final reproducible full-data run and report not yet complete. | Complete actual ETL, S3/Athena checks, model, evidence and report. |

**Security:** Never commit signed WGU forms, student IDs, AWS secrets, IAM credentials, or real large raw datasets. Do not copy workstation-specific home directory paths into reusable scripts.

## 2. Prerequisites on a new Windows PC

Install and verify:
- **Git for Windows** from https://git-scm.com/downloads/win
- **Python 3.13.x** (or a separately tested compatible version) from https://www.python.org/downloads/windows/ ; during installation select the option to add Python to PATH, if offered
- **VS Code** optional, from https://code.visualstudio.com/
- GitHub access to the repository
- Internet to install Python packages and download public TLC Parquet data

Open **Command Prompt (cmd)**, not PowerShell, for the commands below. If you use PowerShell, environment activation and setting PYTHONPATH have different syntax.

### Check installed tools

```cmd
git --version
python --version
```

**Meaning:** Print installed Git and Python versions. These commands don't modify files. If `python` isn't found, fix installation/PATH first.

## 3. Clone and set up on a NEW computer

Choose a working directory, for example `%USERPROFILE%\Documents`, then run each command separately:

```cmd
cd /d "%USERPROFILE%\Documents"
git clone https://github.com/shamim2612/data-engineering-ai-portfolio.git
cd data-engineering-ai-portfolio
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r projects\nyc-taxi-trip-duration\requirements.txt
```

**What each command does:**
1. `cd /d` changes the current working directory (also handles another drive).
2. `git clone` downloads version-controlled code and commit history; **not** ignored large datasets or secrets.
3. `cd` enters the repository.
4. `python -m venv .venv` creates an isolated, per-computer Python environment. Do **not** copy `.venv` between PCs.
5. `.venv\Scripts\activate` switches CMD to that environment; prompt shows `(.venv)`.
6. `python -m pip install -r ...` installs version-constrained project dependencies. It accesses the internet and changes only the local environment, not GitHub or AWS.

### Run unit tests

From the repository root in CMD:

```cmd
set PYTHONPATH=projects\nyc-taxi-trip-duration
python -m pytest
```

**Meaning:** `set PYTHONPATH` tells Python where the `taxi_pipeline` folder lives for this **CMD session only**; pytest discovers and executes automated unit tests. Expected result currently: **2 passed**, without warnings. If the test suite later grows, the count will change. No AWS charges.

**Tip:** Open a new Command Prompt later? Reactivate `.venv\Scripts\activate` and set `PYTHONPATH` again before tests. Future enhancement: install `taxi_pipeline` as a package so no manual PYTHONPATH is needed.

## 4. Set up again on a computer with an EXISTING checkout

Open Command Prompt inside the previously cloned repository and run:

```cmd
git status
git pull --ff-only
.venv\Scripts\activate
python -m pip install -r projects\nyc-taxi-trip-duration\requirements.txt
set PYTHONPATH=projects\nyc-taxi-trip-duration
python -m pytest
```

**Meaning:** `git status` checks for changes; `git pull --ff-only` downloads updates from GitHub **without creating an automatic merge commit**; activation and pip refresh the local runtime. If Git reports local conflicts or a non-fast-forward update, **stop and inspect** rather than discarding changes.

If there is no `.venv` on that workstation, run `python -m venv .venv` before activation.

## 5. Get the NYC Taxi dataset on each computer

Source: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page  
Direct source file: https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-01.parquet

Create the appropriate folder from the **repository root**:

```cmd
mkdir projects\nyc-taxi-trip-duration\data\raw
```

**Meaning:** Creates a local folder for source files if needed. It is excluded by this repository's `.gitignore`.

Download the Parquet file and save it as:

```text
projects\nyc-taxi-trip-duration\data\raw\yellow_tripdata_2025-01.parquet
```

To verify the metadata without loading all records:

```cmd
python -c "import pyarrow.parquet as pq; p=r'projects\nyc-taxi-trip-duration\data\raw\yellow_tripdata_2025-01.parquet'; f=pq.ParquetFile(p); print('Rows:',f.metadata.num_rows); print('Columns:',f.metadata.num_columns)"
```

**Meaning:** Imports PyArrow, reads Parquet metadata, prints total rows and columns. Expected for the verified January 2025 source: **Rows: 3475226** and **Columns: 20**. It reads local data only.

Check Git ignores it:

```cmd
git check-ignore -v projects/nyc-taxi-trip-duration/data/raw/yellow_tripdata_2025-01.parquet
```

**Meaning:** Shows the ignore rule for the file. This matters before any `git add .`. **Never place the 59 MB dataset in the repository root**; the project's raw folder is excluded, whereas a root-level Parquet file may not be.

## 6. Routine development / keeping two PCs in sync

On whichever PC you start work:

```cmd
git status
git pull --ff-only
```

**Meaning:** Check local changes and retrieve the latest remote commits. Pull before changing files to avoid avoidable conflicts.

After editing and testing your own code:

```cmd
git status
git diff
git add path\to\changed_file.py
git commit -m "Describe the change"
git push
```

**Meaning:** Inspect changed files, inspect unstaged edits, stage only the intended file, create a local snapshot, then upload commits to GitHub. `git push` sends commits, not ignored data. If working on another machine, pull these changes there before editing.

If you have work in progress and cannot pull cleanly, commit it to a suitable branch or ask for conflict assistance; avoid using `git reset --hard` to “fix” things.

## 7. How to run the starter ETL (small sample)

From the **repository root**, after activation and `set PYTHONPATH=...`:

```cmd
python -m taxi_pipeline.etl --input projects\nyc-taxi-trip-duration\data\sample_taxi.csv --output projects\nyc-taxi-trip-duration\data\curated\demo_clean.parquet
```

**Meaning:** Runs the project ETL module, reads the included synthetic sample file, validates/cleans it, and writes a local Parquet output. It **modifies/creates** the output but does not upload anything or incur AWS charges. The output location is ignored by Git.

**Full dataset execution** is the next implementation milestone. Validate memory requirements and script CLI behavior before running 3.47 million rows. Keep the original raw file intact.

## 8. AWS and Task 2 continuation

Planned evidence chain:
1. Source download and metadata/column inspection.
2. Document cleaning criteria, excluded-record counts and curated output.
3. Store raw and curated Parquet in **private** S3 prefixes.
4. Create Athena tables that point to the corresponding Parquet prefixes.
5. Run SQL comparison of weekday peak vs non-peak trips, with actual outputs and screenshots.
6. Run documented multiple linear regression, accounting for distance and day of week; report effect, uncertainty, limitations and practical significance.
7. Produce the Task 2 report and separate screenshot evidence PDF.

**Data rules (initial):** January 2025 pickup dates, valid duration >0 to 120 minutes, distance 0.1–30 miles, weekdays Monday–Friday; peak pickups 07:00–09:59 or 16:00–18:59. Validate and document exclusions for the **actual final run**. Correlations are **not** proof of causal traffic effects.

**Lab verification:** S3 creation and file upload succeeded, and Athena successfully queried a small CSV test. Glue execution failed because the selected `voclabs` role did not allow AWS Glue to assume it. A personal AWS account may be used if the learning lab permissions remain restricted. Do not commit credentials, expose S3 buckets, or assume the lab's resources persist.

**WGU:** Topic approval signed and dated November 6, 2026. Verify separate Task 1 evaluation is **passed** before submitting Task 2. Keep signed forms and WGU submissions outside the public repository.

## 9. Troubleshooting quick reference

| Symptom | Likely explanation | Action |
| --- | --- | --- |
| `No module named pytest` | New environment lacks pytest | Activate `.venv`; install from requirements. |
| `No module named pandas` | Missing dependency | Install requirements in active `.venv`. |
| `No module named taxi_pipeline` | Python import path not set | From repo root: `set PYTHONPATH=projects\nyc-taxi-trip-duration`. |
| `FileNotFoundError` for Parquet | File saved elsewhere | Put it in project's `data\raw\` and use the correct relative path. |
| `git push` rejected | GitHub has new commits | Inspect `git status`, then `git pull --ff-only` if safe. |
| `LF will be replaced by CRLF` | Windows line endings conversion | Usually informational; run tests and review diffs. |
| Glue `assume role permissions` error | IAM trust relationship not authorized | Do not bypass lab policy; use approved role or Python fallback. |

## 10. Update this guide as the project advances

When you complete a meaningful milestone, add:
- **Date and outcome** (what actually worked)
- **Exact commands**, with an explanation and location from which they run
- **Confirmed results** (row counts, test counts, output paths)
- **Current blockers**, proposed next steps
- **New dependencies** in `requirements.txt`
- **References or screenshots locations** without private data

Commit the update like any other code change. Suggested messages: `Document validated full-data ETL run`, `Record Athena query results`, `Add workstation setup notes`.

This file persists on GitHub. **Updates are not automatic**: commit changes from your computer or ask ChatGPT to update the connected repository, and pull on other workstations afterward.

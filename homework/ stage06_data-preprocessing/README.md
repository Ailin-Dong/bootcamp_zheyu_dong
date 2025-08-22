# Homework — Stage 05: Data Storage

## Data Storage

### Folder Structure
```
data/
├─ raw/         # Immutable raw pulls (API/scrape) saved as CSV
└─ processed/   # Cleaned / curated data saved as Parquet
```

### Formats Used & Why
- **CSV (raw/):** Human-readable, diff-able in Git, good for raw captures.
- **Parquet (processed/):** Columnar, compressed, preserves dtypes, efficient for analytics.
  - Requires a Parquet engine (`pyarrow` or `fastparquet`).

### Environment Variables
Configured via `.env` (loaded by `python-dotenv`):
```
DATA_DIR_RAW=data/raw
DATA_DIR_PROCESSED=data/processed
```
The notebook uses these to resolve output directories and will create them if missing.

### Read/Write Utilities
The notebook implements two helpers:
- `write_df(df, path)`: routes by file suffix (`.csv` / `.parquet`), ensures parent dirs exist.
- `read_df(path)`: routes by suffix; CSV attempts to parse a `date` column if present.
- If a Parquet engine is missing, a clear error suggests installing `pyarrow` or `fastparquet`.

### Validation
After saving, we reload both CSV and Parquet and validate:
- Shape matches original
- Critical column dtypes (e.g., `date` is datetime, `price` is numeric)

### Repro Steps
1. Ensure `.env` contains:
   ```
   DATA_DIR_RAW=data/raw
   DATA_DIR_PROCESSED=data/processed
   ```
2. Run the notebook top to bottom.
3. Check generated files in `data/raw/` and `data/processed/`.

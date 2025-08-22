# Homework 05 — Data Storage

This package contains the completed Stage 05 Data Storage homework.

## Folder Structure
```
homework05/
├─ stage05_data-storage_homework-homework05-executed.ipynb   # Executed notebook
├─ .env                                                     # Environment variables
├─ data/
│  ├─ raw/         # Raw data files saved as CSV
│  └─ processed/   # Processed data files saved as CSV/JSON/PNG
```

## .env
The `.env` file defines where data is stored:
```
DATA_DIR_RAW=/Users/hust/bootcamp_zheyu_dong/homework/homework05/data/raw
DATA_DIR_PROCESSED=/Users/hust/bootcamp_zheyu_dong/homework/homework05/data/processed
```

## How to Run
1. Ensure you have dependencies installed:
   ```bash
   pip install pandas matplotlib python-dotenv pyarrow
   ```
   (You can replace `pyarrow` with `fastparquet` if preferred.)

2. Open and run the notebook:
   ```
   stage05_data-storage_homework-homework05-executed.ipynb
   ```

3. The notebook will automatically create the folders specified in `.env` and save data in both CSV and Parquet formats.

## Validation
The notebook reloads both CSV and Parquet files and validates:
- Shapes match the original DataFrame
- `date` column is parsed as datetime (if present)
- `price` column is numeric (if present)

## Utilities
Two helper functions are included:
- `write_df(df, path)`: Writes a DataFrame to CSV or Parquet, inferring from file suffix.
- `read_df(path)`: Reads a DataFrame from CSV or Parquet.

Both handle missing directories and give clear errors if Parquet support is missing.

---

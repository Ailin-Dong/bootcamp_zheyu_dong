# Stage 10b — Time Series Baseline

- Features: lag1/lag5 returns, rolling mean/std (5), rolling min/max (10), momentum(10), zscore(20) — all shifted to avoid leakage.
- Split: last 25% as test (time-aware).
- Pipeline: StandardScaler → Ridge.
- Metrics: MAE/RMSE; plot of prediction vs truth.
- Optional: classification baseline with LogisticRegression (accuracy/precision/recall/F1 + confusion matrix).

To run:
1) Open `notebooks/modeling_timeseries_baseline.ipynb`.
2) Run all cells. The synthetic dataset is already at `data/raw/time_series.csv`.


"""
Evaluation utilities for Stage 11 — bootstrap & diagnostics.
Pure NumPy/Pandas + scikit-learn; matplotlib handled in notebook.
"""

from typing import Callable, Tuple, Dict, Any, Optional
import numpy as np
import pandas as pd

def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Root Mean Squared Error."""
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))

def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Mean Absolute Error."""
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    return float(np.mean(np.abs(y_true - y_pred)))

def bootstrap_model_metric(pipeline, X_train: pd.DataFrame, y_train: pd.Series,
                           X_test: pd.DataFrame, y_test: pd.Series,
                           metric_fn: Callable[[np.ndarray, np.ndarray], float],
                           n_boot: int = 500, random_state: Optional[int] = 0) -> Dict[str, Any]:
    """
    Refit pipeline on bootstrap resamples of the TRAIN set, evaluate on the fixed TEST set.
    Returns distribution of metric on test and 95% CI.
    """
    rng = np.random.default_rng(random_state)
    n = len(X_train)
    metrics = np.empty(n_boot, dtype=float)
    for b in range(n_boot):
        idx = rng.integers(0, n, size=n)  # sample with replacement
        Xb = X_train.iloc[idx]
        yb = y_train.iloc[idx]
        m = pipeline.__class__(**pipeline.get_params(deep=True))  # clone-like instantiation
        # Simpler: use sklearn's clone to be safe if available
        try:
            from sklearn.base import clone
            m = clone(pipeline)
        except Exception:
            pass
        m.fit(Xb, yb)
        pred = m.predict(X_test)
        metrics[b] = metric_fn(y_test.values, pred)
    low, high = np.percentile(metrics, [2.5, 97.5])
    return {"metrics": metrics, "ci_low": float(low), "ci_high": float(high)}

def bootstrap_prediction_band(pipeline, X_train: pd.DataFrame, y_train: pd.Series,
                              X_test: pd.DataFrame, n_boot: int = 500, random_state: Optional[int] = 0,
                              quantiles=(2.5, 50, 97.5)) -> Dict[str, Any]:
    """
    Refit pipeline on bootstrap resamples; return prediction bands on X_test.
    """
    rng = np.random.default_rng(random_state)
    n = len(X_train)
    P = np.zeros((n_boot, len(X_test)), dtype=float)
    for b in range(n_boot):
        idx = rng.integers(0, n, size=n)
        Xb = X_train.iloc[idx]
        yb = y_train.iloc[idx]
        try:
            from sklearn.base import clone
            m = clone(pipeline)
        except Exception:
            m = pipeline.__class__(**pipeline.get_params(deep=True))
        m.fit(Xb, yb)
        P[b, :] = m.predict(X_test)
    qs = np.percentile(P, quantiles, axis=0)
    return {"quantiles": qs, "quantiles_order": quantiles}

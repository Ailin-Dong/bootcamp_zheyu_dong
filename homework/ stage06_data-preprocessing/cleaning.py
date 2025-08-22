
import pandas as pd
import numpy as np
from typing import Iterable, Optional, List

__all__ = ["fill_missing_median", "drop_missing", "normalize_data"]

def _ensure_iter(cols) -> Optional[List[str]]:
    if cols is None:
        return None
    if isinstance(cols, (list, tuple, set)):
        return list(cols)
    return [cols]

def fill_missing_median(df: pd.DataFrame, cols: Optional[Iterable[str]] = None) -> pd.DataFrame:
    """
    Fill missing values in numeric columns with the column median.
    If `cols` is None, operate on all numeric columns.
    Returns a new DataFrame (does not modify in place).
    """
    out = df.copy()
    if cols is None:
        cols = out.select_dtypes(include="number").columns
    else:
        cols = _ensure_iter(cols)
    for c in cols:
        if c in out.columns:
            if pd.api.types.is_numeric_dtype(out[c]):
                med = out[c].median()
                out[c] = out[c].fillna(med)
            else:
                # non-numeric: skip
                pass
    return out


def drop_missing(df: pd.DataFrame, how: str = "any", thresh: Optional[int] = None, subset: Optional[Iterable[str]] = None) -> pd.DataFrame:
    """
    Drop rows with missing values.
    - how: "any" (drop if any NA) or "all" (drop if all NA in subset)
    - thresh: require at least `thresh` non-NA values to keep the row (overrides `how` if set)
    - subset: columns to consider; default all columns
    Returns a new DataFrame.
    """
    out = df.copy()
    kwargs = {}
    if thresh is not None:
        kwargs['thresh'] = thresh
    else:
        kwargs['how'] = how
    if subset is not None:
        kwargs['subset'] = subset
    return out.dropna(**kwargs)
def normalize_data(df: pd.DataFrame, cols: Optional[Iterable[str]] = None, method: str = "zscore") -> pd.DataFrame:
    """
    Normalize numeric data.
    - method="zscore": (x - mean) / std
    - method="minmax": (x - min) / (max - min)
    Only numeric columns are normalized; non-numeric are left unchanged.
    Returns a new DataFrame.
    """
    out = df.copy()
    if cols is None:
        cols = out.select_dtypes(include="number").columns
    else:
        cols = _ensure_iter(cols)

    for c in cols:
        if c in out.columns and pd.api.types.is_numeric_dtype(out[c]):
            series = out[c].astype(float)
            if method == "zscore":
                mu = series.mean()
                sd = series.std(ddof=0)
                out[c] = (series - mu) / sd if sd != 0 else 0.0
            elif method == "minmax":
                mn = series.min()
                mx = series.max()
                out[c] = (series - mn) / (mx - mn) if mx != mn else 0.0
            else:
                raise ValueError("Unsupported method: " + str(method))
    return out

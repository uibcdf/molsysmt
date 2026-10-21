"""Normalizing primitive values at declarative serialization boundaries."""

from collections.abc import Mapping

import numpy as np
import pandas as pd


def normalize_scalar(value):
    """Represent nullable table scalars as Python primitives or None."""
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except Exception:
        pass
    return value.item() if isinstance(value, np.generic) else value


def to_builtin(value):
    """Convert dimensionless containers and NumPy scalars to safe YAML values."""
    if isinstance(value, Mapping):
        return {to_builtin(key): to_builtin(item) for key, item in value.items()}
    if isinstance(value, np.ndarray):
        return to_builtin(value.tolist())
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, (list, tuple)):
        return [to_builtin(item) for item in value]
    return value

"""Normalize component declaration values independently of dispatch and storage."""

import numpy as np

from molsysmt._private.smonitor import ArgumentError


def normalize_assignment(name, values, caller):
    """Preserve scalar/singleton conventions while rejecting untyped references."""
    import pandas as pd

    from molsysmt import pyunitwizard as puw

    # Labels are opaque text, including numeric-looking strings and unit names.
    if isinstance(values, str):
        if name != "component_index":
            return values
        raise ArgumentError(name, value=values, caller=caller)
    if puw.is_quantity(values):
        raise ArgumentError(name, value=values, caller=caller)
    if values is None or values is pd.NA:
        return None
    scalar = np.isscalar(values)
    raw = np.asarray([values] if scalar else values, dtype=object)
    if raw.ndim != 1:
        raise ArgumentError(name, value=values, caller=caller)
    normalized = []
    for value in raw:
        if value is None or value is pd.NA:
            normalized.append(None)
        elif isinstance(value, str) and name != "component_index":
            normalized.append(str(value))
        elif (
            name in {"component_id", "component_index"}
            and isinstance(value, (int, np.integer))
            and not isinstance(value, (bool, np.bool_))
            and (name != "component_index" or 0 <= int(value) <= np.iinfo(np.int64).max)
        ):
            normalized.append(int(value))
        else:
            raise ArgumentError(name, value=values, caller=caller)
    # Existing index/id digesters deliver scalar integers as a one-item list.
    # Keep that container convention while native storage handles broadcasting.
    return normalized

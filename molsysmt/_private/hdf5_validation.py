"""Validating integral HDF5 metadata without coercion or declared-size allocation."""

import numpy as np


def integer_metadata(value, name, *, minimum=0):
    """Read one scalar integer in the supported signed index range."""
    array = np.asarray(value)
    if array.shape != () or array.dtype.kind not in "iu":
        raise ValueError(f"Metadata {name!r} must be a scalar integer.")
    value = int(array)
    if value < minimum or value > np.iinfo(np.int64).max:
        raise ValueError(f"Metadata {name!r} is outside the supported integer range.")
    return value


def schema_version(group, versions, label):
    """Check scalar integer encoding and optional admitted versions before decoding."""
    version = integer_metadata(
        group.attrs.get("schema_version"), f"{label}.schema_version", minimum=1
    )
    if versions is not None and version not in versions:
        raise ValueError(f"Unsupported {label} schema.")
    return version


def numbered_group_count(group, attribute, label, *, default=None):
    """Check declared cardinality against stored members before enumerating it."""
    count = integer_metadata(
        group.attrs.get(attribute, default), f"{label}.{attribute}"
    )
    if count != len(group) or any(str(index) not in group for index in range(count)):
        raise ValueError(f"{label} has inconsistent numbered groups.")
    return count

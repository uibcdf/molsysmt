"""Reusing native caller aliases before bound wrapper defaults are forwarded."""

from dataclasses import replace

from molsysmt._private.argdigest.normalization.caller_aliases import (
    TABLES as _NATIVE_TABLES,
)

# Keep alias names and collision semantics owned by the provider/ArgDigest.
# Re-scope the existing table; never discard an explicitly supplied canonical
# value merely because it equals its default.
TABLES = [
    replace(table, applies_to="molsysviewer_molsysmt._basic.compare")
    for table in _NATIVE_TABLES
    if table.applies_to == "molsysmt.basic.compare.compare"
]

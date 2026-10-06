"""Shared atom-selection vocabulary for sparse-result queries.

These filters select existing observations. Detector selection modes and stored
evaluation modes describe the search that produced them and are independent.
"""

QUERY_MODES = (
    "involving_selection",
    "within_selection",
    "across_selection_boundary",
)


def validate_query_mode(mode):
    """Validate selection filters without changing scientific search scope."""
    if not isinstance(mode, str):
        raise ValueError(f"mode must be one of {QUERY_MODES}")
    if mode not in QUERY_MODES:
        raise ValueError(f"mode must be one of {QUERY_MODES}")
    return mode

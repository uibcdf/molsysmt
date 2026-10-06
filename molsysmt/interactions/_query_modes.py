"""Shared atom-selection vocabulary for sparse-result queries.

These filters select existing observations. Detector selection modes and stored
evaluation modes describe the search that produced them and are independent.
"""

QUERY_MODES = (
    "involving_selection",
    "within_selection",
    "across_selection_boundary",
)
QUERY_MODE_ALIASES = {
    "incident": "involving_selection",
    "internal": "within_selection",
    "cross": "across_selection_boundary",
}


def normalize_query_mode(mode):
    """Resolve compatibility values without changing scientific search scope."""
    if not isinstance(mode, str):
        raise ValueError(f"mode must be one of {QUERY_MODES}")
    canonical = QUERY_MODE_ALIASES.get(mode, mode)
    if canonical not in QUERY_MODES:
        raise ValueError(f"mode must be one of {QUERY_MODES}")
    return canonical

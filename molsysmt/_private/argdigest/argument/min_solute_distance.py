"""Validate a periodic source-to-ion clearance."""

from .distance import digest_distance


def digest_min_solute_distance(min_solute_distance, caller=None):
    return digest_distance(min_solute_distance, caller=caller)

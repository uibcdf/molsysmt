"""Validate a periodic ion-to-ion clearance."""

from .distance import digest_distance


def digest_min_ion_distance(min_ion_distance, caller=None):
    return digest_distance(min_ion_distance, caller=caller)

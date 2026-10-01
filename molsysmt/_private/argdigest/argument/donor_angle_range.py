"""Validate the angle range at an interaction donor."""

from ._angle_range import digest_angle_range


def digest_donor_angle_range(donor_angle_range, caller=None):
    return digest_angle_range(donor_angle_range, "donor_angle_range", caller)

"""Validate the angle range at an interaction acceptor."""

from ._angle_range import digest_angle_range


def digest_acceptor_angle_range(acceptor_angle_range, caller=None):
    return digest_angle_range(acceptor_angle_range, "acceptor_angle_range", caller)

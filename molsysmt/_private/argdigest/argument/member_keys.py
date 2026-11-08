"""Validate unique opaque member labels without coercion."""

from molsysmt._private.smonitor import ArgumentError


def digest_member_keys(member_keys, caller=None):
    if member_keys is None:
        return None
    if (
        isinstance(member_keys, (list, tuple))
        and all(isinstance(key, str) for key in member_keys)
        and len(set(member_keys)) == len(member_keys)
    ):
        return list(member_keys)
    raise ArgumentError("member_keys", caller=caller)

"""Validate the H5MSM append block size."""

from argdigest.core.caller import caller_matches

from molsysmt._private.smonitor import ArgumentError


def digest_block_size(block_size, caller=None):
    if caller_matches(caller, "append_structures") and (
        isinstance(block_size, bool)
        or not isinstance(block_size, int)
        or block_size < 1
    ):
        raise ArgumentError("block_size", value=block_size, caller=caller)
    return block_size

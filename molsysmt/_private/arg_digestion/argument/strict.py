from molsysmt._private.smonitor import ArgumentError


def digest_strict(strict, caller=None):
    if isinstance(strict, bool):
        return strict

    raise ArgumentError("strict", value=strict, caller=caller, message=None)

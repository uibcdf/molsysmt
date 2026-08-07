from molsysmt._private.smonitor import ArgumentError


def digest_allow_reassign(allow_reassign, caller=None):
    if isinstance(allow_reassign, bool):
        return allow_reassign

    raise ArgumentError(
        "allow_reassign",
        value=allow_reassign,
        caller=caller,
        message=None,
    )

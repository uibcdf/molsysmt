from molsysmt._private.smonitor import ArgumentError


def digest_typing_scheme(typing_scheme, caller=None):
    if typing_scheme is None or (
        isinstance(typing_scheme, str) and typing_scheme == "autodock4"
    ):
        return typing_scheme
    raise ArgumentError("typing_scheme", value=typing_scheme, caller=caller)

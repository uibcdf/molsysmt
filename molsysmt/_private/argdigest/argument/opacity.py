from molsysmt._private.smonitor import ArgumentError


def digest_opacity(opacity, caller=None):

    if opacity is None:
        return None

    if isinstance(opacity, (int, float)):
        return opacity

    raise ArgumentError("opacity", value=opacity, caller=caller, message=None)

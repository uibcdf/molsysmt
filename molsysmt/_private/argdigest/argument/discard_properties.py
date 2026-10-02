from molsysmt._private.smonitor import ArgumentError


def digest_discard_properties(discard_properties, caller=None):
    """Validating explicit authorization to discard unrepresented SD properties."""
    if isinstance(discard_properties, bool):
        return discard_properties
    raise ArgumentError("discard_properties", value=discard_properties, caller=caller)

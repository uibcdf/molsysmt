from molsysmt._private.smonitor import ArgumentError

def digest_reference_coordinates(reference_coordinates, caller=None):

    if reference_coordinates is None:
        return None

    from .coordinates import digest_coordinates

    try:
        return digest_coordinates(reference_coordinates, caller=caller)
    except Exception:
        raise ArgumentError('reference_coordinates', value=reference_coordinates, caller=caller, message=None)


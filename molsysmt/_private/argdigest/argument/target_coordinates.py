from molsysmt._private.smonitor import ArgumentError


def digest_target_coordinates(target_coordinates, caller=None):
    from .coordinates import digest_coordinates

    if target_coordinates is None:
        return None
    try:
        return digest_coordinates(target_coordinates, caller=caller)
    except Exception as error:
        raise ArgumentError(
            "target_coordinates", value=target_coordinates, caller=caller
        ) from error

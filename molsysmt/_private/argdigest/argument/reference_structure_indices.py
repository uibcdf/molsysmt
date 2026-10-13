from molsysmt._private.smonitor import ArgumentError


def digest_reference_structure_indices(reference_structure_indices, caller=None):

    from ._correspondence_axes import CALLERS, flat_axis
    from .indices import digest_indices

    if caller in CALLERS:
        return flat_axis(
            reference_structure_indices, "reference_structure_indices", caller
        )

    try:
        return digest_indices(reference_structure_indices, caller=caller)
    except Exception:
        raise ArgumentError(
            "reference_structure_indices",
            value=reference_structure_indices,
            caller=caller,
            message=None,
        )

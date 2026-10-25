from molsysmt._private.smonitor import ArgumentError


def digest_source_center_selection(
    source_center_selection, syntax="MolSysMT", caller=None
):
    from .selection import digest_selection

    if source_center_selection is None:
        return None
    try:
        return digest_selection(source_center_selection, syntax=syntax, caller=caller)
    except Exception as error:
        raise ArgumentError(
            "source_center_selection", value=source_center_selection, caller=caller
        ) from error

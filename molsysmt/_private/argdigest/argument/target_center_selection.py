from molsysmt._private.smonitor import ArgumentError


def digest_target_center_selection(
    target_center_selection, syntax="MolSysMT", caller=None
):
    from .selection import digest_selection

    if target_center_selection is None:
        return None
    try:
        return digest_selection(target_center_selection, syntax=syntax, caller=caller)
    except Exception as error:
        raise ArgumentError(
            "target_center_selection", value=target_center_selection, caller=caller
        ) from error

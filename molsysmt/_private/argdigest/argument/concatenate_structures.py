from molsysmt._private.smonitor import ArgumentError


def digest_concatenate_structures(concatenate_structures, caller=None):

    if caller == "molsysmt.basic.view.view":
        if isinstance(concatenate_structures, bool):
            return concatenate_structures

    raise ArgumentError(
        "concatenate_structures",
        value=concatenate_structures,
        caller=caller,
        message=None,
    )

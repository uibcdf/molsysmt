from molsysmt._private.smonitor import ArgumentError


def digest_standard(standard, caller=None):

    if caller == "molsysmt.basic.view.view":
        if isinstance(standard, bool):
            return standard

    raise ArgumentError("standard", value=standard, caller=caller, message=None)

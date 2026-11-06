from molsysmt._private.smonitor import ArgumentError

from ._attribute_query import digest_query_flag


def digest_dispersion_correction(dispersion_correction, caller=None):

    if caller == "molsysmt.basic.get.get":
        return digest_query_flag(
            "dispersion_correction", dispersion_correction, caller=caller
        )

    if caller is not None and caller.startswith("molsysmt.form.") and ".to_" in caller:
        return dispersion_correction
    elif isinstance(dispersion_correction, bool):
        return dispersion_correction

    raise ArgumentError(
        "dispersion_correction",
        value=dispersion_correction,
        caller=caller,
        message=None,
    )

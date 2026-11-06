from molsysmt._private.smonitor import ArgumentError

from ._attribute_query import digest_query_flag


def digest_solvent_dielectric(solvent_dielectric, caller=None):

    if caller == "molsysmt.basic.get.get":
        return digest_query_flag(
            "solvent_dielectric", solvent_dielectric, caller=caller
        )

    if caller.startswith("molsysmt.form.") and caller.count(".to_") == 2:
        return solvent_dielectric

    raise ArgumentError(
        "solvent_dielectric", value=solvent_dielectric, caller=caller, message=None
    )

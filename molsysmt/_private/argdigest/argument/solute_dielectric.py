from molsysmt._private.smonitor import ArgumentError

from ._attribute_query import digest_query_flag


def digest_solute_dielectric(solute_dielectric, caller=None):

    if caller == "molsysmt.basic.get.get":
        return digest_query_flag("solute_dielectric", solute_dielectric, caller=caller)

    if caller.startswith("molsysmt.form.") and caller.count(".to_") == 2:
        return solute_dielectric

    raise ArgumentError(
        "solute_dielectric", value=solute_dielectric, caller=caller, message=None
    )

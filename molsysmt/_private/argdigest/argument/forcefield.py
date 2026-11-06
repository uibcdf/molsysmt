from molsysmt._private.smonitor import ArgumentError

from ._attribute_query import digest_query_flag


def digest_forcefield(forcefield, caller=None):

    if forcefield is None and caller in {
        "molsysmt.physchem.get_partial_charges.get_partial_charges",
        "molsysmt.build.assign_partial_charges.assign_partial_charges",
    }:
        return None

    if caller == "molsysmt.basic.get.get":
        return digest_query_flag("forcefield", forcefield, caller=caller)

    if isinstance(forcefield, str):
        from molsysmt.attribute import attributes

        if forcefield in attributes["forcefield"]["values"]:
            return forcefield

    raise ArgumentError("forcefield", value=forcefield, caller=caller, message=None)

from molsysmt._private.smonitor import ArgumentError


def digest_forcefield(forcefield, caller=None):

    if forcefield is None and caller in {
        "molsysmt.physchem.get_partial_charges.get_partial_charges",
        "molsysmt.build.assign_partial_charges.assign_partial_charges",
    }:
        return None

    if caller == "molsysmt.basic.get.get":
        if isinstance(forcefield, bool):
            return forcefield

    if isinstance(forcefield, str):
        from molsysmt.attribute import attributes

        if forcefield in attributes["forcefield"]["values"]:
            return forcefield

    raise ArgumentError("forcefield", value=forcefield, caller=caller, message=None)

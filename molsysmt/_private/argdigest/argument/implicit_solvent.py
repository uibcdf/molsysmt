from molsysmt._private.smonitor import ArgumentError

from ._attribute_query import digest_query_flag


def digest_implicit_solvent(implicit_solvent, caller=None):

    if caller == "molsysmt.basic.get.get":
        return digest_query_flag("implicit_solvent", implicit_solvent, caller=caller)
    elif caller == "molsysmt.basic.convert.convert" or (
        caller is not None and caller.startswith("molsysmt.molecular_mechanics.")
    ):
        if implicit_solvent is None:
            return implicit_solvent
    elif (
        caller is not None and caller.startswith("molsysmt.form.") and ".to_" in caller
    ):
        if implicit_solvent is None:
            return implicit_solvent
    elif implicit_solvent is None:
        return None

    if isinstance(implicit_solvent, str):
        from molsysmt.molecular_mechanics.forcefields import implicit_solvent_models

        if implicit_solvent in implicit_solvent_models:
            return implicit_solvent

    raise ArgumentError(
        "implicit_solvent", value=implicit_solvent, caller=caller, message=None
    )

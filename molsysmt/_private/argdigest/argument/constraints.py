from molsysmt._private.smonitor import ArgumentError

from ._attribute_query import digest_query_flag


def digest_constraints(constraints, caller=None):

    if caller == "molsysmt.basic.get.get":
        return digest_query_flag("constraints", constraints, caller=caller)

    if constraints is None and caller == "molsysmt.basic.convert.convert":
        return None
    if caller is not None and caller.startswith("molsysmt.form.") and ".to_" in caller:
        return constraints
    elif isinstance(constraints, str):
        return constraints

    raise ArgumentError("constraints", value=constraints, caller=caller, message=None)

from molsysmt._private.smonitor import ArgumentError

from ._attribute_query import digest_query_flag


def digest_flexible_constraints(flexible_constraints, caller=None):

    if caller == "molsysmt.basic.get.get":
        return digest_query_flag(
            "flexible_constraints", flexible_constraints, caller=caller
        )

    if caller is not None and caller.startswith("molsysmt.form.") and ".to_" in caller:
        return flexible_constraints
    elif isinstance(flexible_constraints, str):
        return flexible_constraints

    raise ArgumentError(
        "flexible_constraints", value=flexible_constraints, caller=caller, message=None
    )

from molsysmt._private.smonitor import ArgumentError

from ._attribute_query import digest_query_flag


def digest_non_bonded_method(non_bonded_method, caller=None):

    if caller == "molsysmt.basic.get.get":
        return digest_query_flag("non_bonded_method", non_bonded_method, caller=caller)

    if caller is not None and caller.startswith("molsysmt.form.") and ".to_" in caller:
        return non_bonded_method
    elif isinstance(non_bonded_method, str):
        return non_bonded_method

    raise ArgumentError(
        "non_bonded_method", value=non_bonded_method, caller=caller, message=None
    )

from molsysmt._private.smonitor import ArgumentError

from ._attribute_query import digest_query_flag


def digest_kappa(kappa, caller=None):

    if caller == "molsysmt.basic.get.get":
        return digest_query_flag("kappa", kappa, caller=caller)

    if caller.startswith("molsysmt.form.") and caller.count(".to_") == 2:
        return kappa

    raise ArgumentError("kappa", value=kappa, caller=caller, message=None)

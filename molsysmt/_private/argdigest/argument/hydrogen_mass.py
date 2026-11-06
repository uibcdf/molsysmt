from molsysmt._private.smonitor import ArgumentError

from ._attribute_query import digest_query_flag


def digest_hydrogen_mass(hydrogen_mass, caller=None):

    if caller == "molsysmt.basic.get.get":
        return digest_query_flag("hydrogen_mass", hydrogen_mass, caller=caller)

    if caller is not None and caller.startswith("molsysmt.form.") and ".to_" in caller:
        return hydrogen_mass

    raise ArgumentError(
        "hydrogen_mass", value=hydrogen_mass, caller=caller, message=None
    )

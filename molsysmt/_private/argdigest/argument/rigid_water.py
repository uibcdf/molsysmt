from molsysmt._private.smonitor import ArgumentError

from ._attribute_query import digest_query_flag


def digest_rigid_water(rigid_water, caller=None):

    if caller == "molsysmt.basic.get.get":
        return digest_query_flag("rigid_water", rigid_water, caller=caller)

    if caller is not None and caller.startswith("molsysmt.form.") and ".to_" in caller:
        return rigid_water

    raise ArgumentError("rigid_water", value=rigid_water, caller=caller, message=None)

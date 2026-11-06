from molsysmt._private.smonitor import ArgumentError

from ._attribute_query import digest_query_flag


def digest_salt_concentration(salt_concentration, caller=None):

    if caller == "molsysmt.basic.get.get":
        return digest_query_flag(
            "salt_concentration", salt_concentration, caller=caller
        )

    if caller.startswith("molsysmt.form.") and caller.count(".to_") == 2:
        return salt_concentration

    raise ArgumentError(
        "salt_concentration", value=salt_concentration, caller=caller, message=None
    )

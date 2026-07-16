"""Validating chemical-state metadata query flags."""

from molsysmt._private.smonitor import ArgumentError


def digest_query_flag(name, value, caller=None):
    if caller in {'molsysmt.basic.get.get', 'molsysmt.basic.compare.compare'}:
        if isinstance(value, bool):
            return value
    raise ArgumentError(name, value=value, caller=caller, message=None)

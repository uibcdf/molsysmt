"""Validating the explicit TPSA element-scope switch."""

from molsysmt._private.smonitor import ArgumentError


def digest_include_sulfur_phosphorus(include_sulfur_phosphorus, caller=None):
    if isinstance(include_sulfur_phosphorus, bool):
        return include_sulfur_phosphorus
    raise ArgumentError(
        "include_sulfur_phosphorus", value=include_sulfur_phosphorus, caller=caller
    )

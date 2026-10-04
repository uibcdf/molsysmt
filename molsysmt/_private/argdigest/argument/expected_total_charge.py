"""Validating a declared scalar total for a named charge calculation."""


def digest_expected_total_charge(expected_total_charge, caller=None):
    from molsysmt._private.partial_charges import _charge_value

    _charge_value(expected_total_charge)
    return expected_total_charge

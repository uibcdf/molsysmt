"""Validate the explicitly selected source for neutralization charge."""


def digest_charge_source(charge_source, caller=None):
    from molsysmt._private.smonitor import ArgumentError

    if isinstance(charge_source, str) and charge_source in {
        "formal_charge",
        "partial_charge",
        "physical_pH7",
    }:
        return charge_source
    raise ArgumentError(
        "charge_source",
        value=charge_source,
        caller=caller,
        message="Choose formal_charge, partial_charge or the explicit physical_pH7 approximation.",
    )

from argdigest.core.caller import caller_matches

from molsysmt._private.smonitor import ArgumentError


def digest_molecular_mechanics(molecular_mechanics, caller=None):

    if caller_matches(caller, "molsysmt.h5msm.write_layers"):
        from molsysmt.native import MolecularMechanics

        if molecular_mechanics is None or isinstance(
            molecular_mechanics, MolecularMechanics
        ):
            return molecular_mechanics
        raise ArgumentError(
            "molecular_mechanics", value=molecular_mechanics, caller=caller
        )

    if isinstance(molecular_mechanics, dict):
        from molsysmt.form.molsysmt_MolecularMechanicsDict import (
            is_molsysmt_MolecularMechanicsDict,
        )

        if is_molsysmt_MolecularMechanicsDict(molecular_mechanics):
            return molecular_mechanics

    raise ArgumentError(
        "molecular_mechanics", value=molecular_mechanics, caller=caller, message=None
    )

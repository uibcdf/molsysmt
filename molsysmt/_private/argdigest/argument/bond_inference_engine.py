"""Validating the optional PDB connectivity engine without selecting a fallback."""

from molsysmt._private.smonitor import ArgumentError


def digest_bond_inference_engine(bond_inference_engine, caller=None):
    if bond_inference_engine is None:
        return None
    if isinstance(bond_inference_engine, str):
        engines = {"molsysmt": "MolSysMT", "openmm": "OpenMM"}
        if bond_inference_engine.lower() in engines:
            return engines[bond_inference_engine.lower()]
    raise ArgumentError(
        "bond_inference_engine", value=bond_inference_engine, caller=caller
    )

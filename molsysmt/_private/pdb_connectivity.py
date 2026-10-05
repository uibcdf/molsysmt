"""Retaining reader policy outcomes in the owning chemical-state history."""

import numpy as np


def validate_policy(get_missing_bonds, engine):
    from molsysmt._private.smonitor import ArgumentConflictError, ArgumentError

    if engine not in (None, "MolSysMT", "OpenMM"):
        raise ArgumentError("bond_inference_engine", value=engine)
    if not get_missing_bonds and engine is not None:
        raise ArgumentConflictError(
            "get_missing_bonds",
            "bond_inference_engine",
            reason="Disabled bond inference cannot request an inference engine.",
        )


def record(topology, status, engine, *, error=None, declaration_issues=None):
    """Archive an outcome with original bond indices and producer identity."""
    from molsysmt import __version__
    from molsysmt._private.preparation_history import append_report

    state = topology._reference_chemical_state
    history_index = len(state._preparation_history)
    inferred = (
        state.bonds["evidence"].eq("inferred")
        if "evidence" in state.bonds
        else np.zeros(len(state.bonds), dtype=bool)
    )
    bond_indices = np.flatnonzero(inferred).astype(np.int64)
    if len(bond_indices):
        topology._set_chemical_state_bond_attribute(
            "provenance_index",
            history_index,
            bond_indices=bond_indices,
        )
    report = dict(
        schema="molsysmt.pdb_connectivity@1",
        status=status,
        requested_engine=engine,
        attempted_engine=None if status == "disabled" else "OpenMM",
        actual_engine="OpenMM" if status == "inferred" else None,
        method="openmm_pdb_standard_bonds"
        if status == "inferred"
        else "explicit_pdb_records",
        software={"molsysmt": __version__},
        structure_index=0 if status == "inferred" else None,
        inferred_bond_indices=bond_indices,
        declaration_issues=declaration_issues or {},
        error=None
        if error is None
        else {"type": type(error).__name__, "message": str(error)},
        unassessed_checks=[
            "bond_orders",
            "valence",
            "protonation",
            "connectivity_completeness",
        ],
    )
    if status == "inferred":
        from importlib.metadata import PackageNotFoundError, version

        try:
            report["software"]["openmm"] = version("OpenMM")
        except PackageNotFoundError:
            report["software"]["openmm"] = None
    append_report(state, report, 0)

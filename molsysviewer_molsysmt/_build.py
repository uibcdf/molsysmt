"""Explicit native build diagnostics; no preparation or scene adoption."""

from argdigest import arg_digest
from smonitor import signal

from ._basic import _native_documentation


class _BuildTools:
    _NAMES = (
        "get_residue_chemical_coverage",
        "get_covalent_bond_candidates",
        "get_peptide_bond_candidates",
    )

    def __init__(self, owner):
        self._owner = owner

    def __dir__(self):
        return list(self._NAMES)

    def _call(self, name, parameters):
        from molsysmt import build

        return self._owner._read(getattr(build, name), parameters)

    @_native_documentation("get_residue_chemical_coverage", module="build")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_residue_chemical_coverage(
        self,
        selection="all",
        structure_indices="all",
        chemical_state="reference",
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "get_residue_chemical_coverage",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "chemical_state": chemical_state,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_covalent_bond_candidates", module="build")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_covalent_bond_candidates(
        self,
        selection="all",
        structure_indices="all",
        chemical_state="reference",
        syntax="MolSysMT",
        skip_digestion=False,
        *,
        method="exact_heavy_group_templates",
    ):
        return self._call(
            "get_covalent_bond_candidates",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "chemical_state": chemical_state,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
                "method": method,
            },
        )

    @_native_documentation("get_peptide_bond_candidates", module="build")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_peptide_bond_candidates(
        self,
        selection="all",
        structure_indices="all",
        chemical_state="reference",
        max_bond_length="2 angstroms",
        pbc=False,
        syntax="MolSysMT",
        skip_digestion=False,
        *,
        method="adjacent_backbone_distance",
    ):
        return self._call(
            "get_peptide_bond_candidates",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "chemical_state": chemical_state,
                "max_bond_length": max_bond_length,
                "pbc": pbc,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
                "method": method,
            },
        )

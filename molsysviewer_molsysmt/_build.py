"""Explicit native build diagnostics; no preparation or scene adoption."""

from argdigest import arg_digest
from smonitor import signal

from ._basic import _native_documentation


class _BuildTools:
    _NAMES = (
        "get_residue_chemical_coverage",
        "get_covalent_bond_candidates",
        "get_peptide_bond_candidates",
        "get_missing_heavy_atoms",
        "get_missing_bonds",
        "get_missing_residues",
        "get_missing_terminal_cappings",
        "get_non_standard_residues",
        "get_disulfide_bonds",
        "has_hydrogens",
        "is_solvated",
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

    @_native_documentation("get_missing_heavy_atoms", module="build")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_missing_heavy_atoms(
        self,
        selection="all",
        syntax="MolSysMT",
        engine="MolSysMT",
        *,
        skip_digestion=False,
    ):
        return self._call(
            "get_missing_heavy_atoms",
            {
                "selection": selection,
                "syntax": syntax,
                "engine": engine,
            },
        )

    @_native_documentation("get_missing_bonds", module="build")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_missing_bonds(
        self,
        selection="all",
        structure_index=0,
        max_bond_length="2 angstroms",
        disulfide_bonds=False,
        disulfide_group_names=None,
        pbc=True,
        syntax="MolSysMT",
        engine="MolSysMT",
        sorted=True,
        skip_digestion=False,
    ):
        return self._call(
            "get_missing_bonds",
            {
                "selection": selection,
                "structure_index": structure_index,
                "max_bond_length": max_bond_length,
                "disulfide_bonds": disulfide_bonds,
                "disulfide_group_names": disulfide_group_names,
                "pbc": pbc,
                "syntax": syntax,
                "engine": engine,
                "sorted": sorted,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_missing_residues", module="build")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_missing_residues(
        self,
        sequence=None,
        selection="all",
        syntax="MolSysMT",
        engine="MolSysMT",
        *,
        skip_digestion=False,
    ):
        return self._call(
            "get_missing_residues",
            {
                "sequence": sequence,
                "selection": selection,
                "syntax": syntax,
                "engine": engine,
            },
        )

    @_native_documentation("get_missing_terminal_cappings", module="build")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_missing_terminal_cappings(
        self,
        selection="all",
        syntax="MolSysMT",
        engine="MolSysMT",
        *,
        skip_digestion=False,
    ):
        return self._call(
            "get_missing_terminal_cappings",
            {
                "selection": selection,
                "syntax": syntax,
                "engine": engine,
            },
        )

    @_native_documentation("get_non_standard_residues", module="build")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_non_standard_residues(
        self,
        selection="all",
        syntax="MolSysMT",
        engine="MolSysMT",
        *,
        skip_digestion=False,
    ):
        return self._call(
            "get_non_standard_residues",
            {
                "selection": selection,
                "syntax": syntax,
                "engine": engine,
            },
        )

    @_native_documentation("get_disulfide_bonds", module="build")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_disulfide_bonds(
        self,
        selection="all",
        structure_index=0,
        max_bond_length=None,
        group_names=None,
        pbc=True,
        syntax="MolSysMT",
        engine="MolSysMT",
        sorted=True,
        skip_digestion=False,
    ):
        return self._call(
            "get_disulfide_bonds",
            {
                "selection": selection,
                "structure_index": structure_index,
                "max_bond_length": max_bond_length,
                "group_names": group_names,
                "pbc": pbc,
                "syntax": syntax,
                "engine": engine,
                "sorted": sorted,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("has_hydrogens", module="build")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def has_hydrogens(
        self,
        selection="all",
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "has_hydrogens",
            {
                "selection": selection,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("is_solvated", module="build")
    @signal(tags=["addon", "build"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def is_solvated(
        self,
        skip_digestion=False,
    ):
        return self._call(
            "is_solvated",
            {
                "skip_digestion": skip_digestion,
            },
        )

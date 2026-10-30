"""Explicit read/calculation wrappers for independent native domains."""

from argdigest import arg_digest
from smonitor import signal

from ._basic import _native_documentation


class _ChemicalStatesTools:
    _NAMES = (
        "get_bondgraph",
        "get_covalent_blocks",
        "get_covalent_paths",
        "get_dihedral_quartets",
        "get_rigid_fragments",
        "get_rotatable_bonds",
        "get_rings",
        "get_substructure_matches",
        "get_atom_correspondences",
    )

    def __init__(self, owner):
        self._owner = owner

    def __dir__(self):
        return list(self._NAMES)

    def _call(self, name, parameters, extra=None):
        from molsysmt import chemical_states

        return self._owner._read(getattr(chemical_states, name), parameters, extra)

    @_native_documentation("get_bondgraph", module="chemical_states")
    @signal(tags=["addon", "chemical_states"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_bondgraph(
        self,
        nodes_name="atom_index",
        selection="all",
        syntax="MolSysMT",
        to_form="networkx.Graph",
        *,
        chemical_state="reference",
        structure_indices="all",
        skip_digestion=False,
    ):
        return self._call(
            "get_bondgraph",
            {
                "nodes_name": nodes_name,
                "selection": selection,
                "syntax": syntax,
                "to_form": to_form,
                "chemical_state": chemical_state,
                "structure_indices": structure_indices,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_covalent_blocks", module="chemical_states")
    @signal(tags=["addon", "chemical_states"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_covalent_blocks(
        self,
        selection="all",
        remove_bonds=None,
        output_type="sets",
        syntax="MolSysMT",
        *,
        chemical_state="reference",
        structure_indices="all",
        skip_digestion=False,
    ):
        return self._call(
            "get_covalent_blocks",
            {
                "selection": selection,
                "remove_bonds": remove_bonds,
                "output_type": output_type,
                "syntax": syntax,
                "chemical_state": chemical_state,
                "structure_indices": structure_indices,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_covalent_paths", module="chemical_states")
    @signal(tags=["addon", "chemical_states"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_covalent_paths(
        self,
        path=None,
        selection="all",
        syntax="MolSysMT",
        *,
        chemical_state="reference",
        structure_indices="all",
        skip_digestion=False,
    ):
        return self._call(
            "get_covalent_paths",
            {
                "path": path,
                "selection": selection,
                "syntax": syntax,
                "chemical_state": chemical_state,
                "structure_indices": structure_indices,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_dihedral_quartets", module="chemical_states")
    @signal(tags=["addon", "chemical_states"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_dihedral_quartets(
        self,
        with_blocks=False,
        selection="all",
        syntax="MolSysMT",
        *,
        chemical_state="reference",
        structure_indices="all",
        skip_digestion=False,
        **kwargs,
    ):
        return self._call(
            "get_dihedral_quartets",
            {
                "with_blocks": with_blocks,
                "selection": selection,
                "syntax": syntax,
                "chemical_state": chemical_state,
                "structure_indices": structure_indices,
                "skip_digestion": skip_digestion,
            },
            kwargs,
        )

    @_native_documentation("get_rigid_fragments", module="chemical_states")
    @signal(tags=["addon", "chemical_states"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_rigid_fragments(
        self,
        bond_indices=None,
        chemical_state="reference",
        structure_indices="all",
        skip_digestion=False,
    ):
        return self._call(
            "get_rigid_fragments",
            {
                "bond_indices": bond_indices,
                "chemical_state": chemical_state,
                "structure_indices": structure_indices,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_rotatable_bonds", module="chemical_states")
    @signal(tags=["addon", "chemical_states"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_rotatable_bonds(
        self,
        selection="all",
        structure_indices="all",
        chemical_state="reference",
        method="conjugation_restricted",
        syntax="MolSysMT",
        skip_digestion=False,
    ):
        return self._call(
            "get_rotatable_bonds",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "chemical_state": chemical_state,
                "method": method,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
            },
        )

    @_native_documentation("get_rings", module="chemical_states")
    @signal(tags=["addon", "chemical_states"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_rings(
        self,
        selection="all",
        structure_indices="all",
        chemical_state="reference",
        method="minimum_cycle_basis",
        assume_complete_connectivity=False,
        syntax="MolSysMT",
        skip_digestion=False,
        *,
        max_cyclic_block_size=256,
    ):
        return self._call(
            "get_rings",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "chemical_state": chemical_state,
                "method": method,
                "assume_complete_connectivity": assume_complete_connectivity,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
                "max_cyclic_block_size": max_cyclic_block_size,
            },
        )

    @_native_documentation("get_substructure_matches", module="chemical_states")
    @signal(tags=["addon", "chemical_states"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_substructure_matches(
        self,
        patterns,
        selection="all",
        structure_indices="all",
        chemical_state="reference",
        assume_complete_connectivity=False,
        syntax="MolSysMT",
        skip_digestion=False,
        *,
        max_matches=100000,
    ):
        return self._call(
            "get_substructure_matches",
            {
                "patterns": patterns,
                "selection": selection,
                "structure_indices": structure_indices,
                "chemical_state": chemical_state,
                "assume_complete_connectivity": assume_complete_connectivity,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
                "max_matches": max_matches,
            },
        )

    @_native_documentation("get_atom_correspondences", module="chemical_states")
    @signal(tags=["addon", "chemical_states"])
    @arg_digest(config="molsysviewer_molsysmt._argdigest")
    def get_atom_correspondences(
        self,
        selection="all",
        structure_indices="all",
        reference_molecular_system=None,
        reference_selection=None,
        reference_structure_indices="all",
        chemical_state="reference",
        reference_chemical_state="reference",
        method="declared_graph_isomorphism",
        max_matches=100000,
        syntax="MolSysMT",
        skip_digestion=False,
        *,
        fixed_atom_correspondence=None,
        candidate_atom_correspondences=None,
    ):
        return self._call(
            "get_atom_correspondences",
            {
                "selection": selection,
                "structure_indices": structure_indices,
                "reference_molecular_system": reference_molecular_system,
                "reference_selection": reference_selection,
                "reference_structure_indices": reference_structure_indices,
                "chemical_state": chemical_state,
                "reference_chemical_state": reference_chemical_state,
                "method": method,
                "max_matches": max_matches,
                "syntax": syntax,
                "skip_digestion": skip_digestion,
                "fixed_atom_correspondence": fixed_atom_correspondence,
                "candidate_atom_correspondences": candidate_atom_correspondences,
            },
        )

"""Comprehensive tests for molsysmt_MolSysBuilder get_topological_attributes.

Covers functions not exercised by test_get_attributes_molsysmt_MolSysBuilder.py:

- atom-level getters with explicit index slices
- get_atom_id_from_atom, get_atom_type_from_atom
- get_group_id_from_group, get_group_type_from_group
- get_chain_index_from_atom, get_chain_index_from_group, get_chain_index_from_chain
- get_chain_id_from_chain, get_chain_type_from_chain
- get_molecule_index_from_group, get_molecule_index_from_atom, get_molecule_index_from_molecule
- get_molecule_id_from_molecule, get_molecule_type_from_molecule
- get_entity_index_from_molecule, get_entity_index_from_atom, get_entity_index_from_entity
- get_entity_id_from_entity, get_entity_type_from_entity
- get_n_chains_from_system, get_n_entities_from_system
- counting getters: get_n_atoms_from_group, get_n_groups_from_chain, get_n_groups_from_molecule
- get_n_molecules_from_entity, get_n_atoms_from_chain, get_n_atoms_from_molecule, get_n_atoms_from_entity
- None-projection paths (ungrouped atoms, atoms without molecule)
- partial-index slicing on all multi-element getters
"""

import pytest
import molsysmt as msm
from molsysmt.form.molsysmt_MolSysBuilder import get_topological_attributes as aux


# ---------------------------------------------------------------------------
# Atom-level getters
# ---------------------------------------------------------------------------


class TestAtomGetters:
    """Tests for getters that return per-atom information."""

    def test_get_atom_index_all(self, molsys_builder_complete):
        result = aux.get_atom_index_from_atom(molsys_builder_complete)
        assert result == [0, 1, 2]

    def test_get_atom_index_slice(self, molsys_builder_complete):
        result = aux.get_atom_index_from_atom(molsys_builder_complete, indices=[0, 2])
        assert result == [0, 2]

    def test_get_atom_id_all_none(self, molsys_builder_complete):
        # atom_id was not set when building the fixture, so entries are None
        result = aux.get_atom_id_from_atom(molsys_builder_complete)
        assert isinstance(result, list)
        assert len(result) == 3

    def test_get_atom_id_partial(self, molsys_builder_partial):
        result = aux.get_atom_id_from_atom(molsys_builder_partial, indices=[0])
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_atom_name_all(self, molsys_builder_complete):
        result = aux.get_atom_name_from_atom(molsys_builder_complete)
        assert result == ["N", "CA", "O"]

    def test_get_atom_name_single(self, molsys_builder_complete):
        result = aux.get_atom_name_from_atom(molsys_builder_complete, indices=[1])
        assert result == ["CA"]

    def test_get_atom_type_all_none(self, molsys_builder_complete):
        # atom_type not set in fixture
        result = aux.get_atom_type_from_atom(molsys_builder_complete)
        assert isinstance(result, list)
        assert len(result) == 3

    def test_get_atom_type_partial(self, molsys_builder_partial):
        result = aux.get_atom_type_from_atom(molsys_builder_partial, indices=[0, 1])
        assert isinstance(result, list)
        assert len(result) == 2

    def test_get_group_index_from_atom_all(self, molsys_builder_partial):
        # atom 0 and 1 belong to group 0; atom 2 is ungrouped -> None
        result = aux.get_group_index_from_atom(molsys_builder_partial)
        assert result[0] == 0
        assert result[1] == 0
        assert result[2] is None

    def test_get_group_index_from_atom_single(self, molsys_builder_complete):
        result = aux.get_group_index_from_atom(molsys_builder_complete, indices=[0])
        assert result == [0]

    def test_get_chain_index_from_atom_complete(self, molsys_builder_complete):
        result = aux.get_chain_index_from_atom(molsys_builder_complete)
        assert isinstance(result, list)
        assert len(result) == 3
        # all atoms are in the single chain
        assert all(v == 0 for v in result)

    def test_get_chain_index_from_atom_partial(self, molsys_builder_partial):
        # partial builder has no chain -> all None
        result = aux.get_chain_index_from_atom(molsys_builder_partial)
        assert all(v is None for v in result)


# ---------------------------------------------------------------------------
# Group-level getters
# ---------------------------------------------------------------------------


class TestGroupGetters:
    """Tests for getters that return per-group information."""

    def test_get_group_index_from_group_all(self, molsys_builder_complete):
        result = aux.get_group_index_from_group(molsys_builder_complete)
        assert result == [0, 1]

    def test_get_group_index_from_group_slice(self, molsys_builder_complete):
        result = aux.get_group_index_from_group(molsys_builder_complete, indices=[1])
        assert result == [1]

    def test_get_group_id_from_group_all(self, molsys_builder_complete):
        # group_id not set in fixture
        result = aux.get_group_id_from_group(molsys_builder_complete)
        assert isinstance(result, list)
        assert len(result) == 2

    def test_get_group_id_from_group_partial(self, molsys_builder_partial):
        result = aux.get_group_id_from_group(molsys_builder_partial)
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_group_name_from_group_complete(self, molsys_builder_complete):
        result = aux.get_group_name_from_group(molsys_builder_complete)
        assert result == ["ALA", "HOH"]

    def test_get_group_name_from_group_slice(self, molsys_builder_complete):
        result = aux.get_group_name_from_group(molsys_builder_complete, indices=[0])
        assert result == ["ALA"]

    def test_get_group_type_from_group_all(self, molsys_builder_complete):
        # group_type not set explicitly in fixture
        result = aux.get_group_type_from_group(molsys_builder_complete)
        assert isinstance(result, list)
        assert len(result) == 2

    def test_get_chain_index_from_group_complete(self, molsys_builder_complete):
        result = aux.get_chain_index_from_group(molsys_builder_complete)
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(v == 0 for v in result)

    def test_get_chain_index_from_group_partial(self, molsys_builder_partial):
        # no chain in partial builder -> None values
        result = aux.get_chain_index_from_group(molsys_builder_partial)
        assert all(v is None for v in result)

    def test_get_molecule_index_from_group_complete(self, molsys_builder_complete):
        result = aux.get_molecule_index_from_group(molsys_builder_complete)
        assert result == [0, 1]

    def test_get_molecule_index_from_group_slice(self, molsys_builder_complete):
        result = aux.get_molecule_index_from_group(molsys_builder_complete, indices=[1])
        assert result == [1]

    def test_get_molecule_index_from_group_partial(self, molsys_builder_partial):
        # partial builder has no molecules
        result = aux.get_molecule_index_from_group(molsys_builder_partial)
        assert all(v is None for v in result)


# ---------------------------------------------------------------------------
# Chain-level getters
# ---------------------------------------------------------------------------


class TestChainGetters:
    """Tests for getters that return per-chain information."""

    def test_get_chain_index_from_chain_all(self, molsys_builder_complete):
        result = aux.get_chain_index_from_chain(molsys_builder_complete)
        assert result == [0]

    def test_get_chain_index_from_chain_slice(self, molsys_builder_complete):
        result = aux.get_chain_index_from_chain(molsys_builder_complete, indices=[0])
        assert result == [0]

    def test_get_chain_id_from_chain(self, molsys_builder_complete):
        result = aux.get_chain_id_from_chain(molsys_builder_complete)
        assert result == ["A"]

    def test_get_chain_name_from_chain(self, molsys_builder_complete):
        result = aux.get_chain_name_from_chain(molsys_builder_complete)
        assert result == ["A"]

    def test_get_chain_type_from_chain(self, molsys_builder_complete):
        result = aux.get_chain_type_from_chain(molsys_builder_complete)
        assert result == ["mixed"]


# ---------------------------------------------------------------------------
# Molecule-level getters
# ---------------------------------------------------------------------------


class TestMoleculeGetters:
    """Tests for getters that return per-molecule information."""

    def test_get_molecule_index_from_atom_complete(self, molsys_builder_complete):
        result = aux.get_molecule_index_from_atom(molsys_builder_complete)
        assert isinstance(result, list)
        assert len(result) == 3

    def test_get_molecule_index_from_atom_partial(self, molsys_builder_partial):
        # ungrouped atom -> None propagates through group -> None
        result = aux.get_molecule_index_from_atom(molsys_builder_partial)
        assert isinstance(result, list)
        assert len(result) == 3

    def test_get_molecule_index_from_molecule_all(self, molsys_builder_complete):
        result = aux.get_molecule_index_from_molecule(molsys_builder_complete)
        assert result == [0, 1]

    def test_get_molecule_index_from_molecule_slice(self, molsys_builder_complete):
        result = aux.get_molecule_index_from_molecule(molsys_builder_complete, indices=[0])
        assert result == [0]

    def test_get_molecule_id_from_molecule(self, molsys_builder_complete):
        result = aux.get_molecule_id_from_molecule(molsys_builder_complete)
        assert result == ["10", "11"]

    def test_get_molecule_name_from_molecule(self, molsys_builder_complete):
        result = aux.get_molecule_name_from_molecule(molsys_builder_complete)
        assert result == ["protein 0", "water"]

    def test_get_molecule_name_slice(self, molsys_builder_complete):
        result = aux.get_molecule_name_from_molecule(molsys_builder_complete, indices=[1])
        assert result == ["water"]

    def test_get_molecule_type_from_molecule(self, molsys_builder_complete):
        result = aux.get_molecule_type_from_molecule(molsys_builder_complete)
        assert result == ["protein", "water"]


# ---------------------------------------------------------------------------
# Entity-level getters
# ---------------------------------------------------------------------------


class TestEntityGetters:
    """Tests for getters that return per-entity information."""

    def test_get_entity_index_from_molecule_all(self, molsys_builder_complete):
        result = aux.get_entity_index_from_molecule(molsys_builder_complete)
        assert result == [0, 1]

    def test_get_entity_index_from_molecule_slice(self, molsys_builder_complete):
        result = aux.get_entity_index_from_molecule(molsys_builder_complete, indices=[0])
        assert result == [0]

    def test_get_entity_index_from_atom_complete(self, molsys_builder_complete):
        result = aux.get_entity_index_from_atom(molsys_builder_complete)
        assert isinstance(result, list)
        assert len(result) == 3

    def test_get_entity_index_from_atom_partial(self, molsys_builder_partial):
        result = aux.get_entity_index_from_atom(molsys_builder_partial)
        assert isinstance(result, list)
        assert len(result) == 3
        assert all(v is None for v in result)

    def test_get_entity_index_from_entity_all(self, molsys_builder_complete):
        result = aux.get_entity_index_from_entity(molsys_builder_complete)
        assert result == [0, 1]

    def test_get_entity_index_from_entity_slice(self, molsys_builder_complete):
        result = aux.get_entity_index_from_entity(molsys_builder_complete, indices=[1])
        assert result == [1]

    def test_get_entity_id_from_entity(self, molsys_builder_complete):
        result = aux.get_entity_id_from_entity(molsys_builder_complete)
        assert result == ["20", "21"]

    def test_get_entity_name_from_entity(self, molsys_builder_complete):
        result = aux.get_entity_name_from_entity(molsys_builder_complete)
        assert result == ["protein 0", "water"]

    def test_get_entity_type_from_entity(self, molsys_builder_complete):
        result = aux.get_entity_type_from_entity(molsys_builder_complete)
        assert result == ["protein", "water"]


# ---------------------------------------------------------------------------
# System-level count getters
# ---------------------------------------------------------------------------


class TestSystemCountGetters:
    """Tests for system-level count getters not covered by the existing test."""

    def test_get_n_chains_from_system_complete(self, molsys_builder_complete):
        assert aux.get_n_chains_from_system(molsys_builder_complete) == 1

    def test_get_n_chains_from_system_partial(self, molsys_builder_partial):
        assert aux.get_n_chains_from_system(molsys_builder_partial) == 0

    def test_get_n_entities_from_system_complete(self, molsys_builder_complete):
        assert aux.get_n_entities_from_system(molsys_builder_complete) == 2

    def test_get_n_entities_from_system_partial(self, molsys_builder_partial):
        assert aux.get_n_entities_from_system(molsys_builder_partial) == 0

    def test_get_n_molecules_from_system_complete(self, molsys_builder_complete):
        assert aux.get_n_molecules_from_system(molsys_builder_complete) == 2

    def test_get_n_bonds_from_system_complete(self, molsys_builder_complete):
        assert aux.get_n_bonds_from_system(molsys_builder_complete) == 1

    def test_get_bonded_atom_pairs_no_bonds(self, molsys_builder_complete):
        # complete fixture has exactly 1 bond between atom 0 and 1
        result = aux.get_bonded_atom_pairs_from_system(molsys_builder_complete)
        assert result == [[0, 1]]

    def test_get_bonded_atom_pairs_empty_when_no_bonds(self):
        import molsysmt as msm
        builder = msm.MolSysBuilder()
        builder.add_atom(atom_name="X")
        result = aux.get_bonded_atom_pairs_from_system(builder)
        assert result == []


# ---------------------------------------------------------------------------
# Aggregate count getters (cross-level)
# ---------------------------------------------------------------------------


class TestAggregateCountGetters:
    """Tests for per-element aggregate count getters."""

    def test_get_n_atoms_from_group_all(self, molsys_builder_complete):
        # group 0: atoms 0,1 (N, CA); group 1: atom 2 (O)
        result = aux.get_n_atoms_from_group(molsys_builder_complete)
        assert result == [2, 1]

    def test_get_n_atoms_from_group_slice(self, molsys_builder_complete):
        result = aux.get_n_atoms_from_group(molsys_builder_complete, indices=[0])
        assert result == [2]

    def test_get_n_atoms_from_group_partial(self, molsys_builder_partial):
        # group 0 has 2 atoms; atom 2 is ungrouped (NA group_index).
        # Ungrouped atoms are excluded from the count — group 0 should have 2.
        result = aux.get_n_atoms_from_group(molsys_builder_partial)
        assert result == [2]

    def test_get_n_groups_from_chain_all(self, molsys_builder_complete):
        # single chain containing both groups
        result = aux.get_n_groups_from_chain(molsys_builder_complete)
        assert result == [2]

    def test_get_n_groups_from_chain_slice(self, molsys_builder_complete):
        result = aux.get_n_groups_from_chain(molsys_builder_complete, indices=[0])
        assert result == [2]

    def test_get_n_groups_from_molecule_all(self, molsys_builder_complete):
        # molecule 0 has 1 group (ALA), molecule 1 has 1 group (HOH)
        result = aux.get_n_groups_from_molecule(molsys_builder_complete)
        assert result == [1, 1]

    def test_get_n_groups_from_molecule_slice(self, molsys_builder_complete):
        result = aux.get_n_groups_from_molecule(molsys_builder_complete, indices=[0])
        assert result == [1]

    def test_get_n_molecules_from_entity_all(self, molsys_builder_complete):
        # each entity has exactly 1 molecule
        result = aux.get_n_molecules_from_entity(molsys_builder_complete)
        assert result == [1, 1]

    def test_get_n_molecules_from_entity_slice(self, molsys_builder_complete):
        result = aux.get_n_molecules_from_entity(molsys_builder_complete, indices=[1])
        assert result == [1]

    def test_get_n_atoms_from_chain_all(self, molsys_builder_complete):
        # single chain has 3 atoms
        result = aux.get_n_atoms_from_chain(molsys_builder_complete)
        assert result == [3]

    def test_get_n_atoms_from_chain_slice(self, molsys_builder_complete):
        result = aux.get_n_atoms_from_chain(molsys_builder_complete, indices=[0])
        assert result == [3]

    def test_get_n_atoms_from_molecule_all(self, molsys_builder_complete):
        # molecule 0 has 2 atoms (ALA: N + CA), molecule 1 has 1 atom (HOH: O)
        result = aux.get_n_atoms_from_molecule(molsys_builder_complete)
        assert result == [2, 1]

    def test_get_n_atoms_from_molecule_slice(self, molsys_builder_complete):
        result = aux.get_n_atoms_from_molecule(molsys_builder_complete, indices=[1])
        assert result == [1]

    def test_get_n_atoms_from_entity_all(self, molsys_builder_complete):
        # entity 0 -> protein (2 atoms), entity 1 -> water (1 atom)
        result = aux.get_n_atoms_from_entity(molsys_builder_complete)
        assert result == [2, 1]

    def test_get_n_atoms_from_entity_slice(self, molsys_builder_complete):
        result = aux.get_n_atoms_from_entity(molsys_builder_complete, indices=[0])
        assert result == [2]

"""
Tests for molsysmt_MolSys/set.py — topological attribute setters.

Each setter delegates to the corresponding molsysmt_Topology setter.
Tests use a fresh copy of hp35_pdb_molsys (chicken villin HP35, 1vii.pdb)
for every test function so that mutations never bleed between tests.

HP35 quick reference (1vii.pdb):
  N_ATOMS      = 596
  N_GROUPS     = 36   (all amino acids)
  N_COMPONENTS = 1
  N_MOLECULES  = 1
  N_ENTITIES   = 1
  N_CHAINS     = 1
"""

import pytest
import numpy as np
from molsysmt import pyunitwizard as puw
from molsysmt.form.molsysmt_MolSys import set as aux
from molsysmt.form.molsysmt_MolSys import get_topological_attributes as get_aux

N_ATOMS      = 596
N_GROUPS     = 36
N_COMPONENTS = 1
N_MOLECULES  = 1
N_ENTITIES   = 1
N_CHAINS     = 1


# ---------------------------------------------------------------------------
# Atom-level setters (set_*_to_atom)
# ---------------------------------------------------------------------------

class TestAtomLevelSetters:

    def test_set_atom_name_to_atom_all(self, hp35_pdb_molsys):
        original = get_aux.get_atom_name_from_atom(hp35_pdb_molsys)
        new_names = ['X'] * N_ATOMS
        aux.set_atom_name_to_atom(hp35_pdb_molsys, value=new_names, skip_digestion=True)
        result = get_aux.get_atom_name_from_atom(hp35_pdb_molsys)
        assert result == new_names
        assert result != original

    def test_set_atom_name_to_atom_indices(self, hp35_pdb_molsys):
        aux.set_atom_name_to_atom(hp35_pdb_molsys, indices=[0, 1, 2],
                                  value=['AA', 'BB', 'CC'], skip_digestion=True)
        result = get_aux.get_atom_name_from_atom(hp35_pdb_molsys)
        assert result[0] == 'AA'
        assert result[1] == 'BB'
        assert result[2] == 'CC'

    def test_set_atom_id_to_atom_all(self, hp35_pdb_molsys):
        new_ids = [str(i) for i in range(1000, 1000 + N_ATOMS)]
        aux.set_atom_id_to_atom(hp35_pdb_molsys, value=new_ids, skip_digestion=True)
        result = get_aux.get_atom_id_from_atom(hp35_pdb_molsys)
        assert list(result) == new_ids

    def test_set_atom_id_to_atom_indices(self, hp35_pdb_molsys):
        aux.set_atom_id_to_atom(hp35_pdb_molsys, indices=[0, 1],
                                value=['9001', '9002'], skip_digestion=True)
        result = get_aux.get_atom_id_from_atom(hp35_pdb_molsys)
        assert result[0] == '9001'
        assert result[1] == '9002'

    def test_set_atom_type_to_atom_all(self, hp35_pdb_molsys):
        new_types = ['C'] * N_ATOMS
        aux.set_atom_type_to_atom(hp35_pdb_molsys, value=new_types, skip_digestion=True)
        result = get_aux.get_atom_type_from_atom(hp35_pdb_molsys)
        assert result == new_types

    def test_set_group_name_to_atom_all(self, hp35_pdb_molsys):
        """group_name carried per-atom reflects the group each atom belongs to."""
        original = get_aux.get_group_name_from_atom(hp35_pdb_molsys)
        new_group_names = ['GLY'] * N_ATOMS
        aux.set_group_name_to_atom(hp35_pdb_molsys, value=new_group_names,
                                   skip_digestion=True)
        result = get_aux.get_group_name_from_atom(hp35_pdb_molsys)
        assert result == new_group_names
        assert result != original

    def test_set_group_id_to_atom_all(self, hp35_pdb_molsys):
        new_ids = [99] * N_ATOMS
        aux.set_group_id_to_atom(hp35_pdb_molsys, value=new_ids, skip_digestion=True)
        result = get_aux.get_group_id_from_atom(hp35_pdb_molsys)
        assert list(result) == new_ids

    def test_set_group_type_to_atom_all(self, hp35_pdb_molsys):
        new_types = ['amino acid'] * N_ATOMS
        aux.set_group_type_to_atom(hp35_pdb_molsys, value=new_types,
                                   skip_digestion=True)
        result = get_aux.get_group_type_from_atom(hp35_pdb_molsys)
        assert result == new_types

    def test_set_molecule_name_to_atom_all(self, hp35_pdb_molsys):
        new_names = ['MyProtein'] * N_ATOMS
        aux.set_molecule_name_to_atom(hp35_pdb_molsys, value=new_names,
                                      skip_digestion=True)
        result = get_aux.get_molecule_name_from_atom(hp35_pdb_molsys)
        assert result == new_names

    def test_set_molecule_type_to_atom_all(self, hp35_pdb_molsys):
        new_types = ['peptide'] * N_ATOMS
        aux.set_molecule_type_to_atom(hp35_pdb_molsys, value=new_types,
                                      skip_digestion=True)
        result = get_aux.get_molecule_type_from_atom(hp35_pdb_molsys)
        assert result == new_types

    def test_set_chain_name_to_atom_all(self, hp35_pdb_molsys):
        new_names = ['Z'] * N_ATOMS
        aux.set_chain_name_to_atom(hp35_pdb_molsys, value=new_names,
                                   skip_digestion=True)
        result = get_aux.get_chain_name_from_atom(hp35_pdb_molsys)
        assert result == new_names

    def test_set_chain_id_to_atom_all(self, hp35_pdb_molsys):
        new_ids = ['B'] * N_ATOMS
        aux.set_chain_id_to_atom(hp35_pdb_molsys, value=new_ids, skip_digestion=True)
        result = get_aux.get_chain_id_from_atom(hp35_pdb_molsys)
        assert result == new_ids

    def test_set_entity_name_to_atom_all(self, hp35_pdb_molsys):
        new_names = ['HP35_variant'] * N_ATOMS
        aux.set_entity_name_to_atom(hp35_pdb_molsys, value=new_names,
                                    skip_digestion=True)
        result = get_aux.get_entity_name_from_atom(hp35_pdb_molsys)
        assert result == new_names

    def test_set_entity_type_to_atom_all(self, hp35_pdb_molsys):
        new_types = ['protein'] * N_ATOMS
        aux.set_entity_type_to_atom(hp35_pdb_molsys, value=new_types,
                                    skip_digestion=True)
        result = get_aux.get_entity_type_from_atom(hp35_pdb_molsys)
        assert result == new_types


# ---------------------------------------------------------------------------
# Group-level setters (set_*_to_group)
# ---------------------------------------------------------------------------

class TestGroupLevelSetters:

    def test_set_group_name_to_group_all(self, hp35_pdb_molsys):
        original = get_aux.get_group_name_from_group(hp35_pdb_molsys)
        new_names = ['RES'] * N_GROUPS
        aux.set_group_name_to_group(hp35_pdb_molsys, value=new_names,
                                    skip_digestion=True)
        result = get_aux.get_group_name_from_group(hp35_pdb_molsys)
        assert result == new_names
        assert result != original

    def test_set_group_name_to_group_indices(self, hp35_pdb_molsys):
        aux.set_group_name_to_group(hp35_pdb_molsys, indices=[0, 1],
                                    value=['ALA', 'GLY'], skip_digestion=True)
        result = get_aux.get_group_name_from_group(hp35_pdb_molsys)
        assert result[0] == 'ALA'
        assert result[1] == 'GLY'

    def test_set_group_id_to_group_all(self, hp35_pdb_molsys):
        new_ids = list(range(100, 100 + N_GROUPS))
        aux.set_group_id_to_group(hp35_pdb_molsys, value=new_ids,
                                  skip_digestion=True)
        result = get_aux.get_group_id_from_group(hp35_pdb_molsys)
        assert list(result) == new_ids

    def test_set_group_type_to_group_all(self, hp35_pdb_molsys):
        new_types = ['amino acid'] * N_GROUPS
        aux.set_group_type_to_group(hp35_pdb_molsys, value=new_types,
                                    skip_digestion=True)
        result = get_aux.get_group_type_from_group(hp35_pdb_molsys)
        assert result == new_types

    def test_set_molecule_name_to_group_all(self, hp35_pdb_molsys):
        new_names = ['ProteinA'] * N_GROUPS
        aux.set_molecule_name_to_group(hp35_pdb_molsys, value=new_names,
                                       skip_digestion=True)
        result = get_aux.get_molecule_name_from_group(hp35_pdb_molsys)
        assert result == new_names

    def test_set_molecule_type_to_group_all(self, hp35_pdb_molsys):
        new_types = ['peptide'] * N_GROUPS
        aux.set_molecule_type_to_group(hp35_pdb_molsys, value=new_types,
                                       skip_digestion=True)
        result = get_aux.get_molecule_type_from_group(hp35_pdb_molsys)
        assert result == new_types

    def test_set_chain_name_to_group_all(self, hp35_pdb_molsys):
        new_names = ['Z'] * N_GROUPS
        aux.set_chain_name_to_group(hp35_pdb_molsys, value=new_names,
                                    skip_digestion=True)
        result = get_aux.get_chain_name_from_group(hp35_pdb_molsys)
        assert result == new_names

    def test_set_entity_name_to_group_all(self, hp35_pdb_molsys):
        new_names = ['TargetProtein'] * N_GROUPS
        aux.set_entity_name_to_group(hp35_pdb_molsys, value=new_names,
                                     skip_digestion=True)
        result = get_aux.get_entity_name_from_group(hp35_pdb_molsys)
        assert result == new_names

    def test_set_entity_type_to_group_all(self, hp35_pdb_molsys):
        new_types = ['protein'] * N_GROUPS
        aux.set_entity_type_to_group(hp35_pdb_molsys, value=new_types,
                                     skip_digestion=True)
        result = get_aux.get_entity_type_from_group(hp35_pdb_molsys)
        assert result == new_types


# ---------------------------------------------------------------------------
# Component-level setters (set_*_to_component)
# ---------------------------------------------------------------------------

class TestComponentLevelSetters:

    def test_set_component_name_to_component_all(self, hp35_pdb_molsys):
        new_names = ['CompA'] * N_COMPONENTS
        aux.set_component_name_to_component(hp35_pdb_molsys, value=new_names,
                                            skip_digestion=True)
        result = get_aux.get_component_name_from_component(hp35_pdb_molsys)
        assert result == new_names

    def test_set_component_id_to_component_all(self, hp35_pdb_molsys):
        new_ids = [42] * N_COMPONENTS
        aux.set_component_id_to_component(hp35_pdb_molsys, value=new_ids,
                                          skip_digestion=True)
        result = get_aux.get_component_id_from_component(hp35_pdb_molsys)
        assert list(result) == new_ids

    def test_set_component_type_to_component_all(self, hp35_pdb_molsys):
        new_types = ['peptide'] * N_COMPONENTS
        aux.set_component_type_to_component(hp35_pdb_molsys, value=new_types,
                                            skip_digestion=True)
        result = get_aux.get_component_type_from_component(hp35_pdb_molsys)
        assert result == new_types


# ---------------------------------------------------------------------------
# Molecule-level setters (set_*_to_molecule)
# ---------------------------------------------------------------------------

class TestMoleculeLevelSetters:

    def test_set_molecule_name_to_molecule_all(self, hp35_pdb_molsys):
        original = get_aux.get_molecule_name_from_molecule(hp35_pdb_molsys)
        new_names = ['HP35_test'] * N_MOLECULES
        aux.set_molecule_name_to_molecule(hp35_pdb_molsys, value=new_names,
                                          skip_digestion=True)
        result = get_aux.get_molecule_name_from_molecule(hp35_pdb_molsys)
        assert result == new_names
        assert result != original

    def test_set_molecule_id_to_molecule_all(self, hp35_pdb_molsys):
        new_ids = [77] * N_MOLECULES
        aux.set_molecule_id_to_molecule(hp35_pdb_molsys, value=new_ids,
                                        skip_digestion=True)
        result = get_aux.get_molecule_id_from_molecule(hp35_pdb_molsys)
        assert list(result) == new_ids

    def test_set_molecule_type_to_molecule_all(self, hp35_pdb_molsys):
        original = get_aux.get_molecule_type_from_molecule(hp35_pdb_molsys)
        new_types = ['peptide'] * N_MOLECULES
        aux.set_molecule_type_to_molecule(hp35_pdb_molsys, value=new_types,
                                          skip_digestion=True)
        result = get_aux.get_molecule_type_from_molecule(hp35_pdb_molsys)
        assert result == new_types


# ---------------------------------------------------------------------------
# Chain-level setters (set_*_to_chain)
# ---------------------------------------------------------------------------

class TestChainLevelSetters:

    def test_set_chain_name_to_chain_all(self, hp35_pdb_molsys):
        original = get_aux.get_chain_name_from_chain(hp35_pdb_molsys)
        new_names = ['Z'] * N_CHAINS
        aux.set_chain_name_to_chain(hp35_pdb_molsys, value=new_names,
                                    skip_digestion=True)
        result = get_aux.get_chain_name_from_chain(hp35_pdb_molsys)
        assert result == new_names
        assert result != original

    def test_set_chain_id_to_chain_all(self, hp35_pdb_molsys):
        original = get_aux.get_chain_id_from_chain(hp35_pdb_molsys)
        new_ids = ['B'] * N_CHAINS
        aux.set_chain_id_to_chain(hp35_pdb_molsys, value=new_ids,
                                  skip_digestion=True)
        result = get_aux.get_chain_id_from_chain(hp35_pdb_molsys)
        assert list(result) == new_ids
        assert list(result) != list(original)

    def test_set_chain_id_to_chain_indices(self, hp35_pdb_molsys):
        aux.set_chain_id_to_chain(hp35_pdb_molsys, indices=[0],
                                  value=['C'], skip_digestion=True)
        result = get_aux.get_chain_id_from_chain(hp35_pdb_molsys)
        assert result[0] == 'C'

    def test_set_chain_type_to_chain_all(self, hp35_pdb_molsys):
        new_types = ['peptide'] * N_CHAINS
        aux.set_chain_type_to_chain(hp35_pdb_molsys, value=new_types,
                                    skip_digestion=True)
        result = get_aux.get_chain_type_from_chain(hp35_pdb_molsys)
        assert result == new_types


# ---------------------------------------------------------------------------
# Entity-level setters (set_*_to_entity)
# ---------------------------------------------------------------------------

class TestEntityLevelSetters:

    def test_set_entity_name_to_entity_all(self, hp35_pdb_molsys):
        original = get_aux.get_entity_name_from_entity(hp35_pdb_molsys)
        new_names = ['VillinHP35'] * N_ENTITIES
        aux.set_entity_name_to_entity(hp35_pdb_molsys, value=new_names,
                                      skip_digestion=True)
        result = get_aux.get_entity_name_from_entity(hp35_pdb_molsys)
        assert result == new_names
        assert result != original

    def test_set_entity_id_to_entity_all(self, hp35_pdb_molsys):
        new_ids = [55] * N_ENTITIES
        aux.set_entity_id_to_entity(hp35_pdb_molsys, value=new_ids,
                                    skip_digestion=True)
        result = get_aux.get_entity_id_from_entity(hp35_pdb_molsys)
        assert list(result) == new_ids

    def test_set_entity_type_to_entity_all(self, hp35_pdb_molsys):
        new_types = ['protein'] * N_ENTITIES
        aux.set_entity_type_to_entity(hp35_pdb_molsys, value=new_types,
                                      skip_digestion=True)
        result = get_aux.get_entity_type_from_entity(hp35_pdb_molsys)
        assert result == new_types


# ---------------------------------------------------------------------------
# Cross-check: mutations on copies do not affect a sibling copy
# ---------------------------------------------------------------------------

class TestIsolation:

    def test_copies_are_independent(self, hp35_pdb_molsys):
        """Verify that two copies derived from the base fixture are independent."""
        copy_a = hp35_pdb_molsys.copy()
        copy_b = hp35_pdb_molsys.copy()

        original_names = get_aux.get_atom_name_from_atom(copy_a)[:]

        aux.set_atom_name_to_atom(copy_a, value=['Q'] * N_ATOMS,
                                  skip_digestion=True)

        names_a = get_aux.get_atom_name_from_atom(copy_a)
        names_b = get_aux.get_atom_name_from_atom(copy_b)

        assert names_a == ['Q'] * N_ATOMS
        # copy_b must still have the original names
        assert names_b == original_names
        assert names_b != names_a


# ---------------------------------------------------------------------------
# Atom-level setters — previously uncovered
# ---------------------------------------------------------------------------

class TestAtomLevelSettersUncovered:

    def test_set_group_index_to_atom(self, hp35_pdb_molsys):
        from molsysmt.form.molsysmt_MolSys import get_topological_attributes as get_aux2
        group_indices = get_aux2.get_group_index_from_atom(hp35_pdb_molsys)
        aux.set_group_index_to_atom(hp35_pdb_molsys, value=group_indices, skip_digestion=True)
        result = get_aux2.get_group_index_from_atom(hp35_pdb_molsys)
        assert result == group_indices

    def test_set_component_index_to_atom_broadcast(self, hp35_pdb_molsys):
        """Single-value broadcast path: len(value)==1."""
        aux.set_component_index_to_atom(hp35_pdb_molsys, value=[0], skip_digestion=True)

    def test_set_component_index_to_atom_full(self, hp35_pdb_molsys):
        """Full-array path: len(value)==N_ATOMS."""
        aux.set_component_index_to_atom(hp35_pdb_molsys, value=[0] * N_ATOMS, skip_digestion=True)

    def test_set_component_name_to_atom(self, hp35_pdb_molsys):
        aux.set_component_name_to_atom(hp35_pdb_molsys, value=['CompA'] * N_ATOMS, skip_digestion=True)

    def test_set_component_id_to_atom(self, hp35_pdb_molsys):
        aux.set_component_id_to_atom(hp35_pdb_molsys, value=['0'] * N_ATOMS, skip_digestion=True)

    def test_set_component_type_to_atom(self, hp35_pdb_molsys):
        aux.set_component_type_to_atom(hp35_pdb_molsys, value=['peptide'] * N_ATOMS, skip_digestion=True)

    def test_set_molecule_index_to_atom(self, hp35_pdb_molsys):
        aux.set_molecule_index_to_atom(hp35_pdb_molsys, value=[0] * N_ATOMS, skip_digestion=True)

    def test_set_molecule_id_to_atom(self, hp35_pdb_molsys):
        aux.set_molecule_id_to_atom(hp35_pdb_molsys, value=['mol0'] * N_ATOMS, skip_digestion=True)

    def test_set_chain_type_to_atom(self, hp35_pdb_molsys):
        aux.set_chain_type_to_atom(hp35_pdb_molsys, value=['protein'] * N_ATOMS, skip_digestion=True)

    def test_set_entity_index_to_atom(self, hp35_pdb_molsys):
        aux.set_entity_index_to_atom(hp35_pdb_molsys, value=[0] * N_ATOMS, skip_digestion=True)

    def test_set_entity_id_to_atom(self, hp35_pdb_molsys):
        aux.set_entity_id_to_atom(hp35_pdb_molsys, value=['0'] * N_ATOMS, skip_digestion=True)

    def test_set_velocities_to_atom(self, hp35_pdb_molsys):
        vel = puw.quantity(np.zeros((1, N_ATOMS, 3), dtype=np.float64), 'nm/ps')
        aux.set_velocities_to_atom(hp35_pdb_molsys, value=vel, skip_digestion=True)
        assert hp35_pdb_molsys.structures.velocities is not None


# ---------------------------------------------------------------------------
# Group-level setters — previously uncovered
# ---------------------------------------------------------------------------

class TestGroupLevelSettersUncovered:

    def test_set_molecule_id_to_group(self, hp35_pdb_molsys):
        aux.set_molecule_id_to_group(hp35_pdb_molsys, value=['mol0'] * N_GROUPS, skip_digestion=True)

    def test_set_chain_id_to_group(self, hp35_pdb_molsys):
        aux.set_chain_id_to_group(hp35_pdb_molsys, value=['A'] * N_GROUPS, skip_digestion=True)

    def test_set_chain_type_to_group(self, hp35_pdb_molsys):
        aux.set_chain_type_to_group(hp35_pdb_molsys, value=['protein'] * N_GROUPS, skip_digestion=True)

    def test_set_entity_id_to_group(self, hp35_pdb_molsys):
        aux.set_entity_id_to_group(hp35_pdb_molsys, value=['0'] * N_GROUPS, skip_digestion=True)


# ---------------------------------------------------------------------------
# System-level structural setter — previously uncovered
# ---------------------------------------------------------------------------

class TestSystemLevelSettersUncovered:

    def test_set_coordinates_to_system(self, hp35_pdb_molsys):
        from molsysmt.form.molsysmt_MolSys.get_structural_attributes import get_coordinates_from_atom
        coords = get_coordinates_from_atom(hp35_pdb_molsys, skip_digestion=True)
        aux.set_coordinates_to_system(hp35_pdb_molsys, value=coords, skip_digestion=True)


# ---------------------------------------------------------------------------
# Topology else-branch coverage (specific atom indices)
# ---------------------------------------------------------------------------

class TestTopologyElseBranches:
    """Covers the else (non-all indices) branches in Topology/set.py."""

    def test_set_atom_type_specific_indices(self, hp35_pdb_molsys):
        aux.set_atom_type_to_atom(hp35_pdb_molsys, indices=[0, 1, 2],
                                  value=['C', 'N', 'O'], skip_digestion=True)
        result = get_aux.get_atom_type_from_atom(hp35_pdb_molsys)
        assert result[0] == 'C'
        assert result[1] == 'N'
        assert result[2] == 'O'

    def test_set_group_id_to_atom_specific_indices(self, hp35_pdb_molsys):
        aux.set_group_id_to_atom(hp35_pdb_molsys, indices=[0, 1],
                                 value=['999', '999'], skip_digestion=True)

    def test_set_group_name_to_atom_specific_indices(self, hp35_pdb_molsys):
        aux.set_group_name_to_atom(hp35_pdb_molsys, indices=[0],
                                   value=['ALA'], skip_digestion=True)

    def test_set_group_type_to_atom_specific_indices(self, hp35_pdb_molsys):
        aux.set_group_type_to_atom(hp35_pdb_molsys, indices=[0],
                                   value=['amino acid'], skip_digestion=True)

    def test_set_group_index_to_atom_specific_indices(self, hp35_pdb_molsys):
        aux.set_group_index_to_atom(hp35_pdb_molsys, indices=[0],
                                    value=[0], skip_digestion=True)

    def test_set_component_index_to_atom_specific_indices(self, hp35_pdb_molsys):
        aux.set_component_index_to_atom(hp35_pdb_molsys, indices=[0, 1],
                                        value=[0, 0], skip_digestion=True)


class TestOccupancySetter:

    def test_set_occupancy_to_atom(self, hp35_pdb_molsys):
        from molsysmt.form.molsysmt_MolSys import set as aux
        aux.set_occupancy_to_atom(hp35_pdb_molsys, value=[[1.0] * N_ATOMS], skip_digestion=True)



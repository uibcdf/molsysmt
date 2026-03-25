"""
Tests for molsysmt_Topology/set.py — direct coverage of setter functions
not already reached via the molsysmt_MolSys set tests.

The MolSys set tests delegate to Topology setters for atom-level functions,
but many cross-element setters (group→chain, component→chain, entity→chain,
molecule→component, etc.) are only reachable by calling the Topology form
directly.

HP35 quick reference (1vii.pdb):
  N_ATOMS      = 596
  N_GROUPS     = 36
  N_COMPONENTS = 1
  N_MOLECULES  = 1
  N_ENTITIES   = 1
  N_CHAINS     = 1
"""

import pytest
import numpy as np
import molsysmt as msm
from molsysmt.form.molsysmt_Topology import set as tset
from molsysmt.form.molsysmt_Topology import get_topological_attributes as tget

N_ATOMS      = 596
N_GROUPS     = 36
N_COMPONENTS = 1
N_MOLECULES  = 1
N_ENTITIES   = 1
N_CHAINS     = 1


@pytest.fixture
def hp35_topology(hp35_pdb_molsys):
    """Fresh Topology copy for each test."""
    return hp35_pdb_molsys.topology.copy()


# ---------------------------------------------------------------------------
# Group-level setters — set_*_to_group (not fully exercised via MolSys tests)
# ---------------------------------------------------------------------------

class TestGroupLevelSetters:

    def test_set_group_index_to_group_all(self, hp35_topology):
        new_indices = list(range(N_GROUPS))
        tset.set_group_index_to_group(hp35_topology, value=new_indices, skip_digestion=True)
        result = tget.get_group_index_from_group(hp35_topology, skip_digestion=True)
        assert list(result) == new_indices

    def test_set_group_index_to_group_indices(self, hp35_topology):
        tset.set_group_index_to_group(hp35_topology, indices=[0, 1],
                                      value=[0, 1], skip_digestion=True)

    def test_set_component_index_to_group_all(self, hp35_topology):
        tset.set_component_index_to_group(hp35_topology,
                                          value=[0] * N_GROUPS, skip_digestion=True)

    def test_set_component_name_to_group_all(self, hp35_topology):
        tset.set_component_name_to_group(hp35_topology,
                                         value=['CompA'] * N_GROUPS, skip_digestion=True)

    def test_set_component_id_to_group_all(self, hp35_topology):
        tset.set_component_id_to_group(hp35_topology,
                                       value=['0'] * N_GROUPS, skip_digestion=True)

    def test_set_component_type_to_group_all(self, hp35_topology):
        tset.set_component_type_to_group(hp35_topology,
                                         value=['peptide'] * N_GROUPS, skip_digestion=True)

    def test_set_molecule_index_to_group_all(self, hp35_topology):
        tset.set_molecule_index_to_group(hp35_topology,
                                         value=[0] * N_GROUPS, skip_digestion=True)

    def test_set_chain_index_to_group_all(self, hp35_topology):
        tset.set_chain_index_to_group(hp35_topology,
                                      value=[0] * N_GROUPS, skip_digestion=True)

    def test_set_entity_index_to_group_all(self, hp35_topology):
        tset.set_entity_index_to_group(hp35_topology,
                                       value=[0] * N_GROUPS, skip_digestion=True)

    def test_set_entity_name_to_group_all(self, hp35_topology):
        tset.set_entity_name_to_group(hp35_topology,
                                      value=['villin HP35'] * N_GROUPS, skip_digestion=True)

    def test_set_entity_id_to_group_all(self, hp35_topology):
        tset.set_entity_id_to_group(hp35_topology,
                                    value=['0'] * N_GROUPS, skip_digestion=True)

    def test_set_entity_type_to_group_all(self, hp35_topology):
        tset.set_entity_type_to_group(hp35_topology,
                                      value=['protein'] * N_GROUPS, skip_digestion=True)

    # --- indices != 'all' ---

    def test_set_molecule_name_to_group_indices(self, hp35_topology):
        tset.set_molecule_name_to_group(hp35_topology, indices=[0, 1],
                                        value=['mol0', 'mol0'], skip_digestion=True)

    def test_set_chain_name_to_group_indices(self, hp35_topology):
        tset.set_chain_name_to_group(hp35_topology, indices=[0],
                                     value=['A'], skip_digestion=True)

    def test_set_chain_id_to_group_indices(self, hp35_topology):
        tset.set_chain_id_to_group(hp35_topology, indices=[0],
                                   value=['A'], skip_digestion=True)


# ---------------------------------------------------------------------------
# Component-level setters — set_*_to_component
# ---------------------------------------------------------------------------

class TestComponentLevelSetters:

    def test_set_component_index_to_component_all(self, hp35_topology):
        tset.set_component_index_to_component(hp35_topology,
                                              value=[0], skip_digestion=True)

    def test_set_component_index_to_component_indices(self, hp35_topology):
        tset.set_component_index_to_component(hp35_topology, indices=[0],
                                              value=[0], skip_digestion=True)

    def test_set_molecule_index_to_component_all(self, hp35_topology):
        tset.set_molecule_index_to_component(hp35_topology,
                                             value=[0], skip_digestion=True)

    def test_set_molecule_name_to_component_all(self, hp35_topology):
        tset.set_molecule_name_to_component(hp35_topology,
                                            value=['HP35'], skip_digestion=True)

    def test_set_molecule_id_to_component_all(self, hp35_topology):
        tset.set_molecule_id_to_component(hp35_topology,
                                          value=['0'], skip_digestion=True)

    def test_set_molecule_type_to_component_all(self, hp35_topology):
        tset.set_molecule_type_to_component(hp35_topology,
                                            value=['peptide'], skip_digestion=True)

    def test_set_chain_index_to_component_all(self, hp35_topology):
        tset.set_chain_index_to_component(hp35_topology,
                                          value=[0], skip_digestion=True)

    def test_set_chain_name_to_component_all(self, hp35_topology):
        tset.set_chain_name_to_component(hp35_topology,
                                         value=['A'], skip_digestion=True)

    def test_set_chain_id_to_component_all(self, hp35_topology):
        tset.set_chain_id_to_component(hp35_topology,
                                       value=['A'], skip_digestion=True)

    def test_set_chain_type_to_component_all(self, hp35_topology):
        tset.set_chain_type_to_component(hp35_topology,
                                         value=['protein'], skip_digestion=True)

    def test_set_entity_index_to_component_all(self, hp35_topology):
        tset.set_entity_index_to_component(hp35_topology,
                                           value=[0], skip_digestion=True)

    def test_set_entity_name_to_component_all(self, hp35_topology):
        tset.set_entity_name_to_component(hp35_topology,
                                          value=['villin HP35'], skip_digestion=True)

    def test_set_entity_id_to_component_all(self, hp35_topology):
        tset.set_entity_id_to_component(hp35_topology,
                                        value=['0'], skip_digestion=True)

    def test_set_entity_type_to_component_all(self, hp35_topology):
        tset.set_entity_type_to_component(hp35_topology,
                                          value=['protein'], skip_digestion=True)

    # --- indices != 'all' ---

    def test_set_chain_name_to_component_indices(self, hp35_topology):
        tset.set_chain_name_to_component(hp35_topology, indices=[0],
                                         value=['A'], skip_digestion=True)

    def test_set_entity_name_to_component_indices(self, hp35_topology):
        tset.set_entity_name_to_component(hp35_topology, indices=[0],
                                          value=['villin HP35'], skip_digestion=True)


# ---------------------------------------------------------------------------
# Molecule-level setters — set_*_to_molecule
# ---------------------------------------------------------------------------

class TestMoleculeLevelSetters:

    def test_set_molecule_index_to_molecule_all(self, hp35_topology):
        tset.set_molecule_index_to_molecule(hp35_topology,
                                            value=[0], skip_digestion=True)

    def test_set_chain_index_to_molecule_all(self, hp35_topology):
        tset.set_chain_index_to_molecule(hp35_topology,
                                         value=[0], skip_digestion=True)

    def test_set_chain_name_to_molecule_all(self, hp35_topology):
        tset.set_chain_name_to_molecule(hp35_topology,
                                        value=['A'], skip_digestion=True)

    def test_set_chain_id_to_molecule_all(self, hp35_topology):
        tset.set_chain_id_to_molecule(hp35_topology,
                                      value=['A'], skip_digestion=True)

    def test_set_chain_type_to_molecule_all(self, hp35_topology):
        tset.set_chain_type_to_molecule(hp35_topology,
                                        value=['protein'], skip_digestion=True)

    def test_set_entity_index_to_molecule_all(self, hp35_topology):
        tset.set_entity_index_to_molecule(hp35_topology,
                                          value=[0], skip_digestion=True)

    def test_set_entity_name_to_molecule_all(self, hp35_topology):
        tset.set_entity_name_to_molecule(hp35_topology,
                                         value=['villin HP35'], skip_digestion=True)

    def test_set_entity_id_to_molecule_all(self, hp35_topology):
        tset.set_entity_id_to_molecule(hp35_topology,
                                       value=['0'], skip_digestion=True)

    def test_set_entity_type_to_molecule_all(self, hp35_topology):
        tset.set_entity_type_to_molecule(hp35_topology,
                                         value=['protein'], skip_digestion=True)

    # --- indices != 'all' ---

    def test_set_molecule_index_to_molecule_indices(self, hp35_topology):
        tset.set_molecule_index_to_molecule(hp35_topology, indices=[0],
                                            value=[0], skip_digestion=True)

    def test_set_chain_name_to_molecule_indices(self, hp35_topology):
        tset.set_chain_name_to_molecule(hp35_topology, indices=[0],
                                        value=['A'], skip_digestion=True)


# ---------------------------------------------------------------------------
# Chain-level setters — set_*_to_chain
# ---------------------------------------------------------------------------

class TestChainLevelSetters:

    def test_set_molecule_index_to_chain_all(self, hp35_topology):
        tset.set_molecule_index_to_chain(hp35_topology,
                                         value=[0], skip_digestion=True)

    def test_set_molecule_name_to_chain_all(self, hp35_topology):
        tset.set_molecule_name_to_chain(hp35_topology,
                                        value=['HP35'], skip_digestion=True)

    def test_set_molecule_id_to_chain_all(self, hp35_topology):
        tset.set_molecule_id_to_chain(hp35_topology,
                                      value=['0'], skip_digestion=True)

    def test_set_molecule_type_to_chain_all(self, hp35_topology):
        tset.set_molecule_type_to_chain(hp35_topology,
                                        value=['peptide'], skip_digestion=True)

    def test_set_molecule_index_to_chain_indices(self, hp35_topology):
        tset.set_molecule_index_to_chain(hp35_topology, indices=[0],
                                         value=[0], skip_digestion=True)

    def test_set_chain_index_to_chain_all(self, hp35_topology):
        tset.set_chain_index_to_chain(hp35_topology, value=[0], skip_digestion=True)

    def test_set_chain_index_to_chain_indices(self, hp35_topology):
        tset.set_chain_index_to_chain(hp35_topology, indices=[0],
                                      value=[0], skip_digestion=True)

    def test_set_entity_index_to_chain_all(self, hp35_topology):
        tset.set_entity_index_to_chain(hp35_topology,
                                       value=[0], skip_digestion=True)

    def test_set_entity_name_to_chain_all(self, hp35_topology):
        tset.set_entity_name_to_chain(hp35_topology,
                                      value=['villin HP35'], skip_digestion=True)

    def test_set_entity_id_to_chain_all(self, hp35_topology):
        tset.set_entity_id_to_chain(hp35_topology,
                                    value=['0'], skip_digestion=True)

    def test_set_entity_type_to_chain_all(self, hp35_topology):
        tset.set_entity_type_to_chain(hp35_topology,
                                      value=['protein'], skip_digestion=True)

    # --- indices != 'all' ---

    def test_set_entity_name_to_chain_indices(self, hp35_topology):
        tset.set_entity_name_to_chain(hp35_topology, indices=[0],
                                      value=['villin HP35'], skip_digestion=True)


# ---------------------------------------------------------------------------
# Entity-level setters — set_*_to_entity
# ---------------------------------------------------------------------------

class TestEntityLevelSetters:

    def test_set_entity_index_to_entity_all(self, hp35_topology):
        tset.set_entity_index_to_entity(hp35_topology, value=[0], skip_digestion=True)

    def test_set_entity_index_to_entity_indices(self, hp35_topology):
        tset.set_entity_index_to_entity(hp35_topology, indices=[0],
                                        value=[0], skip_digestion=True)

    def test_set_entity_name_to_entity_indices(self, hp35_topology):
        tset.set_entity_name_to_entity(hp35_topology, indices=[0],
                                       value=['villin HP35'], skip_digestion=True)

    def test_set_entity_id_to_entity_indices(self, hp35_topology):
        tset.set_entity_id_to_entity(hp35_topology, indices=[0],
                                     value=['0'], skip_digestion=True)

    def test_set_entity_type_to_entity_indices(self, hp35_topology):
        tset.set_entity_type_to_entity(hp35_topology, indices=[0],
                                       value=['protein'], skip_digestion=True)


# ---------------------------------------------------------------------------
# Round-trip: set then get, verify value sticks
# ---------------------------------------------------------------------------

class TestRoundTrip:

    def test_group_name_roundtrip(self, hp35_topology):
        original = tget.get_group_name_from_group(hp35_topology, skip_digestion=True)
        new_names = ['GLY'] * N_GROUPS
        tset.set_group_name_to_group(hp35_topology, value=new_names, skip_digestion=True)
        result = tget.get_group_name_from_group(hp35_topology, skip_digestion=True)
        assert result == new_names
        assert result != original

    def test_entity_name_to_entity_roundtrip(self, hp35_topology):
        new_name = ['test_protein']
        tset.set_entity_name_to_entity(hp35_topology, value=new_name, skip_digestion=True)
        result = tget.get_entity_name_from_entity(hp35_topology, skip_digestion=True)
        assert result == new_name

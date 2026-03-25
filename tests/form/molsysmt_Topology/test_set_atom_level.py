"""
Atom-level setter tests for molsysmt_Topology/set.py.

Covers all set_*_to_atom functions with both is_all=True and specific-indices
paths, which were entirely absent from test_set_topological_attributes.py.

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
from molsysmt.form.molsysmt_Topology import set as tset
from molsysmt.form.molsysmt_Topology import get_topological_attributes as tget

N_ATOMS  = 596
N_GROUPS = 36


@pytest.fixture
def hp35_topology(hp35_pdb_molsys):
    """Fresh Topology copy for each test (function-scoped)."""
    return hp35_pdb_molsys.topology.copy()


# ---------------------------------------------------------------------------
# Direct atom attribute setters
# ---------------------------------------------------------------------------

class TestDirectAtomSetters:
    """set_atom_{id,name,type,group_index}_to_atom — is_all and index paths."""

    def test_set_atom_id_to_atom_all(self, hp35_topology):
        new_ids = list(range(1, N_ATOMS + 1))
        tset.set_atom_id_to_atom(hp35_topology, value=new_ids, skip_digestion=True)

    def test_set_atom_id_to_atom_indices(self, hp35_topology):
        tset.set_atom_id_to_atom(hp35_topology, indices=[0, 1, 2],
                                 value=['100', '101', '102'], skip_digestion=True)

    def test_set_atom_name_to_atom_all(self, hp35_topology):
        new_names = ['X'] * N_ATOMS
        tset.set_atom_name_to_atom(hp35_topology, value=new_names, skip_digestion=True)

    def test_set_atom_name_to_atom_indices(self, hp35_topology):
        tset.set_atom_name_to_atom(hp35_topology, indices=[0, 1],
                                   value=['CA', 'CB'], skip_digestion=True)

    def test_set_atom_type_to_atom_all(self, hp35_topology):
        new_types = ['C'] * N_ATOMS
        tset.set_atom_type_to_atom(hp35_topology, value=new_types, skip_digestion=True)

    def test_set_atom_type_to_atom_indices(self, hp35_topology):
        tset.set_atom_type_to_atom(hp35_topology, indices=[0],
                                   value=['N'], skip_digestion=True)

    def test_set_group_index_to_atom_all(self, hp35_topology):
        current = tget.get_group_index_from_atom(hp35_topology, skip_digestion=True)
        tset.set_group_index_to_atom(hp35_topology, value=current, skip_digestion=True)

    def test_set_group_index_to_atom_indices(self, hp35_topology):
        tset.set_group_index_to_atom(hp35_topology, indices=[0],
                                     value=[0], skip_digestion=True)

    def test_set_component_index_to_atom_all_multi(self, hp35_topology):
        """is_all + len(value) > 1 path."""
        current = tget.get_component_index_from_atom(hp35_topology, skip_digestion=True)
        tset.set_component_index_to_atom(hp35_topology, value=current, skip_digestion=True)

    def test_set_component_index_to_atom_all_single(self, hp35_topology):
        """is_all + len(value) == 1 path."""
        tset.set_component_index_to_atom(hp35_topology, value=[0], skip_digestion=True)

    def test_set_component_index_to_atom_indices(self, hp35_topology):
        tset.set_component_index_to_atom(hp35_topology, indices=[0, 1],
                                         value=[0, 0], skip_digestion=True)

    def test_set_chain_index_to_atom_all_multi(self, hp35_topology):
        """is_all + len(value) > 1 path."""
        current = tget.get_chain_index_from_atom(hp35_topology, skip_digestion=True)
        tset.set_chain_index_to_atom(hp35_topology, value=current, skip_digestion=True)

    def test_set_chain_index_to_atom_all_single(self, hp35_topology):
        """is_all + len(value) == 1 path."""
        tset.set_chain_index_to_atom(hp35_topology, value=[0], skip_digestion=True)

    def test_set_chain_index_to_atom_indices(self, hp35_topology):
        tset.set_chain_index_to_atom(hp35_topology, indices=[0, 1],
                                     value=[0, 0], skip_digestion=True)


# ---------------------------------------------------------------------------
# Cross-element atom setters (group attributes)
# ---------------------------------------------------------------------------

class TestCrossElementAtomToGroupSetters:
    """set_{group_id,group_name,group_type}_to_atom — is_all and indices paths."""

    def test_set_group_id_to_atom_all(self, hp35_topology):
        current_ids = tget.get_group_id_from_group(hp35_topology, skip_digestion=True)
        group_idx = tget.get_group_index_from_atom(hp35_topology, skip_digestion=True)
        values = [current_ids[gi] for gi in group_idx]
        tset.set_group_id_to_atom(hp35_topology, value=values, skip_digestion=True)

    def test_set_group_id_to_atom_indices(self, hp35_topology):
        tset.set_group_id_to_atom(hp35_topology, indices=[0],
                                  value=['99'], skip_digestion=True)

    def test_set_group_name_to_atom_all(self, hp35_topology):
        group_names = tget.get_group_name_from_group(hp35_topology, skip_digestion=True)
        group_idx = tget.get_group_index_from_atom(hp35_topology, skip_digestion=True)
        values = [group_names[gi] for gi in group_idx]
        tset.set_group_name_to_atom(hp35_topology, value=values, skip_digestion=True)

    def test_set_group_name_to_atom_indices(self, hp35_topology):
        tset.set_group_name_to_atom(hp35_topology, indices=[0],
                                    value=['GLY'], skip_digestion=True)

    def test_set_group_type_to_atom_all(self, hp35_topology):
        group_types = tget.get_group_type_from_group(hp35_topology, skip_digestion=True)
        group_idx = tget.get_group_index_from_atom(hp35_topology, skip_digestion=True)
        values = [group_types[gi] for gi in group_idx]
        tset.set_group_type_to_atom(hp35_topology, value=values, skip_digestion=True)

    def test_set_group_type_to_atom_indices(self, hp35_topology):
        tset.set_group_type_to_atom(hp35_topology, indices=[0],
                                    value=['amino acid'], skip_digestion=True)


# ---------------------------------------------------------------------------
# Cross-element atom setters (component attributes)
# ---------------------------------------------------------------------------

class TestCrossElementAtomToComponentSetters:

    def test_set_component_id_to_atom_all(self, hp35_topology):
        comp_ids = tget.get_component_id_from_component(hp35_topology, skip_digestion=True)
        comp_idx = tget.get_component_index_from_atom(hp35_topology, skip_digestion=True)
        values = [comp_ids[ci] for ci in comp_idx]
        tset.set_component_id_to_atom(hp35_topology, value=values, skip_digestion=True)

    def test_set_component_id_to_atom_indices(self, hp35_topology):
        tset.set_component_id_to_atom(hp35_topology, indices=[0],
                                      value=['0'], skip_digestion=True)

    def test_set_component_name_to_atom_all(self, hp35_topology):
        comp_names = tget.get_component_name_from_component(hp35_topology, skip_digestion=True)
        comp_idx = tget.get_component_index_from_atom(hp35_topology, skip_digestion=True)
        values = [comp_names[ci] for ci in comp_idx]
        tset.set_component_name_to_atom(hp35_topology, value=values, skip_digestion=True)

    def test_set_component_name_to_atom_indices(self, hp35_topology):
        tset.set_component_name_to_atom(hp35_topology, indices=[0],
                                        value=['HP35'], skip_digestion=True)

    def test_set_component_type_to_atom_all(self, hp35_topology):
        comp_types = tget.get_component_type_from_component(hp35_topology, skip_digestion=True)
        comp_idx = tget.get_component_index_from_atom(hp35_topology, skip_digestion=True)
        values = [comp_types[ci] for ci in comp_idx]
        tset.set_component_type_to_atom(hp35_topology, value=values, skip_digestion=True)

    def test_set_component_type_to_atom_indices(self, hp35_topology):
        tset.set_component_type_to_atom(hp35_topology, indices=[0],
                                        value=['peptide'], skip_digestion=True)


# ---------------------------------------------------------------------------
# Cross-element atom setters (molecule attributes)
# ---------------------------------------------------------------------------

class TestCrossElementAtomToMoleculeSetters:

    def test_set_molecule_index_to_atom_all(self, hp35_topology):
        mol_idx = tget.get_molecule_index_from_atom(hp35_topology, skip_digestion=True)
        tset.set_molecule_index_to_atom(hp35_topology, value=mol_idx, skip_digestion=True)

    def test_set_molecule_index_to_atom_indices(self, hp35_topology):
        tset.set_molecule_index_to_atom(hp35_topology, indices=[0],
                                        value=[0], skip_digestion=True)

    def test_set_molecule_id_to_atom_all(self, hp35_topology):
        mol_ids = tget.get_molecule_id_from_molecule(hp35_topology, skip_digestion=True)
        mol_idx = tget.get_molecule_index_from_atom(hp35_topology, skip_digestion=True)
        values = [mol_ids[mi] for mi in mol_idx]
        tset.set_molecule_id_to_atom(hp35_topology, value=values, skip_digestion=True)

    def test_set_molecule_id_to_atom_indices(self, hp35_topology):
        tset.set_molecule_id_to_atom(hp35_topology, indices=[0],
                                     value=['0'], skip_digestion=True)

    def test_set_molecule_name_to_atom_all(self, hp35_topology):
        mol_names = tget.get_molecule_name_from_molecule(hp35_topology, skip_digestion=True)
        mol_idx = tget.get_molecule_index_from_atom(hp35_topology, skip_digestion=True)
        values = [mol_names[mi] for mi in mol_idx]
        tset.set_molecule_name_to_atom(hp35_topology, value=values, skip_digestion=True)

    def test_set_molecule_name_to_atom_indices(self, hp35_topology):
        tset.set_molecule_name_to_atom(hp35_topology, indices=[0],
                                       value=['HP35'], skip_digestion=True)

    def test_set_molecule_type_to_atom_all(self, hp35_topology):
        mol_types = tget.get_molecule_type_from_molecule(hp35_topology, skip_digestion=True)
        mol_idx = tget.get_molecule_index_from_atom(hp35_topology, skip_digestion=True)
        values = [mol_types[mi] for mi in mol_idx]
        tset.set_molecule_type_to_atom(hp35_topology, value=values, skip_digestion=True)

    def test_set_molecule_type_to_atom_indices(self, hp35_topology):
        tset.set_molecule_type_to_atom(hp35_topology, indices=[0],
                                       value=['peptide'], skip_digestion=True)


# ---------------------------------------------------------------------------
# Cross-element atom setters (chain attributes)
# ---------------------------------------------------------------------------

class TestCrossElementAtomToChainSetters:

    def test_set_chain_id_to_atom_all(self, hp35_topology):
        chain_ids = tget.get_chain_id_from_chain(hp35_topology, skip_digestion=True)
        chain_idx = tget.get_chain_index_from_atom(hp35_topology, skip_digestion=True)
        values = [chain_ids[ci] for ci in chain_idx]
        tset.set_chain_id_to_atom(hp35_topology, value=values, skip_digestion=True)

    def test_set_chain_id_to_atom_indices(self, hp35_topology):
        tset.set_chain_id_to_atom(hp35_topology, indices=[0],
                                  value=['A'], skip_digestion=True)

    def test_set_chain_name_to_atom_all(self, hp35_topology):
        chain_names = tget.get_chain_name_from_chain(hp35_topology, skip_digestion=True)
        chain_idx = tget.get_chain_index_from_atom(hp35_topology, skip_digestion=True)
        values = [chain_names[ci] for ci in chain_idx]
        tset.set_chain_name_to_atom(hp35_topology, value=values, skip_digestion=True)

    def test_set_chain_name_to_atom_indices(self, hp35_topology):
        tset.set_chain_name_to_atom(hp35_topology, indices=[0],
                                    value=['A'], skip_digestion=True)

    def test_set_chain_type_to_atom_all(self, hp35_topology):
        chain_types = tget.get_chain_type_from_chain(hp35_topology, skip_digestion=True)
        chain_idx = tget.get_chain_index_from_atom(hp35_topology, skip_digestion=True)
        values = [chain_types[ci] for ci in chain_idx]
        tset.set_chain_type_to_atom(hp35_topology, value=values, skip_digestion=True)

    def test_set_chain_type_to_atom_indices(self, hp35_topology):
        tset.set_chain_type_to_atom(hp35_topology, indices=[0],
                                    value=['protein'], skip_digestion=True)


# ---------------------------------------------------------------------------
# Cross-element atom setters (entity attributes)
# ---------------------------------------------------------------------------

class TestCrossElementAtomToEntitySetters:

    def test_set_entity_index_to_atom_all(self, hp35_topology):
        ent_idx = tget.get_entity_index_from_atom(hp35_topology, skip_digestion=True)
        tset.set_entity_index_to_atom(hp35_topology, value=ent_idx, skip_digestion=True)

    def test_set_entity_index_to_atom_indices(self, hp35_topology):
        tset.set_entity_index_to_atom(hp35_topology, indices=[0],
                                      value=[0], skip_digestion=True)

    def test_set_entity_id_to_atom_all(self, hp35_topology):
        ent_ids = tget.get_entity_id_from_entity(hp35_topology, skip_digestion=True)
        ent_idx = tget.get_entity_index_from_atom(hp35_topology, skip_digestion=True)
        values = [ent_ids[ei] for ei in ent_idx]
        tset.set_entity_id_to_atom(hp35_topology, value=values, skip_digestion=True)

    def test_set_entity_id_to_atom_indices(self, hp35_topology):
        tset.set_entity_id_to_atom(hp35_topology, indices=[0],
                                   value=['0'], skip_digestion=True)

    def test_set_entity_name_to_atom_all(self, hp35_topology):
        ent_names = tget.get_entity_name_from_entity(hp35_topology, skip_digestion=True)
        ent_idx = tget.get_entity_index_from_atom(hp35_topology, skip_digestion=True)
        values = [ent_names[ei] for ei in ent_idx]
        tset.set_entity_name_to_atom(hp35_topology, value=values, skip_digestion=True)

    def test_set_entity_name_to_atom_indices(self, hp35_topology):
        tset.set_entity_name_to_atom(hp35_topology, indices=[0],
                                     value=['villin HP35'], skip_digestion=True)

    def test_set_entity_type_to_atom_all(self, hp35_topology):
        ent_types = tget.get_entity_type_from_entity(hp35_topology, skip_digestion=True)
        ent_idx = tget.get_entity_index_from_atom(hp35_topology, skip_digestion=True)
        values = [ent_types[ei] for ei in ent_idx]
        tset.set_entity_type_to_atom(hp35_topology, value=values, skip_digestion=True)

    def test_set_entity_type_to_atom_indices(self, hp35_topology):
        tset.set_entity_type_to_atom(hp35_topology, indices=[0],
                                     value=['protein'], skip_digestion=True)

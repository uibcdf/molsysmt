"""
Extended tests for molsysmt.basic.merge covering additional branches:
- selections as a list per system
- to_form explicitly specified
- keep_ids=False
- length mismatch raises ArgumentLengthError
- mixed-form systems (convert branch)
"""
import molsysmt as msm
from molsysmt import systems
import numpy as np
import pandas as pd
import pytest


@pytest.fixture()
def ala_molsys(alanine_molsys):
    return alanine_molsys


@pytest.fixture()
def pro_molsys(proline_molsys):
    return proline_molsys


@pytest.fixture()
def val_molsys(valine_molsys):
    return valine_molsys


# ---------------------------------------------------------------------------
# selections as a list
# ---------------------------------------------------------------------------

def test_merge_with_per_system_selections(pro_molsys, val_molsys):
    """selections as list of 'all' works the same as a single 'all'."""
    n_atoms_pro = msm.get(pro_molsys, element='system', n_atoms=True)
    n_atoms_val = msm.get(val_molsys, element='system', n_atoms=True)
    merged = msm.merge([pro_molsys, val_molsys], selections=['all', 'all'])
    n_atoms = msm.get(merged, element='system', n_atoms=True)
    assert n_atoms == n_atoms_pro + n_atoms_val


def test_merge_with_scalar_selection_broadcasts_to_all_systems(pro_molsys, val_molsys):
    """A scalar atom selection applies independently to every input system."""
    merged = msm.merge([pro_molsys, val_molsys], selections=0)
    assert msm.get(merged, element='system', n_atoms=True) == 2


def test_merge_with_numpy_selection_broadcasts_collection(pro_molsys, val_molsys):
    """A NumPy atom-index collection is shared by every input system."""
    merged = msm.merge([pro_molsys, val_molsys], selections=np.array([0, 1]))
    assert msm.get(merged, element='system', n_atoms=True) == 4


def test_merge_with_per_system_index_collections(pro_molsys, val_molsys):
    """Nested lists preserve distinct atom-index collections per system."""
    merged = msm.merge(
        [pro_molsys, val_molsys],
        selections=[[0, 1], [0, 1, 2]],
    )
    assert msm.get(merged, element='system', n_atoms=True) == 5


def test_merge_three_systems_with_list_selections(pro_molsys, val_molsys, ala_molsys):
    """selections as a list with three 'all' entries merges all atoms."""
    n_atoms_pro = msm.get(pro_molsys, element='system', n_atoms=True)
    n_atoms_val = msm.get(val_molsys, element='system', n_atoms=True)
    n_atoms_ala = msm.get(ala_molsys, element='system', n_atoms=True)
    merged = msm.merge([pro_molsys, val_molsys, ala_molsys], selections=['all', 'all', 'all'])
    n_atoms = msm.get(merged, element='system', n_atoms=True)
    assert n_atoms == n_atoms_pro + n_atoms_val + n_atoms_ala


# ---------------------------------------------------------------------------
# keep_ids=False
# ---------------------------------------------------------------------------

def test_merge_keep_ids_false(pro_molsys, val_molsys):
    """keep_ids=False merges without errors and returns correct atom count."""
    n_atoms_pro = msm.get(pro_molsys, element='system', n_atoms=True)
    n_atoms_val = msm.get(val_molsys, element='system', n_atoms=True)
    merged = msm.merge([pro_molsys, val_molsys], keep_ids=False)
    n_atoms = msm.get(merged, element='system', n_atoms=True)
    assert n_atoms == n_atoms_pro + n_atoms_val


# ---------------------------------------------------------------------------
# output form check
# ---------------------------------------------------------------------------

def test_merge_inherits_first_form(pro_molsys, val_molsys):
    """Merged system inherits the first input system's form when to_form=None."""
    merged = msm.merge([pro_molsys, val_molsys])
    assert msm.get_form(merged) == msm.get_form(pro_molsys)


def test_merge_to_form_topology(pro_molsys, val_molsys):
    """to_form='molsysmt.Topology' returns a Topology object."""
    merged = msm.merge([pro_molsys, val_molsys], to_form='molsysmt.Topology')
    assert msm.get_form(merged) == 'molsysmt.Topology'
    n_atoms_pro = msm.get(pro_molsys, element='system', n_atoms=True)
    n_atoms_val = msm.get(val_molsys, element='system', n_atoms=True)
    n_atoms = msm.get(merged, element='system', n_atoms=True)
    assert n_atoms == n_atoms_pro + n_atoms_val


def test_merge_uses_named_current_schema_and_preserves_state_membership(ala_molsys):
    """The atom schema must not be treated as the retired flat positional layout."""

    left = ala_molsys.topology.copy()
    right = ala_molsys.topology.copy()
    assert left.atoms.columns.tolist() == [
        'atom_id', 'atom_name', 'atom_type', 'isotope', 'group_index', 'chain_index'
    ]
    left._set_chemical_state_atom_attribute(
        'formal_charge', [0] * left.n_atoms
    )
    right._set_chemical_state_atom_attribute(
        'formal_charge', [1] * right.n_atoms
    )

    merged = msm.merge([left, right], to_form='molsysmt.Topology')

    charges = merged._get_chemical_state_atom_attribute('formal_charge').tolist()
    assert charges == [0] * left.n_atoms + [1] * right.n_atoms
    assert merged._get_component_indices().iloc[right.n_atoms] >= left.n_components
    assert merged.atoms['chain_index'].iloc[right.n_atoms] >= left.n_chains


def test_merge_offsets_normalized_bond_atom_references(ala_molsys):
    left = ala_molsys.topology.copy()
    right = ala_molsys.topology.copy()
    bonds = right._get_chemical_state_bonds().copy()
    atom1 = int(bonds.at[0, 'atom1_index'])
    atom2 = int(bonds.at[0, 'atom2_index'])
    n_bonds = len(bonds.index)
    bonds['bond_type'] = pd.array([pd.NA] * n_bonds, dtype='string')
    bonds['donor_atom_index'] = pd.array([pd.NA] * n_bonds, dtype='Int64')
    bonds['acceptor_atom_index'] = pd.array([pd.NA] * n_bonds, dtype='Int64')
    bonds['stereochemistry'] = pd.array([pd.NA] * n_bonds, dtype='string')
    bonds['stereo_atom1_index'] = pd.array([pd.NA] * n_bonds, dtype='Int64')
    bonds['stereo_atom2_index'] = pd.array([pd.NA] * n_bonds, dtype='Int64')
    bonds['joins_components'] = pd.array([pd.NA] * n_bonds, dtype='boolean')
    bonds.at[0, 'bond_type'] = 'dative'
    bonds.at[0, 'donor_atom_index'] = atom2
    bonds.at[0, 'acceptor_atom_index'] = atom1
    bonds.at[0, 'stereochemistry'] = 'E'
    bonds.at[0, 'stereo_atom1_index'] = atom1
    bonds.at[0, 'stereo_atom2_index'] = atom2
    right._set_chemical_state_bonds(bonds)

    merged = msm.merge([left, right], to_form='molsysmt.Topology')
    directional = merged.bonds.loc[merged.bonds['donor_atom_index'].notna()].iloc[0]
    offset = left.n_atoms

    assert directional['atom1_index'] == atom1 + offset
    assert directional['atom2_index'] == atom2 + offset
    assert directional['donor_atom_index'] == atom2 + offset
    assert directional['acceptor_atom_index'] == atom1 + offset
    assert directional['stereo_atom1_index'] == atom1 + offset
    assert directional['stereo_atom2_index'] == atom2 + offset


# ---------------------------------------------------------------------------
# length mismatch errors
# ---------------------------------------------------------------------------

def test_merge_selections_length_mismatch(pro_molsys, val_molsys):
    """selections list with wrong length raises ArgumentLengthError."""
    from molsysmt._private.smonitor import ArgumentLengthError
    with pytest.raises(ArgumentLengthError):
        msm.merge([pro_molsys, val_molsys], selections=['all'])  # len 1 != 2


def test_merge_structure_indices_list_two_all(pro_molsys, val_molsys):
    """structure_indices as ['all', 'all'] merges all structures from both systems."""
    merged = msm.merge([pro_molsys, val_molsys], structure_indices=['all', 'all'])
    n_structures = msm.get(merged, element='system', n_structures=True)
    assert n_structures == 1


def test_merge_flat_structure_indices_are_per_system(pro_molsys, val_molsys):
    """A flat list with one frame index per system keeps its outer meaning."""
    merged = msm.merge([pro_molsys, val_molsys], structure_indices=[0, 0])
    assert msm.get(merged, element='system', n_structures=True) == 1


# ---------------------------------------------------------------------------
# structure_indices as a list
# ---------------------------------------------------------------------------

def test_merge_with_structure_indices_list(pro_molsys, val_molsys):
    """structure_indices=['all', 'all'] works same as single 'all'."""
    merged = msm.merge([pro_molsys, val_molsys], structure_indices=['all', 'all'])
    assert msm.get(merged, element='system', n_structures=True) == 1

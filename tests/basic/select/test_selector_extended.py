"""
Extended unit tests for molsysmt.basic.selector.molsysmt covering branches
not exercised in test_select_molsysmt_MolSys.py.

Branches targeted:
- selection by chain_index (chain column join path)
- selection by component_index (component column join path)
- selection by entity_index (entity column join path)
- selection by molecule_name / entity_name / entity_type
- selection by group_id with numeric comparison (integer coercion path)
- selection by group_index range (>= / <=)
- boolean OR across atom_index
- empty selection (returns [])
- 'in groups of' with explicit before mask (non-all)
- 'in groups of all' (all before mask path)
- 'in molecules of' join
- 'in chains of' path
- 'in entities of' path
- nested 'in groups of ... in molecules of' (two-level in_elements_of)
"""

import molsysmt as msm
import numpy as np
import pytest


# ---------------------------------------------------------------------------
# Basic standard-select branches not in existing test file
# ---------------------------------------------------------------------------

def test_select_chain_index_list(tctim_h5msm_molsys):
    """Selection by chain_index exercises the chain column join path."""
    molsys = tctim_h5msm_molsys
    # TcTIM has 4 chains (0,1 protein; 2,3 water).  Chains 0+1 → 3818 atoms.
    output = msm.select(molsys, 'chain_index==[0,1]')
    assert len(output) == 3818
    assert output[0] == 0


def test_select_component_index(tctim_h5msm_molsys):
    """Selection by component_index exercises the component column join path."""
    molsys = tctim_h5msm_molsys
    output = msm.select(molsys, 'component_index==0')
    assert len(output) == 1906


def test_select_entity_index(tctim_h5msm_molsys):
    """Selection by entity_index exercises the entity column join path."""
    molsys = tctim_h5msm_molsys
    output = msm.select(molsys, 'entity_index==0')
    assert len(output) == 3818


def test_select_entity_type(tctim_h5msm_molsys):
    """Selection by entity_type joins entity table."""
    molsys = tctim_h5msm_molsys
    output = msm.select(molsys, 'entity_type=="protein"')
    assert len(output) == 3818


def test_select_entity_name(tctim_h5msm_molsys):
    """Selection by entity_name joins entity table."""
    molsys = tctim_h5msm_molsys
    output = msm.select(molsys, 'entity_name=="water"')
    assert len(output) == 165


def test_select_molecule_name(tctim_h5msm_molsys):
    """Selection by molecule_name exercises the molecule column join path."""
    molsys = tctim_h5msm_molsys
    output = msm.select(molsys, 'molecule_name=="TRIOSEPHOSPHATE ISOMERASE"')
    assert len(output) == 3818


def test_select_group_id_numeric_coercion(tctim_h5msm_molsys):
    """group_id with a numeric comparison triggers integer coercion of the id
    column (the _id_columns_with_numeric_comparisons + _column_has_integer_strings
    branch)."""
    molsys = tctim_h5msm_molsys
    # TcTIM group ids are stored as numeric strings; group_id < 5 → first 4
    # sequential groups across all chains → 24 atoms (groups 1-4 have 6 atoms
    # each in the PDB numbering that starts at 1).
    output = msm.select(molsys, 'group_id < 5')
    assert len(output) == 24
    assert output[:5] == [0, 1, 2, 3, 4]


def test_select_group_id_numeric_with_chain(tctim_h5msm_molsys):
    """Combination of a numeric group_id comparison with a chain filter."""
    molsys = tctim_h5msm_molsys
    output = msm.select(molsys, 'group_id >= 100 and chain_id=="A"')
    assert len(output) == 1170
    assert output[0] == 736


def test_select_group_index_range(tctim_h5msm_molsys):
    """group_index with >= and <= exercises both comparison operators together."""
    molsys = tctim_h5msm_molsys
    output = msm.select(molsys, 'group_index >= 10 and group_index <= 20')
    assert len(output) == 78
    assert output[0] == 77


def test_select_boolean_or_atom_index(tctim_h5msm_molsys):
    """Boolean OR on atom_index covers the or-branch in query evaluation."""
    molsys = tctim_h5msm_molsys
    output = msm.select(molsys, 'atom_index < 50 or atom_index > 3800')
    assert len(output) == 232
    assert output[0] == 0
    assert output[-1] == 3982


def test_select_empty_selection(tctim_h5msm_molsys):
    """A selection that matches no atoms should return an empty list."""
    molsys = tctim_h5msm_molsys
    output = msm.select(molsys, 'atom_name=="XXXX"')
    assert output == []


# ---------------------------------------------------------------------------
# select_in_elements_of branches
# ---------------------------------------------------------------------------

def test_select_in_groups_of_all(tctim_h5msm_molsys):
    """'in groups of all' hits the is_all(after) branch and returns per-group
    atom lists covering the whole system."""
    molsys = tctim_h5msm_molsys
    output = msm.select(molsys, 'atom_name=="CA" in groups of all')
    # Should return one list per group that contains a CA atom
    assert isinstance(output, list)
    assert len(output) == 497  # 497 groups with CA in TcTIM
    # Each sub-list has exactly one atom index
    assert all(isinstance(sub, list) and len(sub) == 1 for sub in output)


def test_select_in_groups_of_explicit(tctim_h5msm_molsys):
    """'atom_name=="N" in groups of group_index==[0,1,2]' uses the non-all
    before mask path."""
    molsys = tctim_h5msm_molsys
    output = msm.select(molsys, 'atom_name=="N" in groups of group_index==[0,1,2]')
    assert isinstance(output, list)
    # 3 groups, each containing exactly one N atom
    assert len(output) == 3
    flat = [x for sub in output for x in sub]
    assert flat == [0, 9, 16]


def test_select_in_groups_of_chain(tctim_h5msm_molsys):
    """'atom_name=="CA" in groups of chain_id=="A"' filters before mask."""
    molsys = tctim_h5msm_molsys
    output = msm.select(molsys, 'atom_name=="CA" in groups of chain_id=="A"')
    assert isinstance(output, list)
    assert len(output) == 248  # 248 residues in chain A


def test_select_in_molecules_of_chain(tctim_h5msm_molsys):
    """'in molecules of chain_id=="A"' hits the molecules level of
    select_in_elements_of."""
    molsys = tctim_h5msm_molsys
    output = msm.select(molsys, 'all in molecules of chain_id=="A"')
    assert isinstance(output, list)
    # TcTIM chain A → 1 protein molecule
    assert len(output) == 1
    assert len(output[0]) == 1906  # atoms in that protein molecule


def test_select_in_molecules_of_entity(tctim_h5msm_molsys):
    """'in molecules of entity_name=="water"' covers the entity-level merge
    inside select_in_elements_of."""
    molsys = tctim_h5msm_molsys
    output = msm.select(molsys, 'all in molecules of entity_name=="water"')
    assert isinstance(output, list)
    assert len(output) == 165  # 165 water molecules


def test_select_in_chains_of_molecule_type(tctim_h5msm_molsys):
    """'in chains of molecule_type=="protein"' exercises the chains-level path
    inside select_in_elements_of."""
    molsys = tctim_h5msm_molsys
    output = msm.select(molsys, 'all in chains of molecule_type=="protein"')
    assert isinstance(output, list)
    # TcTIM has 2 protein chains
    assert len(output) == 2
    assert len(output[0]) == 1906
    assert len(output[1]) == 1912


def test_select_in_entities_of_molecule_type(tctim_h5msm_molsys):
    """'in entities of molecule_type=="water"' exercises the entities-level path
    inside select_in_elements_of."""
    molsys = tctim_h5msm_molsys
    output = msm.select(molsys, 'all in entities of molecule_type=="water"')
    assert isinstance(output, list)
    # TcTIM has 1 water entity
    assert len(output) == 1
    total_atoms = sum(len(sub) for sub in output)
    assert total_atoms == 165


def test_select_nested_in_groups_of_molecules(tctim_h5msm_molsys):
    """'... in groups of molecule_type=="protein" in molecules of chain_id=="A"'
    exercises the nested two-level in_elements_of path where _in_elements_of
    is True for the 'after' clause."""
    molsys = tctim_h5msm_molsys
    output = msm.select(
        molsys,
        'all in groups of molecule_type=="protein" in molecules of chain_id=="A"',
    )
    assert isinstance(output, list)
    # The outer in-molecules-of-chain A selects 1 molecule; the inner
    # in-groups-of-protein selects groups within it.
    assert len(output) > 0


# ---------------------------------------------------------------------------
# Shortcut / syntax sugar paths
# ---------------------------------------------------------------------------

def test_select_all_mask_returns_subset(tctim_h5msm_molsys):
    """msm.select with selection='all' and a mask returns the mask as a list
    (regression for the is_all fast path)."""
    molsys = tctim_h5msm_molsys
    output = msm.select(molsys, selection='all', mask=[10, 20, 30])
    assert isinstance(output, list)
    assert output == [10, 20, 30]


def test_select_group_element_with_string_selection(tctim_h5msm_molsys):
    """Selecting at element='group' level with a string selection exercises
    the group-level output path."""
    molsys = tctim_h5msm_molsys
    output = msm.select(molsys, 'molecule_type=="water"', element='group')
    assert len(output) == 165
    assert output[0] == 497


def test_select_chain_element_with_string_selection(tctim_h5msm_molsys):
    """Selecting at element='chain' level with a string selection."""
    molsys = tctim_h5msm_molsys
    output = msm.select(molsys, 'molecule_type=="water"', element='chain')
    assert len(output) == 2
    true_output = np.array([2, 3])
    assert np.all(np.array(output) == true_output)


def test_select_molecule_element_with_string_selection(tctim_h5msm_molsys):
    """Selecting at element='molecule' level with a string selection."""
    molsys = tctim_h5msm_molsys
    output = msm.select(molsys, 'molecule_type=="water"', element='molecule')
    assert len(output) == 165
    assert output[0] == 2

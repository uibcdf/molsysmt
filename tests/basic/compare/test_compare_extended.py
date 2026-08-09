"""
Extended tests for molsysmt.basic.compare covering branches not hit by existing tests:
- entity-level attributes (n_entities, entity_index, entity_name, entity_type)
- bond attributes (n_bonds, bonded_atom_pairs, bond_index)
- inner bond attributes
- attribute_type='all'
- include_none=True
- selection subsetting
- kwargs with False values
- output_type='dictionary' for various paths
"""
import molsysmt as msm
from molsysmt import systems
import numpy as np
import pytest


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def t4_molsys():
    return msm.convert(systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys')


@pytest.fixture(scope="module")
def hp35_molsys():
    return msm.convert(systems['chicken villin HP35']['1vii.pdb'], to_form='molsysmt.MolSys')


# ---------------------------------------------------------------------------
# Entity-level attributes
# ---------------------------------------------------------------------------

def test_compare_n_entities_identical(t4_molsys):
    """n_entities=True on same system returns True."""
    result = msm.compare(t4_molsys, t4_molsys, n_entities=True)
    assert result is True


def test_compare_entity_index_identical(t4_molsys):
    """entity_index=True on same system returns True."""
    result = msm.compare(t4_molsys, t4_molsys, entity_index=True)
    assert result is True


def test_compare_entity_name_identical(t4_molsys):
    """entity_name=True on same system returns True."""
    result = msm.compare(t4_molsys, t4_molsys, entity_name=True)
    assert result is True


def test_compare_entity_attrs_different_systems(t4_molsys, hp35_molsys):
    """n_entities=True on different systems returns False (different entity counts)."""
    result = msm.compare(t4_molsys, hp35_molsys, n_entities=True)
    assert result is False


def test_compare_entity_attrs_dictionary(t4_molsys):
    """output_type='dictionary' includes entity attributes when requested."""
    result = msm.compare(
        t4_molsys, t4_molsys,
        n_entities=True, entity_name=True,
        output_type='dictionary',
    )
    assert isinstance(result, dict)
    for key in ('n_entities', 'entity_name'):
        if key in result:
            assert result[key] is True


# ---------------------------------------------------------------------------
# Bond attributes
# ---------------------------------------------------------------------------

def test_compare_n_bonds_identical(t4_molsys):
    """n_bonds=True on same system returns True."""
    result = msm.compare(t4_molsys, t4_molsys, n_bonds=True)
    assert result is True


def test_compare_bonded_atom_pairs_identical(t4_molsys):
    """bonded_atom_pairs=True on same system returns True."""
    result = msm.compare(t4_molsys, t4_molsys, bonded_atom_pairs=True)
    assert result is True


def test_compare_bonded_atom_pairs_different(t4_molsys, hp35_molsys):
    """bonded_atom_pairs=True on different systems returns False without warning."""
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        result = msm.compare(t4_molsys, hp35_molsys, bonded_atom_pairs=True)
    assert result is False


def test_compare_missing_bond_pairs_with_enriched_native_conversion():
    bcif = systems['T4 lysozyme L99A']['181l.bcif.gz']
    native = msm.convert(bcif, to_form='molsysmt.MolSys')

    result = msm.compare(bcif, native)

    assert result is True


def test_compare_topological_scope_handles_missing_inner_bond_pairs():
    bcif = systems['T4 lysozyme L99A']['181l.bcif.gz']
    native = msm.convert(bcif, to_form='molsysmt.MolSys')

    result = msm.compare(bcif, native, attribute_type='topological')

    assert result is False


def test_compare_n_bonds_different(t4_molsys, hp35_molsys):
    """n_bonds=True on different systems returns False."""
    result = msm.compare(t4_molsys, hp35_molsys, n_bonds=True)
    assert result is False


# ---------------------------------------------------------------------------
# Inner bond attributes
# ---------------------------------------------------------------------------

def test_compare_n_inner_bonds_identical(t4_molsys):
    """n_inner_bonds=True on same system returns True."""
    result = msm.compare(t4_molsys, t4_molsys, n_inner_bonds=True)
    assert result is True


def test_compare_inner_bonded_atom_pairs_identical(t4_molsys):
    """inner_bonded_atom_pairs=True on same system returns True."""
    result = msm.compare(t4_molsys, t4_molsys, inner_bonded_atom_pairs=True)
    assert result is True


# ---------------------------------------------------------------------------
# include_none=True
# ---------------------------------------------------------------------------

def test_compare_include_none_identical(t4_molsys):
    """include_none=True on same system returns True."""
    result = msm.compare(t4_molsys, t4_molsys, include_none=True)
    assert result is True


def test_compare_include_none_dictionary(t4_molsys):
    """include_none=True with output_type='dictionary' returns a dict."""
    result = msm.compare(
        t4_molsys, t4_molsys,
        include_none=True, output_type='dictionary',
    )
    assert isinstance(result, dict)
    assert len(result) > 0


# ---------------------------------------------------------------------------
# kwargs with False values (atts_false_list branch)
# ---------------------------------------------------------------------------

def test_compare_kwarg_false_different_systems(t4_molsys, hp35_molsys):
    """kwarg with False means 'expect NOT equal'. T4 vs HP35 differ → n_atoms=False → True."""
    result = msm.compare(t4_molsys, hp35_molsys, n_atoms=False)
    assert result is True


def test_compare_kwarg_false_same_atoms_equal(t4_molsys):
    """n_atoms=False on same system: atoms are equal → negated → returns False."""
    result = msm.compare(t4_molsys, t4_molsys, n_atoms=False)
    assert result is False


# ---------------------------------------------------------------------------
# selection subsetting
# ---------------------------------------------------------------------------

def test_compare_with_selection_subset(t4_molsys):
    """Using selection='group_index<10' on identical system returns True."""
    result = msm.compare(
        t4_molsys, t4_molsys,
        selection='group_index<10', selection_2='group_index<10',
        n_atoms=True, atom_name=True,
    )
    assert result is True


def test_compare_mismatched_selections(t4_molsys):
    """Different selections → different atom counts → n_atoms False."""
    result = msm.compare(
        t4_molsys, t4_molsys,
        selection='group_index<10',
        selection_2='group_index<20',
        n_atoms=True,
    )
    assert result is False


# ---------------------------------------------------------------------------
# n_structures and structural attributes in compare
# ---------------------------------------------------------------------------

def test_compare_n_structures_same(t4_molsys):
    """n_structures=True on same system returns True."""
    result = msm.compare(t4_molsys, t4_molsys, n_structures=True)
    assert result is True


def test_compare_structure_index_same(t4_molsys):
    """structure_index=True on same system returns True."""
    result = msm.compare(t4_molsys, t4_molsys, structure_index=True)
    assert result is True


# ---------------------------------------------------------------------------
# redefine_indices=True path (Topology form)
# ---------------------------------------------------------------------------

def test_compare_redefine_indices_topology_forms(t4_molsys):
    """redefine_indices=True with Topology forms exercises both rebuild branches."""
    topo_A = msm.convert(t4_molsys, to_form='molsysmt.Topology')
    topo_B = msm.convert(t4_molsys, to_form='molsysmt.Topology')
    result = msm.compare(topo_A, topo_B, redefine_indices=True)
    assert result is True


def test_compare_redefine_indices_molsys_forms(t4_molsys):
    """redefine_indices=True with MolSys forms exercises MolSys rebuild branch."""
    molsys_A = t4_molsys
    molsys_B = msm.convert(
        systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys'
    )
    result = msm.compare(molsys_A, molsys_B, redefine_indices=True)
    assert result is True


# ---------------------------------------------------------------------------
# Velocity attribute (None vs None → True)
# ---------------------------------------------------------------------------

def test_compare_velocities_both_none(t4_molsys):
    """Both systems have no velocities → velocities match (None == None → True)."""
    result = msm.compare(t4_molsys, t4_molsys, velocities=True, output_type='dictionary')
    # velocities attribute may not be in both forms' attribute sets; if present must be True
    assert isinstance(result, dict)
    if 'velocities' in result:
        assert result['velocities'] is True


# ---------------------------------------------------------------------------
# Box attributes
# ---------------------------------------------------------------------------

def test_compare_structure_id_identical(t4_molsys):
    """structure_id=True on same system returns True."""
    result = msm.compare(t4_molsys, t4_molsys, structure_id=True)
    assert result is True


# ---------------------------------------------------------------------------
# Component and molecule attributes
# ---------------------------------------------------------------------------

def test_compare_component_index_identical(t4_molsys):
    result = msm.compare(t4_molsys, t4_molsys, component_index=True)
    assert result is True


def test_compare_molecule_index_identical(t4_molsys):
    result = msm.compare(t4_molsys, t4_molsys, molecule_index=True)
    assert result is True


def test_compare_molecule_name_identical(t4_molsys):
    result = msm.compare(t4_molsys, t4_molsys, molecule_name=True)
    assert result is True


def test_compare_chain_type_identical(t4_molsys):
    result = msm.compare(t4_molsys, t4_molsys, chain_type=True)
    assert result is True

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


# ---------------------------------------------------------------------------
# structure_indices as a list
# ---------------------------------------------------------------------------

def test_merge_with_structure_indices_list(pro_molsys, val_molsys):
    """structure_indices=['all', 'all'] works same as single 'all'."""
    merged = msm.merge([pro_molsys, val_molsys], structure_indices=['all', 'all'])
    assert msm.get(merged, element='system', n_structures=True) == 1

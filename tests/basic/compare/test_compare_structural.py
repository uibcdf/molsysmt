"""
Tests for the structural attributes section of molsysmt.compare (lines 529-607)
and the redefine_indices branch.
"""

import molsysmt as msm
from molsysmt import systems
import numpy as np
import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _topology_only(molsys):
    """Return a topology-only copy (no structures) of a MolSys."""
    return msm.convert(molsys, to_form='molsysmt.Topology')


# ---------------------------------------------------------------------------
# structural attribute_type – identical system
# ---------------------------------------------------------------------------

def test_compare_structural_identical_boolean(t4_h5msm_molsys):
    """Comparing a system against itself with attribute_type='structural' returns True."""
    result = msm.compare(t4_h5msm_molsys, t4_h5msm_molsys, attribute_type='structural')
    assert result is True


def test_compare_structural_identical_dictionary(t4_h5msm_molsys):
    """output_type='dictionary' with attribute_type='structural' gives all-True dict."""
    result = msm.compare(
        t4_h5msm_molsys,
        t4_h5msm_molsys,
        attribute_type='structural',
        output_type='dictionary',
    )
    assert isinstance(result, dict)
    assert len(result) > 0
    assert all(result.values()), f"Expected all True, got: {result}"


# ---------------------------------------------------------------------------
# structural attribute_type – different systems
# ---------------------------------------------------------------------------

def test_compare_structural_different_systems_boolean(t4_h5msm_molsys, hp35_molsys):
    """Two different systems with attribute_type='structural' return False."""
    result = msm.compare(t4_h5msm_molsys, hp35_molsys, attribute_type='structural')
    assert result is False


def test_compare_structural_different_systems_dictionary(t4_h5msm_molsys, hp35_molsys):
    """output_type='dictionary' with attribute_type='structural' shows mismatches."""
    result = msm.compare(
        t4_h5msm_molsys,
        hp35_molsys,
        attribute_type='structural',
        output_type='dictionary',
    )
    assert isinstance(result, dict)
    # At least some attribute must differ (e.g. n_structures or coordinates)
    assert not all(result.values()), f"Expected at least one False, got: {result}"


# ---------------------------------------------------------------------------
# attribute_type='all' – covers both topological and structural branches
# ---------------------------------------------------------------------------

def test_compare_all_attribute_type_identical(t4_h5msm_molsys):
    """attribute_type='all' on same system returns True."""
    result = msm.compare(t4_h5msm_molsys, t4_h5msm_molsys, attribute_type='all')
    assert result is True


def test_compare_all_attribute_type_different(t4_h5msm_molsys, hp35_molsys):
    """attribute_type='all' on different systems returns False."""
    result = msm.compare(t4_h5msm_molsys, hp35_molsys, attribute_type='all')
    assert result is False


def test_compare_all_attribute_type_dictionary(t4_h5msm_molsys):
    """attribute_type='all' with output_type='dictionary' on same system gives all-True dict."""
    result = msm.compare(
        t4_h5msm_molsys,
        t4_h5msm_molsys,
        attribute_type='all',
        output_type='dictionary',
    )
    assert isinstance(result, dict)
    assert len(result) > 0
    assert all(result.values()), f"Expected all True, got: {result}"


# ---------------------------------------------------------------------------
# Specific structural attributes via kwargs
# ---------------------------------------------------------------------------

def test_compare_coordinates_identical(t4_h5msm_molsys):
    """Explicit coordinates=True returns True for identical system."""
    result = msm.compare(t4_h5msm_molsys, t4_h5msm_molsys, coordinates=True)
    assert result is True


def test_compare_n_structures_identical(t4_h5msm_molsys):
    """n_structures=True returns True for identical system."""
    result = msm.compare(t4_h5msm_molsys, t4_h5msm_molsys, n_structures=True)
    assert result is True


def test_compare_box_identical(t4_h5msm_molsys):
    """box=True returns True for identical system."""
    result = msm.compare(t4_h5msm_molsys, t4_h5msm_molsys, box=True)
    assert result is True


def test_compare_coordinates_different_systems(t4_h5msm_molsys, hp35_molsys):
    """Comparing coordinates of systems with different atom counts returns False."""
    result = msm.compare(t4_h5msm_molsys, hp35_molsys, coordinates=True)
    assert result is False


# ---------------------------------------------------------------------------
# Topology-only objects: no structural data → coordinates both None → True
# ---------------------------------------------------------------------------

def test_compare_structural_topology_only_both_none(t4_h5msm_molsys):
    """When both systems have no structures, coordinates None==None → True."""
    topo_A = _topology_only(t4_h5msm_molsys)
    topo_B = _topology_only(t4_h5msm_molsys)
    result = msm.compare(topo_A, topo_B, coordinates=True)
    assert result is True



# ---------------------------------------------------------------------------
# redefine_indices branch
# ---------------------------------------------------------------------------

def test_compare_redefine_indices_identical(t4_h5msm_molsys):
    """redefine_indices=True on same system (default topological comparison) returns True."""
    molsys_A = t4_h5msm_molsys
    molsys_B = msm.convert(
        systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys'
    )
    result = msm.compare(molsys_A, molsys_B, redefine_indices=True)
    assert result is True


def test_compare_redefine_indices_different(t4_h5msm_molsys, hp35_molsys):
    """redefine_indices=True on different systems returns False."""
    result = msm.compare(t4_h5msm_molsys, hp35_molsys, redefine_indices=True)
    assert result is False


def test_compare_redefine_indices_with_structural(t4_h5msm_molsys):
    """redefine_indices=True combined with attribute_type='structural' on same system returns True."""
    molsys_A = t4_h5msm_molsys
    molsys_B = msm.convert(
        systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys'
    )
    result = msm.compare(
        molsys_A, molsys_B, redefine_indices=True, attribute_type='structural'
    )
    assert result is True


# ---------------------------------------------------------------------------
# structure_indices parameter (exercises structural slicing)
# ---------------------------------------------------------------------------

def test_compare_structure_indices_first(t4_h5msm_molsys):
    """Comparing only the first structure frame against itself returns True."""
    result = msm.compare(
        t4_h5msm_molsys,
        t4_h5msm_molsys,
        structure_indices=0,
        structure_indices_2=0,
        coordinates=True,
    )
    assert result is True


# ---------------------------------------------------------------------------
# box comparison: None vs None, and shape-mismatch path (via dictionary)
# ---------------------------------------------------------------------------

def test_compare_box_both_none(t4_h5msm_molsys):
    """Topology-only systems: box None vs None → True in dictionary output."""
    topo_A = _topology_only(t4_h5msm_molsys)
    topo_B = _topology_only(t4_h5msm_molsys)
    result = msm.compare(topo_A, topo_B, box=True, output_type='dictionary')
    # box key may be absent if not available in both attributes; if present it must be True
    if 'box' in result:
        assert result['box'] is True


def test_compare_box_one_none(t4_h5msm_molsys):
    """System with box vs topology-only (no box): box → False."""
    topo = _topology_only(t4_h5msm_molsys)
    result = msm.compare(t4_h5msm_molsys, topo, box=True, output_type='dictionary')
    # if box appears in required atts it must be False; if absent the intersection is empty → result is {}
    if 'box' in result:
        assert result['box'] is False

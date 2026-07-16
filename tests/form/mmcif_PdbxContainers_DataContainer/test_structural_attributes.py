"""
Structural attribute tests for mmcif.PdbxContainers.DataContainer form.

Covers get_structural_attributes functions that were previously broken
due to object attributes not provided by a DataContainer (item.x_coord_list, item.num_models,
item.unit_cell, item.bio_assembly).

Oracle: HP35 (1vii) — single-model X-ray structure with unit cell.
"""

import pytest
import numpy as np
import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.form.mmcif_PdbxContainers_DataContainer import get_structural_attributes as gsa


N_ATOMS = 596


@pytest.fixture(scope='function')
def data_container(hp35_bcif_gz_file):
    return msm.convert(str(hp35_bcif_gz_file), to_form='mmcif.PdbxContainers.DataContainer')


# ---------------------------------------------------------------------------
# get_n_structures_from_system
# ---------------------------------------------------------------------------

def test_n_structures_is_one(data_container):
    """HP35 (1vii) is a single X-ray model → 1 structure."""
    n = gsa.get_n_structures_from_system(data_container, skip_digestion=True)
    assert n == 1


def test_n_structures_explicit_indices(data_container):
    """Explicit structure_indices list → len of that list."""
    n = gsa.get_n_structures_from_system(data_container, structure_indices=[0], skip_digestion=True)
    assert n == 1


# ---------------------------------------------------------------------------
# get_coordinates_from_atom
# ---------------------------------------------------------------------------

def test_coordinates_shape(data_container):
    """Coordinates for all atoms → (1, N_ATOMS, 3) pint quantity."""
    xyz = gsa.get_coordinates_from_atom(data_container, skip_digestion=True)
    val = puw.get_value(xyz)
    assert val.shape == (1, N_ATOMS, 3)


def test_coordinates_subset(data_container):
    """Coordinates for first 10 atoms → (1, 10, 3)."""
    xyz = gsa.get_coordinates_from_atom(data_container, indices=list(range(10)), skip_digestion=True)
    val = puw.get_value(xyz)
    assert val.shape == (1, 10, 3)


def test_coordinates_unit_is_nm(data_container):
    """Coordinates are standardized to nm."""
    xyz = gsa.get_coordinates_from_atom(data_container, skip_digestion=True)
    unit_str = str(puw.get_unit(xyz))
    assert 'nm' in unit_str or 'nanometer' in unit_str


# ---------------------------------------------------------------------------
# get_box_from_system
# ---------------------------------------------------------------------------

def test_box_returns_without_error(data_container):
    """get_box_from_system runs without error (HP35/1vii is NMR → None)."""
    box = gsa.get_box_from_system(data_container, skip_digestion=True)
    # 1vii is NMR — no crystallographic unit cell, so box is None
    assert box is None


# ---------------------------------------------------------------------------
# get_n_bioassemblies_from_system
# ---------------------------------------------------------------------------

def test_n_bioassemblies_positive(data_container):
    """HP35 has at least one biological assembly."""
    n = gsa.get_n_bioassemblies_from_system(data_container, skip_digestion=True)
    assert n >= 1


# ---------------------------------------------------------------------------
# get_bioassembly_from_system
# ---------------------------------------------------------------------------

def test_bioassembly_is_dict(data_container):
    """Bioassembly is returned as a dict."""
    ba = gsa.get_bioassembly_from_system(data_container, skip_digestion=True)
    assert isinstance(ba, dict)


def test_bioassembly_keys(data_container):
    """Each bioassembly entry has chain_indices, rotations, translations keys."""
    ba = gsa.get_bioassembly_from_system(data_container, skip_digestion=True)
    for val in ba.values():
        assert 'chain_indices' in val
        assert 'rotations' in val
        assert 'translations' in val


# ---------------------------------------------------------------------------
# get_time_from_system / get_structure_id_from_system
# ---------------------------------------------------------------------------

def test_time_is_none(data_container):
    t = gsa.get_time_from_system(data_container, skip_digestion=True)
    assert t is None


def test_structure_id_is_none(data_container):
    sid = gsa.get_structure_id_from_system(data_container, skip_digestion=True)
    assert sid is None

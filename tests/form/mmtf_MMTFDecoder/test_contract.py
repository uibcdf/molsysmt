"""
Contract and structural-attribute tests for mmtf.MMTFDecoder form.

Oracle: 1l2y.mmtf (Trp-cage NMR, 304 atoms / model, 20 residues, 1 chain,
38 NMR models).  File lives in molsysmt/data/mmtf/.

Covers:
- get_coordinates_from_atom  (item.x_coord_list / y / z + num_atoms)
- get_n_structures_from_system  (item.num_models)
- get_box_from_system  (NMR → unit_cell is None → None)
- get_n_bioassemblies_from_system  (item.bio_assembly)
- get_bioassembly_from_system  (item.bio_assembly)
- topology round-trip via molsysmt.Topology conversion
"""

import pytest
from pathlib import Path
import numpy as np
import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.form.mmtf_MMTFDecoder import get_structural_attributes as gsa


MMTF_PATH  = str(Path(msm.__file__).parent / 'data' / 'mmtf' / '1l2y.mmtf')
N_ATOMS         = 304
N_GROUPS        = 20
N_CHAINS        = 1
N_MODELS        = 38   # NMR ensemble
N_ATOMS_TOTAL   = N_ATOMS * N_MODELS  # 11552 — how MMTF stores all models flat


@pytest.fixture(scope='module')
def decoder():
    """Raw MMTFDecoder object."""
    import mmtf
    return mmtf.parse(MMTF_PATH)


@pytest.fixture(scope='module')
def mmtf_topology():
    return msm.convert(MMTF_PATH, to_form='molsysmt.Topology')


# ---------------------------------------------------------------------------
# Contract: MMTFDecoder can be created
# ---------------------------------------------------------------------------

def test_file_exists():
    import os
    assert os.path.isfile(MMTF_PATH)


def test_decoder_type(decoder):
    import mmtf
    assert isinstance(decoder, mmtf.MMTFDecoder)


# ---------------------------------------------------------------------------
# get_n_structures_from_system
# ---------------------------------------------------------------------------

def test_n_structures_all(decoder):
    """1l2y has 38 NMR models."""
    n = gsa.get_n_structures_from_system(decoder, skip_digestion=True)
    assert n == N_MODELS


def test_n_structures_explicit_indices(decoder):
    n = gsa.get_n_structures_from_system(decoder, structure_indices=[0, 1, 2], skip_digestion=True)
    assert n == 3


# ---------------------------------------------------------------------------
# get_coordinates_from_atom
# ---------------------------------------------------------------------------

def test_coordinates_shape_all(decoder):
    """Coordinates are returned as a pint quantity with correct total atom count.

    Note: the current MMTF implementation stores all NMR models in a flat
    coordinate list (num_atoms = 11552 = 38 × 304).  The reshape uses
    item.num_atoms so the output shape is (1, N_ATOMS_TOTAL, 3).
    """
    xyz = gsa.get_coordinates_from_atom(decoder, skip_digestion=True)
    val = puw.get_value(xyz)
    assert val.ndim == 3
    assert val.shape[2] == 3
    assert val.size == N_ATOMS_TOTAL * 3


def test_coordinates_subset_structures(decoder):
    """structure_indices=[0] → first pseudo-frame."""
    xyz = gsa.get_coordinates_from_atom(decoder, structure_indices=[0], skip_digestion=True)
    val = puw.get_value(xyz)
    assert val.ndim == 3
    assert val.shape[0] == 1


def test_coordinates_unit_is_nm(decoder):
    """Coordinates are standardized to nm."""
    xyz = gsa.get_coordinates_from_atom(decoder, indices=[0], skip_digestion=True)
    unit_str = str(puw.get_unit(xyz))
    assert 'nm' in unit_str or 'nanometer' in unit_str


# ---------------------------------------------------------------------------
# get_box_from_system  (NMR → no unit cell)
# ---------------------------------------------------------------------------

def test_box_is_none_for_nmr(decoder):
    """NMR structures have no unit cell → box is None."""
    box = gsa.get_box_from_system(decoder, skip_digestion=True)
    assert box is None


# ---------------------------------------------------------------------------
# get_n_bioassemblies_from_system
# ---------------------------------------------------------------------------

def test_n_bioassemblies(decoder):
    """bio_assembly list exists — 1l2y has at least one assembly."""
    n = gsa.get_n_bioassemblies_from_system(decoder, skip_digestion=True)
    assert n >= 1


# ---------------------------------------------------------------------------
# get_bioassembly_from_system
# ---------------------------------------------------------------------------

def test_bioassembly_is_dict(decoder):
    ba = gsa.get_bioassembly_from_system(decoder, skip_digestion=True)
    assert isinstance(ba, dict)


def test_bioassembly_has_required_keys(decoder):
    ba = gsa.get_bioassembly_from_system(decoder, skip_digestion=True)
    for val in ba.values():
        assert 'chain_indices' in val
        assert 'rotations' in val
        assert 'translations' in val


# ---------------------------------------------------------------------------
# Topology round-trip
# ---------------------------------------------------------------------------

def test_topology_atom_count(mmtf_topology):
    assert mmtf_topology.n_atoms == N_ATOMS


def test_topology_group_count(mmtf_topology):
    assert mmtf_topology.n_groups == N_GROUPS


def test_topology_chain_count(mmtf_topology):
    assert mmtf_topology.n_chains == N_CHAINS

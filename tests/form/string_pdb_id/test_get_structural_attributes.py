"""
Tests for string_pdb_id/get_structural_attributes.py.

All getters delegate to molsysmt_MolSys after downloading the structure from
RCSB — the individual attribute paths are covered by the molsysmt_MolSys suite.
This file contains only a smoke test that validates the full download +
conversion + structural getter pipeline.

Oracle: 1AKI (chicken egg-white lysozyme), 1 structure, 1079 heavy atoms.
"""

import pytest
from molsysmt.form.string_pdb_id import get_structural_attributes as aux

N_ATOMS = 1079


@pytest.mark.network
def test_download_and_coordinates():
    """Download 1aki from RCSB and verify coordinates shape through the full pipeline."""
    coords = aux.get_coordinates_from_atom('pdb_id:1aki')
    assert coords is not None
    assert coords.shape == (1, N_ATOMS, 3)

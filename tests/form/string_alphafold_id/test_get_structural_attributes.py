"""
Tests for string_alphafold_id/get_structural_attributes.py.

All getters delegate to molsysmt_MolSys after downloading the structure from
AlphaFold DB — the individual attribute paths are covered by the
molsysmt_MolSys suite.  This file contains only a smoke test that validates
the full download + conversion + structural getter pipeline.

Oracle: AF-P62258-F1 (human 14-3-3 protein epsilon, YWHAE), 1 structure,
255 residues.
"""

import pytest
from molsysmt.form.string_alphafold_id import get_structural_attributes as aux


@pytest.mark.network
@pytest.mark.xdist_group("network")
def test_download_and_coordinates():
    """Download AF-P62258-F1 from AlphaFold DB and verify coordinates through the full pipeline."""
    coords = aux.get_coordinates_from_atom('alphafold_id:AF-P62258-F1')
    assert coords is not None
    assert coords.ndim == 3
    assert coords.shape[0] == 1  # 1 structure (predicted model)
    assert coords.shape[2] == 3  # x, y, z

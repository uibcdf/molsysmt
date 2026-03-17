"""
Tests for string_alphafold_id/get_topological_attributes.py.

The string_alphafold_id getters always download from AlphaFold DB before
delegating to molsysmt_Topology.  There is no way to exercise them locally
without a real network call, so this file contains only a
@pytest.mark.network smoke test that validates the full download + conversion
+ getter pipeline.

Oracle: AF-P62258-F1 (human 14-3-3 protein epsilon, YWHAE), 255 residues.
"""

import pytest
from molsysmt.form.string_alphafold_id import get_topological_attributes as aux

N_GROUPS = 255


@pytest.mark.network
def test_download_and_basic_count():
    """Download AF-P62258-F1 from AlphaFold DB and verify group count."""
    n = aux.get_n_groups_from_system('alphafold_id:AF-P62258-F1')
    assert n == N_GROUPS

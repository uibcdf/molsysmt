"""
Tests for string_pdb_id/get_topological_attributes.py.

The string_pdb_id getters always download from RCSB before delegating to
molsysmt_Topology.  There is no way to exercise them locally without a real
network call, so this file contains only a @pytest.mark.network smoke test
that validates the full download + conversion + getter pipeline.

Oracle: 1AKI (chicken egg-white lysozyme), 129 residues, 1079 heavy atoms.
Note: 1L2Y (Trp-cage) has a known IndexError in infer_molecule_types_from_topology
for the RCSB BCIF download path — tracked separately.
"""

import pytest
from molsysmt.form.string_pdb_id import get_topological_attributes as aux

N_ATOMS = 1079


@pytest.mark.network
@pytest.mark.xdist_group("network")
def test_download_and_basic_count():
    """Download 1aki from RCSB and verify atom count through the full pipeline."""
    n = aux.get_n_atoms_from_system('pdb_id:1aki')
    assert n == N_ATOMS

"""
Parity tests for string:pdb_id form.

Parity oracle: chicken villin HP35 (PDB 1vii) is available both as a
network retrieval target (string:pdb_id) and as a locally cached bcif.gz
fixture (hp35_bcif_gz_file).  Parity means that both paths produce the same
topology when converted to molsysmt.Topology.

All tests require network access and are marked @pytest.mark.network.
"""

import pytest
import molsysmt as msm

PDB_ID = 'pdb_id:1vii'
N_ATOMS  = 596
N_GROUPS = 36
N_CHAINS = 1


@pytest.fixture()
def pdb_id_topology():
    return msm.convert(PDB_ID, to_form='molsysmt.Topology')


@pytest.fixture()
def local_topology(hp35_bcif_gz_file):
    return msm.convert(str(hp35_bcif_gz_file), to_form='molsysmt.Topology')


# ---------------------------------------------------------------------------
# Parity: pdb_id download ↔ local bcif.gz
# ---------------------------------------------------------------------------

@pytest.mark.network
@pytest.mark.xdist_group("network")
def test_parity_atom_count_matches_local(pdb_id_topology, local_topology):
    assert pdb_id_topology.n_atoms == local_topology.n_atoms


@pytest.mark.network
@pytest.mark.xdist_group("network")
def test_parity_group_count_matches_local(pdb_id_topology, local_topology):
    assert pdb_id_topology.n_groups == local_topology.n_groups


@pytest.mark.network
@pytest.mark.xdist_group("network")
def test_parity_chain_count_matches_local(pdb_id_topology, local_topology):
    assert pdb_id_topology.n_chains == local_topology.n_chains


@pytest.mark.network
@pytest.mark.xdist_group("network")
def test_parity_atom_names_match_local(pdb_id_topology, local_topology):
    assert pdb_id_topology.atoms['atom_name'].tolist() == local_topology.atoms['atom_name'].tolist()


@pytest.mark.network
@pytest.mark.xdist_group("network")
def test_parity_group_names_match_local(pdb_id_topology, local_topology):
    assert pdb_id_topology.groups['group_name'].tolist() == local_topology.groups['group_name'].tolist()

"""
Parity tests for string:alphafold_id form.

Parity oracle: download AF-P62258-F1 (human 14-3-3 epsilon, YWHAE, 255 aa),
convert to a temporary h5msm file, reload it, and verify the topology is
identical.  This tests that the AlphaFold download path produces a consistent,
losslessly round-trippable topology.

All tests require network access and are marked @pytest.mark.network.
"""

import pytest
import molsysmt as msm

ALPHAFOLD_ID = 'alphafold_id:AF-P62258-F1'
N_GROUPS = 255


@pytest.fixture()
def af_topology():
    return msm.convert(ALPHAFOLD_ID, to_form='molsysmt.Topology')


@pytest.fixture()
def af_roundtrip_topology(af_topology, tmp_path):
    h5_path = str(tmp_path / 'af_roundtrip.h5msm')
    msm.convert(af_topology, to_form='file:h5msm', output_filename=h5_path)
    return msm.convert(h5_path, to_form='molsysmt.Topology')


# ---------------------------------------------------------------------------
# Parity: alphafold_id download → h5msm → Topology round-trip
# ---------------------------------------------------------------------------

@pytest.mark.network
@pytest.mark.xdist_group("network")
def test_parity_group_count_roundtrip(af_topology, af_roundtrip_topology):
    assert af_topology.n_groups == af_roundtrip_topology.n_groups


@pytest.mark.network
@pytest.mark.xdist_group("network")
def test_parity_atom_count_roundtrip(af_topology, af_roundtrip_topology):
    assert af_topology.n_atoms == af_roundtrip_topology.n_atoms


@pytest.mark.network
@pytest.mark.xdist_group("network")
def test_parity_chain_count_roundtrip(af_topology, af_roundtrip_topology):
    assert af_topology.n_chains == af_roundtrip_topology.n_chains


@pytest.mark.network
@pytest.mark.xdist_group("network")
def test_parity_group_names_roundtrip(af_topology, af_roundtrip_topology):
    assert af_topology.groups['group_name'].tolist() == af_roundtrip_topology.groups['group_name'].tolist()


@pytest.mark.network
@pytest.mark.xdist_group("network")
def test_parity_atom_names_roundtrip(af_topology, af_roundtrip_topology):
    assert af_topology.atoms['atom_name'].tolist() == af_roundtrip_topology.atoms['atom_name'].tolist()

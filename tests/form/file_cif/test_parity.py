"""
Parity tests for file:cif form.

Oracle: HP35 (1vii) is available as file:bcif_gz (reference) and as
file:cif (derived by writing the mmcif.DataContainer to a text CIF file).
Parity means that both encodings produce identical topology when converted
to molsysmt.Topology.
"""

import pytest
import molsysmt as msm


@pytest.fixture()
def cif_topology(hp35_cif_file):
    return msm.convert(hp35_cif_file, to_form='molsysmt.Topology')


@pytest.fixture()
def bcif_gz_topology(hp35_bcif_gz_file):
    return msm.convert(str(hp35_bcif_gz_file), to_form='molsysmt.Topology')


# ---------------------------------------------------------------------------
# Parity: file:cif ↔ file:bcif_gz (text CIF vs compressed binary CIF)
# ---------------------------------------------------------------------------

def test_parity_atom_count(cif_topology, bcif_gz_topology):
    assert cif_topology.n_atoms == bcif_gz_topology.n_atoms


def test_parity_group_count(cif_topology, bcif_gz_topology):
    assert cif_topology.n_groups == bcif_gz_topology.n_groups


def test_parity_chain_count(cif_topology, bcif_gz_topology):
    assert cif_topology.n_chains == bcif_gz_topology.n_chains


def test_parity_atom_names(cif_topology, bcif_gz_topology):
    assert cif_topology.atoms['atom_name'].tolist() == bcif_gz_topology.atoms['atom_name'].tolist()


def test_parity_group_names(cif_topology, bcif_gz_topology):
    assert cif_topology.groups['group_name'].tolist() == bcif_gz_topology.groups['group_name'].tolist()

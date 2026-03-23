"""
Parity tests for file:cif.gz form.

Oracle: HP35 (1vii) is available as file:bcif_gz (reference) and as
file:cif.gz (derived by gzip-compressing the text CIF).  Parity means
that both encodings produce identical topology when converted to
molsysmt.Topology.
"""

import pytest
import molsysmt as msm


@pytest.fixture()
def cif_gz_topology(hp35_cif_gz_file):
    return msm.convert(hp35_cif_gz_file, to_form='molsysmt.Topology')


@pytest.fixture()
def bcif_gz_topology(hp35_bcif_gz_file):
    return msm.convert(str(hp35_bcif_gz_file), to_form='molsysmt.Topology')


# ---------------------------------------------------------------------------
# Parity: file:cif.gz ↔ file:bcif_gz (compressed text CIF vs binary CIF)
# ---------------------------------------------------------------------------

def test_parity_atom_count(cif_gz_topology, bcif_gz_topology):
    assert cif_gz_topology.n_atoms == bcif_gz_topology.n_atoms


def test_parity_group_count(cif_gz_topology, bcif_gz_topology):
    assert cif_gz_topology.n_groups == bcif_gz_topology.n_groups


def test_parity_chain_count(cif_gz_topology, bcif_gz_topology):
    assert cif_gz_topology.n_chains == bcif_gz_topology.n_chains


def test_parity_atom_names(cif_gz_topology, bcif_gz_topology):
    assert cif_gz_topology.atoms['atom_name'].tolist() == bcif_gz_topology.atoms['atom_name'].tolist()


def test_parity_group_names(cif_gz_topology, bcif_gz_topology):
    assert cif_gz_topology.groups['group_name'].tolist() == bcif_gz_topology.groups['group_name'].tolist()

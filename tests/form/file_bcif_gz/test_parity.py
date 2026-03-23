"""
Parity tests for file:bcif_gz form.

Oracle: HP35 (1vii) is available as both file:bcif and file:bcif_gz.
Both encodings carry identical content; parity means identical topology
(atom count, group count, chain count, atom names, group names).
"""

import pytest
import molsysmt as msm


@pytest.fixture()
def bcif_topology(hp35_bcif_file):
    return msm.convert(str(hp35_bcif_file), to_form='molsysmt.Topology')


@pytest.fixture()
def bcif_gz_topology(hp35_bcif_gz_file):
    return msm.convert(str(hp35_bcif_gz_file), to_form='molsysmt.Topology')


# ---------------------------------------------------------------------------
# Parity: file:bcif_gz ↔ file:bcif (same structure, different compression)
# ---------------------------------------------------------------------------

def test_parity_atom_count(bcif_gz_topology, bcif_topology):
    assert bcif_gz_topology.n_atoms == bcif_topology.n_atoms


def test_parity_group_count(bcif_gz_topology, bcif_topology):
    assert bcif_gz_topology.n_groups == bcif_topology.n_groups


def test_parity_chain_count(bcif_gz_topology, bcif_topology):
    assert bcif_gz_topology.n_chains == bcif_topology.n_chains


def test_parity_atom_names(bcif_gz_topology, bcif_topology):
    assert bcif_gz_topology.atoms['atom_name'].tolist() == bcif_topology.atoms['atom_name'].tolist()


def test_parity_group_names(bcif_gz_topology, bcif_topology):
    assert bcif_gz_topology.groups['group_name'].tolist() == bcif_topology.groups['group_name'].tolist()

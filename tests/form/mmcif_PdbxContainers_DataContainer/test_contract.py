"""
Contract tests for mmcif.PdbxContainers.DataContainer form.

Oracle: HP35 (1vii) via file:bcif_gz → mmcif.DataContainer.
Contract means that the DataContainer can be created from a bcif file
and that converting it to molsysmt.Topology gives the expected counts.

Parity is verified against the file:bcif_gz source (same structure).
"""

import pytest
import molsysmt as msm


N_ATOMS  = 596
N_GROUPS = 36
N_CHAINS = 1


@pytest.fixture()
def data_container(hp35_bcif_gz_file):
    return msm.convert(str(hp35_bcif_gz_file), to_form='mmcif.PdbxContainers.DataContainer')


@pytest.fixture()
def container_topology(data_container):
    return msm.convert(data_container, to_form='molsysmt.Topology')


@pytest.fixture()
def reference_topology(hp35_bcif_gz_file):
    return msm.convert(str(hp35_bcif_gz_file), to_form='molsysmt.Topology')


# ---------------------------------------------------------------------------
# Contract: DataContainer can be created and converted
# ---------------------------------------------------------------------------

def test_data_container_is_created(data_container):
    from mmcif.api.PdbxContainers import DataContainer
    assert isinstance(data_container, DataContainer)


def test_data_container_to_topology_atom_count(container_topology):
    assert container_topology.n_atoms == N_ATOMS


def test_data_container_to_topology_group_count(container_topology):
    assert container_topology.n_groups == N_GROUPS


def test_data_container_to_topology_chain_count(container_topology):
    assert container_topology.n_chains == N_CHAINS


# ---------------------------------------------------------------------------
# Parity: DataContainer topology == file:bcif_gz topology
# ---------------------------------------------------------------------------

def test_parity_atom_count(container_topology, reference_topology):
    assert container_topology.n_atoms == reference_topology.n_atoms


def test_parity_group_count(container_topology, reference_topology):
    assert container_topology.n_groups == reference_topology.n_groups


def test_parity_chain_count(container_topology, reference_topology):
    assert container_topology.n_chains == reference_topology.n_chains


def test_parity_atom_names(container_topology, reference_topology):
    assert container_topology.atoms['atom_name'].tolist() == reference_topology.atoms['atom_name'].tolist()


def test_parity_group_names(container_topology, reference_topology):
    assert container_topology.groups['group_name'].tolist() == reference_topology.groups['group_name'].tolist()

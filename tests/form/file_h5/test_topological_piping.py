"""Tests for topological attribute delivery from MDTraj HDF5 files."""

import numpy as np

import molsysmt as msm


def test_file_h5_delivers_declared_group_count_through_topology_pipe():
    """Delivering n_groups from the topology embedded in the HDF5 file."""

    molecular_system = msm.systems["pentalanine"]["traj_pentalanine.h5"]

    n_atoms, n_groups = msm.get(
        molecular_system,
        element="system",
        n_atoms=True,
        n_groups=True,
    )

    assert n_atoms == 62
    assert n_groups == 7


def test_file_h5_bulk_topology_attributes_use_embedded_topology():
    """Delivering atom names and group indices through one topology conversion."""

    molecular_system = msm.systems["pentalanine"]["traj_pentalanine.h5"]

    atom_names, group_indices = msm.get(
        molecular_system,
        element="atom",
        atom_name=True,
        group_index=True,
    )

    assert len(atom_names) == 62
    np.testing.assert_array_equal(np.unique(group_indices), np.arange(7))

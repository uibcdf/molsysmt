"""Topology-plus-coordinate conversion preserves explicit axes, units and boxes."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.form.mdtraj_Topology.to_mdtraj_Trajectory import to_mdtraj_Trajectory

pytest.importorskip("mdtraj")


@pytest.mark.parametrize("route", ["direct", "public"])
@pytest.mark.parametrize("length_unit", ["nm", "angstrom"])
def test_topology_to_trajectory_converts_explicit_coordinate_units(
    builder_mdtraj_topology, route, length_unit
):
    expected = np.arange(24, dtype=float).reshape(2, 4, 3) / 10
    coordinates = puw.convert(puw.quantity(expected, "nm"), to_unit=length_unit)
    if route == "direct":
        result = to_mdtraj_Trajectory(builder_mdtraj_topology, coordinates=coordinates)
    else:
        result = msm.convert(
            builder_mdtraj_topology,
            to_form="mdtraj.Trajectory",
            coordinates=coordinates,
        )
    np.testing.assert_allclose(result.xyz, expected, atol=1e-7, rtol=0)


@pytest.mark.parametrize("route", ["direct", "public"])
@pytest.mark.parametrize("atom_indices", [[0, 2], [2, 0, 2]])
def test_topology_to_trajectory_selects_topology_and_full_source_coordinates(
    builder_mdtraj_topology, route, atom_indices
):
    expected = np.arange(24, dtype=float).reshape(2, 4, 3) / 10
    coordinates = puw.quantity(expected, "nm")
    if route == "direct":
        result = to_mdtraj_Trajectory(
            builder_mdtraj_topology, atom_indices=atom_indices, coordinates=coordinates
        )
    else:
        result = msm.convert(
            builder_mdtraj_topology,
            to_form="mdtraj.Trajectory",
            selection=atom_indices,
            coordinates=coordinates,
        )
    assert result.xyz.shape == (2, 2, 3)
    assert [a.name for a in result.topology.atoms] == [
        a.name for a in builder_mdtraj_topology.atoms if a.index in [0, 2]
    ]
    np.testing.assert_allclose(result.xyz, expected[:, [0, 2]], atol=1e-7, rtol=0)
    assert builder_mdtraj_topology.n_atoms == 4


@pytest.mark.parametrize("route", ["direct", "public"])
def test_topology_to_trajectory_retains_explicit_periodic_box(
    builder_mdtraj_topology, route
):
    coordinates = puw.quantity(np.arange(24, dtype=float).reshape(2, 4, 3) / 10, "nm")
    expected = np.array(
        [
            [[3.0, 0, 0], [0.1, 3.1, 0], [0.2, 0.3, 3.2]],
            [[3.5, 0, 0], [0.2, 3.6, 0], [0.1, 0.4, 3.7]],
        ]
    )
    box = puw.quantity(expected * 10, "angstrom")
    if route == "direct":
        result = to_mdtraj_Trajectory(
            builder_mdtraj_topology, coordinates=coordinates, box=box
        )
    else:
        result = msm.convert(
            builder_mdtraj_topology,
            to_form="mdtraj.Trajectory",
            coordinates=coordinates,
            box=box,
        )
    assert result.unitcell_vectors is not None
    np.testing.assert_allclose(result.unitcell_vectors, expected, atol=1e-6, rtol=0)


def test_topology_to_trajectory_broadcasts_single_cell_and_checks_axes(
    builder_mdtraj_topology,
):
    from molsysmt._private.smonitor import ArgumentError

    coordinates = puw.quantity(np.arange(24, dtype=float).reshape(2, 4, 3), "nm")
    box = puw.quantity(np.eye(3)[None] * 3, "nm")
    result = to_mdtraj_Trajectory(
        builder_mdtraj_topology, coordinates=coordinates, box=box
    )
    np.testing.assert_allclose(
        result.unitcell_vectors,
        np.repeat(np.eye(3)[None] * 3, 2, axis=0),
        rtol=0,
        atol=1e-6,
    )
    with pytest.raises(ArgumentError):
        to_mdtraj_Trajectory(builder_mdtraj_topology)
    with pytest.raises(ArgumentError):
        to_mdtraj_Trajectory(
            builder_mdtraj_topology, coordinates=puw.quantity(np.zeros((2, 2, 3)), "nm")
        )
    with pytest.raises(ArgumentError):
        to_mdtraj_Trajectory(
            builder_mdtraj_topology,
            coordinates=coordinates,
            box=puw.quantity(np.repeat(np.eye(3)[None], 3, axis=0), "nm"),
        )
    np.testing.assert_array_equal(
        puw.get_value(coordinates), np.arange(24, dtype=float).reshape(2, 4, 3)
    )

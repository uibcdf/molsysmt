"""Testing trajectory, subset, and cursor contracts for MDAnalysis forms."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw


pytest.importorskip("MDAnalysis")


def test_universe_structural_getters_preserve_frame_and_triclinic_geometry(
    rich_universe,
):
    rich_universe.trajectory[1]
    coordinates, velocities = msm.get(
        rich_universe,
        element="atom",
        selection=[2, 0],
        structure_indices=[2, 0],
        coordinates=True,
        velocities=True,
    )
    time, box, structure_id = msm.get(
        rich_universe,
        element="system",
        structure_indices=[2, 0],
        time=True,
        box=True,
        structure_id=True,
    )

    assert rich_universe.trajectory.frame == 1
    source_coordinates = rich_universe.trajectory.timeseries(order="fac")
    np.testing.assert_allclose(
        puw.get_value(coordinates, to_unit="angstrom"),
        source_coordinates[[2, 0]][:, [2, 0]],
    )
    np.testing.assert_allclose(
        puw.get_value(velocities, to_unit="angstrom/ps"),
        rich_universe.trajectory.velocity_array[[2, 0]][:, [2, 0]],
    )
    np.testing.assert_allclose(puw.get_value(time, to_unit="ps"), [9.0, 5.0])
    np.testing.assert_array_equal(structure_id, ["2", "0"])

    lengths, angles = msm.pbc.get_lengths_and_angles_from_box(box)
    np.testing.assert_allclose(
        puw.get_value(lengths, to_unit="angstrom"),
        [[22.0, 32.0, 42.0], [20.0, 30.0, 40.0]],
        atol=1.0e-5,
    )
    np.testing.assert_allclose(
        puw.get_value(angles, to_unit="degree"),
        [[82.0, 92.0, 102.0], [80.0, 90.0, 100.0]],
        atol=2.0e-5,
    )


def test_universe_to_molsys_keeps_canonical_topology_and_coordinates_aligned(
    rich_universe,
):
    output = msm.convert(
        rich_universe,
        to_form="molsysmt.MolSys",
        selection=[2, 0],
        structure_indices=[2, 0],
    )

    assert output.topology.atoms["atom_id"].tolist() == ["10", "12"]
    np.testing.assert_allclose(
        puw.get_value(output.structures.coordinates, to_unit="angstrom"),
        rich_universe.trajectory.timeseries(order="fac")[[2, 0]][:, [0, 2]],
    )
    np.testing.assert_array_equal(output.structures.structure_id, [2, 0])


def test_universe_self_conversion_materializes_requested_subset(rich_universe):
    output = msm.convert(
        rich_universe,
        to_form="MDAnalysis.Universe",
        selection=[3, 1],
        structure_indices=[2, 0],
    )

    assert output.atoms.ids.tolist() == [13, 11]
    assert len(output.trajectory) == 2
    np.testing.assert_allclose([output.trajectory[index].time for index in range(2)], [9.0, 5.0])
    np.testing.assert_allclose(
        output.trajectory.timeseries(order="fac"),
        rich_universe.trajectory.timeseries(order="fac")[[2, 0]][:, [3, 1]],
    )


def test_universe_iterator_preserves_source_frame(rich_universe):
    rich_universe.trajectory[2]
    iterator = msm.Iterator(
        rich_universe,
        selection=[0, 2],
        structure_indices=[2, 0],
        chunk=1,
        coordinates=True,
        velocities=True,
        time=True,
        structure_id=True,
        box=True,
    )
    output = list(iterator)

    assert rich_universe.trajectory.frame == 2
    assert len(output) == 2
    assert puw.get_value(output[0][0], to_unit="angstrom").shape == (1, 2, 3)
    assert puw.get_value(output[0][1], to_unit="angstrom/ps").shape == (1, 2, 3)
    np.testing.assert_allclose(puw.get_value(output[0][2], to_unit="ps"), [9.0])
    np.testing.assert_array_equal(output[0][3], [2])
    assert puw.get_value(output[0][4], to_unit="angstrom").shape == (1, 3, 3)

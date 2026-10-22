"""Trajectory conversion reaches Modeller using the requested structure and atoms."""

import numpy as np
import pytest

import molsysmt as msm

pytest.importorskip("mdtraj")
pytest.importorskip("openmm")
from molsysmt import pyunitwizard as puw


@pytest.mark.parametrize("route", ["direct", "public"])
@pytest.mark.parametrize("atom_indices", ["all", [0, 2]])
def test_trajectory_to_modeller_preserves_selected_positions(
    builder_mdtraj_topology, route, atom_indices
):
    md = pytest.importorskip("mdtraj")
    pytest.importorskip("openmm")
    from molsysmt.form.mdtraj_Trajectory.to_openmm_Modeller import to_openmm_Modeller

    coordinates = np.arange(24, dtype=np.float32).reshape(2, 4, 3) / 10
    source = md.Trajectory(coordinates.copy(), builder_mdtraj_topology)
    result = (
        to_openmm_Modeller(source, atom_indices=atom_indices, structure_indices=[1])
        if route == "direct"
        else msm.convert(
            source,
            to_form="openmm.Modeller",
            selection=atom_indices,
            structure_indices=[1],
        )
    )
    expected = (
        coordinates[1]
        if isinstance(atom_indices, str)
        else coordinates[1, atom_indices]
    )
    assert result.topology.getNumAtoms() == len(expected)
    observed = puw.get_value(result.positions, to_unit="nm")
    assert observed.shape == (len(expected), 3)
    np.testing.assert_allclose(observed, expected, atol=1e-7, rtol=0)
    np.testing.assert_array_equal(source.xyz, coordinates)


@pytest.mark.parametrize("route", ["direct", "public"])
def test_trajectory_to_openmm_topology_retains_selected_atom_names(
    builder_mdtraj_topology, route
):
    import mdtraj as md

    from molsysmt.form.mdtraj_Trajectory.to_openmm_Topology import to_openmm_Topology

    source = md.Trajectory(np.zeros((1, 4, 3)), builder_mdtraj_topology)
    result = (
        to_openmm_Topology(source, atom_indices=[0, 2])
        if route == "direct"
        else msm.convert(source, to_form="openmm.Topology", selection=[0, 2])
    )
    assert [a.name for a in result.atoms()] == [
        a.name for a in builder_mdtraj_topology.atoms if a.index in [0, 2]
    ]

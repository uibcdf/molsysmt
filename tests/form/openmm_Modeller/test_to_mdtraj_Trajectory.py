"""Modeller conversion reaches MDTraj with selected, explicitly converted positions."""

import numpy as np
import pytest

import molsysmt as msm

pytest.importorskip("mdtraj")
pytest.importorskip("openmm")


@pytest.mark.parametrize("route", ["direct", "public"])
@pytest.mark.parametrize("atom_indices", ["all", [0, 2]])
def test_modeller_to_trajectory_preserves_selected_positions(
    builder_openmm_topology, route, atom_indices
):
    pytest.importorskip("mdtraj")
    pytest.importorskip("openmm")
    from openmm import app, unit

    from molsysmt.form.openmm_Modeller.to_mdtraj_Trajectory import to_mdtraj_Trajectory

    coordinates = np.arange(12, dtype=float).reshape(4, 3) / 10
    source = app.Modeller(builder_openmm_topology, coordinates * 10 * unit.angstrom)
    kwargs = {"atom_indices": atom_indices, "structure_indices": [0]}
    result = (
        to_mdtraj_Trajectory(source, **kwargs)
        if route == "direct"
        else msm.convert(
            source,
            to_form="mdtraj.Trajectory",
            selection=atom_indices,
            structure_indices=[0],
        )
    )
    expected = (
        coordinates if isinstance(atom_indices, str) else coordinates[atom_indices]
    )
    assert result.xyz.shape == (1, len(expected), 3)
    assert result.topology.n_atoms == len(expected)
    np.testing.assert_allclose(result.xyz[0], expected, atol=1e-7, rtol=0)
    assert source.topology.getNumAtoms() == 4

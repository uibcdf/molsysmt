"""Checking current-context box shape, units and pose at PDB export."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw


@pytest.fixture
def simulation():
    openmm = pytest.importorskip("openmm")
    from openmm import app, unit

    topology = app.Topology()
    group = topology.addResidue("UNK", topology.addChain())
    topology.addAtom("C", app.element.carbon, group)
    topology.addAtom("O", app.element.oxygen, group)
    topology.setPeriodicBoxVectors(np.diag([2, 2, 2]) * unit.nanometer)
    system = openmm.System()
    system.addParticle(12 * unit.dalton)
    system.addParticle(16 * unit.dalton)
    output = app.Simulation(
        topology,
        system,
        openmm.VerletIntegrator(0.001 * unit.picosecond),
        openmm.Platform.getPlatformByName("Reference"),
    )
    output.context.setPositions([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]] * unit.nanometer)
    output.context.setPeriodicBoxVectors(*(np.diag([3, 4, 5]) * unit.nanometer))
    return output


@pytest.mark.parametrize("length_unit", ["nm", "angstrom"])
def test_pdb_export_uses_current_context_box_and_keeps_source(
    simulation, tmp_path, length_unit
):
    from openmm import app, unit

    path = tmp_path / "requested.pdb"
    with puw.context(standard_units=[length_unit, "ps"]):
        output = msm.convert(simulation, to_form="file:pdb", output_filename=str(path))
        selected = msm.convert(
            simulation,
            to_form="file:pdb",
            selection=[1],
            structure_indices=0,
            output_filename=str(tmp_path / "selected.pdb"),
        )
    assert output == str(path) and path.is_file()
    pdb = app.PDBFile(output)
    np.testing.assert_allclose(
        pdb.positions.value_in_unit(unit.nanometer),
        [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]],
    )
    np.testing.assert_allclose(
        pdb.topology.getPeriodicBoxVectors().value_in_unit(unit.nanometer),
        np.diag([3, 4, 5]),
    )
    np.testing.assert_allclose(
        simulation.topology.getPeriodicBoxVectors().value_in_unit(unit.nanometer),
        np.diag([2, 2, 2]),
    )
    assert simulation.topology.getNumAtoms() == 2
    subset = app.PDBFile(selected)
    assert subset.topology.getNumAtoms() == 1
    np.testing.assert_allclose(
        subset.positions.value_in_unit(unit.nanometer),
        [[0.4, 0.5, 0.6]],
    )

"""
Contract tests for openmm.Context form.

openmm.Context is a structures-only form: it carries the current
simulation state (positions, velocities, forces) but no independent
topology.  The documented contract is coordinate/state extraction.

Oracle: 1l2y.pdb (Trp-cage, 304 atoms, all hydrogens present) built into
a real openmm.Simulation.  Parity is verified against the source PDB
positions (Context positions should equal the positions set at creation).
"""

import pytest
from pathlib import Path
import numpy as np
import molsysmt as msm
from molsysmt import pyunitwizard as puw


PDB_PATH = str(Path(msm.__file__).parent / 'data' / 'pdb' / '1l2y.pdb')
N_ATOMS = 304


@pytest.fixture(scope='module')
def context():
    from openmm.app import PDBFile, ForceField, Modeller, Simulation
    import openmm as mm
    import openmm.unit as unit

    pdb = PDBFile(PDB_PATH)
    forcefield = ForceField('amber14-all.xml', 'amber14/tip3pfb.xml')
    modeller = Modeller(pdb.topology, pdb.positions)
    modeller.addHydrogens(forcefield)
    system = forcefield.createSystem(
        modeller.topology,
        nonbondedMethod=mm.app.NoCutoff,
        constraints=mm.app.HBonds,
    )
    integrator = mm.LangevinIntegrator(300 * unit.kelvin, 1.0 / unit.picosecond, 0.002 * unit.picosecond)
    platform = mm.Platform.getPlatformByName('CPU')
    sim = Simulation(modeller.topology, system, integrator, platform)
    sim.context.setPositions(modeller.positions)
    return sim.context


@pytest.fixture(scope='module')
def context_structures(context):
    return msm.convert(context, to_form='molsysmt.Structures')


# ---------------------------------------------------------------------------
# Contract: openmm.Context → molsysmt.Structures extracts positions
# ---------------------------------------------------------------------------

def test_context_structures_is_created(context_structures):
    assert context_structures is not None


def test_context_structures_atom_count(context_structures):
    assert context_structures.n_atoms == N_ATOMS


def test_context_structures_frame_count(context_structures):
    assert context_structures.n_structures == 1


def test_context_coordinates_are_finite(context_structures):
    coords = puw.get_value(context_structures.coordinates, to_unit='nm')
    assert np.all(np.isfinite(coords))


def test_context_coordinates_shape(context_structures):
    coords = puw.get_value(context_structures.coordinates, to_unit='nm')
    assert coords.shape == (1, N_ATOMS, 3)


def test_context_reports_integrator_temperature(context):
    temperature = msm.get(context, temperature=True)

    np.testing.assert_allclose(puw.get_value(temperature, to_unit='K'), [300.0])

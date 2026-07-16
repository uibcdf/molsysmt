from pathlib import Path

import pytest

import molsysmt as msm
from molsysmt.systems import systems


PDB_PATH = str(systems['Trp-Cage']['1l2y.pdb'])
PRMTOP_PATH = str(systems['pentalanine']['pentalanine.prmtop'])
PSF_PATH = str(systems['POPC']['popc.psf'])


def _assert_topology_pipe(item, expected_group_name):
    atom_indices, group_names = msm.get(
        item,
        element='atom',
        selection=[0, 1],
        atom_index=True,
        group_name=True,
    )

    assert atom_indices == [0, 1]
    assert group_names == [expected_group_name, expected_group_name]


def test_mdtraj_trajectory_topology_pipe():
    mdtraj = pytest.importorskip('mdtraj')
    item = mdtraj.load(PDB_PATH)

    _assert_topology_pipe(item, 'ASN')


@pytest.mark.parametrize(
    ('constructor_name', 'path', 'expected_group_name'),
    [
        ('PDBFile', PDB_PATH, 'ASN'),
        ('AmberPrmtopFile', PRMTOP_PATH, 'ACE'),
        ('CharmmPsfFile', PSF_PATH, 'POPC'),
    ],
)
def test_openmm_topology_pipes(constructor_name, path, expected_group_name):
    openmm_app = pytest.importorskip('openmm.app')
    constructor = getattr(openmm_app, constructor_name)
    item = constructor(path)

    _assert_topology_pipe(item, expected_group_name)


def test_parmed_gromacs_topology_pipe():
    parmed = pytest.importorskip('parmed')
    from parmed.gromacs import GromacsTopologyFile

    structure = parmed.load_file(PSF_PATH)
    item = GromacsTopologyFile.from_structure(structure)

    _assert_topology_pipe(item, 'POPC')


def test_openmm_gromacs_topology_pipe(tmp_path):
    parmed = pytest.importorskip('parmed')
    openmm_app = pytest.importorskip('openmm.app')
    from parmed.gromacs import GromacsTopologyFile as ParmEdGromacsTopologyFile

    structure = parmed.load_file(PSF_PATH)
    parmed_topology = ParmEdGromacsTopologyFile.from_structure(structure)
    top_path = Path(tmp_path) / 'popc.top'
    parmed_topology.write(str(top_path))
    item = openmm_app.GromacsTopFile(str(top_path), includeDir=str(tmp_path))

    _assert_topology_pipe(item, 'POPC')


def test_openmm_state_native_getters():
    openmm = pytest.importorskip('openmm')
    unit = openmm.unit

    system = openmm.System()
    system.addParticle(12.0)
    system.addParticle(16.0)
    integrator = openmm.VerletIntegrator(0.001)
    context = openmm.Context(system, integrator)
    context.setPositions([[0, 0, 0], [0.1, 0, 0]] * unit.nanometer)
    context.setVelocities([[0, 0, 0], [0, 0, 0]] * unit.nanometer / unit.picosecond)
    state = context.getState(getPositions=True, getVelocities=True)

    atom_indices, coordinates, velocities = msm.get(
        state,
        element='atom',
        atom_index=True,
        coordinates=True,
        velocities=True,
    )

    assert atom_indices == [0, 1]
    assert coordinates.shape == (1, 2, 3)
    assert velocities.shape == (1, 2, 3)
    assert msm.get(state, element='system', n_atoms=True) == 2

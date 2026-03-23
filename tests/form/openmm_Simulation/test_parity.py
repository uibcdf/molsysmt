"""
Parity tests for openmm.Simulation form.

Oracle: 1l2y.pdb (Trp-cage, 304 atoms, all hydrogens present).
Because 1l2y.pdb already includes all hydrogens, addHydrogens is a no-op and
atom count is preserved through the Simulation creation.

Parity means that openmm.Simulation → molsysmt.Topology gives the same
counts and names as loading the same PDB directly as molsysmt.Topology.
"""

import pytest
from pathlib import Path
import molsysmt as msm


PDB_PATH = str(Path(msm.__file__).parent / 'data' / 'pdb' / '1l2y.pdb')


@pytest.fixture(scope='module')
def simulation():
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
    return sim


@pytest.fixture(scope='module')
def source_topology():
    return msm.convert(PDB_PATH, to_form='molsysmt.Topology')


@pytest.fixture(scope='module')
def simulation_topology(simulation):
    return msm.convert(simulation, to_form='molsysmt.Topology')


# ---------------------------------------------------------------------------
# Parity: openmm.Simulation → molsysmt.Topology preserves source topology
# (1l2y has all H already; addHydrogens is a no-op so counts are identical)
# ---------------------------------------------------------------------------

def test_parity_atom_count(simulation_topology, source_topology):
    assert simulation_topology.n_atoms == source_topology.n_atoms


def test_parity_group_count(simulation_topology, source_topology):
    assert simulation_topology.n_groups == source_topology.n_groups


def test_parity_chain_count(simulation_topology, source_topology):
    assert simulation_topology.n_chains == source_topology.n_chains


def test_parity_group_names(simulation_topology, source_topology):
    assert simulation_topology.groups['group_name'].tolist() == source_topology.groups['group_name'].tolist()

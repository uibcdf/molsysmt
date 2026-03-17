"""
Parser regression tests for openmm.Simulation form adapter.

Uses a bundled PDB file (1l2y: Trp-cage miniprotein, 20 residues, 1 chain)
to build a real openmm.Simulation with AMBER14 forcefield on the CPU platform.

The fixture calls openmm.app.Modeller.addHydrogens before creating the System.
For 1l2y, this is a no-op because the bundled PDB already includes all hydrogens
(304 atoms total). Tests use exact atom and bond counts accordingly.

Note: this fixture takes several seconds to build on first use (forcefield
parameterization). It is scope='module' so it runs once per test session.
"""

import pytest
from pathlib import Path

import molsysmt as msm
from molsysmt.form.openmm_Simulation import get_topological_attributes as aux

PDB_PATH = str(Path(msm.__file__).parent / 'data' / 'pdb' / '1l2y.pdb')

# Invariants that do not change when hydrogens are added
N_GROUPS      = 20
N_CHAINS      = 1
N_MOLECULES   = 1
N_ENTITIES    = 1
N_COMPONENTS  = 1
N_AMINO_ACIDS = 20
N_ATOMS       = 304   # 1l2y.pdb already contains all hydrogens; addHydrogens is a no-op
N_BONDS       = 310


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
    integrator = mm.LangevinIntegrator(
        300 * unit.kelvin,
        1.0 / unit.picosecond,
        0.002 * unit.picosecond,
    )
    platform = mm.Platform.getPlatformByName('CPU')
    sim = Simulation(modeller.topology, system, integrator, platform)
    sim.context.setPositions(modeller.positions)
    return sim


# ---------------------------------------------------------------------------
# System-level invariants (stable across H addition)
# ---------------------------------------------------------------------------

def test_n_groups(simulation):
    assert aux.get_n_groups_from_system(simulation) == N_GROUPS

def test_n_chains(simulation):
    assert aux.get_n_chains_from_system(simulation) == N_CHAINS

def test_n_molecules(simulation):
    assert aux.get_n_molecules_from_system(simulation) == N_MOLECULES

def test_n_entities(simulation):
    assert aux.get_n_entities_from_system(simulation) == N_ENTITIES

def test_n_components(simulation):
    assert aux.get_n_components_from_system(simulation) == N_COMPONENTS

def test_n_amino_acids(simulation):
    assert aux.get_n_amino_acids_from_system(simulation) == N_AMINO_ACIDS

def test_n_atoms(simulation):
    assert aux.get_n_atoms_from_system(simulation) == N_ATOMS

def test_n_bonds(simulation):
    assert aux.get_n_bonds_from_system(simulation) == N_BONDS


# ---------------------------------------------------------------------------
# Group names
# ---------------------------------------------------------------------------

def test_group_name_first_five(simulation):
    names = aux.get_group_name_from_group(simulation)
    assert isinstance(names, list)
    assert len(names) == N_GROUPS
    assert names[:5] == ['ASN', 'LEU', 'TYR', 'ILE', 'GLN']

def test_group_name_last(simulation):
    names = aux.get_group_name_from_group(simulation)
    assert names[-1] == 'SER'


# ---------------------------------------------------------------------------
# Chain identity
# ---------------------------------------------------------------------------

def test_chain_id(simulation):
    chain_ids = aux.get_chain_id_from_chain(simulation)
    assert isinstance(chain_ids, list)
    assert chain_ids == ['A']

def test_chain_name_is_none(simulation):
    assert aux.get_chain_name_from_chain(simulation) is None


# ---------------------------------------------------------------------------
# Group-level atom count consistency
# ---------------------------------------------------------------------------

def test_n_atoms_from_group_sums_to_total(simulation):
    per_group = aux.get_n_atoms_from_group(simulation)
    assert isinstance(per_group, list)
    assert len(per_group) == N_GROUPS
    assert sum(per_group) == aux.get_n_atoms_from_system(simulation)

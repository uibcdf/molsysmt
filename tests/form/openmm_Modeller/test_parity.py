"""
Parity tests for openmm.Modeller form.

Oracle: builder_pdb_molsys (4 atoms, 2 groups, 1 chain, 2 bonds).
Parity means that MolSys → openmm.Modeller → molsysmt.Topology
preserves atom count, group count, chain count, bond count,
atom names, and group names.
"""

import pytest
import molsysmt as msm


@pytest.fixture()
def modeller(builder_pdb_molsys):
    from openmm.app import Modeller
    import openmm.unit as unit
    from openmm.vec3 import Vec3

    topo = msm.convert(builder_pdb_molsys, to_form='openmm.Topology')
    positions = [Vec3(0, 0, 0)] * topo.getNumAtoms() * unit.nanometer
    return Modeller(topo, positions)


@pytest.fixture()
def modeller_topology(modeller):
    return msm.convert(modeller, to_form='molsysmt.Topology')


@pytest.fixture()
def source_topology(builder_pdb_molsys):
    return builder_pdb_molsys.topology


# ---------------------------------------------------------------------------
# Parity: MolSys → openmm.Modeller → molsysmt.Topology preserves topology
# ---------------------------------------------------------------------------

def test_parity_atom_count(modeller_topology, source_topology):
    assert modeller_topology.n_atoms == source_topology.n_atoms


def test_parity_group_count(modeller_topology, source_topology):
    assert modeller_topology.n_groups == source_topology.n_groups


def test_parity_chain_count(modeller_topology, source_topology):
    assert modeller_topology.n_chains == source_topology.n_chains


def test_parity_bond_count(modeller_topology, source_topology):
    assert modeller_topology.n_bonds == source_topology.n_bonds


def test_parity_atom_names(modeller_topology, source_topology):
    assert modeller_topology.atoms['atom_name'].tolist() == source_topology.atoms['atom_name'].tolist()


def test_parity_group_names(modeller_topology, source_topology):
    assert modeller_topology.groups['group_name'].tolist() == source_topology.groups['group_name'].tolist()

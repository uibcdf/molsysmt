"""
Tests for openff_Topology/get_topological_attributes.py.

Oracle: single-molecule topology built from caffeine (24 atoms with explicit H).
Multi-molecule topology: caffeine + ethanol (CCO, 9 atoms with H).
  caffeine: 24 atoms, 25 bonds
  ethanol:   9 atoms,  8 bonds
  combined: 33 atoms, 33 bonds
"""

from importlib.util import find_spec

import pytest

if find_spec('openff.toolkit') is None:
    pytest.skip('openff-toolkit is not installed', allow_module_level=True)

from openff.toolkit.topology import Molecule, Topology

CAFFEINE_SMILES = 'CN1C=NC2=C1C(=O)N(C(=O)N2C)C'
ETHANOL_SMILES = 'CCO'


@pytest.fixture(scope="module")
def caffeine_top():
    return Molecule.from_smiles(CAFFEINE_SMILES).to_topology()


@pytest.fixture(scope="module")
def two_mol_top():
    mol_caf = Molecule.from_smiles(CAFFEINE_SMILES)
    mol_eth = Molecule.from_smiles(ETHANOL_SMILES)
    top = Topology()
    top.add_molecule(mol_caf)
    top.add_molecule(mol_eth)
    return top


# ---------------------------------------------------------------------------
# Form recognition
# ---------------------------------------------------------------------------

def test_get_form(caffeine_top):
    import molsysmt as msm
    assert msm.get_form(caffeine_top) == 'openff.Topology'


# ---------------------------------------------------------------------------
# Single-molecule topology
# ---------------------------------------------------------------------------

@pytest.mark.redundant
def test_n_atoms_single(caffeine_top):
    import molsysmt as msm
    assert msm.get(caffeine_top, element='system', n_atoms=True) == 24


@pytest.mark.redundant
def test_n_bonds_single(caffeine_top):
    import molsysmt as msm
    assert msm.get(caffeine_top, element='system', n_bonds=True) == 25


def test_n_components_single(caffeine_top):
    import molsysmt as msm
    assert msm.get(caffeine_top, element='system', n_components=True) == 1


# ---------------------------------------------------------------------------
# Multi-molecule topology
# ---------------------------------------------------------------------------

@pytest.mark.redundant
def test_n_atoms_two_mols(two_mol_top):
    import molsysmt as msm
    # caffeine 24 + ethanol 9 = 33
    assert msm.get(two_mol_top, element='system', n_atoms=True) == 33


def test_n_components_two_mols(two_mol_top):
    # caffeine + ethanol → 2 disconnected components
    import molsysmt as msm
    assert msm.get(two_mol_top, element='system', n_components=True) == 2


# ---------------------------------------------------------------------------
# Conversions
# ---------------------------------------------------------------------------

def test_to_molsysmt_Topology(caffeine_top):
    import molsysmt as msm
    result = msm.convert(caffeine_top, to_form='molsysmt.Topology')
    assert msm.get(result, element='system', n_atoms=True) == 24


def test_to_openmm_Topology(caffeine_top):
    import molsysmt as msm
    result = msm.convert(caffeine_top, to_form='openmm.Topology')
    assert msm.get_form(result) == 'openmm.Topology'


def test_to_openff_Molecule_single(caffeine_top):
    import molsysmt as msm
    result = msm.convert(caffeine_top, to_form='openff.Molecule')
    assert msm.get_form(result) == 'openff.Molecule'
    assert result.n_atoms == 24


def test_roundtrip_molecule_topology(caffeine_top):
    import molsysmt as msm
    mol = msm.convert(caffeine_top, to_form='openff.Molecule')
    back = msm.convert(mol, to_form='openff.Topology')
    assert msm.get_form(back) == 'openff.Topology'
    assert back.n_atoms == 24

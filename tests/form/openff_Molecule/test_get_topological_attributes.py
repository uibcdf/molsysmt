"""
Tests for openff_Molecule/get_topological_attributes.py.

Oracle: caffeine (C8H10N4O2) loaded via openff.toolkit.topology.Molecule.from_smiles.
openff-toolkit adds explicit hydrogens by default:
  n_atoms = 24  (14 heavy + 10 H)
  n_bonds = 25  (15 heavy-atom bonds + 10 C-H/N-H bonds)
"""

from importlib.util import find_spec

import pytest

if find_spec('openff.toolkit') is None:
    pytest.skip('openff-toolkit is not installed', allow_module_level=True)

from openff.toolkit.topology import Molecule

CAFFEINE_SMILES = 'CN1C=NC2=C1C(=O)N(C(=O)N2C)C'


@pytest.fixture(scope="module")
def caffeine_mol():
    return Molecule.from_smiles(CAFFEINE_SMILES)


# ---------------------------------------------------------------------------
# Form recognition
# ---------------------------------------------------------------------------

def test_get_form(caffeine_mol):
    import molsysmt as msm
    assert msm.get_form(caffeine_mol) == 'openff.Molecule'


# ---------------------------------------------------------------------------
# System-level topological attributes
# ---------------------------------------------------------------------------

@pytest.mark.redundant
def test_n_atoms(caffeine_mol):
    import molsysmt as msm
    assert msm.get(caffeine_mol, element='system', n_atoms=True) == 24


@pytest.mark.redundant
def test_n_bonds(caffeine_mol):
    import molsysmt as msm
    assert msm.get(caffeine_mol, element='system', n_bonds=True) == 25


@pytest.mark.redundant
def test_n_groups(caffeine_mol):
    # No residue/group hierarchy in a bare SMILES-derived molecule
    import molsysmt as msm
    assert msm.get(caffeine_mol, element='system', n_groups=True) == 0


@pytest.mark.redundant
def test_n_components(caffeine_mol):
    import molsysmt as msm
    assert msm.get(caffeine_mol, element='system', n_components=True) == 1


@pytest.mark.redundant
def test_n_molecules(caffeine_mol):
    import molsysmt as msm
    assert msm.get(caffeine_mol, element='system', n_molecules=True) == 0


@pytest.mark.redundant
def test_n_entities(caffeine_mol):
    import molsysmt as msm
    assert msm.get(caffeine_mol, element='system', n_entities=True) == 0


# ---------------------------------------------------------------------------
# Conversions
# ---------------------------------------------------------------------------

def test_to_openff_Topology(caffeine_mol):
    import molsysmt as msm
    result = msm.convert(caffeine_mol, to_form='openff.Topology')
    assert msm.get_form(result) == 'openff.Topology'
    assert result.n_atoms == 24


def test_to_molsysmt_Topology(caffeine_mol):
    import molsysmt as msm
    result = msm.convert(caffeine_mol, to_form='molsysmt.Topology')
    assert msm.get(result, element='system', n_atoms=True) == 24


def test_to_rdkit_Mol(caffeine_mol):
    import molsysmt as msm
    result = msm.convert(caffeine_mol, to_form='rdkit.Mol')
    assert msm.get_form(result) == 'rdkit.Mol'


def test_to_string_smiles(caffeine_mol):
    import molsysmt as msm
    result = msm.convert(caffeine_mol, to_form='string:smiles')
    assert result.startswith('smiles:')

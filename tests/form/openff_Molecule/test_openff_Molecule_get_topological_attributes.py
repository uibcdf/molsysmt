"""
Tests for openff_Molecule/get_topological_attributes.py.

Oracle: caffeine (C8H10N4O2) loaded via openff.toolkit.topology.Molecule.from_smiles.
openff-toolkit adds explicit hydrogens by default:
  n_atoms = 24  (14 heavy + 10 H)
  n_bonds = 25  (15 heavy-atom bonds + 10 C-H/N-H bonds)
"""

import pytest

try:
    from openff.toolkit.topology import Molecule
    HAS_OPENFF = True
except ImportError:
    HAS_OPENFF = False

needs_openff = pytest.mark.skipif(not HAS_OPENFF, reason="openff-toolkit not installed")

CAFFEINE_SMILES = 'CN1C=NC2=C1C(=O)N(C(=O)N2C)C'


@pytest.fixture(scope="module")
def caffeine_mol():
    return Molecule.from_smiles(CAFFEINE_SMILES)


# ---------------------------------------------------------------------------
# Form recognition
# ---------------------------------------------------------------------------

@needs_openff
def test_get_form(caffeine_mol):
    import molsysmt as msm
    assert msm.get_form(caffeine_mol) == 'openff.Molecule'


# ---------------------------------------------------------------------------
# System-level topological attributes
# ---------------------------------------------------------------------------

@needs_openff
def test_n_atoms(caffeine_mol):
    import molsysmt as msm
    assert msm.get(caffeine_mol, element='system', n_atoms=True) == 24


@needs_openff
def test_n_bonds(caffeine_mol):
    import molsysmt as msm
    assert msm.get(caffeine_mol, element='system', n_bonds=True) == 25


@needs_openff
def test_n_groups(caffeine_mol):
    # No residue/group hierarchy in a bare SMILES-derived molecule
    import molsysmt as msm
    assert msm.get(caffeine_mol, element='system', n_groups=True) == 0


@needs_openff
def test_n_components(caffeine_mol):
    import molsysmt as msm
    assert msm.get(caffeine_mol, element='system', n_components=True) == 1


@needs_openff
def test_n_molecules(caffeine_mol):
    import molsysmt as msm
    assert msm.get(caffeine_mol, element='system', n_molecules=True) == 0


@needs_openff
def test_n_entities(caffeine_mol):
    import molsysmt as msm
    assert msm.get(caffeine_mol, element='system', n_entities=True) == 0


# ---------------------------------------------------------------------------
# Conversions
# ---------------------------------------------------------------------------

@needs_openff
def test_to_openff_Topology(caffeine_mol):
    import molsysmt as msm
    result = msm.convert(caffeine_mol, to_form='openff.Topology')
    assert msm.get_form(result) == 'openff.Topology'
    assert result.n_atoms == 24


@needs_openff
def test_to_molsysmt_Topology(caffeine_mol):
    import molsysmt as msm
    result = msm.convert(caffeine_mol, to_form='molsysmt.Topology')
    assert msm.get(result, element='system', n_atoms=True) == 24


@needs_openff
def test_to_rdkit_Mol(caffeine_mol):
    import molsysmt as msm
    result = msm.convert(caffeine_mol, to_form='rdkit.Mol')
    assert msm.get_form(result) == 'rdkit.Mol'


@needs_openff
def test_to_string_smiles(caffeine_mol):
    import molsysmt as msm
    result = msm.convert(caffeine_mol, to_form='string:smiles')
    assert result.startswith('smiles:')

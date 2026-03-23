"""
Contract and parity tests for rdkit.Mol form.

rdkit.Mol is a pure topological (small-molecule) form: it carries atom
connectivity and 2-D/3-D geometry but no residue/chain hierarchy.

Oracle: caffeine SMILES 'CN1C=NC2=C1C(=O)N(C(=O)N2C)C'
(14 heavy atoms).  SMILES → rdkit.Mol is the canonical creation path.

Contract: rdkit.Mol is created and carries the right heavy-atom count.
Parity: the molecule round-trips through SMILES (rdkit.Mol → string:smiles)
preserving atom count.

Note: rdkit.Mol has no residue/chain hierarchy, so n_groups is 0.
"""

import pytest
import molsysmt as msm


CAFFEINE_SMILES = 'CN1C=NC2=C1C(=O)N(C(=O)N2C)C'
N_ATOMS = 14     # heavy atoms in caffeine


@pytest.fixture(scope='module')
def caffeine_mol():
    return msm.convert(CAFFEINE_SMILES, to_form='rdkit.Mol')


@pytest.fixture(scope='module')
def smiles_back(caffeine_mol):
    return msm.convert(caffeine_mol, to_form='string:smiles')


@pytest.fixture(scope='module')
def mol_from_smiles_back(smiles_back):
    return msm.convert(smiles_back, to_form='rdkit.Mol')


# ---------------------------------------------------------------------------
# Contract: rdkit.Mol is created from SMILES and has the right atom count
# ---------------------------------------------------------------------------

def test_mol_is_created(caffeine_mol):
    from rdkit.Chem import Mol
    assert isinstance(caffeine_mol, Mol)


def test_mol_atom_count(caffeine_mol):
    assert caffeine_mol.GetNumAtoms() == N_ATOMS


def test_mol_to_smiles(smiles_back):
    assert smiles_back is not None
    assert len(smiles_back) > 0


# ---------------------------------------------------------------------------
# Parity: rdkit.Mol → string:smiles → rdkit.Mol preserves atom count
# ---------------------------------------------------------------------------

def test_parity_atom_count(mol_from_smiles_back):
    assert mol_from_smiles_back.GetNumAtoms() == N_ATOMS

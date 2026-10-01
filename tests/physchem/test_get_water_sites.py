"""Recognize indexed water chemistry rather than residue labels or implicit H."""

import pytest
from rdkit import Chem

import molsysmt as msm
from molsysmt._private.smonitor import UnsupportedHeavyOperationError


@pytest.mark.parametrize('smiles,count', [('O', 1), ('[OH-]', 0), ('[OH3+]', 0), ('CO', 0), ('OO', 0), ('O.O', 2)])
def test_neutral_explicit_water_components_only(smiles, count):
    sites = msm.physchem.get_water_sites(Chem.AddHs(Chem.MolFromSmiles(smiles)))
    assert sites['water_atom_indices'].shape == (count, 3)
    assert sites['water_atom_indices'].dtype.name == 'int64'
    assert 'attribution' in sites and 'rdkit' in sites['software']


def test_implicit_hydrogens_and_partial_selection_never_invent_water():
    assert msm.physchem.get_water_sites(Chem.MolFromSmiles('O'))['water_atom_indices'].shape == (0, 3)
    molecule = Chem.AddHs(Chem.MolFromSmiles('O'))
    assert msm.physchem.get_water_sites(molecule, selection=[0, 1])['water_atom_indices'].shape == (0, 3)
    assert msm.physchem.get_water_sites(molecule, selection=[2, 0, 1])['water_atom_indices'].tolist() == [[0, 1, 2]]
    isotope = Chem.MolFromSmiles('[2H]O[2H]', sanitize=True)
    assert msm.physchem.get_water_sites(isotope)['water_atom_indices'].tolist() == [[1, 0, 2]]
    with pytest.raises(UnsupportedHeavyOperationError):
        msm.physchem.get_water_sites(Chem.AddHs(Chem.MolFromSmiles('O.O')), max_matches=1)

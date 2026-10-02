"""Check full-source chemically restricted metal and ligand recognition."""

import pytest
from rdkit import Chem

import molsysmt as msm
from molsysmt._private.smonitor import UnsupportedHeavyOperationError


def test_reference_metal_set_and_ligand_exclusions():
    molecule = Chem.MolFromSmiles(
        "[Zn+2].[Mg+2].[Na+].[K+].O.N.CN(C)C.C[N+](C)(C)C.C(=O)N.[S-].c1ccncc1"
    )
    sites = msm.physchem.get_metal_coordination_sites(molecule)
    assert sites["metal_atom_indices"].tolist() == [0, 1]
    eligible = sites["ligand_atom_indices"].tolist()
    for atom in molecule.GetAtoms():
        i = atom.GetIdx()
        if atom.GetSymbol() == "O" or atom.GetFormalCharge() < 0:
            assert i in eligible
        if atom.GetFormalCharge() > 0:
            assert i not in eligible
    amide_n = [m[2] for m in molecule.GetSubstructMatches(Chem.MolFromSmarts("C(=O)N"))]
    assert not set(amide_n) & set(eligible)
    selected = msm.physchem.get_metal_coordination_sites(molecule, selection=[1, 4])
    assert selected["metal_atom_indices"].tolist() == [1]
    assert selected["ligand_atom_indices"].tolist() == [4]
    assert "attribution" in sites and "rdkit" in sites["software"]


def test_empty_shapes_and_match_cap():
    sites = msm.physchem.get_metal_coordination_sites(Chem.MolFromSmiles("CC"))
    assert (
        sites["metal_atom_indices"].shape == sites["ligand_atom_indices"].shape == (0,)
    )
    with pytest.raises(UnsupportedHeavyOperationError):
        msm.physchem.get_metal_coordination_sites(
            Chem.MolFromSmiles("[Zn+2].[Zn+2]"), max_matches=1
        )

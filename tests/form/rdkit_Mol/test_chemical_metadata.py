import pytest

Chem = pytest.importorskip("rdkit.Chem")

import molsysmt as msm


def test_rdkit_mol_to_molsys_preserves_bond_order_and_formal_charge():
    mol = Chem.MolFromSmiles("[NH3+]C(=O)O")

    molsys = msm.convert(mol, to_form="molsysmt.MolSys")

    orders = molsys.topology.bonds["order"].tolist()
    types = molsys.topology.bonds["type"].tolist()
    formal_charge = molsys.molecular_mechanics.formal_charge.tolist()

    assert "2" in orders
    assert "double" in types
    assert formal_charge[0] == 1


def test_rdkit_mol_to_molsys_preserves_aromatic_bonds_in_viewerjson():
    mol = Chem.MolFromSmiles("c1ccccc1")

    molsys = msm.convert(mol, to_form="molsysmt.MolSys")
    viewer_json = molsys.to_form("molsysmt.ViewerJSON").to_dict()

    assert set(viewer_json["bonds"]["order"]) == {"aromatic"}
    assert set(viewer_json["bonds"]["type"]) == {"aromatic"}
    assert viewer_json["atoms"]["formal_charge"] == [0] * mol.GetNumAtoms()

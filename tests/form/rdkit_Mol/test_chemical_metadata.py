import pytest
import pandas as pd
import numpy as np

Chem = pytest.importorskip("rdkit.Chem")

import molsysmt as msm
from molsysmt import pyunitwizard as puw


def test_rdkit_mol_to_molsys_preserves_bond_order_and_formal_charge():
    mol = Chem.MolFromSmiles("[NH3+]C(=O)O")

    molsys = msm.convert(mol, to_form="molsysmt.MolSys")

    orders = molsys.topology.bonds["bond_order"].tolist()
    formal_charge = msm.get(molsys, element='atom', formal_charge=True)

    assert 2 in orders
    assert formal_charge[0] == 1


def test_rdkit_mol_to_molsys_preserves_aromatic_bonds_in_viewerjson():
    mol = Chem.MolFromSmiles("c1ccccc1")

    molsys = msm.convert(mol, to_form="molsysmt.MolSys")
    viewer_json = molsys.to_form("molsysmt.ViewerJSON").to_dict()

    assert set(viewer_json["bonds"]["order"]) == {"aromatic"}
    assert set(viewer_json["bonds"]["type"]) == {'covalent'}
    assert viewer_json["atoms"]["formal_charge"] == [0] * mol.GetNumAtoms()
    assert all(msm.get(mol, element='bond', bond_is_aromatic=True))


def test_rdkit_rich_atom_and_bond_fields_remain_independent():
    mol = Chem.MolFromSmiles('[NH3+][C@H](C)C(=O)/N=C/C1=CC=CC=C1')

    topology = msm.convert(mol, to_form='molsysmt.Topology')

    assert msm.get(topology, element='atom', formal_charge=True)[0] == 1
    assert 'R' in msm.get(topology, element='atom', atom_stereochemistry=True)
    assert any(msm.get(topology, element='atom', atom_is_aromatic=True))
    assert any(msm.get(topology, element='bond', bond_is_conjugated=True))
    assert any(
        not pd.isna(value) and value == 'E'
        for value in msm.get(
            topology, element='bond', bond_stereochemistry=True
        )
    )
    aromatic = msm.select(topology, 'bond_is_aromatic==True', element='bond')
    assert aromatic
    assert all(
        value == pytest.approx(1.5)
        for value in msm.get(
            topology,
            element='bond',
            selection=aromatic,
            fractional_bond_order=True,
        )
    )
    assert all(
        pd.isna(value)
        for value in msm.get(
            topology, element='bond', selection=aromatic, bond_order=True
        )
    )


def test_rdkit_dative_direction_is_preserved_without_joining_components():
    mol = Chem.MolFromSmiles('[NH3]->[Cu+2]')

    topology = msm.convert(mol, to_form='molsysmt.Topology')

    assert msm.get(topology, element='bond', bond_type=True) == ['dative']
    assert msm.get(topology, element='bond', bond_donor_atom_index=True) == [0]
    assert msm.get(topology, element='bond', bond_acceptor_atom_index=True) == [1]
    assert msm.get(topology, element='bond', bond_joins_components=True) == [False]
    assert msm.get(topology, element='system', n_components=True) == 2


def test_rdkit_native_conversion_report_is_equivalent_for_supported_subset():
    mol = Chem.MolFromSmiles('c1ccccc1')

    _, report = msm.convert(
        mol, to_form='molsysmt.Topology', return_report=True
    )

    assert report.outcome == 'equivalent'
    assert report.issues == ()


def test_rdkit_isotope_is_preserved_and_no_longer_reported_as_loss():
    mol = Chem.MolFromSmiles('[13CH4]')

    topology, report = msm.convert(
        mol, to_form='molsysmt.Topology', return_report=True
    )

    assert msm.get(topology, element='atom', isotope=True) == [13]
    assert report.outcome == 'equivalent'
    assert report.issues == ()


def test_rdkit_native_roundtrip_preserves_supported_chemical_semantics():
    smiles = 'C[N+](C)(C)C.F[13C@](Cl)(Br)I.C/C=C/C.c1ccccc1'
    molecule = Chem.MolFromSmiles(smiles)
    charges = np.linspace(-0.4, 0.4, molecule.GetNumAtoms())
    for atom, charge in zip(molecule.GetAtoms(), charges):
        atom.SetDoubleProp('_MolSysMTPartialCharge', float(charge))

    native = msm.convert(molecule, to_form='molsysmt.MolSys')
    recovered = msm.convert(native, to_form='rdkit.Mol')

    assert Chem.MolToSmiles(recovered, isomericSmiles=True) == Chem.MolToSmiles(
        molecule, isomericSmiles=True
    )
    recovered_charges = msm.get(
        recovered, element='atom', partial_charge=True
    )
    np.testing.assert_allclose(
        puw.get_value(recovered_charges, to_unit='elementary_charge'), charges
    )


def test_rdkit_native_roundtrip_preserves_namespaced_atom_identity():
    molecule = Chem.MolFromSmiles('CO')
    molecule.GetAtomWithIdx(0).SetProp('_MolSysMTAtomID', 'carbon-alpha')
    molecule.GetAtomWithIdx(0).SetProp('_MolSysMTAtomName', 'CA')

    native = msm.convert(molecule, to_form='molsysmt.MolSys')
    recovered = msm.convert(native, to_form='rdkit.Mol')
    second_native = msm.convert(recovered, to_form='molsysmt.MolSys')

    assert native.topology.atoms['atom_id'].tolist() == ['carbon-alpha', '1']
    assert second_native.topology.atoms['atom_id'].tolist() == [
        'carbon-alpha', '1'
    ]
    assert second_native.topology.atoms['atom_name'].tolist() == ['CA', 'O1']

"""Testing RDKit subset, conformer, and optional-charge contracts."""

import numpy as np
import pytest

Chem = pytest.importorskip('rdkit.Chem')

import molsysmt as msm
from molsysmt import pyunitwizard as puw


def test_rdkit_conformer_selection_uses_positions_and_preserves_ids():
    molecule = Chem.AddHs(Chem.MolFromSmiles('CO'))
    first = Chem.Conformer(molecule.GetNumAtoms())
    first.SetId(7)
    second = Chem.Conformer(molecule.GetNumAtoms())
    second.SetId(19)
    for atom_index in range(molecule.GetNumAtoms()):
        first.SetAtomPosition(atom_index, (atom_index, 1.0, 2.0))
        second.SetAtomPosition(atom_index, (atom_index + 10.0, 3.0, 4.0))
    molecule.AddConformer(first, assignId=False)
    molecule.AddConformer(second, assignId=False)

    structures = msm.convert(
        molecule,
        to_form='molsysmt.Structures',
        selection=[2, 0],
        structure_indices=[1, 0],
    )

    assert structures.structure_id.tolist() == [19, 7]
    assert structures.coordinates.shape == (2, 2, 3)
    np.testing.assert_allclose(
        puw.get_value(structures.coordinates, to_unit='angstrom'),
        [[[12.0, 3.0, 4.0], [10.0, 3.0, 4.0]],
         [[2.0, 1.0, 2.0], [0.0, 1.0, 2.0]]],
    )


def test_rdkit_extract_preserves_an_intact_aromatic_component():
    molecule = Chem.MolFromSmiles('c1ccccc1.CCO')

    output = msm.extract(
        molecule,
        selection=list(range(6)),
        to_form='rdkit.Mol',
    )

    assert Chem.MolToSmiles(output) == 'c1ccccc1'
    assert all(atom.GetIsAromatic() for atom in output.GetAtoms())
    assert all(bond.GetIsAromatic() for bond in output.GetBonds())


def test_rdkit_optional_partial_charge_is_instance_aware_and_imported():
    molecule = Chem.MolFromSmiles('CO')
    assert not msm.has_attribute(molecule, 'partial_charge')

    for atom, charge in zip(molecule.GetAtoms(), [-0.2, 0.2]):
        atom.SetDoubleProp('_GasteigerCharge', charge)

    assert msm.has_attribute(molecule, 'partial_charge')
    charges = msm.get(molecule, element='atom', partial_charge=True)
    np.testing.assert_allclose(
        puw.get_value(charges, to_unit='elementary_charge'),
        [-0.2, 0.2],
    )
    molsys = msm.convert(molecule, to_form='molsysmt.MolSys')
    np.testing.assert_allclose(
        np.asarray(molsys.molecular_mechanics.partial_charge, dtype=float),
        [-0.2, 0.2],
    )

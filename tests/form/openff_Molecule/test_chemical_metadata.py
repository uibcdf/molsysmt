"""Testing canonical chemical-state conversion from OpenFF Molecule."""

import pytest

Molecule = pytest.importorskip('openff.toolkit.topology').Molecule

import molsysmt as msm


def test_openff_preserves_atom_charge_aromaticity_and_stereochemistry():
    molecule = Molecule.from_smiles('[NH3+][C@H](F)Cl')

    topology = msm.convert(molecule, to_form='molsysmt.Topology')

    assert msm.get(topology, element='atom', formal_charge=True)[0] == 1
    assert any(
        value in {'R', 'S', 'r', 's'}
        for value in msm.get(
            topology, element='atom', atom_stereochemistry=True
        )
        if value is not None
    )
    assert msm.get(topology, element='atom', atom_is_aromatic=True) == [
        atom.is_aromatic for atom in molecule.atoms
    ]


def test_openff_keeps_formal_fractional_order_and_aromaticity_independent():
    molecule = Molecule.from_smiles('c1ccccc1')
    molecule.bonds[0].fractional_bond_order = 1.25

    topology = msm.convert(molecule, to_form='molsysmt.Topology')

    assert msm.get(
        topology, element='bond', fractional_bond_order=True
    )[0] == pytest.approx(1.25)
    assert any(msm.get(topology, element='bond', bond_is_aromatic=True))
    assert set(msm.get(topology, element='bond', bond_type=True)) == {'covalent'}
    assert set(msm.get(topology, element='bond', bond_evidence=True)) == {'explicit'}
    assert any(msm.get(molecule, element='bond', bond_is_aromatic=True))


def test_openff_ez_stereo_limitation_is_reported_and_strictly_rejected():
    molecule = Molecule.from_smiles('F/C=C/F')

    _, report = msm.convert(
        molecule, to_form='molsysmt.Topology', return_report=True
    )

    assert report.outcome == 'lossy'
    assert {issue.attribute for issue in report.issues} == {'bond_stereochemistry'}
    with pytest.raises(msm.NotCompatibleConversionError):
        msm.convert(molecule, to_form='molsysmt.Topology', strict=True)

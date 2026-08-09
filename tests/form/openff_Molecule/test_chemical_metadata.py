"""Testing canonical chemical-state conversion from OpenFF Molecule."""

from importlib.util import find_spec

import pytest
import pandas as pd

if find_spec('openff.toolkit') is None:
    pytest.skip('openff-toolkit is not installed', allow_module_level=True)

from openff.toolkit.topology import Molecule

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


def test_openff_ez_stereo_and_reference_atoms_are_preserved():
    molecule = Molecule.from_smiles('F/C=C/F')

    topology, report = msm.convert(
        molecule, to_form='molsysmt.Topology', return_report=True
    )

    stereo = msm.get(topology, element='bond', bond_stereochemistry=True)
    stereo_references = msm.get(
        topology, element='bond', bond_stereo_atom_indices=True
    )
    stereo_index = next(
        index
        for index, value in enumerate(stereo)
        if not pd.isna(value) and value == 'E'
    )
    assert all(
        not pd.isna(value) for value in stereo_references[stereo_index]
    )
    assert report.outcome == 'equivalent'
    assert report.issues == ()

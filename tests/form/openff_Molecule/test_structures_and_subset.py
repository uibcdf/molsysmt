"""Testing instance-aware OpenFF conformer, charge, and subset contracts."""

import numpy as np
import pytest

openff_topology = pytest.importorskip('openff.toolkit.topology')
unit = pytest.importorskip('openff.units').unit

import molsysmt as msm
from molsysmt import pyunitwizard as puw


def _molecule_with_two_conformers():
    molecule = openff_topology.Molecule.from_smiles('CO')
    first = np.arange(molecule.n_atoms * 3, dtype=float).reshape(-1, 3)
    second = first + 100.0
    molecule.add_conformer(first * unit.angstrom)
    molecule.add_conformer(second * unit.angstrom)
    return molecule, first, second


def test_openff_conformers_are_exposed_with_structure_and_atom_selection():
    molecule, first, second = _molecule_with_two_conformers()

    assert msm.has_attribute(molecule, 'coordinates')
    structures = msm.convert(
        molecule,
        to_form='molsysmt.Structures',
        selection=[2, 0],
        structure_indices=[1, 0],
    )

    assert structures.structure_id.tolist() == [1, 0]
    np.testing.assert_allclose(
        puw.get_value(structures.coordinates, to_unit='angstrom'),
        [[second[2], second[0]], [first[2], first[0]]],
    )


def test_openff_partial_charges_are_instance_aware_and_delivered():
    molecule = openff_topology.Molecule.from_smiles('CO')
    assert not msm.has_attribute(molecule, 'partial_charge')
    charges = np.linspace(-0.3, 0.3, molecule.n_atoms)
    molecule.partial_charges = charges * unit.elementary_charge

    assert msm.has_attribute(molecule, 'partial_charge')
    observed = msm.get(molecule, element='atom', partial_charge=True)
    np.testing.assert_allclose(
        puw.get_value(observed, to_unit='elementary_charge'), charges
    )


def test_openff_extract_preserves_selected_conformers_and_partial_charges():
    molecule, first, second = _molecule_with_two_conformers()
    charges = np.linspace(-0.3, 0.3, molecule.n_atoms)
    molecule.partial_charges = charges * unit.elementary_charge
    reverse = list(reversed(range(molecule.n_atoms)))

    output = msm.extract(
        molecule,
        selection=reverse,
        structure_indices=[1],
        to_form='openff.Molecule',
    )

    assert output.n_conformers == 1
    np.testing.assert_allclose(
        output.conformers[0].m_as('angstrom'), second[reverse]
    )
    np.testing.assert_allclose(
        output.partial_charges.m_as('elementary_charge'), charges[reverse]
    )

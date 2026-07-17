"""Testing ParmEd frame, box, B-factor, and partial-charge delivery."""

import numpy as np
import pytest

parmed = pytest.importorskip('parmed')

import molsysmt as msm
from molsysmt import pyunitwizard as puw


def _two_frame_structure():
    structure = parmed.formats.mol2.Mol2File.parse(
        str(msm.systems['caffeine']['caffeine.mol2']), structure=True
    )
    first = np.asarray(structure.coordinates, dtype=np.float64)
    second = first + 10.0
    structure.coordinates = np.stack((first, second))
    structure.box = np.asarray(
        [[20.0, 21.0, 22.0, 90.0, 90.0, 90.0],
         [30.0, 31.0, 32.0, 90.0, 90.0, 90.0]],
        dtype=np.float64,
    )
    structure.atoms[0].bfactor = 12.5
    return structure, first, second


def test_parmed_delivers_selected_frames_atoms_boxes_and_b_factors():
    structure, first, second = _two_frame_structure()

    coordinates, box, b_factor = msm.get(
        structure,
        element='atom',
        selection=[2, 0],
        structure_indices=[1, 0],
        coordinates=True,
        box=True,
        b_factor=True,
    )

    np.testing.assert_allclose(
        puw.get_value(coordinates, to_unit='angstrom'),
        [[second[2], second[0]], [first[2], first[0]]],
    )
    np.testing.assert_allclose(
        puw.get_value(box, to_unit='angstrom')[:, [0, 1, 2], [0, 1, 2]],
        [[30.0, 31.0, 32.0], [20.0, 21.0, 22.0]],
    )
    np.testing.assert_allclose(
        puw.get_value(b_factor, to_unit='angstrom**2'),
        [[0.0, 12.5], [0.0, 12.5]],
    )


def test_parmed_partial_charge_is_mechanical_and_survives_native_conversion():
    structure, _, _ = _two_frame_structure()
    expected = np.asarray([atom.charge for atom in structure.atoms])

    observed = msm.get(structure, element='atom', partial_charge=True)
    np.testing.assert_allclose(
        puw.get_value(observed, to_unit='elementary_charge'), expected
    )
    native = msm.convert(structure, to_form='molsysmt.MolSys')
    np.testing.assert_allclose(
        np.asarray(native.molecular_mechanics.partial_charge, dtype=float),
        expected,
    )

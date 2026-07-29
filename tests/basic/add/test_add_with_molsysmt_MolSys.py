"""
Unit and regression test for the add module of the molsysmt package.
"""

import molsysmt as msm
import numpy as np
import pytest
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentLengthError
from molsysmt.native import Structures


def test_add_with_molsysmt_MolSys(proline_molsys, valine_molsys, lysine_molsys):
    molsys_A = proline_molsys
    molsys_B = valine_molsys
    molsys_C = lysine_molsys
    n_atoms_A = msm.get(molsys_A, element='system', n_atoms=True)
    n_atoms_B = msm.get(molsys_B, element='system', n_atoms=True)
    n_atoms_C = msm.get(molsys_C, element='system', n_atoms=True)
    msm.add(molsys_A, molsys_B)
    msm.add(molsys_A, molsys_C)
    n_atoms, n_structures = msm.get(molsys_A, element='system', n_atoms=True, n_structures=True)
    assert 'molsysmt.MolSys' == msm.get_form(molsys_A)
    assert n_atoms == n_atoms_A + n_atoms_B + n_atoms_C
    assert n_structures == 1


def test_add_with_molsysmt_MolSys_2(proline_molsys, valine_molsys):
    molsys_A = proline_molsys
    molsys_B = valine_molsys
    n_molecules_before = msm.get(molsys_A, n_molecules=True)
    molsys_new = msm.add(molsys_A, molsys_B, in_place=False)
    # molsys_A should remain unmodified
    assert msm.get(molsys_A, n_molecules=True) == n_molecules_before
    # molsys_new should be the modified version
    assert msm.get(molsys_new, n_molecules=True) == n_molecules_before + 1


def test_public_add_on_structures_uses_the_atom_axis_and_returns_a_scalar():
    target = Structures(
        coordinates=puw.quantity(np.zeros((1, 1, 3)), 'nm'),
        velocities=puw.quantity(np.ones((1, 1, 3)), 'nm/ps'),
    )
    source = Structures(
        coordinates=puw.quantity(np.full((1, 2, 3), 2.0), 'nm'),
        velocities=puw.quantity(np.full((1, 2, 3), 3.0), 'nm/ps'),
    )

    result = msm.add(target, source, in_place=False)

    assert isinstance(result, Structures)
    assert target.n_atoms == 1
    assert result.coordinates.shape == (1, 3, 3)
    assert result.velocities.shape == (1, 3, 3)


def test_public_add_processes_every_source_item():
    target = Structures(coordinates=puw.quantity(np.zeros((1, 1, 3)), 'nm'))
    sources = [
        Structures(coordinates=puw.quantity(np.ones((1, 1, 3)), 'nm')),
        Structures(coordinates=puw.quantity(np.full((1, 1, 3), 2.0), 'nm')),
    ]

    msm.add(target, sources)

    assert target.coordinates.shape == (1, 3, 3)
    np.testing.assert_allclose(
        puw.get_value(target.coordinates, to_unit='nm')[0, :, 0],
        [0.0, 1.0, 2.0],
    )


def test_molsys_add_is_atomic_when_structure_counts_do_not_match(
    proline_molsys,
    valine_molsys,
):
    source = valine_molsys.copy()
    source_coordinates = puw.get_value(source.structures.coordinates, to_unit='nm')
    source.structures = Structures(
        coordinates=puw.quantity(
            np.repeat(source_coordinates, 2, axis=0),
            'nm',
        )
    )
    original_n_atoms = proline_molsys.topology.n_atoms
    original_coordinates = proline_molsys.structures.coordinates.copy()

    with pytest.raises(ArgumentLengthError):
        msm.add(proline_molsys, source)

    assert proline_molsys.topology.n_atoms == original_n_atoms
    np.testing.assert_allclose(
        puw.get_value(proline_molsys.structures.coordinates, to_unit='nm'),
        puw.get_value(original_coordinates, to_unit='nm'),
    )

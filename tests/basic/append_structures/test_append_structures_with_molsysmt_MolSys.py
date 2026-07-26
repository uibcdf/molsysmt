"""
Unit and regression test for the concatenate module of the molsysmt package with molsysmt.MolSys
objects.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np
import pytest

from molsysmt._private.smonitor import (
    StructuralAttributeDropWarning,
    StructuralInconsistencyError,
)
from molsysmt.native import MolSys, Structures

def test_append_structures_with_molsysmt_MolSys_1(proline_molsys):
    molsys_A = proline_molsys
    molsys_B = msm.structure.translate(molsys_A, translation='[0.1, 0.1, 0.1] nanometers')
    molsys_C = msm.structure.translate(molsys_A, translation='[0.2, 0.2, 0.2] nanometers')
    n_atoms_A, n_structures_A = msm.get(molsys_A, element='system', n_atoms=True, n_structures=True)
    n_structures_B = msm.get(molsys_B, element='system', n_structures=True)
    n_structures_C = msm.get(molsys_C, element='system', n_structures=True)
    msm.append_structures(molsys_A, molsys_B)
    msm.append_structures(molsys_A, molsys_C)
    n_atoms, n_structures = msm.get(molsys_A, element='system', n_atoms=True, n_structures=True)
    assert 'molsysmt.MolSys'==msm.get_form(molsys_A)
    assert n_atoms == n_atoms_A
    assert n_structures == n_structures_A + n_structures_B + n_structures_C

def test_append_structures_with_molsysmt_MolSys_2(proline_molsys):
    molsys_A = proline_molsys
    molsys_B = msm.structure.translate(molsys_A, translation='[0.1, 0.1, 0.1] nanometers')
    molsys_C = msm.append_structures(molsys_A, molsys_B, in_place=False)
    n_atoms_A, n_structures_A = msm.get(molsys_A, element='system', n_atoms=True, n_structures=True)
    n_atoms_B, n_structures_B = msm.get(molsys_B, element='system', n_atoms=True, n_structures=True)
    n_atoms_C, n_structures_C = msm.get(molsys_C, element='system', n_atoms=True, n_structures=True)
    assert 'molsysmt.MolSys'==msm.get_form(molsys_A)
    assert n_atoms_C == n_atoms_A
    assert n_structures_C == n_structures_A + n_structures_B


def test_append_structures_accepts_coordinate_only_native_source(proline_molsys):
    source = Structures(
        coordinates=proline_molsys.structures.coordinates.copy(),
        skip_digestion=True,
    )
    initial_n_structures = proline_molsys.structures.n_structures

    msm.append_structures(proline_molsys, source)

    assert proline_molsys.structures.n_structures == initial_n_structures + 1
    assert msm.get(proline_molsys, structure_chemical_state_index=True) == [0, 0]


def test_append_structures_keeps_single_state_association_implicit():
    target = MolSys(n_atoms=1)
    target.structures.coordinates = msm.pyunitwizard.quantity(
        np.zeros((1, 1, 3)), 'nm'
    )
    source = Structures(
        coordinates=msm.pyunitwizard.quantity(np.ones((1, 1, 3)), 'nm'),
        skip_digestion=True,
    )

    msm.append_structures(target, source)

    assert target._structure_chemical_state_indices is None
    assert msm.get(target, structure_chemical_state_index=True) == [0, 0]


def test_append_structures_accepts_topology_free_xtc(md_1u19_pdb_molsys):
    xtc = systems['nglview']['md_1u19.xtc']
    expected = msm.get(
        xtc,
        element='atom',
        structure_indices=[0, 1],
        coordinates=True,
    )
    initial_n_structures = md_1u19_pdb_molsys.structures.n_structures

    with pytest.warns(
        StructuralAttributeDropWarning,
        match='time, b_factor, occupancy',
    ):
        msm.append_structures(
            md_1u19_pdb_molsys,
            xtc,
            structure_indices=[0, 1],
        )

    assert md_1u19_pdb_molsys.structures.n_structures == initial_n_structures + 2
    assert md_1u19_pdb_molsys.structures.time is None
    assert md_1u19_pdb_molsys.structures.occupancy is None
    assert np.allclose(
        msm.pyunitwizard.get_value(md_1u19_pdb_molsys.structures.coordinates[-2:]),
        msm.pyunitwizard.get_value(expected),
    )


def test_append_structures_rejects_coordinate_only_atom_count_mismatch(proline_molsys):
    source = Structures(
        coordinates=proline_molsys.structures.coordinates[:, :-1, :],
        skip_digestion=True,
    )

    with pytest.raises(StructuralInconsistencyError, match='do not match target'):
        msm.append_structures(proline_molsys, source)


def test_append_structures_strict_policy_preserves_target_on_rejection():
    target = Structures(
        coordinates=msm.pyunitwizard.quantity(np.zeros((1, 2, 3)), 'nm'),
        velocities=msm.pyunitwizard.quantity(np.ones((1, 2, 3)), 'nm/ps'),
        skip_digestion=True,
    )
    source = Structures(
        coordinates=msm.pyunitwizard.quantity(np.ones((2, 2, 3)), 'nm'),
        skip_digestion=True,
    )

    with pytest.raises(StructuralInconsistencyError, match='velocities'):
        msm.append_structures(target, source, attribute_policy='strict')

    assert target.n_structures == 1
    assert target.velocities is not None


def test_append_structures_dict_uses_the_same_alignment_policy():
    target = {
        'time': msm.pyunitwizard.quantity([0.0], 'ps'),
        'coordinates': msm.pyunitwizard.quantity(np.zeros((1, 2, 3)), 'nm'),
        'velocities': msm.pyunitwizard.quantity(np.ones((1, 2, 3)), 'nm/ps'),
    }
    source = Structures(
        coordinates=msm.pyunitwizard.quantity(np.ones((2, 2, 3)), 'nm'),
        skip_digestion=True,
    )

    with pytest.warns(StructuralAttributeDropWarning, match='time, velocities'):
        msm.append_structures(target, source)

    assert target['coordinates'].shape == (3, 2, 3)
    assert 'time' not in target
    assert 'velocities' not in target

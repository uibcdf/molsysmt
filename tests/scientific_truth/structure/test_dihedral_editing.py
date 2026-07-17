"""Analytic scientific truth tests for covalent dihedral editing."""

import numpy as np

import molsysmt as msm


_QUARTET = np.array([[0, 1, 2, 3]], dtype=int)


def _bonded_chain():
    """Build a non-degenerate five-atom chain with one explicit structure."""

    builder = msm.MolSysBuilder()
    atoms = [builder.add_atom(atom_name="C", atom_type="C") for _ in range(5)]
    builder.add_group(atoms, group_name="MOL")
    for atom_1, atom_2 in zip(atoms[:-1], atoms[1:]):
        builder.add_bond(atom_1, atom_2)
    coordinates = np.array(
        [[0.0, 1.0, 0.0], [0.0, 0.0, 0.0], [1.0, 0.0, 0.0],
         [1.0, 1.0, 1.0], [2.0, 1.0, 1.0]],
        dtype=np.float64,
    )
    builder.set_coordinates(coordinates * msm.pyunitwizard.unit("nm"))
    return builder.build()


def _coordinates(system):
    return msm.pyunitwizard.get_value(system.structures.coordinates, to_unit="nm")


def _angle(system):
    quantity = msm.structure.get_dihedral_angles(
        system, dihedral_quartets=_QUARTET, pbc=False, use_gpu=False
    )
    return msm.pyunitwizard.get_value(quantity, to_unit="radians")


def _pairwise_distances(coordinates):
    displacements = coordinates[:, None, :] - coordinates[None, :, :]
    return np.linalg.norm(displacements, axis=-1)


def test_set_dihedral_reaches_target_and_rigidly_rotates_moving_block(
    float64_kernel_atol,
):
    """Reach an explicit target while preserving the rotated block geometry."""

    system = _bonded_chain()
    before = _coordinates(system)[0]
    target = -1.2
    edited = msm.structure.set_dihedral_angles(
        system,
        dihedral_quartets=_QUARTET,
        angles=np.array([[target]]) * msm.pyunitwizard.unit("radians"),
        pbc=False,
        in_place=False,
    )
    after = _coordinates(edited)[0]

    np.testing.assert_allclose(
        _angle(edited), np.array([[target]]), rtol=0.0, atol=float64_kernel_atol
    )
    np.testing.assert_allclose(
        after[:3], before[:3], rtol=0.0, atol=float64_kernel_atol
    )
    np.testing.assert_allclose(
        _pairwise_distances(after[2:]),
        _pairwise_distances(before[2:]),
        rtol=0.0,
        atol=float64_kernel_atol,
    )


def test_shift_dihedral_adds_signed_increment_modulo_branch_cut(
    float64_kernel_atol,
):
    """Add a signed angular increment under the public wrapped convention."""

    system = _bonded_chain()
    initial = float(_angle(system)[0, 0])
    shift = 0.4
    edited = msm.structure.shift_dihedral_angles(
        system,
        dihedral_quartets=_QUARTET,
        shifts=shift * msm.pyunitwizard.unit("radians"),
        pbc=False,
        in_place=False,
    )
    expected = np.arctan2(np.sin(initial + shift), np.cos(initial + shift))

    np.testing.assert_allclose(
        _angle(edited), np.array([[expected]]), rtol=0.0, atol=float64_kernel_atol
    )

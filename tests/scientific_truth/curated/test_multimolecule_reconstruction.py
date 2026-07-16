"""Scientific truth tests on a curated solvated multi-molecule trajectory."""

import numpy as np
import pytest

import molsysmt as msm


md = pytest.importorskip("mdtraj")


def test_covalent_wrapping_reconstructs_real_solvent_molecules(
    external_float32_atol,
):
    """Recover oracle bond lengths after deliberate periodic image shifts."""

    trajectory_file = msm.systems['chicken villin HP35'][
        'traj_chicken_villin_HP35_solvated.h5'
    ]
    structure_indices = [0, 10, 19]
    molecular_system = msm.convert(
        trajectory_file,
        structure_indices=structure_indices,
        to_form='molsysmt.MolSys',
    )
    bonded_pairs = np.asarray(
        msm.get(
            molecular_system,
            element='atom',
            inner_bonded_atom_pairs=True,
        ),
        dtype=np.int64,
    )
    molecule_indices = np.asarray(
        msm.get(molecular_system, element='atom', molecule_index=True),
        dtype=np.int64,
    )
    assert np.unique(molecule_indices).size == 1257

    reference = md.load(str(trajectory_file))[structure_indices]
    expected_lengths = md.compute_distances(
        reference,
        bonded_pairs,
        periodic=True,
        opt=False,
    )

    coordinates = msm.pyunitwizard.get_value(
        msm.get(molecular_system, coordinates=True),
        to_unit='nm',
    ).copy()
    box = msm.pyunitwizard.get_value(
        msm.get(molecular_system, box=True),
        to_unit='nm',
    )
    solvent_molecules = np.unique(molecule_indices)[-3:]
    shifted_atoms = [
        np.flatnonzero(molecule_indices == molecule_index)[0]
        for molecule_index in solvent_molecules
    ]
    for frame_index, atom_index in enumerate(shifted_atoms):
        coordinates[frame_index, atom_index] += box[frame_index, frame_index]

    msm.set(
        molecular_system,
        coordinates=msm.pyunitwizard.quantity(coordinates, 'nm'),
    )
    broken_lengths = np.linalg.norm(
        coordinates[:, bonded_pairs[:, 1]] - coordinates[:, bonded_pairs[:, 0]],
        axis=2,
    )
    assert np.max(np.abs(broken_lengths - expected_lengths)) > 1.0

    wrapped = msm.pbc.wrap_to_pbc(
        molecular_system,
        keep_covalent_bonds=True,
        in_place=False,
    )
    wrapped_coordinates = msm.pyunitwizard.get_value(
        msm.get(wrapped, coordinates=True),
        to_unit='nm',
    )
    observed_lengths = np.linalg.norm(
        wrapped_coordinates[:, bonded_pairs[:, 1]]
        - wrapped_coordinates[:, bonded_pairs[:, 0]],
        axis=2,
    )

    np.testing.assert_allclose(
        observed_lengths,
        expected_lengths,
        rtol=0.0,
        atol=external_float32_atol,
    )

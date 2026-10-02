"""Validate protein aromatic geometries using fixed rings and covariance planes.

This bounds geometric observation claims on bundled coordinates and controlled
image translations. It is not an energy or universal aromaticity validation.
"""

import numpy as np
import pytest

import molsysmt as msm
from devtools.scripts.pi_pi_validation_systems import (
    cartesian_reference,
    observation_columns,
    prepare_system,
)

pytest.importorskip("rdkit")


@pytest.fixture(scope="module", params=["trp_cage", "villin"])
def aromatic_protein(request):
    return prepare_system(request.param)


def test_fixed_molecular_memberships_match_independent_rdkit_cycles(aromatic_protein):
    from rdkit import Chem

    system, reference, _, molecule = aromatic_protein
    cycles = {
        tuple(sorted(ring))
        for ring in Chem.GetSymmSSSR(molecule)
        if all(
            molecule.GetBondBetweenAtoms(int(a), int(b)).GetIsAromatic()
            for a, b in zip(list(ring), list(ring)[1:] + list(ring)[:1])
        )
    }
    assert cycles == {tuple(ring) for ring in reference["rings"]}
    actual = msm.physchem.get_aromatic_rings(system)
    assert {
        tuple(actual["atom_indices"][a:b])
        for a, b in zip(actual["atom_offsets"][:-1], actual["atom_offsets"][1:])
    } == cycles


@pytest.mark.parametrize("file_source", [False, True])
@pytest.mark.parametrize("heavy_mode", ["off", "force"])
@pytest.mark.parametrize(("distance", "offset"), [(0.6, 0.2), (1.2, 0.8)])
def test_protein_observations_match_exhaustive_covariance_reference(
    aromatic_protein,
    file_source,
    heavy_mode,
    distance,
    offset,
    tmp_path,
):
    system, reference, coordinates, _ = aromatic_protein
    expected = cartesian_reference(
        reference, coordinates, distance=distance, offset=offset
    )
    source = system
    if file_source:
        source = str(tmp_path / "aromatic.h5msm")
        msm.convert(system, to_form=source)
    with msm.configure.context(chunk_size=5):
        result = msm.interactions.pi_pi.get_pi_pi_interactions(
            source,
            f"{distance} nm",
            "30 degrees",
            f"{offset} nm",
            ".02 nm",
            pbc=False,
            heavy_mode=heavy_mode,
        )
    actual = observation_columns(result)
    assert actual.keys() == expected.keys()
    for key in expected:
        np.testing.assert_allclose(actual[key], expected[key], atol=1e-10, rtol=0)
    assert result.evaluated_structure_indices.tolist() == list(range(len(coordinates)))


def test_real_ensemble_periodic_images_reproduce_nonperiodic_reference():
    system, reference, coordinates, _ = prepare_system("villin")
    expected = cartesian_reference(reference, coordinates, distance=1.2, offset=0.8)
    assert expected, "The molecular periodic guard must exercise actual observations."
    box = np.array([[8.0, 0, 0], [1.0, 8.0, 0], [0.5, 0.25, 8.0]])
    moved = coordinates.copy()
    # Move one whole isolated ring, preserving every within-ring coordinate.
    moved[:, reference["rings"][0]] += box[0]
    system.structures.coordinates = msm.pyunitwizard.quantity(moved, "nm")
    system.structures.box = msm.pyunitwizard.quantity(
        np.repeat(box[None], len(moved), axis=0), "nm"
    )
    with msm.configure.context(chunk_size=3):
        result = msm.interactions.pi_pi.get_pi_pi_interactions(
            system,
            "1.2 nm",
            "30 degrees",
            ".8 nm",
            ".02 nm",
            heavy_mode="force",
        )
    actual = observation_columns(result)
    assert actual.keys() == expected.keys()
    assert np.any(result.image_vectors != 0)
    for key in expected:
        np.testing.assert_allclose(actual[key], expected[key], atol=1e-10, rtol=0)
    for occurrence, (frame, relation) in enumerate(
        zip(result.occurrence_structures, result.occurrence_relations)
    ):
        start = result.occurrence_image_offsets[occurrence]
        centers = [
            np.mean(
                moved[frame, part["atom_indices"]]
                + result.image_vectors[start + i] @ box,
                axis=0,
            )
            for i, part in enumerate(result.relation(relation)["participants"])
        ]
        np.testing.assert_allclose(
            np.linalg.norm(centers[1] - centers[0]),
            result.measurements["distance"][occurrence],
            atol=1e-12,
        )

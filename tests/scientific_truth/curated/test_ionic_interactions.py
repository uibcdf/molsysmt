"""Validate declared protein ionic states against independent memberships and geometry.

Evidence: versioned PDB coordinates, fixed participant manifest, RDKit SMARTS,
and exhaustive Cartesian reference distances. Protonation is a declared fixture
state, not inferred experimental truth. Scope is the bounded geometric method.
"""

import numpy as np
import pytest

import molsysmt as msm
from devtools.scripts.ionic_validation_systems import (
    cartesian_reference,
    observation_columns,
    prepare_system,
)

pytest.importorskip("rdkit")


@pytest.fixture(scope="module", params=["trp_cage", "villin"])
def ionic_protein(request):
    return prepare_system(request.param)


def _assert_observations(actual, expected, atol):
    assert actual.keys() == expected.keys()
    for key, value in expected.items():
        np.testing.assert_allclose(actual[key], value, atol=atol, rtol=0)


def test_real_protein_centers_match_curated_membership_and_rdkit(ionic_protein):
    from rdkit import Chem

    system, reference, _, molecule = ionic_protein
    actual = msm.physchem.get_charge_centers(system)
    expected = reference["centers"]
    assert len(actual["center_types"]) == len(expected)
    for index, center in enumerate(expected):
        a, b = actual["atom_offsets"][index : index + 2]
        c, d = actual["geometry_atom_offsets"][index : index + 2]
        np.testing.assert_array_equal(actual["atom_indices"][a:b], center["atoms"])
        np.testing.assert_array_equal(
            actual["geometry_atom_indices"][c:d], center["geometry"]
        )
        assert actual["center_types"][index] == center["kind"]
        assert (
            msm.pyunitwizard.get_value(actual["charges"], to_unit="e")[index]
            == center["charge"]
        )
    for kind, pattern in (
        ("carboxylate", "[CX3](=[OX1])[O-]"),
        ("guanidinium", "[CX3]([NX3])([NX3])=[N+X3]"),
    ):
        matches = molecule.GetSubstructMatches(Chem.MolFromSmarts(pattern))
        assert {tuple(sorted(match)) for match in matches} == {
            tuple(center["atoms"]) for center in expected if center["kind"] == kind
        }


@pytest.mark.parametrize("file_source", [False, True])
@pytest.mark.parametrize("mode", ["off", "force"])
@pytest.mark.parametrize("threshold", [0.4, 0.8])
def test_real_protein_observations_match_exhaustive_cartesian_oracle(
    ionic_protein,
    file_source,
    mode,
    threshold,
    tmp_path,
    float64_kernel_atol,
):
    system, reference, coordinates, _ = ionic_protein
    source = system
    if file_source:
        source = str(tmp_path / "protein.h5msm")
        msm.convert(system, to_form=source)
    expected = cartesian_reference(reference, coordinates, threshold)
    known_counts = {304: {0.4: 20, 0.8: 61}, 596: {0.4: 0, 0.8: 4}}
    assert len(expected) == known_counts[reference["atoms"]][threshold]
    with msm.configure.context(chunk_size=5):
        result = msm.interactions.ionic.get_ionic_interactions(
            source,
            f"{threshold} nm",
            pbc=False,
            heavy_mode=mode,
        )
    _assert_observations(
        observation_columns(result, reference), expected, float64_kernel_atol
    )
    assert result.n_interactions == len(expected)
    np.testing.assert_array_equal(
        result.evaluated_structure_indices, range(len(coordinates))
    )
    assert result.measure_units["distance"] == "nm"


@pytest.mark.parametrize("scope", ["internal", "incident", "between"])
def test_real_ensemble_scopes_and_nonconsecutive_frames(
    scope, tmp_path, float64_kernel_atol
):
    system, reference, coordinates, _ = prepare_system("trp_cage")
    first, second, frames = [162, 163, 164], [233, 234, 235, 236], [37, 0, 13, 37]
    if scope == "internal":
        first = first + second
    kwargs = {"selection": first, "selection_mode": scope, "structure_indices": frames}
    if scope == "between":
        kwargs["selection_2"] = second
    expected = cartesian_reference(
        reference,
        coordinates,
        0.4,
        frames=frames,
        selected=first,
        second=second,
        scope=scope,
    )
    path = str(tmp_path / "ensemble.h5msm")
    msm.convert(system, to_form=path)
    with msm.configure.context(chunk_size=2):
        result = msm.interactions.ionic.get_ionic_interactions(
            path,
            ".4 nm",
            pbc=False,
            heavy_mode="force",
            **kwargs,
        )
    _assert_observations(
        observation_columns(result, reference), expected, float64_kernel_atol
    )
    assert result.n_interactions == len(expected)
    np.testing.assert_array_equal(result.evaluated_structure_indices, [0, 13, 37])
    assert result.query(structure_indices=37).n_interactions == 0
    assert result.query(structure_indices=37).to_dict()[
        "evaluated_structure_indices"
    ].tolist() == [37]
    incident = result.query(atom_indices=[233], structure_indices=[13, 0, 13])
    assert incident.n_interactions == sum(
        frame in {0, 13} and "A:ARG16:guanidinium" in (positive, negative)
        for frame, positive, negative in expected
    )
    system.interactions = {"ionic": result}
    path = str(tmp_path / "named_result.h5msm")
    msm.convert(system, to_form=path)
    restored = msm.convert(path, to_form="molsysmt.MolSys").interactions["ionic"]
    _assert_observations(
        observation_columns(restored, reference), expected, float64_kernel_atol
    )
    np.testing.assert_array_equal(
        restored.query().to_dict()["occurrence_indices"],
        result.query().to_dict()["occurrence_indices"],
    )
    assert restored.parameters == result.parameters
    assert restored.software == result.software


def test_real_ensemble_periodic_images_reconstruct_independent_distances(
    float64_kernel_atol,
):
    system, reference, coordinates, _ = prepare_system("trp_cage")
    # Controlled image representation of real coordinates, not another MD dataset.
    box = np.array([[8.0, 0, 0], [1.0, 8.0, 0], [0.5, 0.25, 8.0]])
    moved = coordinates.copy()
    for center in reference["centers"]:
        if center["charge"] < 0:
            moved[:, center["atoms"]] += box[0]
    system.structures.coordinates = msm.pyunitwizard.quantity(moved, "nm")
    system.structures.box = msm.pyunitwizard.quantity(
        np.repeat(box[None], len(moved), axis=0), "nm"
    )
    expected = cartesian_reference(reference, coordinates, 0.4)
    with msm.configure.context(chunk_size=5):
        result = msm.interactions.ionic.get_ionic_interactions(
            system, ".4 nm", heavy_mode="force"
        )
    _assert_observations(
        observation_columns(result, reference), expected, float64_kernel_atol
    )
    assert result.n_interactions == len(expected) == 20
    assert result.image_vectors is not None and np.any(result.image_vectors != 0)
    for occurrence, (frame, relation) in enumerate(
        zip(result.occurrence_structures, result.occurrence_relations)
    ):
        positive, negative = result.relation_participant_offsets[
            relation : relation + 2
        ]
        assert negative - positive == 2
        references = []
        for participant in range(positive, negative):
            a, b = result.participant_atom_offsets[participant : participant + 2]
            membership = tuple(result.participant_atoms[a:b])
            center = next(
                c for c in reference["centers"] if tuple(c["atoms"]) == membership
            )
            image_start = result.occurrence_image_offsets[occurrence]
            image = result.image_vectors[image_start + participant - positive]
            references.append(moved[frame, center["geometry"]] + image @ box)
        delta = references[0][:, None] - references[1][None]
        observed = np.sqrt((delta * delta).sum(axis=-1)).min()
        np.testing.assert_allclose(
            observed,
            result.measurements["distance"][occurrence],
            atol=float64_kernel_atol,
            rtol=0,
        )

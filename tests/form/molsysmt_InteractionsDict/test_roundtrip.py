"""Round-trip contracts for columnar interaction dictionary forms."""

import numpy as np
import pytest

import molsysmt as msm


def test_empty_evaluated_frames_roundtrip_without_occurrence_objects():
    result = msm.Interactions.from_records(
        [], n_atoms=4, n_structures=5,
        evaluated_structure_indices=[1, 3], method="example",
    )

    encoded = msm.convert(result, to_form="molsysmt.InteractionsDict")
    decoded = msm.convert(encoded, to_form="molsysmt.Interactions")

    assert msm.get_form(result) == "molsysmt.Interactions"
    assert msm.get_form(encoded) == "molsysmt.InteractionsDict"
    assert encoded.data["schema"] == "molsysmt.interactions_dict"
    assert encoded.data["version"] == 1
    assert encoded.data["occurrence_structures"].shape == (0,)
    assert encoded.data["atom_source_indices"] is None
    assert encoded.data["structure_source_indices"] is None
    assert msm.get(encoded, n_atoms=True, n_structures=True) == [4, 5]
    assert decoded.query(structure_indices=[3, 1, 3]).n_interactions == 0
    np.testing.assert_array_equal(decoded.evaluated_structure_indices, [1, 3])


def test_compound_roles_images_measurements_and_source_roundtrip():
    records = [
        {
            "structure_index": 1,
            "interaction_type": "pi_pi",
            "participants": [
                {"role": "ring", "atom_indices": [0, 1, 2]},
                {"role": "ring", "atom_indices": [3, 4, 5]},
            ],
            "images": [[0, 0, 0], [1, 0, 0]],
            "measurements": {"distance": 0.35},
            "evidence": "observed_geometry",
        },
        {
            "structure_index": 4,
            "interaction_type": "hbond",
            "participants": [
                {"role": "donor", "atom_indices": [0]},
                {"role": "hydrogen", "atom_indices": [1]},
                {"role": "acceptor", "atom_indices": [6]},
            ],
            "images": [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            "measurements": {"distance": 0.21},
            "evidence": "inferred_geometry",
        },
    ]
    original = msm.Interactions.from_records(
        records, n_atoms=7, n_structures=6,
        evaluated_structure_indices=[1, 2, 4], method="detector",
        measure_units={"distance": "nm"},
        parameters={"cutoff_nm": 0.4}, source_id="toy",
        atom_source_indices=[10, 3, 5, 12, 8, 1, 6],
        structure_source_indices=[8, 4, 7, 0, 2, 9],
        source_n_atoms=13, source_n_structures=10,
    )

    encoded = msm.convert(original, to_form="molsysmt.InteractionsDict")
    decoded = msm.convert(encoded, to_form="molsysmt.Interactions")

    assert isinstance(encoded.data["occurrence_relations"], np.ndarray)
    assert isinstance(encoded.data["atom_source_indices"], np.ndarray)
    assert isinstance(encoded.data["structure_source_indices"], np.ndarray)
    assert encoded.data["occurrence_relations"].shape == (2,)
    assert decoded.n_interactions == 2
    assert decoded.query(structure_indices=[2]).n_interactions == 0
    assert decoded.query(structure_indices=[4, 1, 4]).n_interactions == 2
    assert decoded.query(atom_indices=[0, 1, 2], mode="internal").n_interactions == 0
    assert decoded.source_id == "toy"
    np.testing.assert_array_equal(
        decoded.atom_source_indices, [10, 3, 5, 12, 8, 1, 6]
    )
    np.testing.assert_array_equal(
        decoded.structure_source_indices, [8, 4, 7, 0, 2, 9]
    )
    assert decoded.source_n_atoms == 13
    assert decoded.source_n_structures == 10
    assert decoded.parameters == {"cutoff_nm": 0.4}
    assert decoded.measure_units == {"distance": "nm"}
    np.testing.assert_array_equal(decoded.image_vectors, original.image_vectors)
    np.testing.assert_array_equal(
        decoded.occurrence_image_offsets, original.occurrence_image_offsets
    )
    np.testing.assert_array_equal(
        decoded.measurements["distance"], original.measurements["distance"]
    )
    assert decoded.relation(0)["interaction_type"] == original.relation(0)[
        "interaction_type"
    ]
    for observed, expected in zip(
        decoded.relation(0)["participants"], original.relation(0)["participants"]
    ):
        assert observed["role"] == expected["role"]
        np.testing.assert_array_equal(observed["atom_indices"], expected["atom_indices"])


def test_dictionary_copy_is_independent_and_invalid_evidence_fails():
    original = msm.Interactions.from_records(
        [{
            "structure_index": 0,
            "interaction_type": "ionic",
            "participants": [
                {"role": "cation", "atom_indices": [0]},
                {"role": "anion", "atom_indices": [1]},
            ],
        }],
        n_atoms=2, n_structures=1,
        evaluated_structure_indices=[0], method="example",
    )
    encoded = msm.convert(original, to_form="molsysmt.InteractionsDict")
    copied = msm.convert(encoded, to_form="molsysmt.InteractionsDict")

    copied.data["occurrence_evidence"][0] = 99
    assert encoded.data["occurrence_evidence"][0] == 0
    with pytest.raises(ValueError, match="evidence"):
        msm.convert(copied, to_form="molsysmt.Interactions")


def test_declared_evaluation_scope_survives_columnar_roundtrip():
    original = msm.Interactions.from_records(
        [], n_atoms=5, n_structures=2, evaluated_structure_indices=[0],
        method="scoped", evaluation_mode="between",
        evaluation_atom_indices=[0, 1], evaluation_atom_indices_b=[3, 4],
        evaluation_universe_indices=[0, 1, 3, 4],
    )
    encoded = msm.convert(original, to_form="molsysmt.InteractionsDict")
    restored = msm.convert(encoded, to_form="molsysmt.Interactions")
    assert encoded.data["evaluation_mode"] == "between"
    assert restored.evaluation_mode == "between"
    np.testing.assert_array_equal(restored.evaluation_scope["atom_indices"], [0, 1])
    np.testing.assert_array_equal(restored.evaluation_scope["atom_indices_b"], [3, 4])
    np.testing.assert_array_equal(restored.evaluation_scope["universe_indices"],
                                  [0, 1, 3, 4])


def test_conversion_rejects_structure_selection_instead_of_ignoring_it():
    original = msm.Interactions.from_records(
        [], n_atoms=2, n_structures=3,
        evaluated_structure_indices=[0, 2], method="example",
    )

    with pytest.raises(ValueError, match="requires all"):
        msm.convert(
            original, to_form="molsysmt.InteractionsDict", structure_indices=[2]
        )

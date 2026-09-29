"""Exercise the public interaction contract across MolSys and H5MSM 0.5."""

import numpy as np

import molsysmt as msm
from molsysmt.native import MolSys


def _record(structure_index, interaction_type, participants, distance, evidence,
            images=None):
    return {
        "structure_index": structure_index,
        "interaction_type": interaction_type,
        "participants": [
            {"role": role, "atom_indices": atoms} for role, atoms in participants
        ],
        "measurements": {"distance": distance},
        "evidence": evidence,
        "images": images if images is not None else [[0, 0, 0]] * len(participants),
    }


def _analysis():
    hydrogen_bond = [
        ("donor", [0]), ("hydrogen", [1]), ("acceptor", [2]),
    ]
    return msm.Interactions.from_records(
        [
            _record(0, "hbond", hydrogen_bond, 0.20, "geometry"),
            _record(0, "pi_pi", [
                ("ring", [3, 4, 5]), ("ring", [6, 7, 8]),
            ], 0.36, "geometry"),
            _record(2, "disulfide_candidate", [
                ("sulfur", [9]), ("sulfur", [10]),
            ], 0.19, "proximity"),
            _record(4, "hbond", hydrogen_bond, 0.21, "geometry",
                    images=[[0, 0, 0], [0, 0, 0], [1, 0, 0]]),
            _record(4, "hbond", hydrogen_bond, 0.22, "independent_observation"),
        ],
        n_atoms=11,
        n_structures=6,
        evaluated_structure_indices=[0, 1, 2, 4],
        method="synthetic_review_fixture",
        measure_units={"distance": "nm"},
        source_id="viewer_review_fixture",
        atom_source_indices=[11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        structure_source_indices=[8, 6, 4, 2, 0, -1],
        source_n_atoms=12,
        source_n_structures=9,
    )


def _assert_queries(result):
    selected = result.query(structure_indices=[4, 1, 0, 4, 3]).to_dict()
    np.testing.assert_array_equal(selected["structure_indices"], [4, 4, 0, 0])
    np.testing.assert_array_equal(selected["occurrence_indices"], [3, 4, 0, 1])
    np.testing.assert_array_equal(
        selected["evaluated_structure_indices"], [4, 1, 0]
    )
    assert result.query(structure_indices=[1]).n_interactions == 0
    assert result.query(structure_indices=[1]).to_dict()[
        "occurrence_indices"
    ].dtype == np.int64
    assert result.query(structure_indices=[3]).to_dict()[
        "evaluated_structure_indices"
    ].size == 0
    assert result.query(atom_indices=[0], mode="incident").n_interactions == 3
    assert result.query([0], [0], mode="cross").n_interactions == 1
    assert result.query([0], [0, 1, 2], mode="internal").n_interactions == 1
    assert result.query([0], [3, 4, 5], mode="internal").n_interactions == 0
    assert result.query([0], [3, 4, 5, 6, 7, 8], mode="internal").n_interactions == 1
    assert result.between([3, 4, 5], [6, 7, 8], exclusive=True).n_interactions == 1
    np.testing.assert_array_equal(
        result.query(atom_indices=[9]).to_dict()["structure_indices"], [2]
    )
    assert result.measure_units == {"distance": "nm"}
    assert result.method == "synthetic_review_fixture"
    assert result.source_id == "viewer_review_fixture"
    np.testing.assert_array_equal(
        result.atom_source_indices, [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    )
    np.testing.assert_array_equal(
        result.structure_source_indices, [8, 6, 4, 2, 0, -1]
    )


def _assert_same_observations(expected, observed):
    expected_columns = expected.query(structure_indices=[4, 1, 0, 4, 3]).to_dict()
    observed_columns = observed.query(structure_indices=[4, 1, 0, 4, 3]).to_dict()
    for name in (
        "evaluated_structure_indices", "occurrence_indices",
        "structure_indices", "relation_indices",
        "evidence", "image_offsets", "image_vectors",
    ):
        np.testing.assert_array_equal(observed_columns[name], expected_columns[name])
    np.testing.assert_allclose(
        observed_columns["measurements"]["distance"],
        expected_columns["measurements"]["distance"],
    )
    assert observed_columns["measure_units"] == expected_columns["measure_units"]
    for relation_index in np.unique(expected_columns["relation_indices"]):
        expected_relation = expected.relation(relation_index)
        observed_relation = observed.relation(relation_index)
        assert observed_relation["interaction_type"] == expected_relation["interaction_type"]
        for expected_participant, observed_participant in zip(
            expected_relation["participants"], observed_relation["participants"]
        ):
            assert observed_participant["role"] == expected_participant["role"]
            np.testing.assert_array_equal(
                observed_participant["atom_indices"],
                expected_participant["atom_indices"],
            )


def test_public_queries_survive_native_attachment_and_h5msm_roundtrip(tmp_path):
    molsys = MolSys(n_atoms=11)
    molsys.structures.append(
        coordinates=np.zeros((6, 11, 3)), skip_digestion=True
    )
    molsys.interactions = {"review": _analysis()}
    filename = str(tmp_path / "viewer_review.h5msm")

    _assert_queries(molsys.interactions["review"])
    msm.h5msm.write(molsys, filename)
    restored = msm.h5msm.read(filename)
    _assert_queries(restored.interactions["review"])
    _assert_same_observations(molsys.interactions["review"],
                              restored.interactions["review"])

    layer = msm.h5msm.read_layers(
        filename, layers="interactions", analysis_names="review"
    )["interactions"]
    _assert_queries(layer["review"])
    _assert_same_observations(molsys.interactions["review"], layer["review"])

    subset = restored.extract(
        atom_indices=[0, 1, 2], structure_indices=[4, 1, 0],
        skip_digestion=True,
    ).interactions["review"]
    np.testing.assert_array_equal(subset.atom_source_indices, [11, 10, 9])
    np.testing.assert_array_equal(subset.structure_source_indices, [0, 6, 8])
    np.testing.assert_array_equal(subset.evaluated_structure_indices, [0, 1, 2])
    np.testing.assert_array_equal(
        subset.query(atom_indices=[0]).to_dict()["structure_indices"],
        [0, 0, 2],
    )

    restored.interactions = {
        "review": restored.interactions["review"].invalidate_structures([4])
    }
    invalidated_filename = str(tmp_path / "invalidated_review.h5msm")
    msm.h5msm.write(restored, invalidated_filename)
    invalidated = msm.h5msm.read(invalidated_filename).interactions["review"]
    assert invalidated.query(structure_indices=[4]).n_interactions == 0
    assert invalidated.query(structure_indices=[4]).to_dict()[
        "evaluated_structure_indices"
    ].size == 0
    np.testing.assert_array_equal(
        invalidated.query(structure_indices=[1]).to_dict()[
            "evaluated_structure_indices"
        ], [1],
    )
    assert invalidated.query(structure_indices=[0]).n_interactions == 2


def test_public_convert_preserves_multiple_named_analyses_and_sparse_columns(tmp_path):
    molsys = MolSys(n_atoms=11)
    molsys.structures.append(
        coordinates=np.zeros((6, 11, 3)), skip_digestion=True
    )
    empty = msm.Interactions.from_records(
        [], n_atoms=11, n_structures=6,
        evaluated_structure_indices=[1, 5], method="empty_review_fixture",
        parameters={"criterion": "synthetic"}, measure_units={"distance": "nm"},
        evaluation_atom_indices=[0, 1], evaluation_universe_indices=[0, 1],
    )
    molsys.interactions = {"review": _analysis(), "empty": empty}
    filename = tmp_path / "converted_review.h5msm"

    msm.convert(molsys, to_form="file:h5msm", output_filename=filename)
    restored = msm.convert(filename, to_form="molsysmt.MolSys")

    assert set(restored.interactions) == {"review", "empty"}
    review = restored.interactions["review"]
    _assert_queries(review)
    _assert_same_observations(molsys.interactions["review"], review)
    assert review.parameters == molsys.interactions["review"].parameters
    assert review.source_n_atoms == 12
    assert review.source_n_structures == 9
    restored_empty = restored.interactions["empty"]
    assert restored_empty.method == empty.method
    assert restored_empty.parameters == empty.parameters
    assert restored_empty.measure_units == empty.measure_units
    np.testing.assert_array_equal(restored_empty.evaluated_structure_indices, [1, 5])
    assert restored_empty.evaluation_scope["mode"] == "internal"
    np.testing.assert_array_equal(restored_empty.evaluation_scope["atom_indices"], [0, 1])
    np.testing.assert_array_equal(restored_empty.evaluation_scope["universe_indices"], [0, 1])
    assert restored_empty.query(structure_indices=[1]).n_interactions == 0
    assert restored_empty.query(structure_indices=[0]).to_dict()[
        "evaluated_structure_indices"
    ].size == 0
    assert restored_empty.to_dict()["measurements"]["distance"].shape == (0,)

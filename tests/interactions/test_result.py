"""Contract tests for sparse interaction results."""

import numpy as np
import pytest

import molsysmt as msm


def _record(frame, kind, participants, **measurements):
    return {
        "structure_index": frame,
        "interaction_type": kind,
        "participants": [
            {"role": role, "atom_indices": atoms} for role, atoms in participants
        ],
        "measurements": measurements,
    }


@pytest.fixture
def interactions():
    records = [
        _record(0, "hbond", [("donor", [0]), ("hydrogen", [1]),
                             ("acceptor", [2])], distance=0.20),
        _record(0, "pi_pi", [("ring", [3, 4, 5]),
                              ("ring", [6, 7, 8])], distance=0.36),
        _record(2, "disulfide_candidate", [("sulfur", [9]),
                                             ("sulfur", [10])], distance=0.19),
        _record(4, "four_body", [("a", [0]), ("b", [3]),
                                 ("c", [6]), ("d", [11])], distance=0.50),
        _record(4, "hbond", [("donor", [0]), ("hydrogen", [1]),
                             ("acceptor", [2])], distance=0.21),
    ]
    return msm.Interactions.from_records(
        records, n_atoms=12, n_structures=6,
        evaluated_structure_indices=[0, 1, 2, 4],
        method="synthetic", measure_units={"distance": "nm"},
        parameters={"threshold": 0.6}, source_id="fixture",
    )


def test_nonconsecutive_structure_order_duplicates_and_empty(interactions):
    selected = interactions.query(structure_indices=[4, 1, 0, 4, 3])
    columns = selected.to_dict()
    np.testing.assert_array_equal(columns["evaluated_structure_indices"], [4, 1, 0])
    np.testing.assert_array_equal(columns["structure_indices"], [4, 4, 0, 0])
    assert selected.n_interactions == 4
    empty = interactions.query(structure_indices=[1])
    assert empty.n_interactions == 0
    assert empty.to_dict()["structure_indices"].dtype == np.int64
    np.testing.assert_array_equal(empty.to_dict()["evaluated_structure_indices"], [1])
    assert interactions.query(structure_indices=[3]).to_dict()[
        "evaluated_structure_indices"
    ].size == 0


def test_incident_internal_cross_include_all_participant_atoms(interactions):
    frame = [0]
    assert interactions.query(frame, [0], "incident").n_interactions == 1
    assert interactions.query(frame, [0], "cross").n_interactions == 1
    assert interactions.query(frame, [0], "internal").n_interactions == 0
    assert interactions.query(frame, [0, 1, 2], "internal").n_interactions == 1
    assert interactions.query(frame, [3], "incident").n_interactions == 1
    assert interactions.query(frame, [3, 4, 5], "internal").n_interactions == 0
    assert interactions.query(frame, [3, 4, 5, 6, 7, 8], "internal").n_interactions == 1
    assert interactions.query([4], [0, 3, 6, 11], "internal").n_interactions == 1


def test_between_disjoint_sets_and_exclusive_scope(interactions):
    pair = interactions.between([9], [10], structure_indices=[2])
    assert pair.n_interactions == 1
    assert pair.relation(pair.to_dict()["relation_indices"][0])["interaction_type"] == (
        "disulfide_candidate"
    )
    assert interactions.between([0], [2], structure_indices=[0]).n_interactions == 1
    assert interactions.between([0], [2], structure_indices=[0], exclusive=True
                                ).n_interactions == 0
    assert interactions.between([0, 1], [2], structure_indices=[0], exclusive=True
                                ).n_interactions == 1
    assert interactions.between([3, 4, 5], [6, 7, 8], structure_indices=[0],
                                exclusive=True).n_interactions == 1
    with pytest.raises(ValueError, match="disjoint"):
        interactions.between([0, 1], [1, 2])


def test_declared_evaluation_scope_distinguishes_empty_from_unsearched_atoms(tmp_path):
    pair = _record(0, "pair", [("a", [0]), ("b", [2])])
    options = dict(n_atoms=5, n_structures=2,
                   evaluated_structure_indices=[0, 1], method="scoped")
    incident = msm.Interactions.from_records(
        [pair], evaluation_mode="incident", evaluation_atom_indices=[0],
        evaluation_universe_indices=[0, 1, 2], **options,
    )
    assert incident.query(structure_indices=[1]).n_interactions == 0
    np.testing.assert_array_equal(incident.evaluation_scope["atom_indices"], [0])
    np.testing.assert_array_equal(incident.evaluation_scope["universe_indices"],
                                  [0, 1, 2])
    projected = incident.remap(atom_indices=[2, 0, 4])
    np.testing.assert_array_equal(projected.evaluation_scope["atom_indices"], [1])
    np.testing.assert_array_equal(projected.evaluation_scope["universe_indices"], [0, 1])
    assert projected.n_interactions == 1
    path = tmp_path / "scoped.h5i"
    projected.save(path)
    loaded = msm.Interactions.load(path)
    assert loaded.evaluation_mode == "incident"
    np.testing.assert_array_equal(loaded.evaluation_scope["universe_indices"], [0, 1])
    with pytest.raises(ValueError, match="outside the evaluated universe"):
        msm.Interactions.from_records(
            [pair], evaluation_universe_indices=[0, 1], **options
        )
    with pytest.raises(ValueError, match="does not satisfy"):
        msm.Interactions.from_records(
            [pair], evaluation_mode="incident", evaluation_atom_indices=[1], **options
        )

    internal = msm.Interactions.from_records(
        [pair], evaluation_universe_indices=[0, 2], **options
    )
    assert internal.evaluation_atom_indices is None
    np.testing.assert_array_equal(internal.evaluation_scope["atom_indices"], [0, 2])
    assert internal.remap().evaluation_atom_indices is None
    assert internal.remap().evaluation_universe_indices is not None
    full_copy = msm.Interactions.from_records([pair], **options).remap()
    assert full_copy.evaluation_atom_indices is None
    assert full_copy.evaluation_universe_indices is None


def test_between_evaluation_scope_accepts_compound_participants():
    ring_pair = _record(0, "pi_pi", [("ring", [0, 1, 2]),
                                         ("ring", [3, 4, 5])])
    result = msm.Interactions.from_records(
        [ring_pair], n_atoms=7, n_structures=1,
        evaluated_structure_indices=[0], method="rings",
        evaluation_mode="between", evaluation_atom_indices=[0, 1, 2],
        evaluation_atom_indices_b=[3, 4, 5],
        evaluation_universe_indices=[0, 1, 2, 3, 4, 5],
    )
    assert result.n_interactions == 1
    np.testing.assert_array_equal(result.evaluation_scope["atom_indices_b"], [3, 4, 5])
    assert result.remap(atom_indices=[0, 1, 2]).n_interactions == 0


def test_atom_queries_across_trajectory_and_chaining(interactions):
    selected = interactions.query(atom_indices=[0], interaction_types=["hbond"])
    np.testing.assert_array_equal(selected.to_dict()["structure_indices"], [0, 4])
    np.testing.assert_array_equal(interactions.query(
        structure_indices=[4, 0, 4], atom_indices=[0],
        interaction_types="hbond",
    ).to_dict()["structure_indices"], [4, 0])
    np.testing.assert_array_equal(selected.query(structure_indices=[4]).to_dict()[
        "structure_indices"
    ], [4])
    assert interactions.query(atom_indices=[]).n_interactions == 0
    assert interactions.query(interaction_types=["absent"]).n_interactions == 0


def test_relation_ids_and_occurrence_order_do_not_depend_on_input_order():
    records = [
        _record(2, "pair", [("first", [4]), ("second", [1])], distance=0.3),
        _record(0, "hbond", [("donor", [0]), ("hydrogen", [2]),
                              ("acceptor", [3])], distance=0.2),
        _record(2, "hbond", [("donor", [0]), ("hydrogen", [2]),
                              ("acceptor", [3])], distance=0.4),
    ]
    options = dict(n_atoms=5, n_structures=3, evaluated_structure_indices=[0, 2],
                   method="synthetic", measure_units={"distance": "nm"})
    forward = msm.Interactions.from_records(records, **options)
    reverse = msm.Interactions.from_records(reversed(records), **options)
    assert forward.relation_types == reverse.relation_types
    np.testing.assert_array_equal(forward.occurrence_relations,
                                  reverse.occurrence_relations)
    np.testing.assert_array_equal(forward.occurrence_structures,
                                  reverse.occurrence_structures)
    np.testing.assert_array_equal(forward.measurements["distance"],
                                  reverse.measurements["distance"])


def test_round_trip_preserves_sparse_contract(interactions, tmp_path):
    path = tmp_path / "interactions.h5i"
    interactions.save(path)
    loaded = msm.Interactions.load(path)
    np.testing.assert_array_equal(loaded.to_dict()["structure_indices"],
                                  interactions.to_dict()["structure_indices"])
    np.testing.assert_allclose(loaded.to_dict()["measurements"]["distance"],
                               interactions.to_dict()["measurements"]["distance"])
    assert loaded.measure_units == {"distance": "nm"}
    assert loaded.method == "synthetic"
    assert loaded.source_id == "fixture"
    ring_relation = next(index for index, kind in enumerate(loaded.relation_types)
                         if kind == "pi_pi")
    assert loaded.relation(ring_relation)["participants"][0]["atom_indices"].tolist() == [3, 4, 5]
    assert loaded.query(structure_indices=[1]).n_interactions == 0
    assert loaded.query(atom_indices=[9], mode="incident").n_interactions == 1


def test_embedded_group_codec_keeps_named_analyses_independent(interactions, tmp_path):
    import h5py

    empty = msm.Interactions.from_records(
        [], n_atoms=12, n_structures=6,
        evaluated_structure_indices=[1], method="empty",
        evaluation_mode="incident", evaluation_atom_indices=[0],
    )
    path = tmp_path / "grouped.h5"
    with h5py.File(path, "w") as file:
        parent = file.create_group("interactions")
        interactions._write_group(parent.create_group("observed"))
        empty._write_group(parent.create_group("empty"))
    with h5py.File(path, "r") as file:
        observed = msm.Interactions._read_group(file["interactions/observed"])
        restored_empty = msm.Interactions._read_group(file["interactions/empty"])
        np.testing.assert_array_equal(observed.occurrence_structures,
                                      interactions.occurrence_structures)
        assert restored_empty.n_interactions == 0
        np.testing.assert_array_equal(restored_empty.evaluated_structure_indices, [1])
        assert restored_empty.evaluation_mode == "incident"
        np.testing.assert_array_equal(
            restored_empty.evaluation_scope["atom_indices"], [0]
        )
    with h5py.File(path, "r+") as file:
        file["interactions/empty"].attrs["schema_version"] = 999
    with h5py.File(path, "r") as file:
        with pytest.raises(ValueError, match="schema version"):
            msm.Interactions._read_group(file["interactions/empty"])


def test_rejects_missing_units_and_out_of_range_indices():
    record = _record(0, "pair", [("a", [0]), ("b", [2])], distance=0.2)
    with pytest.raises(ValueError, match="unit"):
        msm.Interactions.from_records([record], n_atoms=3, n_structures=1,
                                      evaluated_structure_indices=[0], method="test")
    with pytest.raises(ValueError, match="outside"):
        msm.Interactions.from_records([record], n_atoms=2, n_structures=1,
                                      evaluated_structure_indices=[0], method="test",
                                      measure_units={"distance": "nm"})


def test_periodic_images_round_trip_and_sparse_projection(tmp_path):
    record = _record(0, "pair", [("first", [0]), ("second", [1])])
    record["images"] = [[0, 0, 0], [1, 0, 0]]
    result = msm.Interactions.from_records(
        [record], n_atoms=2, n_structures=2,
        evaluated_structure_indices=[0, 1], method="periodic",
    )
    columns = result.query(structure_indices=[0]).to_dict()
    np.testing.assert_array_equal(columns["image_offsets"], [0, 2])
    np.testing.assert_array_equal(columns["image_vectors"], [[0, 0, 0], [1, 0, 0]])
    path = tmp_path / "periodic.h5i"
    result.save(path)
    loaded = msm.Interactions.load(path)
    np.testing.assert_array_equal(loaded.to_dict()["image_vectors"],
                                  columns["image_vectors"])


def test_mixed_missing_and_explicit_periodic_images_fail_instead_of_filling_zeros():
    explicit = _record(0, "pair", [("a", [0]), ("b", [1])])
    explicit["images"] = [[0, 0, 0], [1, 0, 0]]
    missing = _record(1, "pair", [("a", [0]), ("b", [2])])

    with pytest.raises(ValueError, match="every occurrence or none"):
        msm.Interactions.from_records(
            [explicit, missing], n_atoms=3, n_structures=2,
            evaluated_structure_indices=[0, 1], method="mixed-images",
        )


def test_evidence_is_not_truncated_and_unknown_schema_is_rejected(tmp_path):
    import h5py

    record = _record(0, "pair", [("a", [0]), ("b", [1])])
    record["evidence"] = "declared_source_" + "x" * 80
    result = msm.Interactions.from_records(
        [record], n_atoms=2, n_structures=1,
        evaluated_structure_indices=[0], method="source",
    )
    path = tmp_path / "evidence.h5i"
    result.save(path)
    assert msm.Interactions.load(path).to_dict()["evidence"][0] == record["evidence"]
    with h5py.File(path, "r+") as file:
        file.attrs["schema_version"] = 999
    with pytest.raises(ValueError, match="schema version"):
        msm.Interactions.load(path)


def test_remap_preserves_sparse_coverage_and_repeated_output_structures(interactions):
    remapped = interactions.remap(
        atom_indices=[2, 0, 1], structure_indices=[4, 1, 0, 4]
    )

    assert remapped.n_atoms == 3
    assert remapped.n_structures == 4
    assert remapped.source_id == "fixture"
    assert remapped.source_n_atoms == 12
    assert remapped.source_n_structures == 6
    np.testing.assert_array_equal(remapped.atom_source_indices, [2, 0, 1])
    np.testing.assert_array_equal(remapped.structure_source_indices, [4, 1, 0, 4])
    np.testing.assert_array_equal(remapped.evaluated_structure_indices, [0, 1, 2, 3])
    np.testing.assert_array_equal(remapped.occurrence_structures, [0, 2, 3])
    np.testing.assert_allclose(remapped.measurements["distance"], [0.21, 0.20, 0.21])
    assert len(remapped.relation_types) == 1
    np.testing.assert_array_equal(remapped.relation(0)["participants"][0]["atom_indices"], [1])
    np.testing.assert_array_equal(remapped.relation(0)["participants"][2]["atom_indices"], [0])
    assert remapped.query(structure_indices=[1]).n_interactions == 0
    assert interactions.n_interactions == 5
    with pytest.raises(ValueError, match="duplicates"):
        interactions.remap(atom_indices=[0, 0])


def test_remap_periodic_images_and_empty_selection():
    record = _record(1, "pair", [("first", [0]), ("second", [1])])
    record["images"] = [[0, 0, 0], [1, 0, 0]]
    result = msm.Interactions.from_records(
        [record], n_atoms=2, n_structures=3,
        evaluated_structure_indices=[1, 2], method="periodic",
    )

    selected = result.remap(structure_indices=[2, 1, 1])
    np.testing.assert_array_equal(selected.evaluated_structure_indices, [0, 1, 2])
    np.testing.assert_array_equal(selected.occurrence_structures, [1, 2])
    np.testing.assert_array_equal(selected.occurrence_image_offsets, [0, 2, 4])
    np.testing.assert_array_equal(
        selected.image_vectors, [[0, 0, 0], [1, 0, 0], [0, 0, 0], [1, 0, 0]]
    )
    empty = result.remap(atom_indices=[], structure_indices=[2])
    assert empty.n_atoms == 0
    assert empty.n_interactions == 0
    np.testing.assert_array_equal(empty.evaluated_structure_indices, [0])


def test_invalidation_removes_stale_observations_without_claiming_empty_evaluation(
    interactions,
):
    previous_view = interactions.query(structure_indices=[0])
    invalidated = interactions.invalidate_structures([1, 0, 1])

    np.testing.assert_array_equal(invalidated.evaluated_structure_indices, [2, 4])
    np.testing.assert_array_equal(invalidated.occurrence_structures, [2, 4, 4])
    assert invalidated.query(structure_indices=[0]).to_dict()[
        "evaluated_structure_indices"
    ].size == 0
    assert invalidated.query(structure_indices=[1]).to_dict()[
        "evaluated_structure_indices"
    ].size == 0
    assert invalidated.query(structure_indices=[4]).n_interactions == 2
    assert previous_view.n_interactions == 2
    assert interactions.query(structure_indices=[0]).n_interactions == 2
    np.testing.assert_array_equal(
        invalidated.atom_source_indices, interactions.atom_source_indices
    )
    assert invalidated.evaluation_mode == interactions.evaluation_mode
    with pytest.raises(ValueError, match="full"):
        previous_view.invalidate_structures([0])


def test_invalidation_realigns_periodic_images_of_surviving_occurrences():
    first = _record(0, "pair", [("a", [0]), ("b", [1])])
    first["images"] = [[0, 0, 0], [1, 0, 0]]
    second = _record(1, "pair", [("a", [0]), ("b", [2])])
    second["images"] = [[0, 0, 0], [0, -1, 0]]
    result = msm.Interactions.from_records(
        [first, second], n_atoms=3, n_structures=2,
        evaluated_structure_indices=[0, 1], method="periodic",
    )

    invalidated = result.invalidate_structures([0])
    np.testing.assert_array_equal(invalidated.occurrence_image_offsets, [0, 2])
    np.testing.assert_array_equal(invalidated.image_vectors,
                                  [[0, 0, 0], [0, -1, 0]])
    np.testing.assert_array_equal(invalidated.occurrence_structures, [1])


def test_nonidentity_source_maps_compose_across_extractions_and_standalone_file(tmp_path):
    result = msm.Interactions.from_records(
        [_record(1, "pair", [("first", [0]), ("second", [2])])],
        n_atoms=3, n_structures=2, evaluated_structure_indices=[0, 1],
        method="mapped", source_id="source-system",
        atom_source_indices=[8, 3, 6], structure_source_indices=[4, 1],
        source_n_atoms=10, source_n_structures=5,
    )
    selected = result.remap(atom_indices=[2, 0], structure_indices=[1, 0, 1])
    np.testing.assert_array_equal(selected.atom_source_indices, [6, 8])
    np.testing.assert_array_equal(selected.structure_source_indices, [1, 4, 1])
    assert selected.source_id == "source-system"
    assert selected.source_n_atoms == 10
    assert selected.query(atom_indices=[0], mode="incident").n_interactions == 2

    path = tmp_path / "mapped.h5i"
    selected.save(path)
    loaded = msm.Interactions.load(path)
    np.testing.assert_array_equal(loaded.atom_source_indices, [6, 8])
    np.testing.assert_array_equal(loaded.structure_source_indices, [1, 4, 1])
    assert loaded.source_n_atoms == 10
    assert loaded.source_n_structures == 5

    with pytest.raises(ValueError, match="one integer per local index"):
        msm.Interactions.from_records(
            [], n_atoms=2, n_structures=1,
            evaluated_structure_indices=[0], method="invalid",
            atom_source_indices=[0],
        )
    with pytest.raises(ValueError, match="integer"):
        msm.Interactions.from_records(
            [], n_atoms=2, n_structures=1,
            evaluated_structure_indices=[0], method="invalid",
            atom_source_indices=[0.2, 1.8],
        )


def test_legacy_standalone_file_without_source_maps_uses_identity(tmp_path):
    import h5py

    result = msm.Interactions.from_records(
        [], n_atoms=2, n_structures=2,
        evaluated_structure_indices=[1], method="legacy",
    )
    path = tmp_path / "legacy.h5i"
    result.save(path)
    with h5py.File(path, "r+") as file:
        assert "atom_source_indices" not in file
        assert "structure_source_indices" not in file
        import json

        metadata = json.loads(file.attrs["metadata"])
        del metadata["source_n_atoms"]
        del metadata["source_n_structures"]
        file.attrs["metadata"] = json.dumps(metadata)

    loaded = msm.Interactions.load(path)
    np.testing.assert_array_equal(loaded.atom_source_indices, [0, 1])
    np.testing.assert_array_equal(loaded.structure_source_indices, [0, 1])

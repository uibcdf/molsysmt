"""Qualify cheap frame invalidation and the unchanged interchange contract."""

import gc
import pickle
import tracemalloc
import weakref

import numpy as np
import pytest

import molsysmt as msm


def record(frame, distance, *, kind="hbond", participants=None, images=None):
    return {
        "structure_index": frame,
        "interaction_type": kind,
        "participants": (
            participants
            if participants is not None
            else [
                {"role": "donor", "atom_indices": [0]},
                {"role": "hydrogen", "atom_indices": [1]},
                {"role": "acceptor", "atom_indices": [2]},
            ]
        ),
        "evidence": "synthetic",
        "measurements": {"distance": distance},
        **({} if images is None else {"images": images}),
    }


@pytest.fixture
def result():
    return msm.Interactions.from_records(
        [
            record(0, 0.2, images=[[0, 0, 0], [0, 0, 0], [1, 0, 0]]),
            record(2, 0.3, images=[[0, 0, 0], [0, 0, 0], [0, 1, 0]]),
            record(2, 0.4, images=[[0, 0, 0], [0, 0, 0], [-1, 0, 0]]),
            record(
                4,
                0.5,
                kind="pi_pi",
                participants=[
                    {"role": "ring_a", "atom_indices": [0, 3, 4]},
                    {"role": "ring_b", "atom_indices": [2, 5, 6]},
                ],
                images=[[0, 0, 0], [0, 0, 1]],
            ),
        ],
        n_atoms=7,
        n_structures=6,
        evaluated_structure_indices=[4, 0, 1, 2],
        method="synthetic",
        measure_units={"distance": "nm"},
        parameters={"threshold": {"value": 0.6, "unit": "nm"}},
        source_id="fixture",
        software={"producer": "1.2"},
        atom_source_indices=[8, 3, 6, 0, 1, 2, 4],
        source_n_atoms=9,
        structure_source_indices=[9, 7, 5, 3, 1, 0],
        source_n_structures=10,
    )


def test_parallel_occurrence_handles_survive_queries_and_all_codecs(result, tmp_path):
    edited = result.invalidate_structures([0])
    observed = edited.query(structure_indices=[4, 2, 4]).to_dict()
    np.testing.assert_array_equal(observed["occurrence_indices"], [2, 0, 1])
    # Canonical ordering compares periodic images before geometric measures.
    np.testing.assert_allclose(observed["measurements"]["distance"], [0.5, 0.4, 0.3])
    np.testing.assert_array_equal(observed["image_offsets"], [0, 2, 5, 8])
    assert edited._packed_result is None

    standalone = tmp_path / "analysis.h5i"
    edited.save(standalone)
    payload = msm.convert(edited, to_form="molsysmt.InteractionsDict")
    file = tmp_path / "analysis.h5msm"
    msm.h5msm.write_layers(file, interactions={"analysis": edited})
    restored = [
        msm.Interactions.load(standalone),
        msm.convert(payload, to_form="molsysmt.Interactions"),
        msm.convert(file, to_form="molsysmt.MolSys").interactions["analysis"],
    ]
    for candidate in restored:
        data = candidate.query(structure_indices=[4, 2, 4]).to_dict()
        for key in (
            "occurrence_indices",
            "structure_indices",
            "relation_indices",
            "image_offsets",
            "image_vectors",
            "evidence",
        ):
            np.testing.assert_array_equal(data[key], observed[key])
        # H5MSM may canonicalize coverage order; explicit query order is stable.
        np.testing.assert_array_equal(
            np.sort(candidate.evaluated_structure_indices), [1, 2, 4]
        )
        assert candidate.software == {"producer": "1.2"}
        assert candidate.source_id == "fixture"
        assert candidate.measure_units == {"distance": "nm"}
        np.testing.assert_array_equal(
            candidate.atom_source_indices, result.atom_source_indices
        )
        np.testing.assert_array_equal(
            candidate.structure_source_indices, result.structure_source_indices
        )
    assert edited._packed_result is None


def test_pickling_a_full_filtered_analysis_restores_read_only_storage(result):
    edited = result.invalidate_structures([0])
    restored = pickle.loads(pickle.dumps(edited))
    np.testing.assert_array_equal(restored.to_dict()["occurrence_indices"], [0, 1, 2])
    np.testing.assert_allclose(restored.measurements["distance"], [0.4, 0.3, 0.5])
    with pytest.raises(ValueError):
        restored.occurrence_structures[0] = 0
    assert edited._packed_result is None


def test_pickling_filtered_query_views_preserves_handles_and_query_limits(result):
    view = result.invalidate_structures([0]).query(structure_indices=[4, 2])
    restored = pickle.loads(pickle.dumps(view))
    np.testing.assert_array_equal(restored.to_dict()["occurrence_indices"], [2, 0, 1])
    np.testing.assert_array_equal(
        restored.to_dict()["evaluated_structure_indices"], [4, 2]
    )
    assert restored.query(structure_indices=[0]).n_interactions == 0
    assert restored.query(atom_indices=[3]).n_interactions == 1
    with pytest.raises(ValueError, match="full"):
        restored.invalidate_structures([2])


@pytest.mark.parametrize(
    "mode, atoms, distances",
    [
        ("involving_selection", [0], [0.4, 0.3, 0.5]),
        ("within_selection", [0, 1, 2], [0.4, 0.3]),
        ("across_selection_boundary", [0, 1, 2], [0.5]),
        ("within_selection", [0], []),
        ("involving_selection", [], []),
    ],
)
def test_atom_queries_filter_validity_without_packing(result, mode, atoms, distances):
    edited = result.invalidate_structures([0])
    data = edited.query(atom_indices=atoms, mode=mode).to_dict()
    np.testing.assert_allclose(data["measurements"]["distance"], distances)
    np.testing.assert_array_equal(data["evaluated_structure_indices"], [4, 1, 2])
    assert edited._packed_result is None


def test_between_and_nested_queries_retain_compact_handles_and_compound_members(result):
    edited = result.invalidate_structures([0])
    view = edited.between_selections([0], [2], structure_indices=[4, 0, 2, 1, 4])
    data = view.query(atom_indices=[3]).to_dict()
    np.testing.assert_array_equal(data["occurrence_indices"], [2])
    np.testing.assert_array_equal(data["structure_indices"], [4])
    np.testing.assert_array_equal(data["evaluated_structure_indices"], [4, 2, 1])
    assert edited.between_selections([0], [2], exclusive=True).n_interactions == 0
    assert edited.between_selections([0, 1], [2], exclusive=True).n_interactions == 2
    assert edited.query(interaction_types="pi_pi").n_interactions == 1
    assert edited._packed_result is None


def test_repeated_invalidation_preserves_old_views_and_empty_frame_meaning(result):
    original_view = result.query(structure_indices=[0])
    first = result.invalidate_structures([0, 0])
    first_view = first.query(structure_indices=[2])
    second = first.invalidate_structures([1, 2, 1])
    assert original_view.n_interactions == 1
    np.testing.assert_array_equal(first_view.to_dict()["occurrence_indices"], [0, 1])
    assert first.query(structure_indices=[1]).to_dict()[
        "evaluated_structure_indices"
    ].tolist() == [1]
    assert (
        second.query(structure_indices=[1])
        .to_dict()["evaluated_structure_indices"]
        .size
        == 0
    )
    assert (
        second.query(structure_indices=[3])
        .to_dict()["evaluated_structure_indices"]
        .size
        == 0
    )
    np.testing.assert_array_equal(second.to_dict()["occurrence_indices"], [0])
    np.testing.assert_array_equal(second.evaluated_structure_indices, [4])
    assert second._root is result
    assert first._packed_result is second._packed_result is None


def test_materialization_never_revives_invalid_frames_in_remap(result):
    edited = result.invalidate_structures([0])
    remapped = edited.remap(structure_indices=[0, 2, 1, 2, 4])
    np.testing.assert_array_equal(remapped.evaluated_structure_indices, [1, 2, 3, 4])
    np.testing.assert_array_equal(remapped.occurrence_structures, [1, 1, 3, 3, 4])
    np.testing.assert_array_equal(remapped.structure_source_indices, [9, 5, 7, 5, 1])
    assert remapped.n_interactions == 5


def test_metadata_remains_independent_and_packed_export_uses_latest_attribution(
    result, tmp_path
):
    edited = result.invalidate_structures([0])
    edited.parameters["threshold"]["value"] = 0.7
    edited.software["producer"] = "1.3"
    edited.source_id = "edited_label"
    assert result.parameters["threshold"]["value"] == 0.6
    assert result.software == {"producer": "1.2"}
    assert edited.query(structure_indices=[2]).to_dict()["source_id"] == "edited_label"
    again = edited.invalidate_structures([1])
    assert again.source_id == "edited_label"
    assert again.parameters == edited.parameters
    assert again.software == edited.software
    _ = edited.occurrence_structures
    edited.parameters["attribution"] = {"note": "attached later"}
    edited.save(tmp_path / "analysis.h5i")
    restored = msm.Interactions.load(tmp_path / "analysis.h5i")
    assert restored.parameters == edited.parameters
    assert restored.software == edited.software


def test_constructor_owns_storage_and_blocks_mutation_through_input_aliases():
    frames = np.array([0, 1, 2], dtype=np.int64)
    distances = np.array([0.1, 0.2, 0.3])
    result = msm.Interactions(
        n_atoms=2,
        n_structures=3,
        evaluated_structure_indices=np.arange(3),
        relation_types=["pair"],
        relation_participant_offsets=[0, 2],
        participant_roles=["a", "b"],
        participant_atom_offsets=[0, 1, 2],
        participant_atoms=[0, 1],
        occurrence_structures=frames,
        occurrence_relations=[0, 0, 0],
        occurrence_evidence=[0, 0, 0],
        evidence_labels=["synthetic"],
        measurements={"distance": distances},
        measure_units={"distance": "nm"},
        method="synthetic",
    )
    edited = result.invalidate_structures([0])
    frames[:] = 0
    distances[:] = 99
    np.testing.assert_array_equal(
        edited.query(structure_indices=[2]).to_dict()["structure_indices"], [2]
    )
    np.testing.assert_allclose(
        edited.query(structure_indices=[2]).to_dict()["measurements"]["distance"], [0.3]
    )
    with pytest.raises(ValueError):
        result.occurrence_structures[0] = 2
    with pytest.raises(ValueError):
        result.measurements["distance"].setflags(write=True)
    with pytest.raises(TypeError):
        result.measurements["distance"] = distances
    with pytest.raises(AttributeError, match="read-only"):
        result.occurrence_structures = frames


def test_all_observations_removed_release_occurrence_storage_without_losing_empty_coverage(
    result,
):
    root = result.remap()
    reference = weakref.ref(root)
    empty = root.invalidate_structures([0, 2, 4])
    del root
    gc.collect()
    assert reference() is None
    assert empty.n_interactions == 0
    np.testing.assert_array_equal(empty.evaluated_structure_indices, [1])
    assert empty.query(structure_indices=[1]).to_dict()[
        "evaluated_structure_indices"
    ].tolist() == [1]
    assert (
        empty.query(structure_indices=[0]).to_dict()["evaluated_structure_indices"].size
        == 0
    )
    np.testing.assert_array_equal(empty.occurrence_image_offsets, [0])
    assert empty.image_vectors.shape == (0, 3)


@pytest.mark.parametrize("count", [100, 200_000])
def test_one_frame_invalidation_allocation_is_independent_of_occurrence_count(count):
    result = msm.Interactions(
        n_atoms=2,
        n_structures=10,
        evaluated_structure_indices=np.arange(10),
        relation_types=["pair"],
        relation_participant_offsets=[0, 2],
        participant_roles=["a", "b"],
        participant_atom_offsets=[0, 1, 2],
        participant_atoms=[0, 1],
        occurrence_structures=np.arange(count) * 10 // count,
        occurrence_relations=np.zeros(count, dtype=np.int64),
        occurrence_evidence=np.zeros(count, dtype=np.int32),
        evidence_labels=["synthetic"],
        measurements={"distance": np.full(count, 0.2)},
        measure_units={"distance": "nm"},
        method="synthetic",
    )
    result.query(atom_indices=[0])  # Include the already-built inverse indexes.
    tracemalloc.start()
    try:
        edited = result.invalidate_structures([3])
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    assert peak < 100_000, (
        f"Invalidation allocated {peak} bytes for {count} occurrences"
    )
    assert edited.n_interactions == count * 9 // 10
    assert edited.query(structure_indices=[3], atom_indices=[0]).n_interactions == 0
    assert (
        edited.query(structure_indices=[4], atom_indices=[0]).n_interactions
        == count // 10
    )
    assert edited._packed_result is None

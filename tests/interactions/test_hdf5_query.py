"""Selective HDF5 occurrence queries without loading a whole analysis."""

import h5py
import numpy as np
import pytest

import molsysmt as msm
from molsysmt.interactions._h5msm05 import write_interactions_file
from molsysmt.interactions._hdf5_query import (
    HDF5InteractionsReader,
    query_named_interactions_file,
)


def _result():
    records = [
        {
            "structure_index": 0,
            "interaction_type": "hbond",
            "participants": [
                {"role": "donor", "atom_indices": [0]},
                {"role": "hydrogen", "atom_indices": [1]},
                {"role": "acceptor", "atom_indices": [2]},
            ],
            "measurements": {"distance": 0.20},
            "images": [[0, 0, 0], [0, 0, 0], [1, 0, 0]],
        },
        {
            "structure_index": 2,
            "interaction_type": "pi_pi",
            "participants": [
                {"role": "ring", "atom_indices": [3, 4, 5]},
                {"role": "ring", "atom_indices": [6, 7, 8]},
            ],
            "measurements": {"distance": 0.36},
            "images": [[0, 0, 0], [0, 0, 0]],
        },
        {
            "structure_index": 4,
            "interaction_type": "hbond",
            "participants": [
                {"role": "donor", "atom_indices": [0]},
                {"role": "hydrogen", "atom_indices": [1]},
                {"role": "acceptor", "atom_indices": [2]},
            ],
            "measurements": {"distance": 0.21},
            "images": [[0, 0, 0], [0, 0, 0], [1, 0, 0]],
        },
    ]
    return msm.Interactions.from_records(
        records,
        n_atoms=9,
        n_structures=6,
        evaluated_structure_indices=[0, 1, 2, 4],
        method="candidate",
        measure_units={"distance": "nm"},
        atom_source_indices=[8, 7, 6, 5, 4, 3, 2, 1, 0],
        structure_source_indices=[6, 5, 4, 3, 2, 1],
        source_n_atoms=9,
        source_n_structures=7,
    )


def _assert_matches_memory(filename, result, frames, **filters):
    observed = query_named_interactions_file(filename, "mixed", frames, **filters)
    expected = result.query(structure_indices=frames, **filters).to_dict()
    for key in (
        "evaluated_structure_indices",
        "occurrence_indices",
        "structure_indices",
        "relation_indices",
        "evidence",
        "image_offsets",
        "image_vectors",
    ):
        if expected[key] is None:
            assert observed[key] is None
        else:
            np.testing.assert_array_equal(observed[key], expected[key])
    np.testing.assert_allclose(
        observed["measurements"]["distance"], expected["measurements"]["distance"]
    )
    for relation, descriptor in observed["relations"].items():
        expected_descriptor = result.relation(relation)
        assert descriptor["interaction_type"] == expected_descriptor["interaction_type"]
        for left, right in zip(
            descriptor["participants"], expected_descriptor["participants"]
        ):
            assert left["role"] == right["role"]
            np.testing.assert_array_equal(left["atom_indices"], right["atom_indices"])
    return observed


def test_file_query_matches_memory_for_frames_atoms_types_and_images(tmp_path):
    result = _result()
    filename = tmp_path / "indexed.h5msm"
    write_interactions_file(filename, {"mixed": result})
    with h5py.File(filename, "r") as file:
        index = file["interactions/0/query_index"]
        assert index["frame_offsets"][:].tolist() == [0, 1, 1, 2, 2, 3, 3]
        assert index["evaluated_mask"][:].tolist() == [
            True,
            True,
            True,
            False,
            True,
            False,
        ]

    selected = _assert_matches_memory(filename, result, [4, 1, 0, 4, 3])
    assert selected["structure_indices"].tolist() == [4, 0]
    assert selected["evaluated_structure_source_indices"].tolist() == [2, 5, 6]
    assert selected["method"] == "candidate"
    assert selected["evaluation_mode"] == "internal"
    np.testing.assert_array_equal(
        selected["participant_atom_source_indices"],
        result.atom_source_indices[selected["participant_atom_indices"]],
    )
    _assert_matches_memory(
        filename, result, [2, 0, 4], atom_indices=[0], mode="incident"
    )
    _assert_matches_memory(filename, result, [2, 0, 4], atom_indices=[0], mode="cross")
    _assert_matches_memory(
        filename, result, [2, 0, 4], atom_indices=[0, 1, 2], mode="internal"
    )
    _assert_matches_memory(filename, result, [2, 0, 4], interaction_types="pi_pi")
    _assert_matches_memory(
        filename, result, [2], atom_indices=[3, 4, 5], mode="internal"
    )
    for mode in (
        "involving_selection",
        "within_selection",
        "across_selection_boundary",
    ):
        _assert_matches_memory(
            filename, result, [4, 1, 2, 0, 4], atom_indices=[3, 4, 5], mode=mode
        )
    _assert_matches_memory(filename, result, [1])
    _assert_matches_memory(filename, result, [3])


def test_file_query_falls_back_for_legacy_group_without_index(tmp_path):
    result = _result()
    filename = tmp_path / "legacy.h5msm"
    write_interactions_file(filename, {"mixed": result})
    with h5py.File(filename, "r+") as file:
        del file["interactions/0/query_index"]
    _assert_matches_memory(filename, result, [4, 1, 0, 4], atom_indices=[0])


def test_file_query_rejects_unknown_name_and_invalid_index(tmp_path):
    filename = tmp_path / "bad.h5msm"
    write_interactions_file(filename, {"mixed": _result()})
    with pytest.raises(KeyError, match="Unknown interaction analysis"):
        query_named_interactions_file(filename, "missing", [0])
    with h5py.File(filename, "r+") as file:
        file["interactions/0/query_index/frame_offsets"][1] = 999
    with pytest.raises(ValueError, match="frame offsets"):
        query_named_interactions_file(filename, "mixed", [0])


def test_open_reader_supports_repeated_queries_and_closes(tmp_path):
    filename = tmp_path / "persistent.h5msm"
    write_interactions_file(filename, {"mixed": _result()})
    with HDF5InteractionsReader(filename, "mixed") as reader:
        assert reader.query([0])["structure_indices"].tolist() == [0]
        assert reader.query([1])["evaluated_structure_indices"].tolist() == [1]
        assert reader.query([2], atom_indices=[4])["structure_indices"].tolist() == [2]
    with pytest.raises(ValueError, match="closed"):
        reader.query([0])

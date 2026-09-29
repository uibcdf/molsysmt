"""Contracts for embedding named sparse analyses in one HDF5 group."""

import h5py
import numpy as np
import pytest

import molsysmt as msm
from molsysmt.interactions._hdf5_collection import (
    read_named_analyses,
    write_named_analyses,
)


def _analysis(*, evaluated, observations=()):
    return msm.Interactions.from_records(
        observations, n_atoms=3, n_structures=4,
        evaluated_structure_indices=evaluated, method="collection-test",
    )


def test_named_collection_roundtrips_distinct_coverage_and_arbitrary_names(tmp_path):
    observed = _analysis(
        evaluated=[0, 2],
        observations=[{
            "structure_index": 2,
            "interaction_type": "pair",
            "participants": [
                {"role": "first", "atom_indices": [0]},
                {"role": "second", "atom_indices": [1]},
            ],
        }],
    )
    empty = _analysis(evaluated=[1])
    path = tmp_path / "analyses.h5"

    with h5py.File(path, "w") as file:
        write_named_analyses(file.create_group("interactions"), {
            "z/π": observed, "alpha": empty,
        })
    with h5py.File(path, "r") as file:
        group = file["interactions"]
        assert group["0"].attrs["name"] == "alpha"
        assert group["1"].attrs["name"] == "z/π"
        restored = read_named_analyses(group)

    assert list(restored) == ["alpha", "z/π"]
    assert restored["alpha"].n_interactions == 0
    np.testing.assert_array_equal(restored["alpha"].evaluated_structure_indices, [1])
    np.testing.assert_array_equal(restored["z/π"].occurrence_structures, [2])
    assert restored["z/π"].query(structure_indices=[0]).n_interactions == 0


def test_named_collection_rejects_unknown_or_inconsistent_schemas(tmp_path):
    path = tmp_path / "invalid.h5"
    with h5py.File(path, "w") as file:
        group = file.create_group("interactions")
        write_named_analyses(group, {"one": _analysis(evaluated=[0])})
        with pytest.raises(ValueError, match="empty"):
            write_named_analyses(group, {})
        group.attrs["schema_version"] = 999
        with pytest.raises(ValueError, match="schema or version"):
            read_named_analyses(group)
        group.attrs["schema_version"] = 1
        group.attrs["n_analyses"] = 2
        with pytest.raises(ValueError, match="inconsistent"):
            read_named_analyses(group)


def test_present_empty_collection_is_distinct_from_absent_group(tmp_path):
    path = tmp_path / "empty.h5"
    with h5py.File(path, "w") as file:
        assert "interactions" not in file
        write_named_analyses(file.create_group("interactions"), {})
    with h5py.File(path, "r") as file:
        assert "interactions" in file
        assert read_named_analyses(file["interactions"]) == {}


def test_named_selection_skips_unrequested_analysis_payload(tmp_path):
    path = tmp_path / "selected.h5"
    with h5py.File(path, "w") as file:
        write_named_analyses(file.create_group("interactions"), {
            "alpha": _analysis(evaluated=[0]),
            "omega": _analysis(evaluated=[1]),
        })
        file["interactions/1"].attrs["schema_version"] = 999

    with h5py.File(path, "r") as file:
        assert list(read_named_analyses(file["interactions"], names=["alpha"])) == [
            "alpha"
        ]
        with pytest.raises(KeyError, match="missing"):
            read_named_analyses(file["interactions"], names=["missing"])
        with pytest.raises(ValueError, match="schema version"):
            read_named_analyses(file["interactions"])

"""Probe the optional interaction layer in an isolated H5MSM 0.5 file."""

import h5py
import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import FormatError
from molsysmt.interactions._h5msm05 import (
    read_interactions_file,
    write_interactions_file,
)
from molsysmt.native import H5MSMFileHandler


def test_interaction_only_file_preserves_maps_scope_images_and_empty_frames(tmp_path):
    result = msm.Interactions.from_records(
        [{
            "structure_index": 2,
            "interaction_type": "hbond",
            "participants": [
                {"role": "donor", "atom_indices": [0]},
                {"role": "hydrogen", "atom_indices": [1]},
                {"role": "acceptor", "atom_indices": [2]},
            ],
            "measurements": {"distance": 0.2},
            "images": [[0, 0, 0], [0, 0, 0], [1, 0, 0]],
        }],
        n_atoms=4, n_structures=3, evaluated_structure_indices=[0, 2],
        method="candidate", measure_units={"distance": "nm"},
        atom_source_indices=[6, 4, 2, 1], source_n_atoms=7,
        evaluation_mode="incident", evaluation_atom_indices=[0],
        evaluation_universe_indices=[0, 1, 2],
    )
    filename = tmp_path / "interactions_only.h5msm"
    write_interactions_file(filename, {"hydrogen/bonds": result})

    with h5py.File(filename, "r") as file:
        assert file.attrs["version"] == "0.5"
        assert set(file.keys()) == {"interactions"}
    restored = read_interactions_file(filename)
    assert list(restored) == ["hydrogen/bonds"]
    observed = restored["hydrogen/bonds"]
    np.testing.assert_array_equal(observed.atom_source_indices, [6, 4, 2, 1])
    np.testing.assert_array_equal(observed.evaluation_scope["universe_indices"],
                                  [0, 1, 2])
    np.testing.assert_array_equal(observed.image_vectors[-1], [1, 0, 0])
    np.testing.assert_array_equal(observed.evaluated_structure_indices, [0, 2])
    assert observed.query(structure_indices=[0]).n_interactions == 0

    with pytest.raises(FormatError, match="Unsupported H5MSM version"):
        H5MSMFileHandler(filename, io_mode="r")
    with pytest.raises(FileExistsError):
        write_interactions_file(filename, {})


def test_absent_and_present_empty_interaction_layers_are_distinct(tmp_path):
    absent = tmp_path / "absent.h5msm"
    empty = tmp_path / "empty.h5msm"
    write_interactions_file(absent, None)
    write_interactions_file(empty, {})
    assert read_interactions_file(absent) is None
    assert read_interactions_file(empty) == {}


def test_wrong_root_version_and_unknown_collection_schema_fail(tmp_path):
    filename = tmp_path / "invalid.h5msm"
    write_interactions_file(filename, {})
    with h5py.File(filename, "r+") as file:
        file["interactions"].attrs["schema_version"] = 999
    with pytest.raises(ValueError, match="collection schema or version"):
        read_interactions_file(filename)
    with h5py.File(filename, "r+") as file:
        file.attrs["version"] = "0.4"
    with pytest.raises(ValueError, match="H5MSM 0.5"):
        read_interactions_file(filename)

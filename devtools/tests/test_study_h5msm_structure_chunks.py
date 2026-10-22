"""Qualify experimental layouts by delivered values, not their chunk labels."""

import pytest

from devtools.scripts import study_h5msm_structure_chunks as study


@pytest.mark.parametrize("layout", study._LAYOUTS)
def test_each_layout_round_trips_real_queries(tmp_path, layout):
    result = study._worker(4, 7, layout, 1)
    assert set(result["operations"]) == {
        "public_write",
        "public_load",
        "private_one_structure",
        "private_nonconsecutive_two_atoms",
    }
    assert result["file_bytes"] > 0
    for measurement in result["operations"].values():
        assert len(measurement["samples_seconds"]) == 1


@pytest.mark.parametrize(
    "atoms,structures,storage_rows,transfer_rows",
    [
        (62, 5000, 704, 256),
        (10000, 1000, 4, 256),
        (100000, 100, 1, 256),
        (10, 99, 17, 7),
    ],
)
@pytest.mark.parametrize("budget", [65536, 262144, 1048576])
def test_chunks_bound_decompression_and_fit_all_transfer_boundaries(
    atoms, structures, storage_rows, transfer_rows, budget
):
    rows, width, xyz = study._aligned_chunks(
        (structures, atoms, 3), storage_rows, transfer_rows, budget
    )
    assert rows * width * xyz * 8 <= budget
    assert xyz == 3
    assert 1 <= width <= atoms
    assert storage_rows % rows == transfer_rows % rows == 0


@pytest.mark.parametrize("shape", [(0, 4, 3), (7, 0, 3)])
def test_empty_axes_retain_hdf5_automatic_chunk_handling(shape):
    assert study._aligned_chunks(shape, 1, 256, 65536) is None

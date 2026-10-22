"""Bound geometry decompression and avoid rewriting temporal chunks per transfer."""

import h5py
import numpy as np
import pytest

from molsysmt import pyunitwizard as puw
from molsysmt.form import _h5msm05_structures as codec
from molsysmt.native import Structures
from molsysmt.native import _structure_array as storage


@pytest.mark.parametrize("compression", [None, "gzip"])
@pytest.mark.parametrize("transfer_rows,chunk_budget", [(3, 240), (4, 400)])
def test_coordinate_chunks_align_with_writes_and_bound_raw_bytes(
    tmp_path, monkeypatch, compression, transfer_rows, chunk_budget
):
    monkeypatch.setattr(storage, "_BLOCK_BYTES", 336)  # Two complete structures.
    monkeypatch.setattr(codec, "_GEOMETRY_CHUNK_BYTES", chunk_budget, raising=False)
    values = np.arange(7 * 7 * 3, dtype=float).reshape(7, 7, 3)
    source = Structures(coordinates=puw.quantity(values, "angstrom"))
    written = []
    original = h5py.Dataset.__setitem__

    def observe(dataset, key, value):
        if dataset.name == "/structures/coordinates":
            written.append((key.start, key.stop))
        return original(dataset, key, value)

    def forbidden(*args, **kwargs):
        pytest.fail("Geometry transfer assembled the complete protected array")

    monkeypatch.setattr(h5py.Dataset, "__setitem__", observe)
    filename = tmp_path / "aligned.h5msm"
    with monkeypatch.context() as guard, h5py.File(filename, "w") as file:
        guard.setattr(storage._StructureArray, "_dense", forbidden)
        codec.write_independent_structures(
            file, source, compression=compression, block_size=transfer_rows
        )
        dataset = file["structures/coordinates"]
        chunks = dataset.chunks
        assert np.prod(chunks) * dataset.dtype.itemsize <= chunk_budget
        assert chunks[2] == 3
        assert written
        for start, stop in written:
            assert start % chunks[0] == 0
            assert stop % chunks[0] == 0 or stop == 7
        assert dataset.attrs["unit"] == "nm"
        np.testing.assert_allclose(dataset[:], values / 10, atol=1e-14, rtol=0)
        # Append keeps the stored layout even with an unaligned old end index.
        incoming = Structures(coordinates=puw.quantity(values[:3] + 100, "angstrom"))
        codec.append_independent_structures(file, incoming, block_size=transfer_rows)
        assert dataset.chunks == chunks
        selected = codec.read_independent_structures(
            file, structure_indices=[9, 0, 6, 0], atom_indices=[6, 1]
        )
    expected = np.concatenate([values, values[:3] + 100]) / 10
    np.testing.assert_allclose(
        puw.get_value(selected.get_coordinates(), to_unit="nm"),
        expected[[9, 0, 6, 0]][:, [6, 1]],
        atol=1e-14,
        rtol=0,
    )


@pytest.mark.parametrize("shape", [(0, 7, 3), (5, 0, 3)])
def test_empty_coordinate_axes_remain_writable_and_readable(tmp_path, shape):
    source = Structures(coordinates=puw.quantity(np.empty(shape), "nm"))
    with h5py.File(tmp_path / "empty.h5msm", "w") as file:
        codec.write_independent_structures(file, source)
        restored = codec.read_independent_structures(file)
    assert restored.get_coordinates().shape == shape

"""Protecting canonical quantities and source indices at reducer boundaries."""

from contextlib import nullcontext

import numpy as np
import pytest

from molsysmt import pyunitwizard as puw
from molsysmt._private.execution import ChunkedExecutor, Reducer


class _Collector(Reducer):
    def initialize(self, metadata):
        self.metadata = metadata
        self.chunks = []
        self.finalized = False

    def consume(self, chunk):
        self.chunks.append(chunk)

    def finalize(self):
        self.finalized = True
        return self.chunks


def test_normalization_converts_quantities_and_keeps_ids_separate():
    raw = {
        "coordinates": puw.quantity(np.full((2, 1, 3), 10.0), "angstrom"),
        "box": puw.quantity(np.tile(np.eye(3) * 20, (2, 1, 1)), "angstrom"),
        "time": puw.quantity([1.0, 2.0], "ns"),
        "structure_id": np.array(["frame-90", "frame-12"]),
    }
    chunk = ChunkedExecutor._build_chunk(raw)
    np.testing.assert_allclose(chunk["coordinates"], 1.0)
    np.testing.assert_allclose(chunk["box"], np.tile(np.eye(3) * 2, (2, 1, 1)))
    np.testing.assert_allclose(chunk["time"], [1000, 2000])
    assert chunk["structure_indices"] is None
    np.testing.assert_array_equal(chunk["structure_id"], raw["structure_id"])
    for value in chunk.values():
        if isinstance(value, np.ndarray):
            assert not value.flags.writeable
    # Making a reducer view read-only must not freeze caller-owned arrays.
    assert raw["structure_id"].flags.writeable


@pytest.mark.parametrize("heavy", [False, True])
def test_source_indices_nonconsecutive_repeated_partial_chunks(heavy):
    selected = np.array([4, 1, 4, 0, 3], dtype=np.int64)
    reducer = _Collector()
    executor = ChunkedExecutor(
        object(), "synthetic", "identity_test", reducer=reducer,
        structure_indices=selected, chunk_size=2,
    )

    def iterator(structure_indices, chunk_size):
        assert np.array_equal(structure_indices, selected)
        chunks = []
        for start in range(0, len(selected), chunk_size):
            indices = selected[start:start + chunk_size]
            chunks.append({
                "coordinates": puw.quantity(
                    np.repeat(indices[:, None, None], 3, axis=2), "nm"
                ),
                "structure_id": np.array([f"external-{100 + i}" for i in indices]),
            })
        return nullcontext(iter(chunks))

    executor._get_form_iterator = iterator
    chunks = (
        executor._execute_heavy(1, 6) if heavy else executor._execute_eager(1, 6)
    )
    np.testing.assert_array_equal(
        np.concatenate([chunk["structure_indices"] for chunk in chunks]), selected
    )
    assert all(chunk["structure_indices"].dtype == np.int64 for chunk in chunks)
    assert all(not chunk["structure_indices"].flags.writeable for chunk in chunks)
    assert reducer.metadata["n_structures"] == len(selected)
    assert reducer.metadata["n_structures_total"] == 6
    assert reducer.metadata["n_chunks"] == (3 if heavy else 1)


@pytest.mark.parametrize("heavy", [False, True])
def test_empty_selection_finalizes_without_opening_a_source(heavy):
    reducer = _Collector()
    executor = ChunkedExecutor(
        object(), "synthetic", "empty_test", reducer=reducer,
        structure_indices=np.empty(0, dtype=np.int64), chunk_size=2,
    )

    def forbidden(*args):
        raise AssertionError("An empty selection must not open a trajectory.")

    executor._get_form_iterator = forbidden
    assert (
        executor._execute_heavy(1, 6) if heavy else executor._execute_eager(1, 6)
    ) == []
    assert reducer.metadata["n_structures"] == 0
    assert reducer.metadata["n_chunks"] == 0


@pytest.mark.parametrize("fault", ["short", "extra", "wrong_indices", "misaligned", "noninteger_indices"])
def test_invalid_traversal_never_finalizes_partial_results(fault):
    reducer = _Collector()
    executor = ChunkedExecutor(
        object(), "synthetic", "invalid_test", reducer=reducer,
        structure_indices=np.array([2, 0]), chunk_size=1,
    )
    raw = {"coordinates": puw.quantity(np.zeros((2, 1, 3)), "nm")}
    if fault == "short":
        raw["coordinates"] = puw.quantity(np.zeros((1, 1, 3)), "nm")
    elif fault == "extra":
        raw["coordinates"] = puw.quantity(np.zeros((3, 1, 3)), "nm")
    elif fault == "wrong_indices":
        raw["structure_indices"] = np.array([0, 1])
    elif fault == "noninteger_indices":
        raw["structure_indices"] = np.array([2.0, 0.0])
    else:
        raw["time"] = puw.quantity([0], "ps")
    executor._get_form_iterator = lambda *args: nullcontext(iter([raw]))
    with pytest.raises(ValueError):
        executor._execute_eager(1, 3)
    assert not reducer.finalized


@pytest.mark.parametrize("heavy", [False, True])
def test_zero_structure_source_does_not_open_an_iterator(heavy):
    reducer = _Collector()
    executor = ChunkedExecutor(
        object(), "synthetic", "zero_test", reducer=reducer, chunk_size=2,
    )

    def forbidden(*args):
        raise AssertionError("A zero-structure source must not open a trajectory.")

    executor._get_form_iterator = forbidden
    assert (
        executor._execute_heavy(1, 0) if heavy else executor._execute_eager(1, 0)
    ) == []
    assert reducer.metadata["n_structures_total"] == 0

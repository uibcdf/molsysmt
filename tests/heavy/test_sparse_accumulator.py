"""Checking typed sparse buffers and failure before retaining oversized blocks."""

import numpy as np
import pytest

from molsysmt._private.execution.sparse_accumulator import SparseColumnAccumulator
from molsysmt._private.smonitor import MemoryBudgetExceededError


def test_sparse_blocks_keep_numeric_columns_and_typed_empty_shape():
    accumulator = SparseColumnAccumulator(
        {"pairs": (np.int64, (2,)), "distance": (np.float64, ())}, budget_bytes=10000,
    )
    assert accumulator.concatenate("pairs").shape == (0, 2)
    assert accumulator.concatenate("distance").dtype == np.float64
    for count in (2, 0, 1):
        accumulator.append({
            "pairs": np.zeros((count, 2), dtype=np.int64),
            "distance": np.ones(count, dtype=np.float64),
        })
    assert accumulator.n_rows == 3
    assert accumulator.nbytes == 72
    assert accumulator.concatenate("pairs").shape == (3, 2)
    accumulator.clear()
    assert accumulator.concatenate("pairs").shape == (0, 2)
    assert accumulator.nbytes == 0 and accumulator.n_rows == 0


def test_result_working_budget_rejects_a_block_without_retaining_it():
    accumulator = SparseColumnAccumulator({"frames": (np.int64, ())}, budget_bytes=100)
    accumulator.append({"frames": np.array([4], dtype=np.int64)})
    with pytest.raises(MemoryBudgetExceededError):
        accumulator.append({"frames": np.array([1, 2], dtype=np.int64)})
    assert accumulator.n_rows == 1 and accumulator.nbytes == 8
    np.testing.assert_array_equal(accumulator.concatenate("frames"), [4])


@pytest.mark.parametrize("fault", ["dtype", "shape", "rows", "names"])
def test_column_schema_rejects_misaligned_numeric_buffers(fault):
    accumulator = SparseColumnAccumulator(
        {"pairs": (np.int64, (2,)), "distance": (np.float64, ())}, budget_bytes=10000,
    )
    columns = {"pairs": np.zeros((2, 2), dtype=np.int64), "distance": np.ones(2)}
    if fault == "dtype":
        columns["pairs"] = columns["pairs"].astype(np.int32)
    elif fault == "shape":
        columns["pairs"] = np.zeros((2, 3), dtype=np.int64)
    elif fault == "rows":
        columns["distance"] = np.ones(1)
    else:
        del columns["distance"]
    with pytest.raises(ValueError):
        accumulator.append(columns)
    assert accumulator.n_rows == 0

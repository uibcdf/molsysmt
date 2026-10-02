"""Accumulating typed sparse numeric blocks with an explicit working estimate."""

import numpy as np

from molsysmt._private.smonitor import MemoryBudgetExceededError


class SparseColumnAccumulator:
    """Retain column blocks without allocating a Python object per occurrence."""

    def __init__(self, columns, *, budget_bytes, fixed_bytes=0, packing_factor=6):
        if any(np.dtype(dtype).kind not in "biufc" for dtype, _ in columns.values()):
            raise ValueError("Sparse accumulator columns must use numeric dtypes.")
        self._specifications = columns
        self._blocks = {name: [] for name in columns}
        self._budget = budget_bytes
        self._fixed = fixed_bytes
        self._packing_factor = packing_factor
        self.nbytes = 0
        self.n_rows = 0

    def check_budget(self, extra_bytes=0):
        predicted = self._fixed + self._packing_factor * self.nbytes + extra_bytes
        if predicted > self._budget:
            raise MemoryBudgetExceededError(
                reason="Estimated resident sparse-result working memory exceeds the RAM budget.",
                predicted_bytes=predicted,
                available_bytes=self._budget,
                caller="molsysmt._private.execution.sparse_accumulator",
            )

    def append(self, columns):
        if set(columns) != set(self._specifications):
            raise ValueError(
                "Sparse column names disagree with the accumulator schema."
            )
        rows = None
        for name, (dtype, tail_shape) in self._specifications.items():
            value = columns[name]
            if value.dtype != np.dtype(dtype) or value.shape[1:] != tail_shape:
                raise ValueError(
                    "Sparse column dtype or trailing shape disagrees with its schema."
                )
            if rows is None:
                rows = len(value)
            elif rows != len(value):
                raise ValueError("Sparse columns have inconsistent row counts.")
        added = sum(value.nbytes for value in columns.values())
        self.check_budget(extra_bytes=added * self._packing_factor)
        for name, value in columns.items():
            self._blocks[name].append(value)
        self.n_rows += rows
        self.nbytes += added

    def concatenate(self, name):
        blocks = self._blocks[name]
        if not blocks:
            dtype, tail_shape = self._specifications[name]
            return np.empty((0, *tail_shape), dtype=dtype)
        return np.concatenate(blocks, axis=0)

    def clear(self):
        for blocks in self._blocks.values():
            blocks.clear()
        self.n_rows = 0
        self.nbytes = 0

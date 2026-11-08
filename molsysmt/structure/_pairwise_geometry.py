"""Bounded numeric support for pairwise geometric analyses."""

import numpy as np

from molsysmt._private.execution import Reducer
from molsysmt._private.smonitor import (
    ArgumentError,
    MemoryBudgetExceededError,
    StructuralInconsistencyError,
    UnsupportedHeavyOperationError,
)


def check_budget(numeric_bytes, work, max_work, caller):
    """Leave half the configured numeric budget for delivery and kernel blocks."""
    from molsysmt import configure

    if work > max_work:
        raise UnsupportedHeavyOperationError(
            operation=caller,
            form="bounded pairwise geometry",
            reason=f"Estimated work {work} exceeds max_work={max_work}.",
        )
    if numeric_bytes > configure.max_ram_usage // 2:
        raise MemoryBudgetExceededError(
            reason="Resident pairwise geometry exceeds its numeric working budget.",
            predicted_bytes=numeric_bytes,
            available_bytes=configure.max_ram_usage // 2,
            caller=caller,
        )


def member_labels(member_keys, count, caller):
    """Retain opaque labels without conflating repeated structures with members."""
    if member_keys is None:
        return [str(index) for index in range(count)]
    if len(member_keys) != count:
        raise ArgumentError("member_keys", caller=caller)
    return list(member_keys)


def symmetric_maps(table, atoms, caller):
    """Require a reflexive, inverse-closed chemical permutation population."""
    maps = np.searchsorted(atoms, table[:, :, 1])
    identity = np.arange(len(atoms), dtype=np.int64)
    if not np.any(np.all(maps == identity, axis=1)):
        raise ArgumentError(
            "correspondences",
            caller=caller,
            message="Pairwise comparison requires the identity correspondence.",
        )
    row_type = np.dtype((np.void, maps.shape[1] * maps.dtype.itemsize))
    rows = np.ascontiguousarray(maps).view(row_type).ravel()
    inverses = np.ascontiguousarray(np.argsort(maps, axis=1)).view(row_type).ravel()
    ordered = np.sort(rows)
    positions = np.searchsorted(ordered, inverses)
    if np.any(positions >= len(ordered)) or not np.array_equal(
        ordered[np.minimum(positions, len(ordered) - 1)], inverses
    ):
        raise ArgumentError(
            "correspondences",
            caller=caller,
            message="Directional correspondence sets cannot define a symmetric matrix.",
        )
    return maps


class CoordinatePopulation(Reducer):
    """Collect a pre-budgeted selected population from projected coordinate blocks."""

    def __init__(self, count, n_atoms, caller):
        self.count, self.n_atoms, self.caller = count, n_atoms, caller
        self.metadata = {"execution": {}}

    def initialize(self, metadata):
        self.coordinates = np.empty((self.count, self.n_atoms, 3), dtype=np.float64)
        self.offset, self.blocks = 0, 0

    def consume(self, chunk):
        values = np.asarray(chunk["coordinates"], dtype=np.float64)
        end = self.offset + len(values)
        if (
            values.shape[1:] != (self.n_atoms, 3)
            or end > self.count
            or not np.isfinite(values).all()
        ):
            raise StructuralInconsistencyError(
                reason="Pairwise RMSD requires finite coordinates on the declared atom axis.",
                caller=self.caller,
            )
        self.coordinates[self.offset : end] = values
        self.offset, self.blocks = end, self.blocks + 1

    def finalize(self):
        if self.offset != self.count:
            raise StructuralInconsistencyError(
                reason="Coordinate delivery did not cover the requested population.",
                caller=self.caller,
            )
        self.metadata["execution"]["n_blocks"] = self.blocks
        return self


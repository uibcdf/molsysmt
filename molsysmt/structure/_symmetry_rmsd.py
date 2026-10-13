"""Bounded positional RMSD reduction over already admitted chemical mappings."""

import numpy as np

from molsysmt._private import rust_backend as kernels
from molsysmt._private.execution import Reducer
from molsysmt._private.smonitor import StructuralInconsistencyError


class SymmetryRMSDReducer(Reducer):
    """Reduce compiled positional RMSDs without a coordinate permutation tensor."""

    def __init__(self, frames, reference, maps, baseline, tolerance, caller):
        self.frames, self.reference, self.maps = frames, reference, maps
        self.baseline, self.tolerance = baseline, tolerance
        self.caller = caller
        self.metadata = {"execution": {}}

    def initialize(self, metadata):
        self.rmsd = np.empty(len(self.frames), dtype=np.float64)
        self.winners = np.empty(len(self.frames), dtype=np.int64)
        self.tie_counts = np.empty(len(self.frames), dtype=np.int64)
        self.raw = (
            None
            if self.baseline is None
            else np.empty(len(self.frames), dtype=np.float64)
        )
        self.offset, self.blocks = 0, 0

    def consume(self, chunk):
        coordinates = np.asarray(chunk["coordinates"], dtype=np.float64)
        if (
            coordinates.shape[1:] != (self.maps.shape[1], 3)
            or not np.isfinite(coordinates).all()
        ):
            raise StructuralInconsistencyError(
                reason="RMSD requires finite coordinates aligned to the selected atom axis.",
                caller=self.caller,
            )
        count = len(coordinates)
        values = np.empty((count, len(self.maps)), dtype=np.float64)
        for index, mapping in enumerate(self.maps):
            values[:, index] = kernels.get_rmsd_with_single_reference_structure(
                coordinates, self.reference[mapping]
            )
        if not np.isfinite(values).all():
            raise StructuralInconsistencyError(
                reason="RMSD arithmetic is not finite.", caller=self.caller
            )
        winners = values.argmin(axis=1)
        best = values[np.arange(count), winners]
        end = self.offset + count
        self.rmsd[self.offset : end] = best
        self.winners[self.offset : end] = winners
        self.tie_counts[self.offset : end] = (
            np.abs(values - best[:, None]) <= self.tolerance
        ).sum(axis=1)
        if self.raw is not None:
            raw = kernels.get_rmsd_with_single_reference_structure(
                coordinates, self.reference[self.baseline]
            )
            if not np.isfinite(raw).all():
                raise StructuralInconsistencyError(
                    reason="Baseline RMSD arithmetic is not finite.", caller=self.caller
                )
            self.raw[self.offset : end] = raw
        self.offset, self.blocks = end, self.blocks + 1

    def finalize(self):
        if self.offset != len(self.frames):
            raise StructuralInconsistencyError(
                reason="Coordinate delivery did not cover every requested structure.",
                caller=self.caller,
            )
        self.metadata["execution"]["n_blocks"] = self.blocks
        return self

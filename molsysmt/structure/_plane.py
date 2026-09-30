"""Fitting unweighted planes to canonical coordinate blocks."""

import numpy as np

from molsysmt._private.execution import Reducer
from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt.pbc._whole_participants import require_whole_participants


def fit_planes(coordinates, offsets, positions, *, caller):
    """Return centroids, unoriented normals and orthogonal deviations in nm.

    Positions index the projected coordinate axis. Each group is an atom set.
    Scaling before SVD avoids squaring the condition number as covariance does.
    """
    n_frames, n_groups = len(coordinates), len(offsets) - 1
    centers = np.empty((n_frames, n_groups, 3), dtype=np.float64)
    normals = np.empty_like(centers)
    rms = np.empty((n_frames, n_groups), dtype=np.float64)
    maximum = np.empty_like(rms)
    for group, (start, stop) in enumerate(zip(offsets[:-1], offsets[1:])):
        xyz = coordinates[:, positions[start:stop]]
        relative = xyz - xyz[:, :1]
        center = relative.mean(axis=1)
        centered = relative - center[:, None]
        scale = np.max(np.abs(centered), axis=(1, 2))
        if not np.isfinite(centered).all() or np.any(scale == 0):
            raise StructuralInconsistencyError(
                reason=f"Plane group {group} contains coincident or unrepresentable coordinates.",
                caller=caller,
            )
        scaled = centered / scale[:, None, None]
        _, singular, axes = np.linalg.svd(scaled, full_matrices=False)
        tolerance = 1e-12 * singular[:, 0]
        if np.any(singular[:, 1] - singular[:, 2] <= tolerance):
            raise StructuralInconsistencyError(
                reason=f"Plane group {group} has no unique normal (collinear or degenerate geometry).",
                caller=caller,
            )
        normal = axes[:, -1]
        pivot = np.argmax(np.abs(normal), axis=1)
        normal *= np.where(normal[np.arange(n_frames), pivot] < 0, -1.0, 1.0)[:, None]
        residual = np.einsum("faj,fj->fa", scaled, normal)
        centers[:, group] = xyz[:, 0] + center
        normals[:, group] = normal
        rms[:, group] = np.sqrt(np.mean(residual * residual, axis=1)) * scale
        maximum[:, group] = np.max(np.abs(residual), axis=1) * scale
    return centers, normals, rms, maximum


class PlaneReducer(Reducer):
    """Fill preallocated dense output while keeping coordinate work in blocks."""

    def __init__(self, offsets, positions, n_atoms, pbc, caller):
        self.offsets, self.positions = offsets, positions
        self.n_atoms, self.pbc, self.caller = n_atoms, pbc, caller

    def initialize(self, metadata):
        shape = (metadata["n_structures"], len(self.offsets) - 1)
        self.outputs = (
            np.empty((*shape, 3)), np.empty((*shape, 3)),
            np.empty(shape), np.empty(shape),
        )
        self.cursor = 0

    def consume(self, chunk):
        coordinates, frames = chunk["coordinates"], chunk["structure_indices"]
        if coordinates is None or (
            coordinates.shape != (len(frames), self.n_atoms, 3)
            or not np.isfinite(coordinates).all()
        ):
            raise StructuralInconsistencyError(
                reason="Finite coordinates are required for all selected plane atoms.",
                caller=self.caller,
            )
        if not len(frames):
            return
        if self.pbc:
            boxes = chunk["box"]
            if boxes is None or (
                boxes.shape != (len(frames), 3, 3) or not np.isfinite(boxes).all()
            ):
                raise StructuralInconsistencyError(
                    reason="PBC plane fitting requires finite, nonsingular boxes for every selected structure.",
                    caller=self.caller,
                )
            scale = np.max(np.abs(boxes), axis=(1, 2))
            if np.any(scale == 0) or np.any(
                np.abs(np.linalg.det(boxes / scale[:, None, None])) <= 1e-12
            ):
                raise StructuralInconsistencyError(
                    reason="Periodic boxes are numerically singular after scale normalization.",
                    caller=self.caller,
                )
            for xyz, box in zip(coordinates, boxes):
                require_whole_participants(xyz, box, self.offsets, self.positions, self.caller)
        block = fit_planes(coordinates, self.offsets, self.positions, caller=self.caller)
        end = self.cursor + len(frames)
        for output, values in zip(self.outputs, block):
            output[self.cursor:end] = values
        self.cursor = end

    def finalize(self):
        if self.cursor != len(self.outputs[0]):
            raise ValueError("Plane fitting did not receive every requested structure.")
        return self.outputs

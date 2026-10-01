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
    from molsysmt._private.rust_backend import get_least_squares_planes

    try:
        return get_least_squares_planes(coordinates, offsets, positions)
    except ValueError as error:
        raise StructuralInconsistencyError(reason=str(error), caller=caller) from error


def plane_pair_geometry(centers, normals, pairs, target_images, box=None):
    """Measure unoriented plane pairs in the observed second-participant image.

    Inputs are canonical numeric arrays, with row lattice vectors. Return
    centroid distance, acute plane angle in radians, and each lateral offset.
    No interaction criterion or chemical interpretation is applied here.
    """
    first, second = pairs.T
    delta = centers[second] - centers[first]
    if box is not None:
        delta = delta + target_images @ box
    a, b = normals[first], normals[second]
    angle = np.arctan2(np.linalg.norm(np.cross(a, b), axis=1),
                       np.abs(np.einsum("ij,ij->i", a, b)))
    offset_a = np.linalg.norm(delta - np.einsum("ij,ij->i", delta, a)[:, None] * a, axis=1)
    offset_b = np.linalg.norm(delta - np.einsum("ij,ij->i", delta, b)[:, None] * b, axis=1)
    return np.linalg.norm(delta, axis=1), angle, offset_a, offset_b



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

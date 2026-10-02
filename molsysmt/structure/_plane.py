"""Fitting unweighted planes to canonical coordinate blocks."""

import numpy as np

from molsysmt._private.execution import Reducer
from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt.pbc._whole_participants import (
    require_whole_participants,
    validate_periodic_boxes,
)


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
    angle = np.arctan2(
        np.linalg.norm(np.cross(a, b), axis=1), np.abs(np.einsum("ij,ij->i", a, b))
    )
    offset_a = np.linalg.norm(
        delta - np.einsum("ij,ij->i", delta, a)[:, None] * a, axis=1
    )
    offset_b = np.linalg.norm(
        delta - np.einsum("ij,ij->i", delta, b)[:, None] * b, axis=1
    )
    return np.linalg.norm(delta, axis=1), angle, offset_a, offset_b


def plane_point_geometry(points, centers, normals):
    """Measure point distances, acute normal angles, lateral offsets and heights.

    Corresponding rows refer to the same observed Cartesian image; lengths
    retain the numerical input unit and angles are radians. No chemical or
    interaction criterion is applied. Normals must be unit vectors.
    """
    delta = points - centers
    projection = np.einsum("ij,ij->i", delta, normals)
    offset = np.linalg.norm(delta - projection[:, None] * normals, axis=1)
    height = np.abs(projection)
    return np.linalg.norm(delta, axis=1), np.arctan2(offset, height), offset, height


def centroid_edge_planes(coordinates, offsets, positions):
    """Form centroid planes from the first two ordered members of each group.

    This reproduces ProLIF's geometric construction; it is not a least-squares
    fit. Degenerate centroid edges produce NaN normals/deviations, allowing a
    caller to reject undefined angular observations without changing the group.
    """
    from molsysmt.structure._centroid import packed_centroids

    centers = packed_centroids(coordinates, offsets, positions)
    first = coordinates[:, positions[offsets[:-1]]] - centers
    second = coordinates[:, positions[offsets[:-1] + 1]] - centers
    normals = np.cross(first, second)
    lengths = np.linalg.norm(normals, axis=-1)
    normals = np.divide(
        normals,
        lengths[..., None],
        out=np.full_like(normals, np.nan),
        where=lengths[..., None] > 0,
    )
    groups = np.repeat(np.arange(len(centers[0])), np.diff(offsets))
    delta = coordinates[:, positions] - centers[:, groups]
    deviation = np.einsum("tij,tij->ti", delta, normals[:, groups])
    rms = np.sqrt(
        np.add.reduceat(deviation**2, offsets[:-1], axis=1) / np.diff(offsets)
    )
    maximum = np.maximum.reduceat(np.abs(deviation), offsets[:-1], axis=1)
    return centers, normals, rms, maximum


def triangle_planes(coordinates, offsets, positions):
    """Form normals from the first three ordered atoms, retaining group centroids.

    This is Mol*'s charged-interaction geometric construction. Undefined
    triangles produce NaN normals; they are not replaced with fitted planes.
    """
    from molsysmt.structure._centroid import packed_centroids

    centers = packed_centroids(coordinates, offsets, positions)
    first = coordinates[:, positions[offsets[:-1]]]
    second = coordinates[:, positions[offsets[:-1] + 1]]
    third = coordinates[:, positions[offsets[:-1] + 2]]
    normals = np.cross(second - first, third - first)
    lengths = np.linalg.norm(normals, axis=-1)
    normals = np.divide(
        normals,
        lengths[..., None],
        out=np.full_like(normals, np.nan),
        where=lengths[..., None] > 0,
    )
    groups = np.repeat(np.arange(len(centers[0])), np.diff(offsets))
    deviation = np.einsum(
        "tij,tij->ti",
        coordinates[:, positions] - centers[:, groups],
        normals[:, groups],
    )
    rms = np.sqrt(
        np.add.reduceat(deviation**2, offsets[:-1], axis=1) / np.diff(offsets)
    )
    maximum = np.maximum.reduceat(np.abs(deviation), offsets[:-1], axis=1)
    return centers, normals, rms, maximum


def plane_intersection_projection(
    centers_a, normals_a, centers_b, normals_b, *, near_singular=False
):
    """Project the first centroid on the line common to two planes.

    Return a point per row, or NaNs when the planes cannot define the line.
    This general geometric operation has no ring or interaction criterion.
    The projection depends on which plane is first. near_singular selects
    NumPy's default isclose determinant tolerance rather than exact singularity.
    Lengths retain the numerical input unit; normals must be unit vectors.
    """
    direction = np.cross(normals_a, normals_b)
    matrices = np.stack((normals_a, normals_b, direction), axis=1)
    determinants = np.linalg.det(matrices)
    valid = np.isfinite(determinants) & ~(
        np.isclose(determinants, 0) if near_singular else determinants == 0
    )
    output = np.full_like(centers_a, np.nan, dtype=np.float64)
    if valid.any():
        a, b, line = normals_a[valid], normals_b[valid], direction[valid]
        rhs = np.column_stack(
            (
                np.einsum("ij,ij->i", a, centers_a[valid]),
                np.einsum("ij,ij->i", b, centers_b[valid]),
                np.zeros(valid.sum()),
            )
        )
        point = np.linalg.solve(matrices[valid], rhs[..., None])[..., 0]
        line /= np.linalg.norm(line, axis=1)[:, None]
        output[valid] = (
            point
            + np.einsum("ij,ij->i", centers_a[valid] - point, line)[:, None] * line
        )
    return output


class PlaneReducer(Reducer):
    """Fill preallocated dense output while keeping coordinate work in blocks."""

    def __init__(self, offsets, positions, n_atoms, pbc, caller):
        self.offsets, self.positions = offsets, positions
        self.n_atoms, self.pbc, self.caller = n_atoms, pbc, caller

    def initialize(self, metadata):
        shape = (metadata["n_structures"], len(self.offsets) - 1)
        self.outputs = (
            np.empty((*shape, 3)),
            np.empty((*shape, 3)),
            np.empty(shape),
            np.empty(shape),
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
            validate_periodic_boxes(boxes, len(frames), caller=self.caller)
            for xyz, box in zip(coordinates, boxes):
                require_whole_participants(
                    xyz, box, self.offsets, self.positions, self.caller
                )
        block = fit_planes(
            coordinates, self.offsets, self.positions, caller=self.caller
        )
        end = self.cursor + len(frames)
        for output, values in zip(self.outputs, block):
            output[self.cursor : end] = values
        self.cursor = end

    def finalize(self):
        if self.cursor != len(self.outputs[0]):
            raise ValueError("Plane fitting did not receive every requested structure.")
        return self.outputs

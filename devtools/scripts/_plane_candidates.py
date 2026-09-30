"""Keeping the measured NumPy controls for the plane-kernel comparison.

These are benchmark controls for #265, not runtime fallbacks or public tools.
The grouped control preserves the pre-optimization arithmetic for comparison.
"""

import numpy as np

from molsysmt._private.smonitor import StructuralInconsistencyError


def _numpy_grouped(coordinates, offsets, positions, *, caller):
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


def _numpy_batched(coordinates, offsets, positions, *, workspace_bytes=8 * 1024**2):
    """Tile frames/groups of equal length under a numerical workspace estimate."""
    ns, ng = len(coordinates), len(offsets) - 1
    outputs = (np.empty((ns, ng, 3)), np.empty((ns, ng, 3)), np.empty((ns, ng)), np.empty((ns, ng)))
    lengths = np.diff(offsets)
    for length in np.unique(lengths):
        indices = np.flatnonzero(lengths == length)
        frame_size = max(1, min(ns, workspace_bytes // (192 * int(length))))
        for begin in range(0, ns, frame_size):
            end = min(ns, begin + frame_size)
            group_size = max(1, workspace_bytes // (192 * int(length) * (end - begin)))
            for start in range(0, len(indices), group_size):
                selected = indices[start:start + group_size]
                membership = np.stack([positions[offsets[i]:offsets[i + 1]] for i in selected])
                xyz = coordinates[begin:end, membership]
                relative = xyz - xyz[:, :, :1]
                center = relative.mean(axis=2)
                centered = relative - center[:, :, None]
                scale = np.max(np.abs(centered), axis=(2, 3))
                if not np.isfinite(centered).all() or np.any(scale == 0):
                    raise ValueError("Coincident or unrepresentable geometry.")
                scaled = centered / scale[:, :, None, None]
                _, singular, axes = np.linalg.svd(scaled, full_matrices=False)
                if np.any(singular[:, :, 1] - singular[:, :, 2] <= 1e-12 * singular[:, :, 0]):
                    raise ValueError("No unique plane normal.")
                normal = axes[:, :, -1]
                pivot = np.argmax(np.abs(normal), axis=2)
                lead = np.take_along_axis(normal, pivot[:, :, None], axis=2)[:, :, 0]
                normal *= np.where(lead < 0, -1., 1.)[:, :, None]
                residual = np.einsum("fgaj,fgj->fga", scaled, normal)
                outputs[0][begin:end, selected] = xyz[:, :, 0] + center
                outputs[1][begin:end, selected] = normal
                outputs[2][begin:end, selected] = np.sqrt(np.mean(residual * residual, axis=2)) * scale
                outputs[3][begin:end, selected] = np.max(np.abs(residual), axis=2) * scale
    return outputs

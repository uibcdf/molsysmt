"""Applying attributed ring geometry criteria without perceiving chemistry."""

import numpy as np

from molsysmt.structure._plane import plane_intersection_projection


def reference_pi_masks(method, centers, normals, pairs, shifts, box, distances,
                       plane_angles, offset_a, offset_b, thresholds):
    """Return face/edge decisions, both normal angles and intersection distances."""
    a, b = pairs.T
    first, second = centers[a], centers[b]
    if box is not None:
        second = second + shifts @ box
    delta = second - first
    n_a, n_b = normals[a], normals[b]
    cos_a = np.divide(np.abs(np.einsum("ij,ij->i", delta, n_a)), distances,
                      out=np.full(len(pairs), np.nan), where=distances > 0)
    cos_b = np.divide(np.abs(np.einsum("ij,ij->i", delta, n_b)), distances,
                      out=np.full(len(pairs), np.nan), where=distances > 0)
    angle_a = np.arccos(np.clip(cos_a, 0, 1))
    angle_b = np.arccos(np.clip(cos_b, 0, 1))
    intersection = np.full(len(pairs), np.nan)
    if method == "molstar_geometry":
        limit, offset = thresholds["angle_threshold"], thresholds["offset_threshold"]
        lateral = np.minimum(offset_a, offset_b) <= offset
        return (plane_angles <= limit) & lateral, (np.pi / 2 - plane_angles <= limit) & lateral, angle_a, angle_b, intersection
    plane_cosine = np.abs(np.einsum("ij,ij->i", n_a, n_b))
    plane_angles = np.arccos(np.clip(plane_cosine, 0, 1))
    face = (distances <= thresholds["face_distance"]) & (plane_angles <= np.deg2rad(35))
    face &= (angle_a <= np.deg2rad(33)) | (angle_b <= np.deg2rad(33))
    edge = (distances <= thresholds["edge_distance"]) & (plane_angles >= np.deg2rad(50))
    edge &= (angle_a <= np.deg2rad(30)) | (angle_b <= np.deg2rad(30))
    # The inspected core projects the first centroid; preserve that role order.
    if edge.any():
        point = plane_intersection_projection(first[edge], n_a[edge], second[edge], n_b[edge],
                                              near_singular=method == "mdtraj_geometry")
        intersection[edge] = np.minimum(np.linalg.norm(point - first[edge], axis=1),
                                        np.linalg.norm(point - second[edge], axis=1))
        edge &= intersection <= .15
    return face, edge, angle_a, angle_b, intersection

"""Reduce projected coordinate blocks to attributed sparse cation-ring observations."""

import numpy as np

from molsysmt._private.execution import Reducer
from molsysmt._private.execution.sparse_accumulator import SparseColumnAccumulator
from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt._private.sparse_membership import pack_membership
from molsysmt.interactions.result import Interactions
from molsysmt.pbc._whole_participants import (
    require_whole_participants,
    validate_periodic_boxes,
)
from molsysmt.structure._centroid import packed_centroids
from molsysmt.structure._group_minimum_contacts import bounded_group_minimum_contacts
from molsysmt.structure._plane import (
    centroid_edge_planes,
    fit_planes,
    plane_point_geometry,
    triangle_planes,
)


class _CationPiReducer(Reducer):
    def __init__(self, *, members, active, universe, searches, excluded, thresholds,
                 n_cations, charges, method, metadata, budget_bytes):
        self.members, self.active, self.universe = members, active, universe
        self.searches, self.thresholds, self.method = searches, thresholds, method
        self.metadata, self.budget_bytes, self.charges = metadata, budget_bytes, charges
        atoms, self.offsets = pack_membership([members[i] for i in active])
        self.positions = np.searchsorted(universe, atoms)
        self.active_positions = np.full(len(members), -1, dtype=np.int64)
        self.active_positions[active] = np.arange(len(active))
        self.cat_local = np.flatnonzero(active < n_cations)
        self.ring_local = np.flatnonzero(active >= n_cations)
        ring_atoms, self.ring_offsets = pack_membership([members[i] for i in active[active >= n_cations]])
        self.ring_positions = np.searchsorted(universe, ring_atoms)
        self.pair_dtype = np.dtype([("a", np.int64), ("b", np.int64)])
        self.excluded = np.asarray(sorted(excluded), dtype=np.int64).reshape(-1, 2).view(self.pair_dtype).ravel()

    def initialize(self, metadata):
        self.schema = {"frames": (np.int64, ()), "pairs": (np.int64, (2,)), "images": (np.int32, (2, 3))}
        self.schema.update({name: (np.float64, ()) for name in self.metadata["measure_units"]})
        fixed = 8 * (2 * self.metadata["n_atoms"] + 4 * self.metadata["n_structures"])
        fixed += sum(value.nbytes for value in (self.positions, self.offsets, self.active_positions,
                     self.ring_offsets, self.ring_positions, self.cat_local, self.ring_local, self.excluded, self.charges))
        self.columns = SparseColumnAccumulator(self.schema, budget_bytes=self.budget_bytes // 2, fixed_bytes=fixed)
        self.columns.check_budget()
        self.chunks, self.periodic = 0, None

    def consume(self, chunk):
        coordinates, boxes, frames = chunk["coordinates"], chunk["box"], chunk["structure_indices"]
        caller = self.metadata["method"]
        if coordinates is None or coordinates.shape != (len(frames), len(self.universe), 3) or not np.isfinite(coordinates).all():
            raise StructuralInconsistencyError(reason="Finite coordinates are required for every evaluated participant atom.", caller=caller)
        if boxes is not None:
            validate_periodic_boxes(boxes, len(frames), caller=caller)
            for xyz, box in zip(coordinates, boxes):
                require_whole_participants(xyz, box, self.offsets, self.positions, caller)
        has_box = boxes is not None
        if self.periodic is not None and self.periodic != has_box:
            raise StructuralInconsistencyError(reason="Periodic box availability changed between blocks.", caller=caller)
        self.periodic, self.chunks = has_box, self.chunks + 1
        centers = packed_centroids(coordinates, self.offsets, self.positions)
        normals = np.zeros_like(centers)
        rms = np.zeros(centers.shape[:2])
        maximum = np.zeros_like(rms)
        if self.method == "prolif":
            ring_centers, ring_normals, ring_rms, ring_max = centroid_edge_planes(
                coordinates, self.ring_offsets, self.ring_positions)
            angle_low, angle_high = self.thresholds["angle_threshold"]
            angle_cutoff = angle_high
            offset_cutoff, planarity_cutoff = np.inf, np.inf
        elif self.method == "molstar_geometry":
            ring_centers, ring_normals, ring_rms, ring_max = triangle_planes(
                coordinates, self.ring_offsets, self.ring_positions)
            angle_cutoff, planarity_cutoff = np.inf, np.inf
            offset_cutoff = self.thresholds["offset_threshold"]
        else:
            ring_centers, ring_normals, ring_rms, ring_max = fit_planes(
                coordinates, self.ring_offsets, self.ring_positions, caller=caller)
            angle_cutoff = min(np.nextafter(self.thresholds["angle_threshold"], np.inf), np.nextafter(np.pi / 2, -np.inf))
            offset_cutoff, planarity_cutoff = [np.nextafter(self.thresholds[name], np.inf)
                                             for name in ("offset_threshold", "planarity_threshold")]
        centers[:, self.ring_local] = ring_centers
        normals[:, self.ring_local], rms[:, self.ring_local], maximum[:, self.ring_local] = ring_normals, ring_rms, ring_max
        distance_cutoff = self.thresholds["distance_threshold"]
        for local, frame in enumerate(frames):
            center, normal = centers[local], normals[local]
            box = None if boxes is None else boxes[local]
            planar = maximum[local] <= planarity_cutoff
            for first, second in self.searches:
                second = second[planar[self.active_positions[second]]]
                if not len(first) or not len(second):
                    continue
                pairs, _, shifts = bounded_group_minimum_contacts(
                    center[self.active_positions[first]], first,
                    center[self.active_positions[second]], second,
                    distance_cutoff, box, self.budget_bytes // 8)
                if len(self.excluded):
                    canonical = np.ascontiguousarray(pairs).view(self.pair_dtype).ravel()
                    keep = ~np.isin(canonical, self.excluded)
                    pairs, shifts = pairs[keep], shifts[keep]
                if not len(pairs):
                    continue
                a, b = self.active_positions[pairs].T
                observed_ring = center[b] if box is None else center[b] + shifts @ box
                distances, angles, offsets, heights = plane_point_geometry(center[a], observed_ring, normal[b])
                if self.method == "prolif":
                    signed_height = np.einsum("ij,ij->i", center[a] - observed_ring, normal[b])
                    oriented_cosine = np.divide(signed_height, distances, out=np.full(len(distances), np.nan), where=distances > 0)
                    oriented_angles = np.arccos(np.clip(oriented_cosine, -1., 1.))
                    cosine = np.divide(heights, distances, out=np.full(len(distances), np.nan), where=distances > 0)
                    angles = np.arccos(np.clip(cosine, 0., 1.))
                    keep = (distances <= distance_cutoff) & (angles >= angle_low) & (angles <= angle_high)
                elif self.method == "molstar_geometry":
                    keep = (distances > 0) & (distances <= distance_cutoff) & (offsets <= offset_cutoff)
                else:
                    keep = (distances > 0) & (distances <= np.nextafter(distance_cutoff, np.inf)) & (angles <= angle_cutoff) & (offsets <= offset_cutoff)
                if not keep.any():
                    continue
                pairs, shifts = pairs[keep], shifts[keep]
                images = np.zeros((len(pairs), 2, 3), dtype=np.int32)
                images[:, 1] = shifts
                self.columns.append({
                    "frames": np.full(len(pairs), frame, dtype=np.int64), "pairs": pairs, "images": images,
                    "distance": distances[keep], "normal_angle": angles[keep], "offset": offsets[keep], "height": heights[keep],
                    "ring_rms_deviation": rms[local, b[keep]], "ring_max_deviation": maximum[local, b[keep]],
                    "cation_charge": self.charges[pairs[:, 0]],
                    **({"oriented_normal_angle": oriented_angles[keep]} if self.method == "prolif" else {}),
                })

    def finalize(self):
        self.metadata["execution"]["execution_chunks"] = self.chunks
        if not self.columns.n_rows:
            return Interactions.from_records([], **self.metadata)
        relation_pairs, occurrence_relations = np.unique(self.columns.concatenate("pairs"), axis=0, return_inverse=True)
        membership_count = sum(len(self.members[i]) for i in relation_pairs.ravel())
        self.columns.check_budget(extra_bytes=24 * membership_count + 128 * len(relation_pairs))
        frames = self.columns.concatenate("frames")
        order = np.lexsort((occurrence_relations, frames))
        atoms, offsets = pack_membership([self.members[i] for i in relation_pairs.ravel()])
        result = Interactions(
            relation_types=["cation_pi"] * len(relation_pairs),
            relation_participant_offsets=np.arange(len(relation_pairs) + 1, dtype=np.int64) * 2,
            participant_roles=[role for _ in relation_pairs for role in ("cation", "ring")],
            participant_atom_offsets=offsets, participant_atoms=atoms,
            occurrence_structures=frames[order], occurrence_relations=occurrence_relations[order],
            occurrence_evidence=np.zeros(len(order), dtype=np.int32),
            evidence_labels=["prolif_cation_pi_geometry" if self.method == "prolif" else "formal_cation_declared_aromatic_geometry"],
            measurements={name: self.columns.concatenate(name)[order] for name in self.metadata["measure_units"]},
            occurrence_image_offsets=np.arange(len(order) + 1, dtype=np.int64) * 2 if self.periodic else None,
            image_vectors=self.columns.concatenate("images")[order].reshape(-1, 3) if self.periodic else None,
            **self.metadata)
        self.columns.clear()
        return result

"""Reducing projected structural blocks to sparse ring-pair observations."""

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
from molsysmt.structure._group_minimum_contacts import bounded_group_minimum_contacts
from molsysmt.structure._plane import (
    centroid_edge_planes,
    fit_planes,
    plane_pair_geometry,
    triangle_planes,
)


class _PiPiReducer(Reducer):
    def __init__(self, *, members, active, universe, searches, excluded, thresholds,
                 geometry, method, metadata, budget_bytes):
        self.members, self.active, self.universe = members, active, universe
        self.searches, self.thresholds, self.geometry = searches, thresholds, geometry
        self.metadata, self.budget_bytes = metadata, budget_bytes
        self.method = method
        atoms, self.offsets = pack_membership([members[i] for i in active])
        self.positions = np.searchsorted(universe, atoms)
        self.active_positions = np.full(len(members), -1, dtype=np.int64)
        self.active_positions[active] = np.arange(len(active))
        self.pair_dtype = np.dtype([("a", np.int64), ("b", np.int64)])
        self.excluded = np.asarray(sorted(excluded), dtype=np.int64).reshape(-1, 2).view(self.pair_dtype).ravel()

    def initialize(self, metadata):
        self.schema = {"frames": (np.int64, ()), "pairs": (np.int64, (2,)),
                       "evidence": (np.int32, ()), "images": (np.int32, (2, 3))}
        self.schema.update({name: (np.float64, ()) for name in self.metadata["measure_units"]})
        fixed = 8 * (2 * self.metadata["n_atoms"] + 4 * self.metadata["n_structures"])
        fixed += self.positions.nbytes + self.offsets.nbytes + self.active_positions.nbytes + self.excluded.nbytes
        self.columns = SparseColumnAccumulator(self.schema, budget_bytes=self.budget_bytes // 2, fixed_bytes=fixed)
        self.columns.check_budget()
        self.chunks, self.periodic = 0, None

    def consume(self, chunk):
        coordinates, boxes, frames = chunk["coordinates"], chunk["box"], chunk["structure_indices"]
        caller = self.metadata["method"]
        if coordinates is None or coordinates.shape != (len(frames), len(self.universe), 3) or not np.isfinite(coordinates).all():
            raise StructuralInconsistencyError(reason="Finite coordinates are required for every evaluated ring atom.", caller=caller)
        if boxes is not None:
            validate_periodic_boxes(boxes, len(frames), caller=caller)
            for xyz, box in zip(coordinates, boxes):
                require_whole_participants(xyz, box, self.offsets, self.positions, caller)
        has_box = boxes is not None
        if self.periodic is not None and self.periodic != has_box:
            raise StructuralInconsistencyError(reason="Periodic box availability changed between blocks.", caller=caller)
        self.periodic = has_box
        self.chunks += 1
        if self.method == "centroid_angle_offset":
            centers, normals, rms, maximum = fit_planes(coordinates, self.offsets, self.positions, caller=caller)
        else:
            plane = triangle_planes if self.method == "molstar_geometry" else centroid_edge_planes
            centers, normals, rms, maximum = plane(coordinates, self.offsets, self.positions)
        distance_cutoff = self.thresholds["distance_threshold"]
        angle_cutoff, offset_cutoff, planarity_cutoff = [np.nextafter(self.thresholds.get(name, np.inf), np.inf)
            for name in ("angle_threshold", "offset_threshold", "planarity_threshold")]
        # Roundoff must not make the two nominally disjoint classes overlap.
        angle_cutoff = min(angle_cutoff, np.nextafter(np.pi / 4, -np.inf))
        for local, frame in enumerate(frames):
            center, normal, max_dev, rms_dev = centers[local], normals[local], maximum[local], rms[local]
            box = None if boxes is None else boxes[local]
            planar = max_dev <= planarity_cutoff
            for first, second, triangular in self.searches:
                first = first[planar[self.active_positions[first]]]
                second = second[planar[self.active_positions[second]]]
                if not len(first) or not len(second):
                    continue
                pairs, _, shifts = bounded_group_minimum_contacts(
                    center[self.active_positions[first]], first,
                    center[self.active_positions[second]], second,
                    distance_cutoff, box, self.budget_bytes // 8,
                )
                if triangular:
                    keep = pairs[:, 0] < pairs[:, 1]
                    pairs, shifts = pairs[keep], shifts[keep]
                reverse = pairs[:, 0] > pairs[:, 1]
                pairs[reverse] = pairs[reverse, ::-1]
                shifts[reverse] *= -1
                if len(self.excluded):
                    canonical = np.ascontiguousarray(pairs).view(self.pair_dtype).ravel()
                    keep = ~np.isin(canonical, self.excluded)
                    pairs, shifts = pairs[keep], shifts[keep]
                if not len(pairs):
                    continue
                projected_pairs = self.active_positions[pairs]
                distances, angles, offset_a, offset_b = plane_pair_geometry(center, normal, projected_pairs, shifts, box)
                extra = {}
                if self.method == "centroid_angle_offset":
                    parallel = (angles <= angle_cutoff) & (np.maximum(offset_a, offset_b) <= offset_cutoff)
                    edge = (np.pi / 2 - angles <= angle_cutoff) & (np.minimum(offset_a, offset_b) <= offset_cutoff)
                else:
                    from molsysmt.interactions.pi_pi._criteria import reference_pi_masks

                    a, b = projected_pairs.T
                    angles = np.arccos(np.clip(np.abs(np.einsum("ij,ij->i", normal[a], normal[b])), 0, 1))
                    parallel, edge, normal_a, normal_b, intersection = reference_pi_masks(
                        self.method, center, normal, projected_pairs, shifts, box,
                        distances, angles, offset_a, offset_b, self.thresholds)
                    extra = dict(normal_angle_a=normal_a, normal_angle_b=normal_b, intersection_distance=intersection)
                keep = parallel if self.geometry == "parallel" else edge if self.geometry == "edge_to_face" else parallel | edge
                limit = np.nextafter(distance_cutoff, np.inf) if self.method == "centroid_angle_offset" else distance_cutoff
                keep &= (distances > 0) & (distances <= limit)
                if not keep.any():
                    continue
                pairs, shifts = pairs[keep], shifts[keep]
                a, b = projected_pairs[keep].T
                images = np.zeros((len(pairs), 2, 3), dtype=np.int32)
                images[:, 1] = shifts
                self.columns.append({
                    "frames": np.full(len(pairs), frame, dtype=np.int64), "pairs": pairs,
                    "evidence": (~parallel[keep]).astype(np.int32), "images": images,
                    "distance": distances[keep], "plane_angle": angles[keep],
                    "offset_a": offset_a[keep], "offset_b": offset_b[keep],
                    "rms_deviation_a": rms_dev[a], "rms_deviation_b": rms_dev[b],
                    "max_deviation_a": max_dev[a], "max_deviation_b": max_dev[b],
                    **{name: values[keep] for name, values in extra.items()},
                })

    def finalize(self):
        self.metadata["parameters"]["execution_chunks"] = self.chunks
        if not self.columns.n_rows:
            return Interactions.from_records([], **self.metadata)
        relation_pairs, occurrence_relations = np.unique(self.columns.concatenate("pairs"), axis=0, return_inverse=True)
        membership_count = sum(len(self.members[i]) for i in relation_pairs.ravel())
        self.columns.check_budget(extra_bytes=24 * membership_count + 128 * len(relation_pairs))
        frames = self.columns.concatenate("frames")
        order = np.lexsort((occurrence_relations, frames))
        atoms, offsets = pack_membership([self.members[i] for i in relation_pairs.ravel()])
        result = Interactions(
            relation_types=["pi_pi"] * len(relation_pairs),
            relation_participant_offsets=np.arange(len(relation_pairs) + 1, dtype=np.int64) * 2,
            participant_roles=[role for _ in relation_pairs for role in ("ring_a", "ring_b")],
            participant_atom_offsets=offsets, participant_atoms=atoms,
            occurrence_structures=frames[order], occurrence_relations=occurrence_relations[order],
            occurrence_evidence=self.columns.concatenate("evidence")[order],
            evidence_labels=["declared_aromatic_parallel_geometry", "declared_aromatic_edge_to_face_geometry"],
            measurements={name: self.columns.concatenate(name)[order] for name in self.metadata["measure_units"]},
            occurrence_image_offsets=np.arange(len(order) + 1, dtype=np.int64) * 2 if self.periodic else None,
            image_vectors=self.columns.concatenate("images")[order].reshape(-1, 3) if self.periodic else None,
            **self.metadata,
        )
        self.columns.clear()
        return result

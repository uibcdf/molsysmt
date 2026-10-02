"""Reducing canonical coordinate blocks to one sparse ionic analysis."""

import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.execution import Reducer
from molsysmt._private.execution.sparse_accumulator import SparseColumnAccumulator
from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt._private.sparse_membership import pack_membership
from molsysmt.interactions.result import Interactions
from molsysmt.pbc._whole_participants import require_whole_participants
from molsysmt.structure._group_minimum_contacts import bounded_group_minimum_contacts


class _IonicReducer(Reducer):
    def __init__(
        self,
        *,
        centers,
        members,
        universe,
        active,
        searches,
        threshold,
        excluded,
        metadata,
        budget_bytes,
    ):
        self.centers, self.members, self.universe = centers, members, universe
        self.threshold, self.metadata = threshold, metadata
        self.budget_bytes = budget_bytes
        self.searches = []
        geometry = centers["geometry_atom_indices"]
        offsets = centers["geometry_atom_offsets"]
        for first, second in searches:
            planned = []
            for indices in (first, second):
                groups = [geometry[offsets[i] : offsets[i + 1]] for i in indices]
                atoms = np.concatenate(groups)
                planned.extend(
                    (
                        np.searchsorted(universe, atoms),
                        np.repeat(indices, [len(group) for group in groups]),
                    )
                )
            self.searches.append(tuple(planned))
        self.pair_dtype = np.dtype([("a", np.int64), ("b", np.int64)])
        self.excluded_rows = (
            np.asarray(sorted(excluded), dtype=np.int64)
            .reshape(-1, 2)
            .view(self.pair_dtype)
            .ravel()
        )
        whole_atoms = np.concatenate([members[i] for i in active])
        self.whole_offsets = np.concatenate(
            ([0], np.cumsum([len(members[i]) for i in active]))
        )
        self.whole_positions = np.searchsorted(universe, whole_atoms)

    def initialize(self, metadata):
        self.columns = SparseColumnAccumulator(
            {
                "frames": (np.int64, ()),
                "pairs": (np.int64, (2,)),
                "distances": (np.float64, ()),
                "images": (np.int32, (2, 3)),
            },
            budget_bytes=self.budget_bytes // 2,
            fixed_bytes=8
            * (2 * self.metadata["n_atoms"] + 4 * self.metadata["n_structures"]),
        )
        self.columns.check_budget()
        self.periodic = None
        self.chunks = 0

    def consume(self, chunk):
        coordinates, boxes, frames = (
            chunk["coordinates"],
            chunk["box"],
            chunk["structure_indices"],
        )
        caller = self.metadata["method"]
        if coordinates is None or (
            coordinates.shape != (len(frames), len(self.universe), 3)
            or not np.isfinite(coordinates).all()
        ):
            raise StructuralInconsistencyError(
                reason="Finite coordinates are required for every evaluated center.",
                caller=caller,
            )
        if boxes is not None and (
            boxes.shape != (len(frames), 3, 3)
            or not np.isfinite(boxes).all()
            or np.any(np.abs(np.linalg.det(boxes)) < 1e-12)
        ):
            raise StructuralInconsistencyError(
                reason="Periodic boxes must be finite and nonsingular.",
                caller=caller,
            )
        has_box = boxes is not None
        if self.periodic is not None and self.periodic != has_box:
            raise StructuralInconsistencyError(
                reason="Periodic box availability changed between coordinate blocks.",
                caller=caller,
            )
        self.periodic = has_box
        self.chunks += 1
        pending = {name: [] for name in ("frames", "pairs", "distances", "images")}
        pending_bytes = 0
        for local_frame, frame in enumerate(frames):
            xyz, box = (
                coordinates[local_frame],
                None if boxes is None else boxes[local_frame],
            )
            if box is not None:
                require_whole_participants(
                    xyz, box, self.whole_offsets, self.whole_positions, caller
                )
            observations = [
                bounded_group_minimum_contacts(
                    xyz[pos_positions],
                    pos_centers,
                    xyz[neg_positions],
                    neg_centers,
                    self.threshold,
                    box,
                    self.budget_bytes // 8,
                )
                for pos_positions, pos_centers, neg_positions, neg_centers in self.searches
            ]
            pairs, distances, target_images = [
                np.concatenate(parts) for parts in zip(*observations)
            ]
            if len(self.excluded_rows):
                canonical = (
                    np.ascontiguousarray(np.sort(pairs, axis=1))
                    .view(self.pair_dtype)
                    .ravel()
                )
                keep = ~np.isin(canonical, self.excluded_rows)
                pairs, distances, target_images = (
                    pairs[keep],
                    distances[keep],
                    target_images[keep],
                )
            if not len(pairs):
                continue
            images = np.zeros((len(pairs), 2, 3), dtype=np.int32)
            images[:, 1] = target_images
            columns = {
                "frames": np.full(len(pairs), frame, dtype=np.int64),
                "pairs": pairs,
                "distances": distances,
                "images": images,
            }
            pending_bytes += sum(value.nbytes for value in columns.values())
            self.columns.check_budget(extra_bytes=6 * pending_bytes)
            for name, value in columns.items():
                pending[name].append(value)
        if pending["frames"]:
            self.columns.append(
                {name: np.concatenate(blocks) for name, blocks in pending.items()}
            )

    def finalize(self):
        self.metadata["execution"]["execution_chunks"] = self.chunks
        if not self.columns.n_rows:
            return Interactions.from_records([], **self.metadata)
        relation_pairs, occurrence_relations = np.unique(
            self.columns.concatenate("pairs"),
            axis=0,
            return_inverse=True,
        )
        membership_count = sum(len(self.members[i]) for i in relation_pairs.ravel())
        self.columns.check_budget(
            extra_bytes=24 * membership_count + 128 * len(relation_pairs)
        )
        occurrence_frames = self.columns.concatenate("frames")
        order = np.lexsort((occurrence_relations, occurrence_frames))
        occurrence_relations, occurrence_frames = (
            occurrence_relations[order],
            occurrence_frames[order],
        )
        atoms, atom_offsets = pack_membership(
            [self.members[i] for i in relation_pairs.ravel()]
        )
        charges = puw.get_value(self.centers["charges"], to_unit="e")
        result = Interactions(
            relation_types=["ionic_contact"] * len(relation_pairs),
            relation_participant_offsets=np.arange(len(relation_pairs) + 1) * 2,
            participant_roles=[
                role for _ in relation_pairs for role in ("positive", "negative")
            ],
            participant_atom_offsets=atom_offsets,
            participant_atoms=atoms,
            occurrence_structures=occurrence_frames,
            occurrence_relations=occurrence_relations,
            occurrence_evidence=np.zeros(len(occurrence_relations), dtype=np.int32),
            evidence_labels=["formal_charge_geometric_proximity"],
            measurements={
                "distance": self.columns.concatenate("distances")[order],
                "positive_charge": charges[relation_pairs[occurrence_relations, 0]],
                "negative_charge": charges[relation_pairs[occurrence_relations, 1]],
            },
            occurrence_image_offsets=np.arange(len(order) + 1) * 2
            if self.periodic
            else None,
            image_vectors=self.columns.concatenate("images")[order].reshape(-1, 3)
            if self.periodic
            else None,
            **self.metadata,
        )
        self.columns.clear()
        return result

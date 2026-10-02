"""Reduce projected coordinates to canonical metal coordination atom pairs."""

import numpy as np

from molsysmt._private.execution import Reducer
from molsysmt._private.execution.sparse_accumulator import SparseColumnAccumulator
from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt.interactions.result import Interactions
from molsysmt.pbc._triplet_images import observed_chains
from molsysmt.pbc._whole_participants import validate_periodic_boxes
from molsysmt.structure._group_minimum_contacts import bounded_group_minimum_contacts


class _MetalCoordinationReducer(Reducer):
    def __init__(self, *, universe, searches, distance, metadata, budget_bytes):
        self.universe, self.searches, self.distance = universe, searches, distance
        self.metadata, self.budget_bytes = metadata, budget_bytes

    def initialize(self, metadata):
        fixed = 8 * (2 * self.metadata["n_atoms"] + 4 * self.metadata["n_structures"])
        fixed += self.universe.nbytes + sum(
            a.nbytes + b.nbytes for a, b in self.searches
        )
        self.columns = SparseColumnAccumulator(
            {
                "frames": (np.int64, ()),
                "pairs": (np.int64, (2,)),
                "distance": (np.float64, ()),
                "images": (np.int32, (2, 3)),
            },
            budget_bytes=self.budget_bytes // 2,
            fixed_bytes=fixed,
        )
        self.columns.check_budget()
        self.chunks, self.periodic = 0, None

    def consume(self, chunk):
        xyz, boxes, frames = (
            chunk["coordinates"],
            chunk["box"],
            chunk["structure_indices"],
        )
        caller = self.metadata["method"]
        if (
            xyz is None
            or xyz.shape != (len(frames), len(self.universe), 3)
            or not np.isfinite(xyz).all()
        ):
            raise StructuralInconsistencyError(
                reason="Finite coordinates are required for every examined metal coordination site.",
                caller=caller,
            )
        if boxes is not None:
            validate_periodic_boxes(boxes, len(frames), caller=caller)
        has_box = boxes is not None
        if self.periodic is not None and self.periodic != has_box:
            raise StructuralInconsistencyError(
                reason="Periodic box availability changed between blocks.",
                caller=caller,
            )
        self.periodic, self.chunks = has_box, self.chunks + 1
        for local, frame in enumerate(frames):
            coordinates, box = xyz[local], None if boxes is None else boxes[local]
            for first, second in self.searches:
                pairs, _, _ = bounded_group_minimum_contacts(
                    coordinates[np.searchsorted(self.universe, first)],
                    first,
                    coordinates[np.searchsorted(self.universe, second)],
                    second,
                    self.distance,
                    box,
                    self.budget_bytes // 8,
                )
                pairs = pairs[pairs[:, 0] != pairs[:, 1]]
                if not len(pairs):
                    continue
                # Directed roles anchor the observed MIC image on the metal.
                observed, images = observed_chains(
                    coordinates,
                    np.searchsorted(self.universe, pairs),
                    box,
                    caller=caller,
                )
                distances = np.linalg.norm(observed[:, 1] - observed[:, 0], axis=1)
                keep = distances <= self.distance
                if keep.any():
                    self.columns.append(
                        dict(
                            frames=np.full(keep.sum(), frame, dtype=np.int64),
                            pairs=pairs[keep],
                            distance=distances[keep],
                            images=images[keep],
                        )
                    )

    def finalize(self):
        self.metadata["execution"]["execution_chunks"] = self.chunks
        if not self.columns.n_rows:
            return Interactions.from_records([], **self.metadata)
        pairs, occurrence_relations = np.unique(
            self.columns.concatenate("pairs"), axis=0, return_inverse=True
        )
        self.columns.check_budget(extra_bytes=len(pairs) * 192)
        frames = self.columns.concatenate("frames")
        order = np.lexsort((occurrence_relations, frames))
        result = Interactions(
            relation_types=["metal_coordination_candidate"] * len(pairs),
            relation_participant_offsets=np.arange(len(pairs) + 1, dtype=np.int64) * 2,
            participant_roles=[role for _ in pairs for role in ("metal", "ligand")],
            participant_atom_offsets=np.arange(pairs.size + 1, dtype=np.int64),
            participant_atoms=pairs.ravel(),
            occurrence_structures=frames[order],
            occurrence_relations=occurrence_relations[order],
            occurrence_evidence=np.zeros(len(order), dtype=np.int32),
            evidence_labels=["smarts_metal_ligand_proximity"],
            measurements={"distance": self.columns.concatenate("distance")[order]},
            occurrence_image_offsets=np.arange(len(order) + 1, dtype=np.int64) * 2
            if self.periodic
            else None,
            image_vectors=self.columns.concatenate("images")[order].reshape(-1, 3)
            if self.periodic
            else None,
            **self.metadata,
        )
        self.columns.clear()
        return result

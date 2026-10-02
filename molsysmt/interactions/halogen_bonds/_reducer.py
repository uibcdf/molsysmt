"""Reduce projected coordinate blocks to directional halogen observations."""

import numpy as np

from molsysmt._private.execution import Reducer
from molsysmt._private.execution.sparse_accumulator import SparseColumnAccumulator
from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt.interactions.result import Interactions
from molsysmt.pbc._triplet_images import observed_chains
from molsysmt.pbc._whole_participants import validate_periodic_boxes
from molsysmt.structure._group_minimum_contacts import bounded_group_minimum_contacts
from molsysmt.structure._triplet_geometry import triplet_geometry


class _HalogenReducer(Reducer):
    def __init__(
        self,
        *,
        donors,
        acceptors,
        universe,
        searches,
        first,
        second,
        distance,
        donor_angle,
        acceptor_angle,
        metadata,
        budget_bytes,
    ):
        self.donors, self.acceptors, self.universe = donors, acceptors, universe
        self.searches, self.first, self.second = searches, first, second
        self.distance, self.donor_angle, self.acceptor_angle = (
            distance,
            donor_angle,
            acceptor_angle,
        )
        self.metadata, self.budget_bytes = metadata, budget_bytes
        self.donor_positions = np.searchsorted(universe, donors)
        self.acceptor_positions = np.searchsorted(universe, acceptors)

    def initialize(self, metadata):
        schema = {
            "frames": (np.int64, ()),
            "chains": (np.int64, (4,)),
            "images": (np.int32, (4, 3)),
        }
        schema.update(
            {name: (np.float64, ()) for name in self.metadata["measure_units"]}
        )
        fixed = 8 * (2 * self.metadata["n_atoms"] + 4 * self.metadata["n_structures"])
        fixed += sum(
            value.nbytes
            for value in (
                self.donors,
                self.acceptors,
                self.universe,
                self.donor_positions,
                self.acceptor_positions,
                self.first,
            )
        )
        self.columns = SparseColumnAccumulator(
            schema, budget_bytes=self.budget_bytes // 2, fixed_bytes=fixed
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
                reason="Finite coordinates are required for every examined halogen-bond site.",
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
            for donor_rows, acceptor_rows in self.searches:
                pairs, _, _ = bounded_group_minimum_contacts(
                    coordinates[self.donor_positions[donor_rows, 1]],
                    donor_rows,
                    coordinates[self.acceptor_positions[acceptor_rows, 0]],
                    acceptor_rows,
                    self.distance,
                    box,
                    self.budget_bytes // 8,
                )
                if not len(pairs):
                    continue
                d, a = pairs.T
                chains = np.column_stack((self.donors[d], self.acceptors[a]))
                if self.second is not None:
                    chains = chains[
                        np.isin(chains, self.first).any(axis=1)
                        & np.isin(chains, self.second).any(axis=1)
                    ]
                if not len(chains):
                    continue
                observed, images = observed_chains(
                    coordinates,
                    np.searchsorted(self.universe, chains),
                    box,
                    caller=caller,
                )
                dx, _, distance, _, donor_angle = triplet_geometry(observed[:, :3])
                _, _, ar, _, acceptor_angle = triplet_geometry(observed[:, 1:])
                keep = (
                    (distance <= self.distance)
                    & np.isfinite(donor_angle)
                    & np.isfinite(acceptor_angle)
                )
                keep &= (donor_angle >= self.donor_angle[0]) & (
                    donor_angle <= self.donor_angle[1]
                )
                keep &= (acceptor_angle >= self.acceptor_angle[0]) & (
                    acceptor_angle <= self.acceptor_angle[1]
                )
                if keep.any():
                    self.columns.append(
                        dict(
                            frames=np.full(keep.sum(), frame, dtype=np.int64),
                            chains=chains[keep],
                            images=images[keep],
                            distance=distance[keep],
                            donor_angle=donor_angle[keep],
                            acceptor_angle=acceptor_angle[keep],
                            donor_halogen_distance=dx[keep],
                            acceptor_reference_distance=ar[keep],
                        )
                    )

    def finalize(self):
        self.metadata["execution"]["execution_chunks"] = self.chunks
        if not self.columns.n_rows:
            return Interactions.from_records([], **self.metadata)
        relations, occurrence_relations = np.unique(
            self.columns.concatenate("chains"), axis=0, return_inverse=True
        )
        self.columns.check_budget(extra_bytes=len(relations) * 320)
        frames = self.columns.concatenate("frames")
        order = np.lexsort((occurrence_relations, frames))
        result = Interactions(
            relation_types=["halogen_bond"] * len(relations),
            relation_participant_offsets=np.arange(len(relations) + 1, dtype=np.int64)
            * 4,
            participant_roles=[
                role
                for _ in relations
                for role in ("donor", "halogen", "acceptor", "acceptor_reference")
            ],
            participant_atom_offsets=np.arange(relations.size + 1, dtype=np.int64),
            participant_atoms=relations.ravel(),
            occurrence_structures=frames[order],
            occurrence_relations=occurrence_relations[order],
            occurrence_evidence=np.zeros(len(order), dtype=np.int32),
            evidence_labels=["distance_two_angles_halogen_geometry"],
            measurements={
                name: self.columns.concatenate(name)[order]
                for name in self.metadata["measure_units"]
            },
            occurrence_image_offsets=np.arange(len(order) + 1, dtype=np.int64) * 4
            if self.periodic
            else None,
            image_vectors=self.columns.concatenate("images")[order].reshape(-1, 3)
            if self.periodic
            else None,
            **self.metadata,
        )
        self.columns.clear()
        return result

"""Reduce bounded coordinate blocks to sparse attributed hydrogen-bond triples."""

import numpy as np

from molsysmt._private.execution import Reducer
from molsysmt._private.execution.sparse_accumulator import SparseColumnAccumulator
from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt.interactions.result import Interactions
from molsysmt.pbc._triplet_images import observed_triplets
from molsysmt.pbc._whole_participants import validate_periodic_boxes
from molsysmt.structure._group_minimum_contacts import bounded_group_minimum_contacts
from molsysmt.structure._triplet_geometry import triplet_geometry


class _HBondReducer(Reducer):
    def __init__(self, *, donors, acceptors, universe, searches, first, second,
                 method, distance, angle, metadata, budget_bytes):
        self.donors, self.acceptors, self.universe = donors, acceptors, universe
        self.searches, self.first, self.second = searches, first, second
        self.method, self.distance, self.angle = method, distance, angle
        self.metadata, self.budget_bytes = metadata, budget_bytes
        self.donor_positions = np.searchsorted(universe, donors)
        self.acceptor_positions = np.searchsorted(universe, acceptors)

    def initialize(self, metadata):
        schema = {"frames": (np.int64, ()), "triples": (np.int64, (3,)), "images": (np.int32, (3, 3))}
        schema.update({name: (np.float64, ()) for name in self.metadata["measure_units"]})
        fixed = 8 * (2 * self.metadata["n_atoms"] + 4 * self.metadata["n_structures"])
        fixed += sum(value.nbytes for value in (self.donors, self.acceptors, self.universe,
                                               self.donor_positions, self.acceptor_positions, self.first))
        self.columns = SparseColumnAccumulator(schema, budget_bytes=self.budget_bytes // 2, fixed_bytes=fixed)
        self.columns.check_budget()
        self.chunks, self.periodic = 0, None

    def consume(self, chunk):
        xyz, boxes, frames = chunk["coordinates"], chunk["box"], chunk["structure_indices"]
        caller = self.metadata["method"]
        if xyz is None or xyz.shape != (len(frames), len(self.universe), 3) or not np.isfinite(xyz).all():
            raise StructuralInconsistencyError(reason="Finite coordinates are required for every examined hydrogen-bond site.", caller=caller)
        if boxes is not None:
            validate_periodic_boxes(boxes, len(frames), caller=caller)
        has_box = boxes is not None
        if self.periodic is not None and self.periodic != has_box:
            raise StructuralInconsistencyError(reason="Periodic box availability changed between blocks.", caller=caller)
        self.periodic, self.chunks = has_box, self.chunks + 1
        hydrogen_search = self.method == "baker_hubbard"
        for local, frame in enumerate(frames):
            coordinates, box = xyz[local], None if boxes is None else boxes[local]
            for donor_rows, acceptor_rows in self.searches:
                pairs, _, _ = bounded_group_minimum_contacts(
                    coordinates[self.donor_positions[donor_rows, int(hydrogen_search)]], donor_rows,
                    coordinates[self.acceptor_positions[acceptor_rows]], acceptor_rows,
                    self.distance, box, self.budget_bytes // 8)
                if not len(pairs):
                    continue
                d, a = pairs.T
                triples = np.column_stack((self.donors[d], self.acceptors[a]))
                keep = (triples[:, 0] != triples[:, 2]) & (triples[:, 1] != triples[:, 2])
                if self.second is not None:
                    keep &= np.isin(triples, self.first).any(axis=1) & np.isin(triples, self.second).any(axis=1)
                triples = triples[keep]
                if not len(triples):
                    continue
                observed, images, mic_da = observed_triplets(
                    coordinates, np.searchsorted(self.universe, triples), box,
                    anchor=0 if self.method == "wernet_nilsson" else 1,
                    require_whole_first_pair=self.method == "cpptraj", caller=caller)
                dh, da, ha, hda, dha = triplet_geometry(observed)
                if box is not None and self.method not in {"baker_hubbard", "wernet_nilsson"}:
                    if not np.allclose(da, mic_da, rtol=1e-8, atol=1e-8):
                        raise StructuralInconsistencyError(reason="Independent D-A and H-centered MIC geometry cannot be represented by one observed triplet image.", caller=caller)
                if self.method == "cpptraj":
                    keep = (da <= self.distance) & (dha >= self.angle)
                elif self.method == "prolif":
                    keep = (da <= self.distance) & (dha >= self.angle)
                elif self.method == "baker_hubbard":
                    keep = (ha < self.distance) & (dha > self.angle)
                elif self.method == "mdanalysis_geometry":
                    keep = (da > .1) & (da <= self.distance) & (dha > self.angle)
                else:
                    keep = da < self.distance - .000044 * np.rad2deg(hda) ** 2
                keep &= np.isfinite(dha) & np.isfinite(hda)
                if keep.any():
                    self.columns.append(dict(frames=np.full(keep.sum(), frame, dtype=np.int64),
                                             triples=triples[keep], images=images[keep],
                                             donor_hydrogen_distance=dh[keep], donor_acceptor_distance=da[keep],
                                             hydrogen_acceptor_distance=ha[keep], dha_angle=dha[keep], hda_angle=hda[keep]))

    def finalize(self):
        self.metadata["parameters"]["execution_chunks"] = self.chunks
        if not self.columns.n_rows:
            return Interactions.from_records([], **self.metadata)
        relations, occurrence_relations = np.unique(self.columns.concatenate("triples"), axis=0, return_inverse=True)
        self.columns.check_budget(extra_bytes=len(relations) * 256)
        frames = self.columns.concatenate("frames")
        order = np.lexsort((occurrence_relations, frames))
        result = Interactions(
            relation_types=["hbond"] * len(relations),
            relation_participant_offsets=np.arange(len(relations) + 1, dtype=np.int64) * 3,
            participant_roles=[role for _ in relations for role in ("donor", "hydrogen", "acceptor")],
            participant_atom_offsets=np.arange(relations.size + 1, dtype=np.int64),
            participant_atoms=relations.ravel(), occurrence_structures=frames[order],
            occurrence_relations=occurrence_relations[order], occurrence_evidence=np.zeros(len(order), dtype=np.int32),
            evidence_labels=[self.method + "_hbond_geometry"],
            measurements={name: self.columns.concatenate(name)[order] for name in self.metadata["measure_units"]},
            occurrence_image_offsets=np.arange(len(order) + 1, dtype=np.int64) * 3 if self.periodic else None,
            image_vectors=self.columns.concatenate("images")[order].reshape(-1, 3) if self.periodic else None,
            **self.metadata)
        self.columns.clear()
        return result

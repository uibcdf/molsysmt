"""Join sparse simultaneous leg observations without a dense pair tensor."""

import numpy as np

from molsysmt._private.execution.sparse_accumulator import SparseColumnAccumulator
from molsysmt.interactions.result import Interactions
from molsysmt.pbc._shared_images import join_shared_images


def join_water_legs(legs, *, all_water_oxygen, first, second, metadata, budget_bytes):
    schema = {"frames": (np.int64, ()), "paths": (np.int64, (6,)),
              "images": (np.int32, (6, 3))}
    schema.update({name: (np.float64, ()) for name in metadata["measure_units"]})
    fixed = legs.numeric_nbytes + 128 * legs.n_interactions
    fixed += 8 * (2 * metadata["n_atoms"] + 4 * metadata["n_structures"])
    columns = SparseColumnAccumulator(schema, budget_bytes=budget_bytes // 2, fixed_bytes=fixed)
    columns.check_budget()
    triples = legs.participant_atoms.reshape(-1, 3)[legs.occurrence_relations]
    water_donor = np.isin(triples[:, 0], all_water_oxygen)
    water_acceptor = np.isin(triples[:, 2], all_water_oxygen)
    usable = water_donor ^ water_acceptor
    oxygen = np.where(water_donor, triples[:, 0], triples[:, 2])
    endpoint = np.where(water_donor, triples[:, 2], triples[:, 0])
    periodic = legs.image_vectors is not None
    images = None if not periodic else legs.image_vectors.reshape(-1, 3, 3)
    mode, caller = metadata["evaluation_mode"], metadata["method"]
    # Block the fan-out of one water: do not allocate n_legs squared pairs.
    block_size = max(1, min(1024, budget_bytes // 16384))
    for frame in metadata["evaluated_structure_indices"]:
        start, stop = np.searchsorted(legs.occurrence_structures, [frame, frame + 1])
        rows = np.arange(start, stop, dtype=np.int64)
        rows = rows[usable[start:stop]]
        rows = rows[np.lexsort((triples[rows, 2], triples[rows, 1], triples[rows, 0], endpoint[rows], oxygen[rows]))]
        _, offsets = np.unique(oxygen[rows], return_index=True)
        for group_start, group_stop in zip(offsets, np.r_[offsets[1:], len(rows)]):
            group = rows[group_start:group_stop]
            for position, left in enumerate(group[:-1]):
                for offset in range(position + 1, len(group), block_size):
                    right = group[offset:offset + block_size]
                    paths = np.column_stack((np.broadcast_to(triples[left], (len(right), 3)), triples[right]))
                    keep = endpoint[right] != endpoint[left]
                    if mode == "internal":
                        keep &= np.isin(paths, first).all(axis=1)
                    else:
                        keep &= np.isin(paths, first).any(axis=1)
                        if second is not None:
                            keep &= np.isin(paths, second).any(axis=1)
                            keep &= np.isin(paths, np.union1d(first, second)).all(axis=1)
                    paths, right = paths[keep], right[keep]
                    if not len(right):
                        continue
                    observed_images = np.zeros((len(right), 6, 3), dtype=np.int32)
                    if periodic:
                        observed_images = join_shared_images(
                            images[left], images[right], 0 if water_donor[left] else 2,
                            np.where(water_donor[right], 0, 2), atoms=paths, caller=caller)
                    data = dict(frames=np.full(len(right), frame, dtype=np.int64),
                                paths=paths, images=observed_images)
                    for name, values in legs.measurements.items():
                        data[f"leg_1_{name}"] = np.full(len(right), values[left], dtype=np.float64)
                        data[f"leg_2_{name}"] = values[right]
                    columns.append(data)
    if not columns.n_rows:
        return Interactions.from_records([], **metadata)
    relations, occurrence_relations = np.unique(columns.concatenate("paths"), axis=0, return_inverse=True)
    columns.check_budget(extra_bytes=len(relations) * 448)
    frames = columns.concatenate("frames")
    order = np.lexsort((occurrence_relations, frames))
    roles = tuple(f"leg_{branch}_{role}" for branch in (1, 2) for role in ("donor", "hydrogen", "acceptor"))
    result = Interactions(
        relation_types=["water_bridge"] * len(relations),
        relation_participant_offsets=np.arange(len(relations) + 1, dtype=np.int64) * 6,
        participant_roles=roles * len(relations),
        participant_atom_offsets=np.arange(relations.size + 1, dtype=np.int64),
        participant_atoms=relations.ravel(), occurrence_structures=frames[order],
        occurrence_relations=occurrence_relations[order], occurrence_evidence=np.zeros(len(order), dtype=np.int32),
        evidence_labels=["two_simultaneous_hbonds_shared_indexed_water"],
        measurements={name: columns.concatenate(name)[order] for name in metadata["measure_units"]},
        occurrence_image_offsets=np.arange(len(order) + 1, dtype=np.int64) * 6 if periodic else None,
        image_vectors=columns.concatenate("images")[order].reshape(-1, 3) if periodic else None,
        **metadata,
    )
    columns.clear()
    return result

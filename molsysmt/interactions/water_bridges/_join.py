"""Join sparse simultaneous leg observations without a dense pair tensor."""

import numpy as np

from molsysmt._private.execution.sparse_accumulator import SparseColumnAccumulator
from molsysmt.interactions.result import Interactions
from molsysmt.pbc._shared_images import join_shared_images


def _path_batches(
    rows, triples, water_donor, water_acceptor, oxygen, endpoint, block_size, order
):
    """Yield observed-leg rows in canonical endpoint traversal order."""
    terminal = rows[(water_donor ^ water_acceptor)[rows]]
    terminal = terminal[
        np.lexsort(
            (
                triples[terminal, 2],
                triples[terminal, 1],
                triples[terminal, 0],
                endpoint[terminal],
                oxygen[terminal],
            )
        )
    ]
    waters, offsets = np.unique(oxygen[terminal], return_index=True)
    groups = {
        int(water): terminal[start:stop]
        for water, start, stop in zip(
            waters, offsets, np.r_[offsets[1:], len(terminal)]
        )
    }
    if order == 1:
        for group in groups.values():
            for position, left in enumerate(group[:-1]):
                for offset in range(position + 1, len(group), block_size):
                    right = group[offset : offset + block_size]
                    right = right[endpoint[right] != endpoint[left]]
                    if len(right):
                        yield np.column_stack(
                            (np.full(len(right), left, dtype=np.int64), right)
                        )
        return
    # Only existing water-water edges connect terminal groups. No all-water pairs
    # or all-path Cartesian product is materialized.
    central = rows[(water_donor & water_acceptor)[rows]]
    for middle in central:
        water_left, water_right = triples[middle, [0, 2]]
        if water_left == water_right:
            continue
        left_group, right_group = (
            groups.get(int(water_left), ()),
            groups.get(int(water_right), ()),
        )
        for left in left_group:
            for offset in range(0, len(right_group), block_size):
                right = right_group[offset : offset + block_size]
                right = right[endpoint[right] != endpoint[left]]
                if not len(right):
                    continue
                batch = np.column_stack(
                    (
                        np.full(len(right), left, dtype=np.int64),
                        np.full(len(right), middle, dtype=np.int64),
                        right,
                    )
                )
                reverse = endpoint[left] > endpoint[right]
                batch[reverse] = batch[reverse, ::-1]
                yield batch


def join_water_legs(legs, *, all_water_oxygen, first, second, metadata, budget_bytes):
    order = metadata["parameters"]["mediator_order"]
    n_legs, width = order + 1, 3 * (order + 1)
    schema = {
        "frames": (np.int64, ()),
        "paths": (np.int64, (width,)),
        "images": (np.int32, (width, 3)),
    }
    schema.update({name: (np.float64, ()) for name in metadata["measure_units"]})
    fixed = legs.numeric_nbytes + 128 * legs.n_interactions
    fixed += 8 * (2 * metadata["n_atoms"] + 4 * metadata["n_structures"])
    columns = SparseColumnAccumulator(
        schema, budget_bytes=budget_bytes // 2, fixed_bytes=fixed
    )
    columns.check_budget()
    triples = legs.participant_atoms.reshape(-1, 3)[legs.occurrence_relations]
    water_donor = np.isin(triples[:, 0], all_water_oxygen)
    water_acceptor = np.isin(triples[:, 2], all_water_oxygen)
    oxygen = np.where(water_donor, triples[:, 0], triples[:, 2])
    endpoint = np.where(water_donor, triples[:, 2], triples[:, 0])
    periodic = legs.image_vectors is not None
    images = None if not periodic else legs.image_vectors.reshape(-1, 3, 3)
    mode, caller = metadata["evaluation_mode"], metadata["method"]
    union = first if second is None else np.union1d(first, second)
    block_size = max(1, min(1024, budget_bytes // 16384))
    for frame in metadata["evaluated_structure_indices"]:
        start, stop = np.searchsorted(legs.occurrence_structures, [frame, frame + 1])
        rows = np.arange(start, stop, dtype=np.int64)
        for batch in _path_batches(
            rows,
            triples,
            water_donor,
            water_acceptor,
            oxygen,
            endpoint,
            block_size,
            order,
        ):
            paths = triples[batch].reshape(-1, width)
            if mode == "internal":
                keep = np.isin(paths, first).all(axis=1)
            else:
                keep = np.isin(paths, first).any(axis=1)
                if second is not None:
                    keep &= np.isin(paths, second).any(axis=1)
                    keep &= np.isin(paths, union).all(axis=1)
            paths, batch = paths[keep], batch[keep]
            if not len(batch):
                continue
            observed_images = np.zeros((len(batch), width, 3), dtype=np.int32)
            if periodic:
                observed_images = images[batch[:, 0]]
                for branch in range(1, n_legs):
                    # Each adjacent pair shares exactly its mediator oxygen.
                    previous = triples[batch[:, branch - 1]]
                    current = triples[batch[:, branch]]
                    same_donor = previous[:, 0] == current[:, 0]
                    donor_acceptor = previous[:, 0] == current[:, 2]
                    left_anchor = np.where(same_donor | donor_acceptor, 0, 2)
                    shared_atom = previous[np.arange(len(batch)), left_anchor]
                    right_anchor = np.where(current[:, 0] == shared_atom, 0, 2)
                    observed_images = join_shared_images(
                        observed_images,
                        images[batch[:, branch]],
                        3 * (branch - 1) + left_anchor,
                        right_anchor,
                        atoms=paths[:, : 3 * (branch + 1)],
                        caller=caller,
                    )
            data = dict(
                frames=np.full(len(batch), frame, dtype=np.int64),
                paths=paths,
                images=observed_images,
            )
            for name, values in legs.measurements.items():
                for branch in range(n_legs):
                    data[f"leg_{branch + 1}_{name}"] = values[batch[:, branch]]
            columns.append(data)
    if not columns.n_rows:
        return Interactions.from_records([], **metadata)
    relations, occurrence_relations = np.unique(
        columns.concatenate("paths"), axis=0, return_inverse=True
    )
    columns.check_budget(extra_bytes=len(relations) * (width * 64 + 64))
    frames = columns.concatenate("frames")
    sort_order = np.lexsort((occurrence_relations, frames))
    roles = tuple(
        f"leg_{branch}_{role}"
        for branch in range(1, n_legs + 1)
        for role in ("donor", "hydrogen", "acceptor")
    )
    result = Interactions(
        relation_types=["water_bridge"] * len(relations),
        relation_participant_offsets=np.arange(len(relations) + 1, dtype=np.int64)
        * width,
        participant_roles=roles * len(relations),
        participant_atom_offsets=np.arange(relations.size + 1, dtype=np.int64),
        participant_atoms=relations.ravel(),
        occurrence_structures=frames[sort_order],
        occurrence_relations=occurrence_relations[sort_order],
        occurrence_evidence=np.zeros(len(sort_order), dtype=np.int32),
        evidence_labels=[
            "two_simultaneous_hbonds_shared_indexed_water"
            if order == 1
            else "three_simultaneous_hbonds_two_distinct_indexed_waters"
        ],
        measurements={
            name: columns.concatenate(name)[sort_order]
            for name in metadata["measure_units"]
        },
        occurrence_image_offsets=np.arange(len(sort_order) + 1, dtype=np.int64) * width
        if periodic
        else None,
        image_vectors=columns.concatenate("images")[sort_order].reshape(-1, 3)
        if periodic
        else None,
        **metadata,
    )
    columns.clear()
    return result

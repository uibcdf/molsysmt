"""Bounded inspection projections over packed, invalidated and patched analyses."""

from copy import deepcopy

import numpy as np

from .result import Interactions


def _rows(source, offset, limit):
    """Select source columns without touching complete edited occurrence arrays."""
    if not hasattr(source, "_root") and not hasattr(source, "_segments"):
        positions = source._positions[offset : offset + limit]
        return [(source, positions, None, None, None, None)]
    end = min(source.n_interactions, offset + limit)
    if offset >= end:
        return []
    from ._hdf5_writer import _frame_offsets

    offsets = getattr(source, "_frame_offsets", None)
    if offsets is None:
        offsets = getattr(source, "_page_frame_offsets", None)
    if offsets is None:
        offsets = _frame_offsets(source)
        source._page_frame_offsets = offsets
    first = np.searchsorted(offsets, offset, side="right") - 1
    last = np.searchsorted(offsets, end - 1, side="right") - 1
    columns = []
    for frame in range(first, last + 1):
        begin, stop = (
            max(offset, int(offsets[frame])),
            min(end, int(offsets[frame + 1])),
        )
        if begin == stop:
            continue
        if hasattr(source, "_segments"):
            base, _, relations, evidence = source._segments[source._frame_owners[frame]]
        else:
            base, relations, evidence = source._root, None, None
        start = np.searchsorted(base.occurrence_structures, frame, side="left")
        positions = np.arange(
            start + begin - offsets[frame],
            start + stop - offsets[frame],
            dtype=np.int64,
        )
        columns.append(
            (
                base,
                positions,
                np.full(len(positions), frame, dtype=np.int64),
                np.arange(begin, stop, dtype=np.int64),
                relations,
                evidence,
            )
        )
    return columns


def _catalog(source, relations):
    kinds, roles, atoms = [], [], []
    relation_offsets, atom_offsets = [0], [0]
    for relation in relations:
        kinds.append(source.relation_types[relation])
        first, last = source.relation_participant_offsets[relation : relation + 2]
        for participant in range(first, last):
            roles.append(source.participant_roles[participant])
            begin, end = source.participant_atom_offsets[participant : participant + 2]
            atoms.append(source.participant_atoms[begin:end])
            atom_offsets.append(atom_offsets[-1] + end - begin)
        relation_offsets.append(len(roles))
    return dict(
        relation_catalog_indices=relations,
        relation_types=tuple(kinds),
        relation_participant_offsets=np.asarray(relation_offsets, dtype=np.int64),
        participant_roles=tuple(roles),
        participant_atom_offsets=np.asarray(atom_offsets, dtype=np.int64),
        participant_atoms=np.concatenate(atoms)
        if atoms
        else np.empty(0, dtype=np.int64),
    )


def _shared(values):
    view = values.view()
    view.setflags(write=False)
    return view


def occurrence_page(source, offset, limit, max_participant_atoms):
    columns = _rows(source, offset, limit)
    relation_columns = []
    for base, positions, _, _, mapping, _ in columns:
        relations = base.occurrence_relations[positions]
        relation_columns.append(relations if mapping is None else mapping[relations])
    relations, counts = np.unique(
        np.concatenate(relation_columns)
        if relation_columns
        else np.empty(0, dtype=np.int64),
        return_counts=True,
    )
    constituent_count = 0
    for relation, count in zip(relations, counts):
        first, last = source.relation_participant_offsets[relation : relation + 2]
        constituent_count += int(count) * int(
            source.participant_atom_offsets[last]
            - source.participant_atom_offsets[first]
        )
    if constituent_count > max_participant_atoms:
        raise ValueError(
            f"Page requires {constituent_count} participant atoms, exceeding max_participant_atoms={max_participant_atoms}; reduce limit or increase the explicit budget."
        )
    if hasattr(source, "_segments"):
        view = source._projection(columns, source._coverage, False)
    elif hasattr(source, "_root"):
        from ._frame_validity import _metadata

        positions = (
            np.concatenate([item[1] for item in columns])
            if columns
            else np.empty(0, dtype=np.int64)
        )
        view = source._root._view(positions, source._coverage)
        view.__dict__.update(_metadata(source))
        view._row_removal = source._row_removal
    else:
        positions = columns[0][1]
        view = source._view(positions, source._coverage)
    page = Interactions._occurrence_dict(view, view._positions, copy_coverage=False)
    page.update(_catalog(source, relations))
    copied = len(page["occurrence_indices"])
    page.update(
        schema="molsysmt.interactions.page@1",
        total_count=source.n_interactions,
        offset=offset,
        limit=limit,
        next_offset=offset + copied
        if copied and offset + copied < source.n_interactions
        else None,
        method=source.method,
        parameters=deepcopy(source.parameters),
        atom_source_indices=_shared(source.atom_source_indices),
        structure_source_indices=_shared(source.structure_source_indices),
        evaluated_structure_indices=_shared(source._coverage),
    )
    return page

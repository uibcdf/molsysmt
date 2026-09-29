#!/usr/bin/env python3
"""Probe typed, ragged, complete query projections from flat HDF5 blocks.

This reader uses the experimental flat-block file schema. It selects the
requested occurrences and returns one typed columnar result, without creating
one Python record per occurrence. The complete-record decoder is only an
independent-oracle adapter used after query timing and memory measurement.
"""

from __future__ import annotations

import operator
from collections import Counter

import numpy as np
from benchmark_interactions_contract import UNITS, _signature
from benchmark_interactions_flat_blocks import FlatReader


def _ragged_take(offsets, indices):
    """Return rebased offsets and flattened source positions for selected rows."""
    starts = np.asarray(offsets[indices], dtype=np.int64)
    counts = np.asarray(offsets[indices + 1], dtype=np.int64) - starts
    output_offsets = np.empty(len(indices) + 1, dtype=np.int64)
    output_offsets[0] = 0
    np.cumsum(counts, out=output_offsets[1:])
    positions = (np.repeat(starts, counts)
                 + np.arange(output_offsets[-1], dtype=np.int64)
                 - np.repeat(output_offsets[:-1], counts))
    return output_offsets, positions


def _empty_columns():
    return {
        "structure_indices": np.empty(0, dtype=np.int64),
        "type_codes": np.empty(0, dtype=np.uint32),
        "evidence_codes": np.empty(0, dtype=np.int32),
        "measure_distance": np.empty(0, dtype=np.float64),
        "measure_angle": np.empty(0, dtype=np.float64),
        "participant_offsets": np.array([0], dtype=np.int64),
        "role_codes": np.empty(0, dtype=np.uint32),
        "atom_offsets": np.array([0], dtype=np.int64),
        "atoms": np.empty(0, dtype=np.int64),
        "image_vectors": np.empty((0, 3), dtype=np.int32),
    }


def _join_batches(batches):
    if not batches:
        return _empty_columns()
    output = {}
    for name in ("structure_indices", "type_codes", "evidence_codes",
                 "measure_distance", "measure_angle", "role_codes", "atoms",
                 "image_vectors"):
        output[name] = np.concatenate([batch[name] for batch in batches])
    for name in ("participant_offsets", "atom_offsets"):
        offsets = []
        total = 0
        for batch in batches:
            offsets.append(batch[name][:-1] + total)
            total += int(batch[name][-1])
        output[name] = np.concatenate(
            (*offsets, np.asarray([total], dtype=np.int64))
        )
    return output


def _take_rows(columns, rows):
    """Reorder complete ragged observations without expanding Python records."""
    rows = np.asarray(rows, dtype=np.int64)
    part_offsets, parts = _ragged_take(columns["participant_offsets"], rows)
    atom_offsets, atoms = _ragged_take(columns["atom_offsets"], parts)
    return {
        "structure_indices": columns["structure_indices"][rows],
        "type_codes": columns["type_codes"][rows],
        "evidence_codes": columns["evidence_codes"][rows],
        "measure_distance": columns["measure_distance"][rows],
        "measure_angle": columns["measure_angle"][rows],
        "participant_offsets": part_offsets,
        "role_codes": columns["role_codes"][parts],
        "atom_offsets": atom_offsets,
        "atoms": columns["atoms"][atoms],
        "image_vectors": columns["image_vectors"][parts],
    }


def _hit_counts(columns, selected_atoms):
    """Count distinct selected participant atoms in each typed observation."""
    n_events = len(columns["structure_indices"])
    if not n_events or not len(selected_atoms):
        return np.zeros(n_events, dtype=np.int64)
    parts_per_event = np.diff(columns["participant_offsets"])
    atoms_per_part = np.diff(columns["atom_offsets"])
    part_events = np.repeat(np.arange(n_events), parts_per_event)
    atom_events = np.repeat(part_events, atoms_per_part)
    selected = np.isin(columns["atoms"], selected_atoms)
    if not np.any(selected):
        return np.zeros(n_events, dtype=np.int64)
    pairs = np.column_stack((atom_events[selected], columns["atoms"][selected]))
    distinct = np.unique(pairs, axis=0)
    return np.bincount(distinct[:, 0], minlength=n_events)


class PackedReader(FlatReader):
    """Return complete typed columns for selected frames or atom postings."""

    def _selected_block(self, block, positions):
        common, descriptors, scope = self._block(block)
        positions = np.asarray(positions, dtype=np.int64)
        if scope == "global":
            relations = descriptors["occurrence_relations"][positions]
            types = descriptors["relation_type_codes"][relations]
            participant_bounds = descriptors["relation_participant_offsets"]
        else:
            relations = positions
            types = descriptors["occurrence_type_codes"][positions]
            participant_bounds = descriptors["occurrence_participant_offsets"]
        part_offsets, part_positions = _ragged_take(
            participant_bounds, relations
        )
        atom_offsets, atom_positions = _ragged_take(
            descriptors["participant_atom_offsets"], part_positions
        )
        image_offsets, image_positions = _ragged_take(
            common["occurrence_image_offsets"], positions
        )
        if not np.array_equal(part_offsets, image_offsets):
            raise AssertionError("image and participant offsets differ")
        return {
            "structure_indices": common["occurrence_structures"][positions],
            "type_codes": types,
            "evidence_codes": common["occurrence_evidence"][positions],
            "measure_distance": common["measure_distance"][positions],
            "measure_angle": common["measure_angle"][positions],
            "participant_offsets": part_offsets,
            "role_codes": descriptors["participant_role_codes"][part_positions],
            "atom_offsets": atom_offsets,
            "atoms": descriptors["participant_atoms"][atom_positions],
            "image_vectors": common["image_vectors"][image_positions],
        }

    def query_frame_columns(self, frame):
        if frame not in self.covered:
            return [], _empty_columns()
        block = frame // self.metadata["block_size"]
        local = frame - block * self.metadata["block_size"]
        position = self.column_index["frame_offsets"]
        start = int(self.offsets[position, block])
        first, last = self.file["data/frame_offsets"][
            start + local:start + local + 2
        ]
        if first == last:
            return [frame], _empty_columns()
        return [frame], self._selected_block(block, np.arange(first, last))

    def query_atom_columns(self, atom):
        offsets = self.file["index/atom_offsets"][atom:atom + 2]
        ids = self.file["index/atom_occurrences"][int(offsets[0]):int(offsets[1])]
        blocks = np.searchsorted(self.block_event_offsets, ids, side="right") - 1
        batches = []
        for block in np.unique(blocks):
            positions = ids[blocks == block] - self.block_event_offsets[block]
            batches.append(self._selected_block(int(block), positions))
        return self.coverage, _join_batches(batches)

    def _indices(self, values, limit, label):
        indices = list(dict.fromkeys(operator.index(value) for value in values))
        if any(index < 0 or index >= limit for index in indices):
            raise IndexError(f"{label} contains an out-of-range index")
        return indices

    def _coverage(self, structure_indices):
        if structure_indices is None:
            return self.coverage, None
        requested = self._indices(
            structure_indices, self.metadata["n_structures"],
            "structure_indices",
        )
        coverage = [frame for frame in requested if frame in self.covered]
        return coverage, np.asarray(coverage, dtype=np.int64)

    def _postings(self, atom_indices):
        atoms = self._indices(
            atom_indices, self.metadata["n_atoms"], "atom_indices"
        )
        offsets = self.file["index/atom_offsets"]
        postings = self.file["index/atom_occurrences"]
        groups = []
        for atom in atoms:
            first, last = offsets[atom:atom + 2]
            if first != last:
                groups.append(postings[int(first):int(last)])
        if not groups:
            return np.empty(0, dtype=np.int64), np.empty(0, dtype=np.int64)
        return np.unique(np.concatenate(groups), return_counts=True)

    def _posting_count(self, atom_indices):
        offsets = self.file["index/atom_offsets"]
        return sum(int(offsets[atom + 1]) - int(offsets[atom])
                   for atom in atom_indices)

    def _frame_candidate_count(self, coverage):
        grouped = {}
        block_size = self.metadata["block_size"]
        for frame in coverage:
            grouped.setdefault(frame // block_size, []).append(frame % block_size)
        dataset = self.file["data/frame_offsets"]
        column = self.column_index["frame_offsets"]
        total = 0
        for block, locals_ in grouped.items():
            first = int(self.offsets[column, block])
            last = int(self.offsets[column, block + 1])
            offsets = dataset[first:last]
            local = np.asarray(locals_, dtype=np.int64)
            total += int(np.sum(offsets[local + 1] - offsets[local]))
        return total

    def _order_columns(self, columns, coverage, requested_frames):
        if requested_frames is None or not len(columns["structure_indices"]):
            return columns
        rank = np.empty(self.metadata["n_structures"], dtype=np.int64)
        rank[requested_frames] = np.arange(len(requested_frames))
        order = np.argsort(rank[columns["structure_indices"]], kind="stable")
        return _take_rows(columns, order)

    def _frame_first(self, coverage, requested_frames, predicate):
        grouped = {}
        block_size = self.metadata["block_size"]
        for frame in coverage:
            grouped.setdefault(frame // block_size, []).append(frame % block_size)
        batches = []
        for block in sorted(grouped):
            common, _, _ = self._block(block)
            offsets = common["frame_offsets"]
            positions = np.concatenate([
                np.arange(offsets[local], offsets[local + 1])
                for local in grouped[block]
            ])
            if not len(positions):
                continue
            columns = self._selected_block(block, positions)
            selected = np.flatnonzero(predicate(columns))
            if len(selected):
                batches.append(_take_rows(columns, selected))
        columns = self._order_columns(
            _join_batches(batches), coverage, requested_frames
        )
        return coverage, columns

    def _gather_ids(self, ids, coverage, requested_frames, hits=None,
                    keep_equal=True):
        if (not len(ids)
                or requested_frames is not None and not len(requested_frames)):
            return coverage, _empty_columns()
        blocks = np.searchsorted(self.block_event_offsets, ids, side="right") - 1
        batches = []
        for block in np.unique(blocks):
            selected = blocks == block
            positions = ids[selected] - self.block_event_offsets[block]
            common, _, _ = self._block(int(block))
            keep = np.ones(len(positions), dtype=bool)
            if requested_frames is not None:
                keep &= np.isin(
                    common["occurrence_structures"][positions], requested_frames
                )
            if hits is not None:
                internal = (hits[selected]
                            == common["occurrence_atom_count"][positions])
                keep &= internal if keep_equal else ~internal
            if np.any(keep):
                batches.append(self._selected_block(int(block), positions[keep]))
        return coverage, self._order_columns(
            _join_batches(batches), coverage, requested_frames
        )

    def query_columns(self, structure_indices=None, atom_indices=None,
                      mode="incident", planner="auto"):
        """Query typed columns by source structure and atom indices."""
        if mode not in {"incident", "internal", "cross"}:
            raise ValueError("mode must be incident, internal, or cross")
        if planner not in {"auto", "frame", "atom"}:
            raise ValueError("planner must be auto, frame, or atom")
        coverage, requested_frames = self._coverage(structure_indices)
        if atom_indices is None:
            if requested_frames is None:
                batches = []
                for block in range(len(self.scopes)):
                    count = (self.block_event_offsets[block + 1]
                             - self.block_event_offsets[block])
                    if count:
                        batches.append(self._selected_block(
                            block, np.arange(count)
                        ))
                return coverage, _join_batches(batches)
            return coverage, _join_batches([
                self.query_frame_columns(int(frame))[1] for frame in coverage
            ])
        atom_indices = self._indices(
            atom_indices, self.metadata["n_atoms"], "atom_indices"
        )
        use_frames = requested_frames is not None and (
            planner == "frame" or (
                planner == "auto" and self._frame_candidate_count(coverage)
                <= self._posting_count(atom_indices)
            )
        )
        if use_frames:
            def select(columns):
                hits = _hit_counts(columns, atom_indices)
                if mode == "incident":
                    return hits > 0
                total = _hit_counts(columns, columns["atoms"])
                return ((hits == total) & (hits > 0) if mode == "internal"
                        else (hits > 0) & (hits < total))

            return self._frame_first(coverage, requested_frames, select)
        ids, hits = self._postings(atom_indices)
        return self._gather_ids(
            ids, coverage, requested_frames,
            hits=None if mode == "incident" else hits,
            keep_equal=mode == "internal",
        )

    def between_columns(self, atom_indices_a, atom_indices_b,
                        structure_indices=None, exclusive=False,
                        planner="auto"):
        """Query relations touching both atom sets with optional exclusivity."""
        if planner not in {"auto", "frame", "atom"}:
            raise ValueError("planner must be auto, frame, or atom")
        coverage, requested_frames = self._coverage(structure_indices)
        atom_indices_a = self._indices(
            atom_indices_a, self.metadata["n_atoms"], "atom_indices_a"
        )
        atom_indices_b = self._indices(
            atom_indices_b, self.metadata["n_atoms"], "atom_indices_b"
        )
        use_frames = requested_frames is not None and (
            planner == "frame" or (
                planner == "auto" and self._frame_candidate_count(coverage)
                <= min(self._posting_count(atom_indices_a),
                       self._posting_count(atom_indices_b))
            )
        )
        if use_frames:
            union_atoms = list(dict.fromkeys((*atom_indices_a, *atom_indices_b)))

            def select(columns):
                found = ((_hit_counts(columns, atom_indices_a) > 0)
                         & (_hit_counts(columns, atom_indices_b) > 0))
                if exclusive:
                    found &= (_hit_counts(columns, union_atoms)
                              == _hit_counts(columns, columns["atoms"]))
                return found

            return self._frame_first(coverage, requested_frames, select)
        ids_a, _ = self._postings(atom_indices_a)
        ids_b, _ = self._postings(atom_indices_b)
        ids = np.intersect1d(ids_a, ids_b, assume_unique=True)
        if not exclusive or not len(ids):
            return self._gather_ids(ids, coverage, requested_frames)
        union_atoms = list(dict.fromkeys((*atom_indices_a, *atom_indices_b)))
        union_ids, hits = self._postings(union_atoms)
        positions = np.searchsorted(union_ids, ids)
        return self._gather_ids(
            ids, coverage, requested_frames, hits=hits[positions]
        )


def decoded_counter(columns, labels):
    """Materialize selected typed columns solely for full-record oracle checks."""
    output = Counter()
    count = len(columns["structure_indices"])
    for row in range(count):
        part_start = int(columns["participant_offsets"][row])
        part_stop = int(columns["participant_offsets"][row + 1])
        participants = []
        for part in range(part_start, part_stop):
            first = int(columns["atom_offsets"][part])
            last = int(columns["atom_offsets"][part + 1])
            participants.append({
                "role": labels["roles"][int(columns["role_codes"][part])],
                "atom_indices": columns["atoms"][first:last].tolist(),
            })
        record = {
            "structure_index": columns["structure_indices"][row],
            "interaction_type": labels["types"][int(columns["type_codes"][row])],
            "participants": participants,
            "evidence": labels["evidence"][int(columns["evidence_codes"][row])],
            "measurements": {name: columns[f"measure_{name}"][row]
                             for name in UNITS},
            "images": columns["image_vectors"][part_start:part_stop],
        }
        output[_signature(record)] += 1
    return output


def column_bytes(columns):
    """Count the typed result payload, excluding Python container overhead."""
    return sum(value.nbytes for value in columns.values())

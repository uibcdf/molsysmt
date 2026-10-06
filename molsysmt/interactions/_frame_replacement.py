"""Immutable frame replacement using independently indexed source blocks.

Each evaluated frame has one owner. Replacing frames changes ownership and a
small relation registry, without copying unaffected occurrence columns. Full
column access packs the active blocks; selected queries pack only relevant rows.
"""

from collections.abc import Mapping
from types import MappingProxyType

import numpy as np

from molsysmt._private.argdigest import arg_digest

from ._frame_validity import _FrameFilteredInteractions, _interchange_result, _metadata
from ._query_modes import normalize_query_mode
from .result import (
    _RESULT_DIGEST,
    Interactions,
    _check_skip_digestion,
    _immutable_array,
    _indices,
)


def _equal(a, b):
    if isinstance(a, Mapping) and isinstance(b, Mapping):
        return a.keys() == b.keys() and all(_equal(a[key], b[key]) for key in a)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(
            _equal(left, right) for left, right in zip(a, b)
        )
    if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
        return np.array_equal(a, b)
    return a == b


def _compatible(source, replacement):
    if not isinstance(replacement, Interactions):
        raise TypeError("replacement must be an Interactions analysis")
    if not source._is_full or not replacement._is_full:
        raise ValueError("Frame replacement requires two full interaction results")
    for name in (
        "n_atoms",
        "n_structures",
        "source_n_atoms",
        "source_n_structures",
        "atom_source_indices",
        "structure_source_indices",
        "source_id",
        "method",
        "parameters",
        "software",
        "measure_units",
    ):
        if not _equal(getattr(source, name), getattr(replacement, name)):
            raise ValueError(f"Frame replacement requires matching {name}")

    def same_set(a, b):
        if a is None or b is None:
            explicit = b if a is None else a
            # Scope vectors are validated, unique and sorted at construction.
            return explicit is None or len(explicit) == source.n_atoms
        return np.array_equal(a, b)

    def selected(result):
        return (
            result.evaluation_universe_indices
            if result.evaluation_atom_indices is None
            else result.evaluation_atom_indices
        )

    if (
        source.evaluation_mode != replacement.evaluation_mode
        or not same_set(
            source.evaluation_universe_indices, replacement.evaluation_universe_indices
        )
        or not same_set(selected(source), selected(replacement))
        or not _equal(
            source.evaluation_atom_indices_b, replacement.evaluation_atom_indices_b
        )
    ):
        raise ValueError("Frame replacement requires matching evaluation_scope")


def _parts(source):
    if isinstance(source, _FramePatchedInteractions):
        return list(source._segments)
    if isinstance(source, _FrameFilteredInteractions):
        return [(source._root, source._coverage, None, None)]
    return [(source, source._coverage, None, None)]


def _key(source, index):
    first, last = source.relation_participant_offsets[index : index + 2]
    return (
        source.relation_types[index],
        tuple(
            (
                source.participant_roles[item],
                tuple(
                    source.participant_atoms[
                        source.participant_atom_offsets[
                            item
                        ] : source.participant_atom_offsets[item + 1]
                    ]
                ),
            )
            for item in range(first, last)
        ),
    )


def _fingerprint(key):
    # Process-local accelerator only; equality always checks the full key.
    return hash(key)


def _relation_index(source):
    index = getattr(source, "_relation_key_index", None)
    if index is None:
        values = np.fromiter(
            (
                _fingerprint(_key(source, item))
                for item in range(len(source.relation_types))
            ),
            dtype=np.int64,
            count=len(source.relation_types),
        )
        order = np.argsort(values, kind="stable")
        index = (_immutable_array(values[order]), _immutable_array(order))
    return index


def _same_relations(source, incoming):
    for name in (
        "relation_types",
        "participant_roles",
        "relation_participant_offsets",
        "participant_atom_offsets",
        "participant_atoms",
    ):
        a, b = getattr(source, name), getattr(incoming, name)
        if a is not b and not _equal(a, b):
            return False
    return True


def _implicit_identity(values):
    # None means local indices already equal the registry indices. This avoids
    # allocating an identity vector for an unchanged base or matching prefix.
    values = np.asarray(values)
    if all(int(value) == index for index, value in enumerate(values)):
        return None
    return _immutable_array(values)


def _registry(source, incoming):
    """Share existing definitions and translate only the incoming catalog."""
    fields = {}
    added = {}
    index = getattr(source, "_relation_key_index", None)
    if _same_relations(source, incoming):
        relations = None
    else:
        relations = np.empty(len(incoming.relation_types), dtype=np.int64)
        if len(relations):
            index = _relation_index(source)
            hashes, indices = index
            fields["_relation_key_index"] = index
        for item in range(len(relations)):
            key = _key(incoming, item)
            fingerprint = _fingerprint(key)
            first, last = (
                np.searchsorted(hashes, fingerprint, side="left"),
                np.searchsorted(hashes, fingerprint, side="right"),
            )
            match = next(
                (
                    int(candidate)
                    for candidate in indices[first:last]
                    if _key(source, candidate) == key
                ),
                None,
            )
            if match is None:
                if key not in added:
                    added[key] = len(source.relation_types) + len(added)
                match = added[key]
            relations[item] = match
        relations = _implicit_identity(relations)
    if added:
        types = list(source.relation_types)
        roles = list(source.participant_roles)
        relation_offsets = list(source.relation_participant_offsets)
        atom_offsets = list(source.participant_atom_offsets)
        atoms = list(source.participant_atoms)
        for kind, participants in added:
            types.append(kind)
            for role, members in participants:
                roles.append(role)
                atoms.extend(members)
                atom_offsets.append(len(atoms))
            relation_offsets.append(len(roles))
        fields.update(relation_types=tuple(types), participant_roles=tuple(roles))
        for name, values in (
            ("relation_participant_offsets", relation_offsets),
            ("participant_atom_offsets", atom_offsets),
            ("participant_atoms", atoms),
        ):
            fields[name] = _immutable_array(np.asarray(values, dtype=np.int64))
        # Extend the numeric accelerator without regenerating old key tuples.
        values = np.r_[
            index[0], np.fromiter((_fingerprint(key) for key in added), dtype=np.int64)
        ]
        indices = np.r_[
            index[1], np.arange(len(source.relation_types), len(types), dtype=np.int64)
        ]
        order = np.argsort(values, kind="stable")
        fields["_relation_key_index"] = (
            _immutable_array(values[order]),
            _immutable_array(indices[order]),
        )
    if incoming.evidence_labels == source.evidence_labels:
        evidence = None
    else:
        labels = list(source.evidence_labels)
        evidence = []
        for label in incoming.evidence_labels:
            if label not in labels:
                labels.append(label)
            evidence.append(labels.index(label))
        evidence = _implicit_identity(np.asarray(evidence, dtype=np.int32))
        if len(labels) != len(source.evidence_labels):
            fields["evidence_labels"] = tuple(labels)
    return fields, relations, evidence


def _without(active, removed):
    mask = np.isin(active, removed)
    return active[~mask] if mask.any() else active


def _ordered_frames(frames):
    if len(frames) > 1 and np.any(frames[1:] < frames[:-1]):
        return _immutable_array(np.sort(frames))
    return _immutable_array(frames) if frames.flags.writeable else frames


def _mapped(mapping, values):
    return values if mapping is None else mapping[values]


def _snapshot(source, parts, coverage, fields=None):
    # Keep registry buffers, existing translations and unaffected frame vectors.
    parts = [
        (base, _ordered_frames(frames), relations, evidence)
        for base, frames, relations, evidence in parts
        if len(frames)
    ]
    offsets = np.zeros(source.n_structures + 1, dtype=np.int64)
    counts = offsets[1:]
    owners = np.full(
        source.n_structures, -1, dtype=np.int32 if len(parts) < 2**31 else np.int64
    )
    image_presence = set()
    for index, (base, frames, _, _) in enumerate(parts):
        owners[frames] = index
        lengths = np.searchsorted(base.occurrence_structures, frames, side="right")
        lengths -= np.searchsorted(base.occurrence_structures, frames, side="left")
        counts[frames] = lengths
        if lengths.sum():
            image_presence.add(base.image_vectors is not None)
    if len(image_presence) > 1:
        raise ValueError(
            "Frame replacement cannot mix known and unknown periodic images"
        )
    result = object.__new__(_FramePatchedInteractions)
    result.__dict__ = source.__dict__.copy()
    for name in ("_root", "_row_removal", "_public_occurrence_indices"):
        result.__dict__.pop(name, None)
    result.__dict__.update(fields or {})
    result.__dict__.update(_metadata(source))
    result.__dict__["evaluated_structure_indices"] = (
        source.evaluated_structure_indices
        if coverage is source._coverage
        else _immutable_array(coverage)
    )
    result._coverage = result.evaluated_structure_indices
    result._segments = tuple(parts)
    np.cumsum(counts, out=counts)
    result._frame_offsets = _immutable_array(offsets)
    result._frame_owners = _immutable_array(owners)
    result._active_count = int(offsets[-1])
    result._has_images = True in image_presence
    result._packed_result = None
    # Source columns are reached only through active segments, not through an
    # accidental shallow copy of an obsolete analysis or materialized cache.
    for name in (
        "occurrence_structures",
        "occurrence_relations",
        "occurrence_evidence",
        "occurrence_image_offsets",
        "image_vectors",
        "measurements",
        "_positions",
    ):
        result.__dict__.pop(name, None)
    for name in (
        "_atom_relation_offsets",
        "_atom_relation_ids",
        "_relation_occurrence_offsets",
        "_relation_occurrence_ids",
    ):
        result.__dict__[name] = None
    if not result._active_count:
        # Evaluated-empty frames need coverage, not references to retired rows.
        return result._packed()
    return result


def _replace(source, replacement):
    _compatible(source, replacement)
    with _interchange_result(replacement) as incoming:
        frames = incoming.evaluated_structure_indices
        fields, relations, evidence = _registry(source, incoming)
        parts = [
            (base, _without(active, frames), rel, ev)
            for base, active, rel, ev in _parts(source)
        ]
        parts.append((incoming, frames, relations, evidence))
        extra = frames[~np.isin(frames, source._coverage)]
        coverage = np.r_[source._coverage, extra] if len(extra) else source._coverage
        from ._execution_provenance import replace

        result = _snapshot(source, parts, coverage, fields)
        result._execution_records = replace(source, incoming, frames)
        return result


def _invalidate_patch(source, frames):
    coverage = _without(source._coverage, frames)
    parts = [
        (base, _without(active, frames), rel, ev)
        for base, active, rel, ev in _parts(source)
    ]
    return _snapshot(source, parts, coverage)


def _images(base, positions):
    lengths = (
        base.occurrence_image_offsets[positions + 1]
        - base.occurrence_image_offsets[positions]
    )
    offsets = np.r_[0, np.cumsum(lengths)]
    vectors = np.empty((offsets[-1], 3), dtype=np.int32)
    # Positions are in canonical source order here; copy contiguous runs.
    breaks = np.r_[0, np.flatnonzero(np.diff(positions) != 1) + 1, len(positions)]
    for first, last in zip(breaks[:-1], breaks[1:]):
        if first != last:
            vectors[offsets[first] : offsets[last]] = base.image_vectors[
                base.occurrence_image_offsets[
                    positions[first]
                ] : base.occurrence_image_offsets[positions[last - 1] + 1]
            ]
    return offsets, vectors


class _FramePatchedInteractions(_FrameFilteredInteractions):
    """A full logical analysis composed of disjoint immutable frame blocks."""

    @property
    def numeric_nbytes(self):
        arrays = {}
        seen = set()

        def visit(value):
            if id(value) in seen:
                return
            seen.add(id(value))
            if isinstance(value, np.ndarray):
                arrays[id(value)] = value
            elif isinstance(value, Interactions):
                for item in vars(value).values():
                    visit(item)
            elif isinstance(value, Mapping):
                for item in value.values():
                    visit(item)
            elif isinstance(value, (tuple, list)):
                for item in value:
                    visit(item)

        visit(self)
        return sum(value.nbytes for value in arrays.values())

    def _collect(self, structure_indices, query_arguments, between=False):
        coverage = (
            self._coverage
            if structure_indices is None
            else self._query_frames(structure_indices)
        )
        columns = []
        segments = (
            self._segments
            if structure_indices is None
            else [
                self._segments[index]
                for index in np.unique(self._frame_owners[coverage])
            ]
        )
        for base, active, relation_map, evidence_map in segments:
            requested = (
                None
                if structure_indices is None
                else coverage[np.isin(coverage, active)]
            )
            if (
                structure_indices is None
                and not between
                and query_arguments["atom_indices"] is None
                and query_arguments["interaction_types"] is None
            ):
                requested = active
            if requested is not None and not len(requested):
                continue
            view = (
                base.between_selections(
                    structure_indices=requested, skip_digestion=True, **query_arguments
                )
                if between
                else base.query(
                    structure_indices=requested, skip_digestion=True, **query_arguments
                )
            )
            positions = view._positions
            positions = np.sort(
                positions[np.isin(base.occurrence_structures[positions], active)]
            )
            if not len(positions):
                continue
            frames = base.occurrence_structures[positions]
            handles = (
                self._frame_offsets[frames]
                + positions
                - np.searchsorted(base.occurrence_structures, frames, side="left")
            )
            columns.append(
                (base, positions, frames, handles, relation_map, evidence_map)
            )
        return self._projection(columns, coverage, structure_indices is not None)

    def _projection(self, columns, coverage, requested_order):
        structures = (
            np.concatenate([item[2] for item in columns])
            if columns
            else np.empty(0, dtype=np.int64)
        )
        order = np.argsort(structures, kind="stable")
        relations = (
            np.concatenate(
                [
                    _mapped(mapping, base.occurrence_relations[pos])
                    for base, pos, _, _, mapping, _ in columns
                ]
            )
            if columns
            else np.empty(0, dtype=np.int64)
        )
        evidence = (
            np.concatenate(
                [
                    _mapped(mapping, base.occurrence_evidence[pos])
                    for base, pos, _, _, _, mapping in columns
                ]
            )
            if columns
            else np.empty(0, dtype=np.int32)
        )
        measurements = {
            name: (
                np.concatenate(
                    [base.measurements[name][pos] for base, pos, *_ in columns]
                )[order]
                if columns
                else np.empty(0)
            )
            for name in self.measure_units
        }
        if self._has_images:
            # Image blocks follow the same row permutation as every measure.
            images = [_images(base, pos) for base, pos, *_ in columns]
            lengths = (
                np.concatenate([np.diff(offsets) for offsets, _ in images])
                if images
                else np.empty(0, dtype=np.int64)
            )
            raw_offsets = np.r_[0, np.cumsum(lengths)]
            raw_vectors = (
                np.concatenate([vectors for _, vectors in images])
                if images
                else np.empty((0, 3), dtype=np.int32)
            )
            offsets = np.r_[0, np.cumsum(lengths[order])]
            vector_order = (
                np.repeat(raw_offsets[order], lengths[order])
                + np.arange(offsets[-1])
                - np.repeat(offsets[:-1], lengths[order])
            )
            vectors = raw_vectors[vector_order]
        else:
            offsets = vectors = None
        # The shared registry is already validated and immutable. Building a
        # selected view must not validate/copy every unrelated relation again.
        result = object.__new__(Interactions)
        result.__dict__ = self.__dict__.copy()
        for name in (
            "_segments",
            "_frame_offsets",
            "_frame_owners",
            "_packed_result",
            "_active_count",
            "_has_images",
        ):
            result.__dict__.pop(name, None)
        result.__dict__.update(_metadata(self))
        result.__dict__["evaluated_structure_indices"] = _immutable_array(coverage)
        for name, value in (
            ("occurrence_structures", structures[order]),
            ("occurrence_relations", relations[order]),
            ("occurrence_evidence", evidence[order]),
            ("occurrence_image_offsets", offsets),
            ("image_vectors", vectors),
        ):
            result.__dict__[name] = None if value is None else _immutable_array(value)
        result.__dict__["measurements"] = MappingProxyType(
            {name: _immutable_array(values) for name, values in measurements.items()}
        )
        handles = (
            np.concatenate([item[3] for item in columns])[order]
            if columns
            else np.empty(0, dtype=np.int64)
        )
        result._public_occurrence_indices = _immutable_array(handles)
        positions = np.arange(len(order), dtype=np.int64)
        if requested_order and len(positions):
            sorted_coverage = np.argsort(coverage)
            ranks = sorted_coverage[
                np.searchsorted(coverage[sorted_coverage], result.occurrence_structures)
            ]
            positions = positions[np.argsort(ranks, kind="stable")]
        return result._view(positions, coverage)

    @arg_digest(**_RESULT_DIGEST)
    def query(
        self,
        structure_indices=None,
        atom_indices=None,
        mode="involving_selection",
        interaction_types=None,
        *,
        skip_digestion=False,
    ):
        _check_skip_digestion(skip_digestion)
        mode = normalize_query_mode(mode)
        if atom_indices is not None:
            atom_indices = _indices(atom_indices, self.n_atoms, "atom_indices")
        return self._collect(
            structure_indices,
            dict(
                atom_indices=atom_indices,
                mode=mode,
                interaction_types=interaction_types,
            ),
        )

    @arg_digest(**_RESULT_DIGEST)
    def between_selections(
        self,
        atom_indices_a,
        atom_indices_b,
        structure_indices=None,
        exclusive=False,
        interaction_types=None,
        *,
        skip_digestion=False,
    ):
        _check_skip_digestion(skip_digestion)
        a = _indices(atom_indices_a, self.n_atoms, "atom_indices_a")
        b = _indices(atom_indices_b, self.n_atoms, "atom_indices_b")
        if np.intersect1d(a, b).size:
            raise ValueError("atom_indices_a and atom_indices_b must be disjoint")
        return self._collect(
            structure_indices,
            dict(
                atom_indices_a=a,
                atom_indices_b=b,
                exclusive=exclusive,
                interaction_types=interaction_types,
            ),
            between=True,
        )

    def _packed(self):
        if self._packed_result is None:
            packed = self.query()
            packed._is_full = True
            packed.__dict__.pop("_public_occurrence_indices", None)
            self._packed_result = packed
        self._packed_result.__dict__.update(_metadata(self))
        return self._packed_result

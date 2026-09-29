"""Sparse interaction results for one molecular system."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def _indices(values, limit, name):
    array = np.asarray(values)
    if array.size == 0:
        array = np.asarray(values, dtype=np.int64)
    if array.ndim == 0:
        array = array.reshape(1)
    if array.ndim != 1 or array.dtype.kind not in "iu":
        raise ValueError(f"{name} must be a one-dimensional array of integer indices")
    if np.any(array < 0) or np.any(array >= limit):
        raise ValueError(f"{name} contains an index outside [0, {limit})")
    return array.astype(np.int64, copy=False)


def _unique_in_order(values):
    return np.fromiter(dict.fromkeys(values.tolist()), dtype=np.int64)


def _source_map(values, local_size, name):
    """Normalize one local-to-source map without coercing noninteger values."""

    if values is None:
        return np.arange(local_size, dtype=np.int64)
    array = np.asarray(values)
    if array.size == 0:
        array = np.asarray(values, dtype=np.int64)
    if array.ndim != 1 or array.shape != (local_size,) or array.dtype.kind not in "iu":
        raise ValueError(f"{name} must contain one integer per local index")
    return array.astype(np.int64, copy=True)


def _scope_indices(values, limit, name):
    """Normalize an optional atom set; None denotes the complete local axis."""

    if values is None:
        return None
    return np.unique(_indices(values, limit, name))


class Interactions:
    """Storing sparse interaction observations and querying their participants.

    Instances use local atom and structure indices, with explicit maps to the
    source system. A query returns a
    lightweight view sharing the relation and occurrence arrays with its parent.
    Only the selected occurrence indices and evaluated structure indices are new.

    Notes
    -----
    This experimental result stores one analysis method per instance. It does
    not attach itself to a molecular system or declare covalent connectivity.

    .. versionadded:: 1.0.0
    """

    def __init__(self, *, n_atoms, n_structures, evaluated_structure_indices,
                 relation_types, relation_participant_offsets, participant_roles,
                 participant_atom_offsets, participant_atoms, occurrence_structures,
                 occurrence_relations, occurrence_evidence, measurements,
                 measure_units, method, parameters=None, source_id=None,
                 occurrence_image_offsets=None, image_vectors=None,
                 evidence_labels=None, atom_source_indices=None,
                 structure_source_indices=None, source_n_atoms=None,
                 source_n_structures=None, evaluation_mode="internal",
                 evaluation_atom_indices=None, evaluation_atom_indices_b=None,
                 evaluation_universe_indices=None):
        self.n_atoms = int(n_atoms)
        self.n_structures = int(n_structures)
        self.source_n_atoms = (
            self.n_atoms if source_n_atoms is None else int(source_n_atoms)
        )
        self.source_n_structures = (
            self.n_structures if source_n_structures is None
            else int(source_n_structures)
        )
        self.atom_source_indices = _source_map(
            atom_source_indices, self.n_atoms, "atom_source_indices"
        )
        self.structure_source_indices = _source_map(
            structure_source_indices, self.n_structures,
            "structure_source_indices",
        )
        self.evaluation_mode = str(evaluation_mode)
        self.evaluation_atom_indices = _scope_indices(
            evaluation_atom_indices, self.n_atoms, "evaluation_atom_indices"
        )
        self.evaluation_atom_indices_b = _scope_indices(
            evaluation_atom_indices_b, self.n_atoms, "evaluation_atom_indices_b"
        )
        self.evaluation_universe_indices = _scope_indices(
            evaluation_universe_indices, self.n_atoms, "evaluation_universe_indices"
        )
        self.evaluated_structure_indices = _unique_in_order(
            _indices(evaluated_structure_indices, self.n_structures,
                     "evaluated_structure_indices")
        )
        self.relation_types = tuple(relation_types)
        self.relation_participant_offsets = np.asarray(
            relation_participant_offsets, dtype=np.int64
        )
        self.participant_roles = tuple(participant_roles)
        self.participant_atom_offsets = np.asarray(
            participant_atom_offsets, dtype=np.int64
        )
        self.participant_atoms = np.asarray(participant_atoms, dtype=np.int64)
        self.occurrence_structures = np.asarray(occurrence_structures, dtype=np.int64)
        self.occurrence_relations = np.asarray(occurrence_relations, dtype=np.int64)
        if evidence_labels is None:
            self.evidence_labels = tuple(dict.fromkeys(occurrence_evidence))
            evidence_lookup = {
                label: index for index, label in enumerate(self.evidence_labels)
            }
            self.occurrence_evidence = np.fromiter(
                (evidence_lookup[label] for label in occurrence_evidence),
                dtype=np.int32,
            )
        else:
            self.evidence_labels = tuple(evidence_labels)
            self.occurrence_evidence = np.asarray(
                occurrence_evidence, dtype=np.int32
            )
        self.occurrence_image_offsets = (
            None if occurrence_image_offsets is None else
            np.asarray(occurrence_image_offsets, dtype=np.int64)
        )
        self.image_vectors = (
            None if image_vectors is None else np.asarray(image_vectors, dtype=np.int32)
        )
        self.measurements = {key: np.asarray(value, dtype=np.float64)
                             for key, value in measurements.items()}
        self.measure_units = dict(measure_units)
        self.method = str(method)
        self.parameters = dict(parameters or {})
        self.source_id = source_id
        self._positions = np.arange(len(self.occurrence_relations), dtype=np.int64)
        self._coverage = self.evaluated_structure_indices
        self._is_full = True
        self._atom_relation_offsets = None
        self._atom_relation_ids = None
        self._relation_occurrence_offsets = None
        self._relation_occurrence_ids = None
        self._validate()

    def _validate(self):
        if self.n_atoms < 0 or self.n_structures < 0:
            raise ValueError("n_atoms and n_structures must be nonnegative")
        if self.source_n_atoms < 0 or self.source_n_structures < 0:
            raise ValueError("source atom and structure counts must be nonnegative")
        if (self.atom_source_indices.shape != (self.n_atoms,)
                or self.structure_source_indices.shape != (self.n_structures,)):
            raise ValueError("source-index maps must match the local atom and structure axes")
        if (np.any(self.atom_source_indices < -1)
                or np.any(self.atom_source_indices >= self.source_n_atoms)
                or np.any(self.structure_source_indices < -1)
                or np.any(self.structure_source_indices >= self.source_n_structures)):
            raise ValueError("source-index maps contain out-of-range indices")
        mapped_atoms = self.atom_source_indices[self.atom_source_indices >= 0]
        if np.unique(mapped_atoms).size != mapped_atoms.size:
            raise ValueError("atom source indices must be unique when known")
        if self.evaluation_mode not in {"internal", "incident", "between"}:
            raise ValueError("evaluation_mode must be 'internal', 'incident', or 'between'")
        universe = self._scope_axis(self.evaluation_universe_indices)
        selected = self._scope_selected()
        universe_mask = np.zeros(self.n_atoms, dtype=np.bool_)
        universe_mask[universe] = True
        selected_mask = np.zeros(self.n_atoms, dtype=np.bool_)
        selected_mask[selected] = True
        if not np.all(universe_mask[selected]):
            raise ValueError("evaluation atom set must be within the evaluated universe")
        if self.evaluation_mode == "internal":
            if self.evaluation_atom_indices_b is not None:
                raise ValueError("internal evaluation does not use a second atom set")
        elif self.evaluation_mode == "incident":
            if self.evaluation_atom_indices is None:
                raise ValueError("incident evaluation requires an explicit atom set")
            if self.evaluation_atom_indices_b is not None:
                raise ValueError("incident evaluation does not use a second atom set")
        else:
            if self.evaluation_atom_indices is None or self.evaluation_atom_indices_b is None:
                raise ValueError("between evaluation requires two explicit atom sets")
            b_mask = np.zeros(self.n_atoms, dtype=np.bool_)
            b_mask[self.evaluation_atom_indices_b] = True
            if np.any(selected_mask[self.evaluation_atom_indices_b]):
                raise ValueError("between evaluation atom sets must be disjoint")
            if not np.all(universe_mask[self.evaluation_atom_indices_b]):
                raise ValueError("evaluation atom sets must be within the evaluated universe")
        n_relations = len(self.relation_types)
        n_participants = len(self.participant_roles)
        if (len(self.relation_participant_offsets) != n_relations + 1
                or self.relation_participant_offsets[0] != 0
                or self.relation_participant_offsets[-1] != n_participants
                or np.any(np.diff(self.relation_participant_offsets) <= 0)):
            raise ValueError("each relation must have at least one participant")
        if (len(self.participant_atom_offsets) != n_participants + 1
                or self.participant_atom_offsets[0] != 0
                or self.participant_atom_offsets[-1] != len(self.participant_atoms)
                or np.any(np.diff(self.participant_atom_offsets) <= 0)):
            raise ValueError("each participant must contain at least one atom")
        _indices(self.participant_atoms, self.n_atoms, "participant_atoms")
        for relation in range(n_relations):
            atoms = self._relation_atoms(relation)
            if not np.all(universe_mask[atoms]):
                raise ValueError("relation contains atoms outside the evaluated universe")
            if self.evaluation_mode == "internal":
                valid = np.all(selected_mask[atoms])
            else:
                valid = selected_mask[atoms].any()
                if self.evaluation_mode == "between":
                    valid = valid and b_mask[atoms].any()
            if not valid:
                raise ValueError("relation does not satisfy the declared evaluation scope")
        n_occurrences = len(self.occurrence_relations)
        if (len(self.occurrence_structures) != n_occurrences
                or len(self.occurrence_evidence) != n_occurrences):
            raise ValueError("occurrence columns must have equal lengths")
        if (np.any(self.occurrence_evidence < 0)
                or np.any(self.occurrence_evidence >= len(self.evidence_labels))):
            raise ValueError("occurrence evidence code is outside the label table")
        if np.any(np.diff(self.occurrence_structures) < 0):
            raise ValueError("occurrences must be ordered by structure")
        _indices(self.occurrence_structures, self.n_structures,
                 "occurrence_structures")
        _indices(self.occurrence_relations, n_relations, "occurrence_relations")
        if not np.all(np.isin(self.occurrence_structures,
                            self.evaluated_structure_indices)):
            raise ValueError("an occurrence belongs to an unevaluated structure")
        if set(self.measurements) != set(self.measure_units):
            raise ValueError("each measurement requires an explicit unit")
        if any(value.shape != (n_occurrences,) for value in self.measurements.values()):
            raise ValueError("measurement columns must align with occurrences")
        if (self.occurrence_image_offsets is None) != (self.image_vectors is None):
            raise ValueError("image offsets and vectors must be supplied together")
        if self.image_vectors is not None:
            offsets = self.occurrence_image_offsets
            if (offsets.shape != (n_occurrences + 1,) or offsets[0] != 0
                    or offsets[-1] != len(self.image_vectors)
                    or self.image_vectors.shape != (len(self.image_vectors), 3)):
                raise ValueError("periodic image columns have inconsistent shapes")
            arities = np.diff(self.relation_participant_offsets)[
                self.occurrence_relations
            ]
            if not np.array_equal(np.diff(offsets), arities):
                raise ValueError("each occurrence needs one image per participant")

    @classmethod
    def from_records(cls, records, *, n_atoms, n_structures,
                     evaluated_structure_indices, method, measure_units=None,
                     parameters=None, source_id=None, atom_source_indices=None,
                     structure_source_indices=None, source_n_atoms=None,
                     source_n_structures=None, evaluation_mode="internal",
                     evaluation_atom_indices=None, evaluation_atom_indices_b=None,
                     evaluation_universe_indices=None):
        """Building a sparse result from frame-specific interaction records.

        Parameters
        ----------
        records : iterable of dict
            Records with ``structure_index``, ``interaction_type``, and
            ``participants``. Each participant has ``role`` and ``atom_indices``.
            Optional ``measurements`` map names to numeric values, and
            ``evidence`` defaults to ``observed_geometry``. Optional ``images``
            holds one integer lattice vector per participant, in relation
            order. For a box with row vectors, add ``images[p] @ box`` to the
            coordinates of every atom in participant ``p``; relative geometry
            uses the image difference from the first participant.
        n_atoms : int
            Number of atoms in the local index space.
        n_structures : int
            Number of structures in the local index space.
        evaluated_structure_indices : array-like of int
            Explicitly evaluated structures, including empty ones.
        method : str
            Name of the analysis method.
        measure_units : dict or None, default=None
            Unit for every measurement column; use ``"dimensionless"`` for scores.
        parameters : dict or None, default=None
            Method parameters used for this result.
        source_id : str or None, default=None
            Optional source identity supplied by the caller.
        atom_source_indices : array-like of int or None, default=None
            Local-to-source atom indices. ``-1`` denotes no source counterpart.
        structure_source_indices : array-like of int or None, default=None
            Local-to-source structure indices. ``-1`` denotes no source counterpart.
        source_n_atoms : int or None, default=None
            Size of the source atom-index space; defaults to ``n_atoms``.
        source_n_structures : int or None, default=None
            Size of the source structure-index space; defaults to ``n_structures``.
        evaluation_mode : {'internal', 'incident', 'between'}, default='internal'
            Declared atom search scope, shared by all evaluated structures.
        evaluation_atom_indices : array-like of int or None, default=None
            First atom set. ``None`` means the evaluated universe for ``internal``.
        evaluation_atom_indices_b : array-like of int or None, default=None
            Required disjoint second atom set for ``between``.
        evaluation_universe_indices : array-like of int or None, default=None
            Atoms searched for participants; ``None`` means all local atoms.

        Returns
        -------
        Interactions
            Sparse result in local index space.

        Examples
        --------
        >>> from molsysmt import Interactions
        >>> result = Interactions.from_records([], n_atoms=2, n_structures=1,
        ...     evaluated_structure_indices=[0], method="example")
        >>> result.query(structure_indices=[0]).n_interactions
        0

        .. versionadded:: 1.0.0
        """
        units = dict(measure_units or {})
        coverage = _unique_in_order(_indices(
            evaluated_structure_indices, int(n_structures),
            "evaluated_structure_indices"
        ))
        relation_keys = set()
        coverage_set = set(coverage.tolist())
        rows = []
        for record in records:
            frame = int(record["structure_index"])
            if frame not in coverage_set:
                raise ValueError("an occurrence belongs to an unevaluated structure")
            participants = tuple(
                (str(item["role"]), tuple(int(atom) for atom in item["atom_indices"]))
                for item in record["participants"]
            )
            if not participants or any(not indices for _, indices in participants):
                raise ValueError("each relation needs nonempty participants")
            key = (str(record["interaction_type"]), participants)
            relation_keys.add(key)
            measures = dict(record.get("measurements", {}))
            if set(measures) - set(units):
                raise ValueError("every measurement needs an explicit unit")
            images = record.get("images")
            if images is not None:
                images = np.asarray(images)
                if (images.shape != (len(participants), 3)
                        or images.dtype.kind not in "iu"):
                    raise ValueError("images must contain an integer vector per participant")
                images = images.astype(np.int32)
            rows.append((frame, key, str(record.get("evidence", "observed_geometry")),
                         measures, images))
        relation_lookup = {key: index for index, key in enumerate(sorted(relation_keys))}
        relation_types = []
        relation_participant_offsets = [0]
        roles = []
        participant_atom_offsets = [0]
        atoms = []
        for kind, participants in sorted(relation_keys):
            relation_types.append(kind)
            for role, indices in participants:
                roles.append(role)
                atoms.extend(indices)
                participant_atom_offsets.append(len(atoms))
            relation_participant_offsets.append(len(roles))
        rows = [(frame, relation_lookup[key], evidence, measures, images)
                for frame, key, evidence, measures, images in rows]
        rows.sort(key=lambda row: (row[0], row[1],
                                   () if row[4] is None else tuple(row[4].flat),
                                   row[2], tuple(sorted(row[3].items()))))
        has_images = any(row[4] is not None for row in rows)
        if has_images and any(row[4] is None for row in rows):
            raise ValueError(
                "periodic images must be supplied for every occurrence or none"
            )
        image_offsets = [0] if has_images else None
        image_vectors = [] if has_images else None
        if has_images:
            for _, _, _, _, images in rows:
                image_vectors.extend(images)
                image_offsets.append(len(image_vectors))
        return cls(
            n_atoms=n_atoms, n_structures=n_structures,
            evaluated_structure_indices=coverage, relation_types=relation_types,
            relation_participant_offsets=relation_participant_offsets,
            participant_roles=roles, participant_atom_offsets=participant_atom_offsets,
            participant_atoms=atoms,
            occurrence_structures=[row[0] for row in rows],
            occurrence_relations=[row[1] for row in rows],
            occurrence_evidence=[row[2] for row in rows],
            measurements={name: [row[3].get(name, np.nan) for row in rows]
                          for name in units}, measure_units=units, method=method,
            parameters=parameters, source_id=source_id,
            occurrence_image_offsets=image_offsets, image_vectors=image_vectors,
            atom_source_indices=atom_source_indices,
            structure_source_indices=structure_source_indices,
            source_n_atoms=source_n_atoms, source_n_structures=source_n_structures,
            evaluation_mode=evaluation_mode,
            evaluation_atom_indices=evaluation_atom_indices,
            evaluation_atom_indices_b=evaluation_atom_indices_b,
            evaluation_universe_indices=evaluation_universe_indices,
        )

    def _scope_axis(self, values):
        return np.arange(self.n_atoms, dtype=np.int64) if values is None else values

    def _scope_selected(self):
        if self.evaluation_atom_indices is None and self.evaluation_mode == "internal":
            return self._scope_axis(self.evaluation_universe_indices)
        return self._scope_axis(self.evaluation_atom_indices)

    @property
    def evaluation_scope(self):
        """Returning the declared atom search scope in local indices."""

        return {
            "mode": self.evaluation_mode,
            "atom_indices": self._scope_selected().copy(),
            "atom_indices_b": (
                None if self.evaluation_atom_indices_b is None
                else self.evaluation_atom_indices_b.copy()
            ),
            "universe_indices": self._scope_axis(
                self.evaluation_universe_indices
            ).copy(),
        }

    @property
    def n_interactions(self):
        """Returning the number of selected occurrences."""
        return len(self._positions)

    @property
    def numeric_nbytes(self):
        """Returning numeric array bytes, excluding Python object overhead."""
        arrays = (
            self.evaluated_structure_indices,
            self.relation_participant_offsets,
            self.participant_atom_offsets,
            self.participant_atoms,
            self.occurrence_structures,
            self.occurrence_relations,
            self.occurrence_evidence,
            self._positions,
            self.atom_source_indices,
            self.structure_source_indices,
            *(value for value in (
                self.evaluation_atom_indices,
                self.evaluation_atom_indices_b,
                self.evaluation_universe_indices,
            ) if value is not None),
            *self.measurements.values(),
        )
        if self.image_vectors is not None:
            arrays += (self.occurrence_image_offsets, self.image_vectors)
        if self._atom_relation_offsets is not None:
            arrays += (
                self._atom_relation_offsets,
                self._atom_relation_ids,
                self._relation_occurrence_offsets,
                self._relation_occurrence_ids,
            )
        return sum(array.nbytes for array in arrays)

    def relation(self, relation_index):
        """Returning the kind and participants of one relation."""
        index = int(relation_index)
        if index < 0 or index >= len(self.relation_types):
            raise IndexError("relation_index is out of range")
        begin = self.relation_participant_offsets[index]
        end = self.relation_participant_offsets[index + 1]
        participants = []
        for item in range(begin, end):
            start = self.participant_atom_offsets[item]
            stop = self.participant_atom_offsets[item + 1]
            participants.append({"role": self.participant_roles[item],
                                 "atom_indices": self.participant_atoms[start:stop].copy()})
        return {"interaction_type": self.relation_types[index],
                "participants": participants}

    def _relation_atoms(self, index):
        first = self.relation_participant_offsets[index]
        last = self.relation_participant_offsets[index + 1]
        return self.participant_atoms[
            self.participant_atom_offsets[first]:self.participant_atom_offsets[last]
        ]

    def _build_indexes(self):
        if self._atom_relation_offsets is not None:
            return
        posting_atoms = []
        posting_relations = []
        for relation in range(len(self.relation_types)):
            atoms = np.unique(self._relation_atoms(relation))
            posting_atoms.extend(atoms)
            posting_relations.extend([relation] * len(atoms))
        if posting_atoms:
            order = np.lexsort((posting_relations, posting_atoms))
            atoms_sorted = np.asarray(posting_atoms, dtype=np.int64)[order]
            self._atom_relation_ids = np.asarray(posting_relations, dtype=np.int64)[order]
            counts = np.bincount(atoms_sorted, minlength=self.n_atoms)
        else:
            self._atom_relation_ids = np.empty(0, dtype=np.int64)
            counts = np.zeros(self.n_atoms, dtype=np.int64)
        self._atom_relation_offsets = np.r_[0, np.cumsum(counts)]
        order = np.argsort(self.occurrence_relations, kind="stable")
        self._relation_occurrence_ids = order.astype(np.int64, copy=False)
        counts = np.bincount(self.occurrence_relations,
                             minlength=len(self.relation_types))
        self._relation_occurrence_offsets = np.r_[0, np.cumsum(counts)]

    def _view(self, positions, coverage):
        view = object.__new__(Interactions)
        view.__dict__ = self.__dict__.copy()
        view._positions = np.asarray(positions, dtype=np.int64)
        view._coverage = np.asarray(coverage, dtype=np.int64)
        view._is_full = False
        return view

    def query(self, structure_indices=None, atom_indices=None, mode="incident",
              interaction_types=None):
        """Selecting occurrences by structures, atoms, and interaction kind.

        Parameters
        ----------
        structure_indices : array-like of int or None, default=None
            Local structure indices; repeats are removed in first-seen order.
        atom_indices : array-like of int or None, default=None
            Local atom indices defining the set used by ``mode``.
        mode : {'incident', 'internal', 'cross'}, default='incident'
            Whether any, all, or only some relation atoms belong to the set.
        interaction_types : iterable of str or None, default=None
            Kinds to retain. ``None`` retains every kind.

        Returns
        -------
        Interactions
            Lightweight selection sharing the stored numeric arrays.

        .. versionadded:: 1.0.0
        """
        if mode not in {"incident", "internal", "cross"}:
            raise ValueError("mode must be 'incident', 'internal', or 'cross'")
        if structure_indices is None:
            coverage = self._coverage
        else:
            requested = _unique_in_order(_indices(
                structure_indices, self.n_structures, "structure_indices"
            ))
            coverage = requested[np.isin(requested, self._coverage)]
        if atom_indices is None and interaction_types is None:
            if structure_indices is None:
                frame_positions = self._positions
            elif self._is_full:
                chunks = []
                for frame in coverage:
                    begin = np.searchsorted(self.occurrence_structures, frame, side="left")
                    end = np.searchsorted(self.occurrence_structures, frame, side="right")
                    chunks.append(np.arange(begin, end, dtype=np.int64))
                frame_positions = (np.concatenate(chunks) if chunks else
                                   np.empty(0, dtype=np.int64))
            else:
                frames = self.occurrence_structures[self._positions]
                positions = self._positions[np.isin(frames, coverage)]
                frame_order = {int(frame): index for index, frame in enumerate(coverage)}
                priorities = np.fromiter(
                    (frame_order[int(frame)]
                     for frame in self.occurrence_structures[positions]),
                    dtype=np.int64,
                )
                frame_positions = positions[np.lexsort((positions, priorities))]
            return self._view(frame_positions, coverage)
        self._build_indexes()
        if atom_indices is None:
            relations = np.arange(len(self.relation_types), dtype=np.int64)
        else:
            atoms = np.unique(_indices(atom_indices, self.n_atoms, "atom_indices"))
            if len(atoms):
                incident = np.unique(np.concatenate(
                    [self._atom_relation_ids[
                        self._atom_relation_offsets[atom]:
                        self._atom_relation_offsets[atom + 1]
                    ] for atom in atoms]
                ))
            else:
                incident = np.empty(0, dtype=np.int64)
            if mode == "incident":
                relations = incident
            else:
                internal = np.asarray(
                    [relation for relation in incident
                     if np.all(np.isin(self._relation_atoms(relation), atoms))],
                    dtype=np.int64,
                )
                relations = internal if mode == "internal" else np.setdiff1d(
                    incident, internal, assume_unique=True
                )
        if interaction_types is not None:
            allowed = ({interaction_types} if isinstance(interaction_types, str)
                       else set(interaction_types))
            relations = relations[[self.relation_types[index] in allowed
                                   for index in relations]]
        if not len(coverage) or not len(relations):
            return self._view([], coverage)
        if structure_indices is not None:
            bounds = [(
                np.searchsorted(self.occurrence_structures, frame, side="left"),
                np.searchsorted(self.occurrence_structures, frame, side="right"),
            ) for frame in coverage]
            frame_count = sum(end - begin for begin, end in bounds)
            relation_count = np.sum(
                self._relation_occurrence_offsets[relations + 1]
                - self._relation_occurrence_offsets[relations]
            )
            if frame_count < relation_count:
                chunks = [np.arange(begin, end, dtype=np.int64)
                          for begin, end in bounds]
                positions = np.concatenate(chunks) if chunks else np.empty(
                    0, dtype=np.int64
                )
                if not self._is_full:
                    positions = positions[np.isin(positions, self._positions)]
                positions = positions[np.isin(
                    self.occurrence_relations[positions], relations
                )]
                return self._view(positions, coverage)
        relevant = np.unique(np.concatenate([
            self._relation_occurrence_ids[
                self._relation_occurrence_offsets[relation]:
                self._relation_occurrence_offsets[relation + 1]
            ] for relation in relations
        ]))
        if structure_indices is None and self._is_full:
            positions = relevant
        elif structure_indices is None:
            positions = self._positions[np.isin(self._positions, relevant)]
        else:
            if not self._is_full:
                relevant = relevant[np.isin(relevant, self._positions)]
            frames = self.occurrence_structures[relevant]
            positions = relevant[np.isin(frames, coverage)]
            frame_order = {int(frame): index for index, frame in enumerate(coverage)}
            priorities = np.fromiter(
                (frame_order[int(frame)]
                 for frame in self.occurrence_structures[positions]),
                dtype=np.int64,
            )
            positions = positions[np.lexsort((positions, priorities))]
        return self._view(positions, coverage)

    def between(self, atom_indices_a, atom_indices_b, structure_indices=None,
                exclusive=False, interaction_types=None):
        """Selecting relations that involve atoms from each disjoint set.

        Parameters
        ----------
        atom_indices_a : array-like of int
            First set of local atom indices.
        atom_indices_b : array-like of int
            Second disjoint set of local atom indices.
        structure_indices : array-like of int or None, default=None
            Structures to inspect; ``None`` uses evaluated structures.
        exclusive : bool, default=False
            Require all relation atoms to belong to the union of both sets.
        interaction_types : iterable of str or None, default=None
            Interaction kinds to retain.

        Returns
        -------
        Interactions
            Selected occurrences and evaluated-frame coverage.

        .. versionadded:: 1.0.0
        """
        a = np.unique(_indices(atom_indices_a, self.n_atoms, "atom_indices_a"))
        b = np.unique(_indices(atom_indices_b, self.n_atoms, "atom_indices_b"))
        if np.intersect1d(a, b).size:
            raise ValueError("atom_indices_a and atom_indices_b must be disjoint")
        candidates = self.query(structure_indices=structure_indices,
                                atom_indices=a, interaction_types=interaction_types)
        relations = np.unique(self.occurrence_relations[candidates._positions])
        allowed = [int(relation) for relation in relations
                   if np.intersect1d(self._relation_atoms(relation), b).size
                   and (not exclusive or np.all(np.isin(
                       self._relation_atoms(relation), np.union1d(a, b)
                   )))]
        if not allowed:
            return candidates._view([], candidates._coverage)
        positions = candidates._positions[np.isin(
            self.occurrence_relations[candidates._positions], allowed
        )]
        return candidates._view(positions, candidates._coverage)

    def to_dict(self):
        """Returning selected occurrence columns and explicit coverage.

        ``occurrence_indices`` are row positions in this complete analysis.
        Queries retain them, including when parallel observations share a
        structure and relation. A remap or edit creates a new analysis with
        newly assigned positions.
        """
        positions = self._positions
        if self.image_vectors is None:
            image_offsets = None
            image_vectors = None
        else:
            lengths = (self.occurrence_image_offsets[positions + 1]
                       - self.occurrence_image_offsets[positions])
            image_offsets = np.r_[0, np.cumsum(lengths)]
            image_vectors = np.concatenate([
                self.image_vectors[
                    self.occurrence_image_offsets[index]:
                    self.occurrence_image_offsets[index + 1]
                ] for index in positions
            ]) if len(positions) else np.empty((0, 3), dtype=np.int32)
        return {
            "n_atoms": self.n_atoms,
            "n_structures": self.n_structures,
            "source_n_atoms": self.source_n_atoms,
            "source_n_structures": self.source_n_structures,
            "source_id": self.source_id,
            "evaluated_structure_indices": self._coverage.copy(),
            "occurrence_indices": positions.copy(),
            "structure_indices": self.occurrence_structures[positions].copy(),
            "relation_indices": self.occurrence_relations[positions].copy(),
            "evidence": np.asarray(self.evidence_labels, dtype=str)[
                self.occurrence_evidence[positions]
            ],
            "measurements": {name: values[positions].copy()
                             for name, values in self.measurements.items()},
            "measure_units": self.measure_units.copy(),
            "image_offsets": image_offsets,
            "image_vectors": image_vectors,
        }

    def remap(self, atom_indices="all", structure_indices="all"):
        """Extracting interactions into new atom and structure index spaces.

        Relations are retained only when every atom of every participant is
        selected. Repeated structure indices create distinct output structures
        and duplicate their occurrences. Evaluated-empty structures remain
        evaluated. Local-to-source maps are composed, retaining the original
        source identity and leaving new local indices explicit.

        Parameters
        ----------
        atom_indices : array-like of int or 'all', default='all'
            Local atoms in their desired output order, without duplicates.
        structure_indices : array-like of int or 'all', default='all'
            Local structures in their desired output order; repeats are allowed.

        Returns
        -------
        Interactions
            Independent sparse result with local atom and structure indices.

        Raises
        ------
        ValueError
            If this is a query view or atom indices repeat.

        .. versionadded:: 1.0.0
        """
        from molsysmt._private.variables import is_all

        if not self._is_full:
            raise ValueError("Remapping requires a full interaction result.")
        atoms = (
            np.arange(self.n_atoms, dtype=np.int64)
            if is_all(atom_indices) else _indices(atom_indices, self.n_atoms, "atom_indices")
        )
        frames = (
            np.arange(self.n_structures, dtype=np.int64)
            if is_all(structure_indices) else
            _indices(structure_indices, self.n_structures, "structure_indices")
        )
        if np.unique(atoms).size != atoms.size:
            raise ValueError("atom_indices must not contain duplicates")

        atom_map = np.full(self.n_atoms, -1, dtype=np.int64)
        atom_map[atoms] = np.arange(atoms.size, dtype=np.int64)
        def mapped_scope(values):
            mapped = atom_map[values]
            return np.unique(mapped[mapped >= 0])

        mapped_universe = mapped_scope(
            self._scope_axis(self.evaluation_universe_indices)
        )
        mapped_selected = mapped_scope(self._scope_selected())
        mapped_b = (
            None if self.evaluation_atom_indices_b is None else
            mapped_scope(self.evaluation_atom_indices_b)
        )
        universe_arg = (
            None if mapped_universe.size == atoms.size else mapped_universe
        )
        selected_arg = (
            None if self.evaluation_mode == "internal"
            and np.array_equal(mapped_selected, mapped_universe)
            else mapped_selected
        )
        mapped_participant_atoms = atom_map[self.participant_atoms]
        relation_map = np.full(len(self.relation_types), -1, dtype=np.int64)
        relation_types = []
        relation_offsets = [0]
        participant_roles = []
        participant_offsets = [0]
        participant_atoms = []
        for old_relation, relation_type in enumerate(self.relation_types):
            first = self.relation_participant_offsets[old_relation]
            last = self.relation_participant_offsets[old_relation + 1]
            if any(np.any(mapped_participant_atoms[
                self.participant_atom_offsets[participant]:
                self.participant_atom_offsets[participant + 1]
            ] < 0) for participant in range(first, last)):
                continue
            relation_map[old_relation] = len(relation_types)
            relation_types.append(relation_type)
            for participant in range(first, last):
                participant_roles.append(self.participant_roles[participant])
                mapped = mapped_participant_atoms[
                    self.participant_atom_offsets[participant]:
                    self.participant_atom_offsets[participant + 1]
                ]
                participant_atoms.extend(mapped)
                participant_offsets.append(len(participant_atoms))
            relation_offsets.append(len(participant_roles))

        coverage_mask = np.zeros(self.n_structures, dtype=np.bool_)
        coverage_mask[self.evaluated_structure_indices] = True
        coverage = np.flatnonzero(coverage_mask[frames]).astype(np.int64)
        position_chunks = []
        frame_chunks = []
        for new_frame, old_frame in enumerate(frames):
            first = np.searchsorted(self.occurrence_structures, old_frame, side="left")
            last = np.searchsorted(self.occurrence_structures, old_frame, side="right")
            selected = np.arange(first, last, dtype=np.int64)
            selected = selected[relation_map[self.occurrence_relations[selected]] >= 0]
            if selected.size:
                position_chunks.append(selected)
                frame_chunks.append(np.full(selected.size, new_frame, dtype=np.int64))
        positions = (
            np.concatenate(position_chunks) if position_chunks else
            np.empty(0, dtype=np.int64)
        )
        occurrence_structures = (
            np.concatenate(frame_chunks) if frame_chunks else
            np.empty(0, dtype=np.int64)
        )
        if self.image_vectors is None:
            image_offsets = None
            image_vectors = None
        else:
            lengths = np.diff(self.occurrence_image_offsets)[positions]
            image_offsets = np.r_[0, np.cumsum(lengths)]
            image_positions = (
                np.arange(image_offsets[-1], dtype=np.int64)
                - np.repeat(image_offsets[:-1], lengths)
                + np.repeat(self.occurrence_image_offsets[positions], lengths)
            )
            image_vectors = self.image_vectors[image_positions].copy()

        return Interactions(
            n_atoms=atoms.size,
            n_structures=frames.size,
            evaluated_structure_indices=coverage,
            relation_types=relation_types,
            relation_participant_offsets=np.asarray(relation_offsets, dtype=np.int64),
            participant_roles=participant_roles,
            participant_atom_offsets=np.asarray(participant_offsets, dtype=np.int64),
            participant_atoms=np.asarray(participant_atoms, dtype=np.int64),
            occurrence_structures=occurrence_structures,
            occurrence_relations=relation_map[self.occurrence_relations[positions]],
            occurrence_evidence=self.occurrence_evidence[positions].copy(),
            evidence_labels=self.evidence_labels,
            measurements={name: values[positions].copy()
                          for name, values in self.measurements.items()},
            measure_units=self.measure_units,
            method=self.method,
            parameters=self.parameters,
            source_id=self.source_id,
            atom_source_indices=self.atom_source_indices[atoms].copy(),
            structure_source_indices=self.structure_source_indices[frames].copy(),
            source_n_atoms=self.source_n_atoms,
            source_n_structures=self.source_n_structures,
            evaluation_mode=self.evaluation_mode,
            evaluation_atom_indices=selected_arg,
            evaluation_atom_indices_b=mapped_b,
            evaluation_universe_indices=universe_arg,
            occurrence_image_offsets=image_offsets,
            image_vectors=image_vectors,
        )

    def invalidate_structures(self, structure_indices):
        """Marking selected structures unevaluated and removing their observations.

        A new result is returned. Its atom and structure index spaces remain
        unchanged, and the source result and existing query views are not
        modified. This operation is appropriate when coordinates or chemical
        context changed and the affected structures need reanalysis.

        Parameters
        ----------
        structure_indices : array-like of int
            Local structure indices whose analysis is no longer valid.

        Returns
        -------
        Interactions
            Independent result with selected structures unevaluated.

        Raises
        ------
        ValueError
            If this is a query view or an index is outside the structure axis.

        Examples
        --------
        >>> from molsysmt import Interactions
        >>> result = Interactions.from_records([], n_atoms=2, n_structures=1,
        ...     evaluated_structure_indices=[0], method="example")
        >>> result.invalidate_structures([0]).evaluated_structure_indices.tolist()
        []

        .. versionadded:: 1.0.0
        """
        if not self._is_full:
            raise ValueError("Invalidation requires a full interaction result")
        frames = np.unique(_indices(
            structure_indices, self.n_structures, "structure_indices"
        ))
        keep_coverage = self.evaluated_structure_indices[
            ~np.isin(self.evaluated_structure_indices, frames)
        ]
        positions = np.flatnonzero(~np.isin(self.occurrence_structures, frames))
        if self.image_vectors is None:
            image_offsets = None
            image_vectors = None
        else:
            lengths = np.diff(self.occurrence_image_offsets)[positions]
            image_offsets = np.r_[0, np.cumsum(lengths)]
            image_positions = (
                np.arange(image_offsets[-1], dtype=np.int64)
                - np.repeat(image_offsets[:-1], lengths)
                + np.repeat(self.occurrence_image_offsets[positions], lengths)
            )
            image_vectors = self.image_vectors[image_positions].copy()
        return Interactions(
            n_atoms=self.n_atoms,
            n_structures=self.n_structures,
            evaluated_structure_indices=keep_coverage.copy(),
            relation_types=self.relation_types,
            relation_participant_offsets=self.relation_participant_offsets.copy(),
            participant_roles=self.participant_roles,
            participant_atom_offsets=self.participant_atom_offsets.copy(),
            participant_atoms=self.participant_atoms.copy(),
            occurrence_structures=self.occurrence_structures[positions].copy(),
            occurrence_relations=self.occurrence_relations[positions].copy(),
            occurrence_evidence=self.occurrence_evidence[positions].copy(),
            evidence_labels=self.evidence_labels,
            measurements={name: value[positions].copy()
                          for name, value in self.measurements.items()},
            measure_units=self.measure_units,
            method=self.method,
            parameters=self.parameters,
            source_id=self.source_id,
            atom_source_indices=self.atom_source_indices.copy(),
            structure_source_indices=self.structure_source_indices.copy(),
            source_n_atoms=self.source_n_atoms,
            source_n_structures=self.source_n_structures,
            evaluation_mode=self.evaluation_mode,
            evaluation_atom_indices=(
                None if self.evaluation_atom_indices is None
                else self.evaluation_atom_indices.copy()
            ),
            evaluation_atom_indices_b=(
                None if self.evaluation_atom_indices_b is None
                else self.evaluation_atom_indices_b.copy()
            ),
            evaluation_universe_indices=(
                None if self.evaluation_universe_indices is None
                else self.evaluation_universe_indices.copy()
            ),
            occurrence_image_offsets=image_offsets,
            image_vectors=image_vectors,
        )

    def save(self, filename):
        """Writing the full result to a versioned standalone HDF5 file."""
        if not self._is_full:
            raise ValueError("save the full result, not a query view")
        import h5py

        with h5py.File(Path(filename), "w") as file:
            self._write_group(file)

    def _write_group(self, group):
        """Write the typed result into one HDF5 file or group."""
        if not self._is_full:
            raise ValueError("write the full result, not a query view")
        import h5py

        group.attrs["format"] = "molsysmt.interactions"
        group.attrs["schema_version"] = 1
        group.attrs["metadata"] = json.dumps({
            "n_atoms": self.n_atoms, "n_structures": self.n_structures,
            "source_n_atoms": self.source_n_atoms,
            "source_n_structures": self.source_n_structures,
            "method": self.method, "parameters": self.parameters,
            "source_id": self.source_id, "measure_units": self.measure_units,
            "evaluation_mode": self.evaluation_mode,
        })
        query_index = group.create_group("query_index")
        query_index.attrs["schema_version"] = 1
        frame_counts = np.bincount(
            self.occurrence_structures, minlength=self.n_structures
        )
        frame_offsets = np.r_[0, np.cumsum(frame_counts, dtype=np.int64)]
        evaluated_mask = np.zeros(self.n_structures, dtype=np.bool_)
        evaluated_mask[self.evaluated_structure_indices] = True
        query_index.create_dataset(
            "frame_offsets", data=frame_offsets,
            compression="gzip" if frame_offsets.size else None,
        )
        query_index.create_dataset(
            "evaluated_mask", data=evaluated_mask,
            compression="gzip" if evaluated_mask.size else None,
        )
        labels = group.create_group("labels")
        string_dtype = h5py.string_dtype(encoding="utf-8")
        for name, values in (
            ("relation_types", self.relation_types),
            ("participant_roles", self.participant_roles),
        ):
            unique = tuple(dict.fromkeys(values))
            lookup = {value: index for index, value in enumerate(unique)}
            codes = np.fromiter((lookup[value] for value in values), dtype=np.uint32)
            labels.create_dataset(
                name, data=np.asarray(unique, dtype=string_dtype),
                compression="gzip" if unique else None,
            )
            group.create_dataset(f"{name}_codes", data=codes,
                                 compression="gzip" if codes.size else None)
        labels.create_dataset("evidence",
                              data=np.asarray(self.evidence_labels, dtype=string_dtype),
                              compression="gzip" if self.evidence_labels else None)
        arrays = {
            "evaluated_structure_indices": self.evaluated_structure_indices,
            "atom_source_indices": self.atom_source_indices,
            "structure_source_indices": self.structure_source_indices,
            "relation_participant_offsets": self.relation_participant_offsets,
            "participant_atom_offsets": self.participant_atom_offsets,
            "participant_atoms": self.participant_atoms,
            "occurrence_structures": self.occurrence_structures,
            "occurrence_relations": self.occurrence_relations,
            "occurrence_evidence": self.occurrence_evidence,
        }
        for name in (
            "evaluation_atom_indices", "evaluation_atom_indices_b",
            "evaluation_universe_indices",
        ):
            value = getattr(self, name)
            if value is not None:
                group.create_dataset(name, data=value,
                                     compression="gzip" if value.size else None)
        if np.array_equal(self.atom_source_indices, np.arange(self.n_atoms)):
            del arrays["atom_source_indices"]
        if np.array_equal(self.structure_source_indices, np.arange(self.n_structures)):
            del arrays["structure_source_indices"]
        for name, value in arrays.items():
            group.create_dataset(name, data=value,
                                 compression="gzip" if value.size else None)
        if self.image_vectors is not None:
            group.create_dataset("occurrence_image_offsets",
                                 data=self.occurrence_image_offsets, compression="gzip")
            group.create_dataset("image_vectors", data=self.image_vectors,
                                 compression="gzip")
        measures = group.create_group("measurements")
        for name, value in self.measurements.items():
            measures.create_dataset(name, data=value,
                                    compression="gzip" if value.size else None)

    @classmethod
    def load(cls, filename):
        """Loading a versioned standalone interaction result into memory."""
        import h5py

        with h5py.File(Path(filename), "r") as file:
            return cls._read_group(file)

    @classmethod
    def _read_group(cls, group):
        """Read one versioned typed result from an HDF5 file or group."""
        if group.attrs.get("format") != "molsysmt.interactions" or group.attrs.get(
            "schema_version"
        ) != 1:
            raise ValueError("unsupported Interactions file format or schema version")
        metadata = json.loads(group.attrs["metadata"])
        evidence_labels = group["labels/evidence"].asstr()[:]
        type_labels = group["labels/relation_types"].asstr()[:]
        role_labels = group["labels/participant_roles"].asstr()[:]
        return cls(
            n_atoms=metadata["n_atoms"], n_structures=metadata["n_structures"],
            source_n_atoms=metadata.get("source_n_atoms", metadata["n_atoms"]),
            source_n_structures=metadata.get(
                "source_n_structures", metadata["n_structures"]
            ),
            atom_source_indices=(
                group["atom_source_indices"][:] if "atom_source_indices" in group
                else None
            ),
            structure_source_indices=(
                group["structure_source_indices"][:]
                if "structure_source_indices" in group else None
            ),
            evaluation_mode=metadata.get("evaluation_mode", "internal"),
            evaluation_atom_indices=(
                group["evaluation_atom_indices"][:]
                if "evaluation_atom_indices" in group else None
            ),
            evaluation_atom_indices_b=(
                group["evaluation_atom_indices_b"][:]
                if "evaluation_atom_indices_b" in group else None
            ),
            evaluation_universe_indices=(
                group["evaluation_universe_indices"][:]
                if "evaluation_universe_indices" in group else None
            ),
            evaluated_structure_indices=group["evaluated_structure_indices"][:],
            relation_types=[type_labels[index]
                            for index in group["relation_types_codes"][:]],
            relation_participant_offsets=group["relation_participant_offsets"][:],
            participant_roles=[role_labels[index]
                               for index in group["participant_roles_codes"][:]],
            participant_atom_offsets=group["participant_atom_offsets"][:],
            participant_atoms=group["participant_atoms"][:],
            occurrence_structures=group["occurrence_structures"][:],
            occurrence_relations=group["occurrence_relations"][:],
            occurrence_evidence=[evidence_labels[index]
                                 for index in group["occurrence_evidence"][:]],
            measurements={name: dataset[:] for name, dataset
                          in group["measurements"].items()},
            measure_units=metadata["measure_units"], method=metadata["method"],
            parameters=metadata["parameters"], source_id=metadata["source_id"],
            occurrence_image_offsets=(
                group["occurrence_image_offsets"][:]
                if "occurrence_image_offsets" in group else None
            ),
            image_vectors=(
                group["image_vectors"][:] if "image_vectors" in group else None
            ),
        )

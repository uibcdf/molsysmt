"""Frame-validity snapshots over immutable interaction columns.

Filtered results retain a single packed base, never a chain of earlier filters.
Queries use its existing postings; complete-column access is an explicit packing
boundary. This module does not implement replacement or an incremental writer.
"""

from contextlib import contextmanager
from copy import deepcopy
from types import MappingProxyType

import numpy as np

from .result import Interactions, _immutable_array, _indices, _unique_in_order


def _metadata(source):
    return {
        "_execution_records": source._execution_records,
        "parameters": deepcopy(source.parameters),
        "measure_units": source.measure_units.copy(),
        "software": source.software.copy(),
        "method": source.method,
        "source_id": deepcopy(source.source_id),
    }


@contextmanager
def _interchange_result(result):
    """Temporarily pack invalidated columns at an interchange boundary."""
    if not isinstance(result, _FrameFilteredInteractions):
        yield result
        return
    previously_packed = result._packed_result is not None
    try:
        yield result._packed()
    finally:
        if not previously_packed:
            result._packed_result = None


def _invalidate(source, frames):
    if hasattr(source, "_segments"):
        from ._frame_replacement import _invalidate_patch

        return _invalidate_patch(source, frames)
    root = source._root if isinstance(source, _FrameFilteredInteractions) else source
    coverage = source.evaluated_structure_indices[
        ~np.isin(source.evaluated_structure_indices, frames)
    ]
    removed = np.sort(
        root.evaluated_structure_indices[
            ~np.isin(root.evaluated_structure_indices, coverage)
        ]
    )
    starts = np.searchsorted(root.occurrence_structures, removed, side="left")
    ends = np.searchsorted(root.occurrence_structures, removed, side="right")
    lengths = ends - starts
    ends = ends[lengths != 0]
    lengths = lengths[lengths != 0]
    count = root.n_interactions - int(lengths.sum())
    if count == 0:
        # Release the occurrence base when no observations survive. Old views
        # can still keep it alive, but this empty result has no such reference.
        result = object.__new__(Interactions)
        result.__dict__ = root.__dict__.copy()
        result.__dict__.update(_metadata(source))
        for name in ("occurrence_structures", "occurrence_relations", "_positions"):
            result.__dict__[name] = _immutable_array(np.empty(0, dtype=np.int64))
        result.__dict__["occurrence_evidence"] = _immutable_array(
            np.empty(0, dtype=np.int32)
        )
        result.__dict__["measurements"] = MappingProxyType(
            {name: _immutable_array(np.empty(0)) for name in root.measurements}
        )
        if root.image_vectors is not None:
            result.__dict__["occurrence_image_offsets"] = _immutable_array(
                np.array([0], dtype=np.int64)
            )
            result.__dict__["image_vectors"] = _immutable_array(
                np.empty((0, 3), dtype=np.int32)
            )
        for name in (
            "_atom_relation_offsets",
            "_atom_relation_ids",
            "_relation_occurrence_offsets",
            "_relation_occurrence_ids",
        ):
            result.__dict__[name] = None
    else:
        result = object.__new__(_FrameFilteredInteractions)
        result.__dict__ = root.__dict__.copy()
        result.__dict__.update(_metadata(source))
        result._root = root
        result._packed_result = None
        result._active_count = count
        result._row_removal = (
            _immutable_array(ends),
            _immutable_array(np.r_[0, np.cumsum(lengths)]),
        )
    result.__dict__["evaluated_structure_indices"] = _immutable_array(coverage)
    result._coverage = result.evaluated_structure_indices
    return result


class _FrameFilteredInteractions(Interactions):
    """A full logical analysis with some packed-base frames unevaluated."""

    @property
    def n_interactions(self):
        return self._active_count

    @property
    def numeric_nbytes(self):
        # Includes referenced shared storage once; this is not incremental RAM.
        arrays = [self.evaluated_structure_indices, *self._row_removal]
        index = getattr(self, "_relation_key_index", None)
        if index is not None and index is not getattr(
            self._root, "_relation_key_index", None
        ):
            arrays.extend(index)
        return (
            self._root.numeric_nbytes
            + sum(value.nbytes for value in arrays)
            + (0 if self._packed_result is None else self._packed_result.numeric_nbytes)
        )

    def _query_frames(self, requested):
        if requested is None:
            return None
        frames = _unique_in_order(
            _indices(requested, self.n_structures, "structure_indices")
        )
        return frames[np.isin(frames, self._coverage)]

    def _project(self, view):
        coverage = view._coverage[np.isin(view._coverage, self._coverage)]
        if view._positions.size:
            valid = np.isin(
                self._root.occurrence_structures[view._positions], self._coverage
            )
            view = view._view(view._positions[valid], coverage)
        else:
            view = view._view([], coverage)
        view._row_removal = self._row_removal
        view._execution_records = self._execution_records
        view.parameters = self.parameters
        view.measure_units = self.measure_units
        view.software = self.software
        view.method = self.method
        view.source_id = self.source_id
        return view

    def query(
        self,
        structure_indices=None,
        atom_indices=None,
        mode="incident",
        interaction_types=None,
    ):
        frames = self._query_frames(structure_indices)
        if (
            structure_indices is None
            and atom_indices is None
            and interaction_types is None
        ):
            view = self._root.query(
                structure_indices=np.sort(self._coverage), mode=mode
            )
            view._coverage = self._coverage
        else:
            view = self._root.query(
                structure_indices=frames,
                atom_indices=atom_indices,
                mode=mode,
                interaction_types=interaction_types,
            )
        return self._project(view)

    def between(
        self,
        atom_indices_a,
        atom_indices_b,
        structure_indices=None,
        exclusive=False,
        interaction_types=None,
    ):
        return self._project(
            self._root.between(
                atom_indices_a,
                atom_indices_b,
                structure_indices=self._query_frames(structure_indices),
                exclusive=exclusive,
                interaction_types=interaction_types,
            )
        )

    def to_dict(self):
        return self.query().to_dict()

    def _packed(self):
        if self._packed_result is None:
            root = self._root
            positions = self.query()._positions
            if root.image_vectors is None:
                offsets = vectors = None
            else:
                lengths = np.diff(root.occurrence_image_offsets)[positions]
                offsets = np.r_[0, np.cumsum(lengths)]
                vectors = np.empty((offsets[-1], 3), dtype=np.int32)
                # Copy contiguous surviving runs, not Python objects per row.
                breaks = np.r_[
                    0, np.flatnonzero(np.diff(positions) != 1) + 1, len(positions)
                ]
                for first, last in zip(breaks[:-1], breaks[1:]):
                    if first == last:
                        continue
                    vectors[offsets[first] : offsets[last]] = root.image_vectors[
                        root.occurrence_image_offsets[
                            positions[first]
                        ] : root.occurrence_image_offsets[positions[last - 1] + 1]
                    ]
            self._packed_result = Interactions(
                n_atoms=self.n_atoms,
                n_structures=self.n_structures,
                source_n_atoms=self.source_n_atoms,
                source_n_structures=self.source_n_structures,
                atom_source_indices=self.atom_source_indices,
                structure_source_indices=self.structure_source_indices,
                evaluated_structure_indices=self._coverage,
                evaluation_mode=self.evaluation_mode,
                evaluation_atom_indices=self.evaluation_atom_indices,
                evaluation_atom_indices_b=self.evaluation_atom_indices_b,
                evaluation_universe_indices=self.evaluation_universe_indices,
                relation_types=self.relation_types,
                relation_participant_offsets=self.relation_participant_offsets,
                participant_roles=self.participant_roles,
                participant_atom_offsets=self.participant_atom_offsets,
                participant_atoms=self.participant_atoms,
                occurrence_structures=root.occurrence_structures[positions],
                occurrence_relations=root.occurrence_relations[positions],
                occurrence_evidence=root.occurrence_evidence[positions],
                evidence_labels=self.evidence_labels,
                measurements={
                    name: values[positions]
                    for name, values in root.measurements.items()
                },
                measure_units=self.measure_units,
                method=self.method,
                parameters=self.parameters,
                software=self.software,
                source_id=self.source_id,
                occurrence_image_offsets=offsets,
                image_vectors=vectors,
                execution_records=self.execution_records,
            )
        # Attribution may be attached after construction. Keep the packed
        # interchange projection consistent with this analysis's metadata.
        self._packed_result.__dict__.update(_metadata(self))
        return self._packed_result

    @property
    def occurrence_structures(self):
        return self._packed().occurrence_structures

    @property
    def occurrence_relations(self):
        return self._packed().occurrence_relations

    @property
    def occurrence_evidence(self):
        return self._packed().occurrence_evidence

    @property
    def occurrence_image_offsets(self):
        return self._packed().occurrence_image_offsets

    @property
    def image_vectors(self):
        return self._packed().image_vectors

    @property
    def measurements(self):
        return self._packed().measurements

    def remap(self, atom_indices="all", structure_indices="all"):
        with _interchange_result(self) as packed:
            return packed.remap(
                atom_indices=atom_indices, structure_indices=structure_indices
            )

    def _write_group(self, group):
        super()._write_group(group)

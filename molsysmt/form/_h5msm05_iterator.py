"""Projecting numeric H5MSM 0.5 structural series into bounded frame blocks."""

import h5py
import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.variables import is_all

from ._h5msm05_structures import (
    _FIELDS,
    _atom_rows,
    _rows,
    _selection,
    _validate_structure_series,
)


class _StructuresIterator05:
    """Own one file handle and read only requested series and atom/frame rows."""

    def __init__(
        self, filename, *, atom_indices="all", structure_indices=None,
        start=0, stop=None, step=1, chunk=1, output_type="values", **attributes,
    ):
        self._file = h5py.File(filename, "r")
        try:
            if self._file.attrs.get("type") != "h5msm" or self._file.attrs.get("version") != "0.5":
                raise ValueError("Expected an H5MSM 0.5 modular file.")
            self._group = self._file["structures"]
            if self._group.attrs.get("schema_version") != 1:
                raise ValueError("Unsupported H5MSM 0.5 structures layer schema.")
            n_frames = int(self._group.attrs["n_structures"])
            n_atoms = int(self._group.attrs["n_atoms"])
            if n_frames < 0 or n_atoms < -1:
                raise ValueError("Invalid structures layer axis cardinality.")
            unknown = set(self._group) - set(_FIELDS) - {"bioassembly", "alternate_location"}
            if unknown:
                raise ValueError(f"Unknown structural series {sorted(unknown)}.")
            for name in set(self._group) & set(_FIELDS):
                _validate_structure_series(self._group, name, n_frames, n_atoms)
            self._attributes = [name for name, enabled in attributes.items() if enabled]
            if set(self._attributes) - {"coordinates", "box", "time", "structure_id"}:
                raise ValueError("The H5MSM 0.5 iterator supports coordinates, box, time, and structure_id.")
            indices = (
                np.arange(n_frames, dtype=np.int64)
                if structure_indices is None or is_all(structure_indices)
                else _selection(structure_indices, n_frames, "structure_indices")
            )
            self._frames = indices[slice(start, stop, step)]
            self._atoms = (
                None if is_all(atom_indices)
                else _selection(atom_indices, n_atoms, "atom_indices")
            )
            if not isinstance(chunk, int) or chunk < 1:
                raise ValueError("H5MSM 0.5 iterator chunk must be a positive integer.")
            if output_type not in {"values", "dictionary"}:
                raise ValueError("Unsupported structural iterator output type.")
            self._chunk = chunk
            self._output_type = output_type
            self._offset = 0
        except Exception:
            self._file.close()
            raise

    def __iter__(self):
        return self

    def __next__(self):
        if self._offset >= len(self._frames):
            self._file.close()
            raise StopIteration
        frames = self._frames[self._offset:self._offset + self._chunk]
        self._offset += len(frames)
        result = {}
        for name in self._attributes:
            if name not in self._group:
                result[name] = None
                continue
            dataset = self._group[name]
            values = (
                _atom_rows(dataset, frames, self._atoms)
                if name == "coordinates" and self._atoms is not None
                else _rows(dataset, frames)
            )
            if name == "structure_id" and dataset.attrs.get("value_kind") == "string":
                values = np.asarray([
                    value.decode("utf-8") if isinstance(value, bytes) else str(value)
                    for value in values
                ], dtype=object)
            unit = _FIELDS[name][1]
            result[name] = values if unit is None else puw.quantity(values, unit)
        if self._output_type == "dictionary":
            return result
        values = list(result.values())
        return values[0] if len(values) == 1 else values

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._file.close()
        return False

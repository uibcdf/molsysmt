"""Sharing PDBQT structure iteration without changing the universal Iterator."""

import numpy as np

from molsysmt._private.indices import indices_iterator
from molsysmt._private.smonitor import ArgumentError

STRUCTURAL = {
    "coordinates",
    "occupancy",
    "b_factor",
    "structure_id",
    "structure_index",
    "n_structures",
}


class PDBQTStructuresIterator:
    def __init__(
        self,
        molecular_system,
        atom_indices,
        start,
        stop,
        step,
        chunk,
        structure_indices,
        output_type,
        kwargs,
    ):
        from molsysmt.native import PDBQTFileHandler

        self._owns = not isinstance(molecular_system, PDBQTFileHandler)
        self._handler = (
            molecular_system if not self._owns else PDBQTFileHandler(molecular_system)
        )
        self._closed = False
        try:
            self.arguments = [key for key, value in kwargs.items() if value]
            for key, value in kwargs.items():
                if key not in STRUCTURAL or not isinstance(value, bool):
                    raise ArgumentError(
                        key, value=value, caller="PDBQT StructuresIterator"
                    )
            if not self.arguments:
                self.arguments = ["coordinates"]
            if output_type not in {"values", "dictionary"}:
                raise ArgumentError(
                    "output_type", value=output_type, caller="PDBQT StructuresIterator"
                )
            if chunk < 1 or step < 1 or start < 0:
                raise ArgumentError(
                    "chunk/step/start", caller="PDBQT StructuresIterator"
                )
            self.atom_indices = self._handler._axis(
                atom_indices, self._handler.n_atoms, "atom_indices"
            )
            structures = self._handler._axis(
                structure_indices, self._handler.n_structures, "structure_indices"
            )
            self._indices = indices_iterator(
                structures, start=start, stop=stop, step=step, chunk=chunk
            )
            self._output_type = output_type
        except BaseException:
            self._close()
            raise

    @property
    def closed(self):
        """Report whether further blocks can be requested from this iterator."""
        return self._closed

    def _close(self):
        if not self._closed:
            self._closed = True
            self._indices = None
            if self._owns:
                self._handler.close()

    def __iter__(self):
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._close()
        return False

    def __next__(self):
        if self._closed:
            raise StopIteration
        try:
            structures = np.asarray(next(self._indices), dtype=np.int64)
            output = self._handler._block(self.arguments, self.atom_indices, structures)
            if self._output_type == "dictionary":
                return output
            values = list(output.values())
            return values[0] if len(values) == 1 else values
        except BaseException:
            self._close()
            raise

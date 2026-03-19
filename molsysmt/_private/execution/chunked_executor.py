"""
ChunkedExecutor: orchestrates chunked heavy trajectory processing.

Responsibilities:
- Pre-flight footprint estimate
- Eager/heavy decision (emits SMonitor telemetry)
- Storage budget check for disk-backed outputs
- Sequential chunk loop calling a Reducer
- Does NOT own scientific logic
"""
from __future__ import annotations

import time

import numpy as np


class ChunkedExecutor:
    """
    Orchestrates chunked (heavy) or eager trajectory processing.

    Parameters
    ----------
    molecular_system : object
        The source molecular system (any MolSysMT form).
    form : str
        Form name string (e.g. 'file:xtc', 'molsysmt.H5MSMFileHandler').
    operation : str
        Name of the analysis operation (for telemetry).
    reducer : Reducer
        A Reducer instance that accumulates chunk results.
    atom_indices : array-like or 'all'
        Atom selection.
    structure_indices : array-like or None
        Frame selection.
    chunk_size : int or None
        Frames per chunk. None uses molsysmt.config.chunk_size.
    heavy_mode : str
        'auto' | 'force' | 'off'
    """

    def __init__(
        self,
        molecular_system,
        form: str,
        operation: str,
        reducer,
        atom_indices='all',
        structure_indices=None,
        chunk_size: int | None = None,
        heavy_mode: str = 'auto',
        attributes: list | None = None,
    ):
        self.molecular_system = molecular_system
        self.form = form
        self.operation = operation
        self.reducer = reducer
        self.atom_indices = atom_indices
        self.structure_indices = structure_indices
        self.heavy_mode = heavy_mode
        # Attributes to request from StructuresIterator per chunk.
        # Defaults to coordinates only; callers may add 'box', 'time', 'structure_id'.
        self.attributes = attributes if attributes is not None else ['coordinates']

        import molsysmt.config as config
        self.chunk_size = chunk_size if chunk_size is not None else config.chunk_size

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    def execute(self):
        """
        Run the analysis. Returns the reducer's final result.
        Chooses eager or heavy path based on footprint and heavy_mode.
        """
        from .memory_policy import estimate_footprint, decide_mode
        from molsysmt._private.smonitor import info

        n_atoms, n_structures = self._get_dimensions()
        footprint = estimate_footprint(n_atoms, n_structures)
        mode = decide_mode(footprint, self.heavy_mode)

        import molsysmt.config as config

        if mode == 'heavy':
            info("HeavyPathSelected", extra={
                "operation": self.operation,
                "form": self.form,
                "footprint_bytes": footprint,
                "max_ram_usage": config.max_ram_usage,
            })
            return self._execute_heavy(n_atoms, n_structures)
        else:
            info("EagerPathAccepted", extra={
                "operation": self.operation,
                "footprint_bytes": footprint,
            })
            return self._execute_eager()

    # ------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------

    def _get_dimensions(self):
        """Return (n_atoms, n_structures) from the molecular system."""
        from molsysmt.basic import get
        n_atoms = get(self.molecular_system, element='system', n_atoms=True)
        n_structures = get(self.molecular_system, element='system', n_structures=True)
        return int(n_atoms), int(n_structures)

    def _get_form_iterator(self, chunk_size):
        """
        Instantiate the form's StructuresIterator directly (internal API).

        ChunkedExecutor is internal code — it bypasses the public msm.Iterator
        and uses the form's StructuresIterator with already-resolved atom_indices.
        """
        from molsysmt.form import _dict_modules
        form_module = _dict_modules[self.form]
        attr_kwargs = {attr: True for attr in self.attributes}
        return form_module.StructuresIterator(
            self.molecular_system,
            atom_indices=self.atom_indices,
            structure_indices=self.structure_indices,
            chunk=chunk_size,
            output_type='dictionary',
            skip_digestion=True,
            **attr_kwargs,
        )

    def _execute_heavy(self, n_atoms, n_structures):
        """Run the chunked processing loop using the form's StructuresIterator."""
        from molsysmt._private.smonitor import SlowChunkIOWarning, CorruptFrameSkippedWarning
        import warnings
        import molsysmt.config as config

        metadata = {
            'n_atoms': n_atoms,
            'n_structures': n_structures,
            'operation': self.operation,
            'form': self.form,
            'atom_indices': self.atom_indices,
            'structure_indices': self.structure_indices,
        }
        self.reducer.initialize(metadata)

        chunk_index = 0
        with self._get_form_iterator(self.chunk_size) as it:
            for raw_chunk in it:
                t0 = time.perf_counter()

                try:
                    chunk = self._build_chunk(raw_chunk)
                    self.reducer.consume(chunk)
                except Exception as exc:
                    if config.emit_heavy_telemetry:
                        warnings.warn(CorruptFrameSkippedWarning(
                            chunk_index=chunk_index,
                            frame_index=chunk_index * self.chunk_size,
                            reason=str(exc),
                        ))
                    chunk_index += 1
                    continue

                elapsed = time.perf_counter() - t0
                if config.emit_heavy_telemetry and elapsed > 5.0:
                    warnings.warn(SlowChunkIOWarning(
                        chunk_index=chunk_index,
                        io_time_s=elapsed,
                    ))

                chunk_index += 1

        return self.reducer.finalize()

    def _execute_eager(self):
        """
        Eager path using a single full chunk via the form's StructuresIterator.
        Available for parity testing (heavy_mode='force' on small data).
        """
        n_atoms, n_structures = self._get_dimensions()
        self.reducer.initialize({
            'n_atoms': n_atoms,
            'n_structures': n_structures,
            'operation': self.operation,
        })

        with self._get_form_iterator(n_structures) as it:
            for raw_chunk in it:
                chunk = self._build_chunk(raw_chunk)
                self.reducer.consume(chunk)

        return self.reducer.finalize()

    @staticmethod
    def _build_chunk(raw_chunk: dict) -> dict:
        """
        Convert the raw iterator output dict into a standardized chunk dict
        with pure float64 numpy arrays in canonical units (nm, ps).

        The chunk is immutable by contract — reducers must not modify it.
        """
        from molsysmt import pyunitwizard as puw
        import numpy as np

        def _to_float64(q):
            if q is None:
                return None
            val = puw.get_value(q)
            return np.asarray(val, dtype=np.float64)

        coords = _to_float64(raw_chunk.get('coordinates'))
        box = _to_float64(raw_chunk.get('box'))
        time_ = _to_float64(raw_chunk.get('time'))
        structure_id = raw_chunk.get('structure_id')

        chunk = {
            'coordinates': coords,
            'box': box,
            'time': time_,
            'structure_indices': np.asarray(structure_id) if structure_id is not None else None,
        }
        # Make arrays read-only
        for key, arr in chunk.items():
            if isinstance(arr, np.ndarray):
                arr.flags.writeable = False

        return chunk

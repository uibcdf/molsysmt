"""
ChunkedExecutor: orchestrates chunked heavy trajectory processing.

Responsibilities:
- Pre-flight footprint estimate
- Eager/heavy decision (emits SMonitor telemetry)
- Heavy-support validation per form
- Storage budget check for disk-backed outputs (via PersistentResultHandle)
- Multi-reducer single-pass support
- Sequential chunk loop calling one or more Reducers
- Progress telemetry (MSM-INFO-HVY-003)
- Checkpoint / resume
- Does NOT own scientific logic
"""
from __future__ import annotations

import time

import numpy as np

from molsysmt._private.smonitor import ArgumentError, ArgumentConflictError


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
    reducer : Reducer or None
        A single Reducer instance.  execute() returns a single value.
        Mutually exclusive with *reducers*.
    reducers : list[Reducer] or None
        Multiple Reducer instances for read-once / analyze-many.
        execute() returns a list of results in the same order.
        Mutually exclusive with *reducer*.
    atom_indices : array-like or 'all'
        Atom selection.
    structure_indices : array-like or None
        Frame selection.
    chunk_size : int or None
        Frames per chunk. None uses molsysmt.configure.chunk_size.
    heavy_mode : str
        'auto' | 'force' | 'off'
    attributes : list or None
        Attributes to request per chunk (default: ['coordinates']).
    checkpoint_interval : int
        Save a checkpoint every N completed chunks (0 = disabled).
    checkpoint_path : str or Path or None
        Directory or file path for checkpoint output.
        If a directory, files are named automatically.
    restore_from : str or Path or None
        Path to a previously saved checkpoint file to resume from.
    output_path : str or Path or None
        If provided, the PersistentResultHandle (when created) will write to
        this path instead of a temporary file. The file is NOT deleted on
        cleanup(), giving the caller full lifecycle control.
        If None (default), a temporary file is used and deleted on cleanup().
    """

    def __init__(
        self,
        molecular_system,
        form: str,
        operation: str,
        reducer=None,
        reducers=None,
        atom_indices='all',
        structure_indices=None,
        chunk_size: int | None = None,
        heavy_mode: str = 'auto',
        attributes: list | None = None,
        checkpoint_interval: int = 0,
        checkpoint_path=None,
        restore_from=None,
        output_path=None,
    ):
        self.molecular_system = molecular_system
        self.form = form
        self.operation = operation
        self.atom_indices = atom_indices
        self.structure_indices = structure_indices
        self.heavy_mode = heavy_mode
        self.attributes = attributes if attributes is not None else ['coordinates']
        self.checkpoint_interval = checkpoint_interval
        self.checkpoint_path = checkpoint_path
        self.restore_from = restore_from
        self.output_path = output_path

        import molsysmt.configure as config
        self.chunk_size = chunk_size if chunk_size is not None else config.chunk_size

        # Normalize reducer(s) to an internal list
        if reducer is not None and reducers is not None:
            raise ArgumentConflictError(arg1='reducer', arg2='reducers',
                                         reason='Specify either reducer or reducers, not both.',
                                         caller='molsysmt._private.execution.ChunkedExecutor.__init__')
        if reducer is not None:
            self._reducers = [reducer]
            self._single = True
        elif reducers is not None:
            self._reducers = list(reducers)
            self._single = False
        else:
            raise ArgumentError(argument='reducer / reducers',
                                 caller='molsysmt._private.execution.ChunkedExecutor.__init__',
                                 message="Must provide 'reducer' or 'reducers'.")

        # Backward-compat alias for callers that access .reducer directly
        self.reducer = self._reducers[0] if self._single else None

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    def execute(self):
        """
        Run the analysis. Returns the reducer's final result.

        Returns the single result when constructed with *reducer*, or a list
        of results (same order as *reducers*) when constructed with *reducers*.

        Chooses eager or heavy path based on footprint and heavy_mode.
        Raises UnsupportedHeavyOperationError if heavy path is needed but unavailable.
        """
        from .memory_policy import estimate_footprint, decide_mode
        from molsysmt._private.smonitor import info, UnsupportedHeavyOperationError
        from molsysmt.form import _dict_modules

        n_atoms, n_structures = self._get_dimensions()
        footprint = estimate_footprint(n_atoms, n_structures)
        mode = decide_mode(footprint, self.heavy_mode)

        import molsysmt.configure as config

        if mode == 'heavy':
            # Validate that the form supports heavy mode for all requested attributes
            form_module = _dict_modules.get(self.form)
            heavy_support = getattr(form_module, '_heavy_support', {})
            for attr in self.attributes:
                if not heavy_support.get(attr, False):
                    raise UnsupportedHeavyOperationError(
                        operation=self.operation,
                        form=self.form,
                        reason=f"Form does not support heavy mode for attribute '{attr}'",
                    )

            # --- Footprint-Aware Heuristic chunk size optimization ---
            n_structures_selected = len(self.structure_indices) if self.structure_indices is not None else n_structures
            from .memory_policy import optimize_chunk_size
            advisory_chunk_size = self.chunk_size
            self.chunk_size = optimize_chunk_size(
                n_atoms=n_atoms,
                n_structures_selected=n_structures_selected,
                advisory_chunk_size=advisory_chunk_size,
                max_ram_usage=config.max_ram_usage,
                chunk_memory_fraction=config.chunk_memory_fraction,
            )

            info("HeavyPathSelected", extra={
                "operation": self.operation,
                "form": self.form,
                "footprint_bytes": footprint,
                "max_ram_usage": config.max_ram_usage,
                "advisory_chunk_size": advisory_chunk_size,
                "optimized_chunk_size": self.chunk_size,
            })
            return self._execute_heavy(n_atoms, n_structures)
        else:
            info("EagerPathAccepted", extra={
                "operation": self.operation,
                "footprint_bytes": footprint,
            })
            return self._execute_eager(n_atoms, n_structures)

    # ------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------

    def _get_dimensions(self):
        """Return (n_atoms, n_structures) from the molecular system."""
        from molsysmt.basic import get
        n_atoms = get(self.molecular_system, element='system', n_atoms=True)
        n_structures = get(self.molecular_system, element='system', n_structures=True)
        return int(n_atoms), int(n_structures)

    def _get_form_iterator(self, structure_indices, chunk_size):
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
            structure_indices=structure_indices,
            chunk=chunk_size,
            output_type='dictionary',
            skip_digestion=True,
            **attr_kwargs,
        )

    def _execute_heavy(self, n_atoms, n_structures):
        """Run the chunked processing loop using the form's StructuresIterator."""
        from .memory_policy import check_disk_budget
        from .persistent_result import PersistentResultHandle
        from molsysmt._private.smonitor import (
            SlowChunkIOWarning, MemoryPressureWarning, info,
        )
        import warnings
        import molsysmt.configure as config

        _EMA_ALPHA = 0.3   # exponential moving-average weight for ETA

        n_chunks = max(1, int(np.ceil(n_structures / self.chunk_size)))

        # --- Checkpoint / resume: determine starting chunk ---
        start_chunk = 0
        if self.restore_from is not None:
            ckpt = self._load_checkpoint(self.restore_from)
            start_chunk = ckpt['chunk_index'] + 1
            for i, reducer in enumerate(self._reducers):
                reducer.restore(ckpt['reducer_states'][i])

        # Adjust structure_indices to skip already-processed frames
        structure_indices = self.structure_indices
        if start_chunk > 0:
            frames_to_skip = start_chunk * self.chunk_size
            if structure_indices is None:
                structure_indices = list(range(frames_to_skip, n_structures))
            else:
                structure_indices = list(structure_indices)[frames_to_skip:]
            n_chunks_active = max(1, int(np.ceil(len(structure_indices) / self.chunk_size)))
        else:
            n_chunks_active = n_chunks

        # n_structures to process may be smaller than total when structure_indices is a subset
        if structure_indices is None:
            n_structures_selected = n_structures
        else:
            n_structures_selected = len(structure_indices)

        # --- Build shared base metadata ---
        base_metadata = {
            'n_atoms': n_atoms,
            'n_structures': n_structures_selected,
            'n_structures_total': n_structures,
            'n_chunks': n_chunks_active,
            'operation': self.operation,
            'form': self.form,
            'atom_indices': self.atom_indices,
            'structure_indices': structure_indices,
        }

        # --- Initialize reducers; create PersistentResultHandle when requested ---
        handles = []
        for reducer in self._reducers:
            meta = dict(base_metadata)
            shape = reducer.estimate_output_shape(meta)
            if shape is not None:
                nbytes = int(np.prod(shape)) * np.dtype(np.float64).itemsize
                check_disk_budget(nbytes)
                handle = PersistentResultHandle(shape, path=self.output_path)
                handles.append(handle)
                meta['output_handle'] = handle
            else:
                handles.append(None)
            if start_chunk == 0:
                # Fresh run: initialize clears any previous state
                reducer.initialize(meta)
            # else: state already restored by reducer.restore(); skip initialize

        chunk_index = start_chunk
        t_ema = None   # exponential moving average of per-chunk elapsed time
        memory_pressure_active = False

        with self._get_form_iterator(structure_indices, self.chunk_size) as it:
            for raw_chunk in it:
                t0 = time.perf_counter()

                chunk = self._build_chunk(raw_chunk)
                for reducer in self._reducers:
                    reducer.consume(chunk)

                elapsed = time.perf_counter() - t0

                if config.emit_heavy_telemetry:
                    # Slow I/O warning
                    if elapsed > 5.0:
                        warnings.warn(SlowChunkIOWarning(
                            chunk_index=chunk_index,
                            io_time_s=elapsed,
                        ))

                    # Adaptive ETA via exponential moving average
                    if t_ema is None:
                        t_ema = elapsed
                    else:
                        t_ema = _EMA_ALPHA * elapsed + (1.0 - _EMA_ALPHA) * t_ema

                    chunks_remaining = n_chunks - chunk_index - 1
                    eta_s = t_ema * chunks_remaining

                    # Progress telemetry (MSM-INFO-HVY-003)
                    info("ChunkProcessed", extra={
                        "operation": self.operation,
                        "chunk_index": chunk_index,
                        "n_chunks": n_chunks,
                        "elapsed_s": round(elapsed, 4),
                        "eta_s": round(eta_s, 1),
                    })

                    # Memory pressure telemetry (MSM-WARN-HVY-003)
                    try:
                        import psutil as _psutil
                        rss = _psutil.Process().memory_info().rss
                        pressure = rss / config.max_ram_usage
                        if pressure > config.memory_pressure_threshold and not memory_pressure_active:
                            warnings.warn(MemoryPressureWarning(
                                chunk_index=chunk_index,
                                rss_bytes=rss,
                                budget_bytes=config.max_ram_usage,
                                pressure_pct=round(pressure * 100, 1),
                            ))
                            memory_pressure_active = True
                        elif pressure <= config.memory_pressure_threshold:
                            memory_pressure_active = False
                    except ImportError:
                        pass  # psutil not installed; skip RSS check

                # Checkpoint (after successful consume)
                if (self.checkpoint_interval > 0
                        and self.checkpoint_path is not None
                        and (chunk_index + 1) % self.checkpoint_interval == 0):
                    self._save_checkpoint(chunk_index)

                chunk_index += 1

        results = [r.finalize() for r in self._reducers]
        return results[0] if self._single else results

    def _execute_eager(self, n_atoms, n_structures):
        """
        Eager path: load all frames in a single chunk via the form's StructuresIterator.
        Used when heavy_mode='off' or footprint is within RAM budget.
        """
        meta = {
            'n_atoms': n_atoms,
            'n_structures': n_structures,
            'n_chunks': 1,
            'operation': self.operation,
        }
        for reducer in self._reducers:
            reducer.initialize(dict(meta))

        with self._get_form_iterator(self.structure_indices, n_structures) as it:
            for raw_chunk in it:
                chunk = self._build_chunk(raw_chunk)
                for reducer in self._reducers:
                    reducer.consume(chunk)

        results = [r.finalize() for r in self._reducers]
        return results[0] if self._single else results

    def _save_checkpoint(self, chunk_index: int) -> None:
        """Serialize all reducer states to a checkpoint file."""
        import pickle
        from pathlib import Path

        states = [reducer.checkpoint() for reducer in self._reducers]
        ckpt = {'chunk_index': chunk_index, 'reducer_states': states}

        path = Path(self.checkpoint_path)
        if path.is_dir():
            path = path / f'checkpoint_{self.operation}_{chunk_index:06d}.pkl'
        with open(path, 'wb') as f:
            pickle.dump(ckpt, f)

    @staticmethod
    def _load_checkpoint(path) -> dict:
        """Load a checkpoint file produced by _save_checkpoint."""
        import pickle
        with open(path, 'rb') as f:
            return pickle.load(f)

    @staticmethod
    def _build_chunk(raw_chunk: dict) -> dict:
        """
        Convert the raw iterator output dict into a standardized chunk dict
        with pure float64 numpy arrays in canonical units (nm, ps).

        The chunk is immutable by contract — reducers must not modify it.
        """
        from molsysmt import pyunitwizard as puw

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
        for arr in chunk.values():
            if isinstance(arr, np.ndarray):
                arr.flags.writeable = False

        return chunk

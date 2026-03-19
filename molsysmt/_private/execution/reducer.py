"""
Reducer protocol for chunked heavy trajectory processing.

A Reducer accumulates partial results from chunks and produces
a final result when all chunks have been consumed.
"""
from __future__ import annotations
from abc import ABC, abstractmethod


class Reducer(ABC):
    """
    Base class for chunked analysis reducers.

    Subclasses must implement initialize(), consume(), and finalize().
    The remaining methods (estimate_output_shape, checkpoint, restore, merge)
    are optional extensions — override them to enable the corresponding features.

    Lifecycle
    ---------
    1. reducer.initialize(metadata)      — called once before the chunk loop
    2. reducer.consume(chunk) × N        — called once per chunk (read-only chunk)
    3. result = reducer.finalize()       — called once after all chunks

    Contract
    --------
    - Chunks are read-only numpy float64 arrays in canonical units (nm, ps).
    - Persistent cross-chunk state belongs in the reducer, not in closures.
    - finalize() may return an in-memory array or a PersistentResultHandle.

    Optional extensions
    -------------------
    estimate_output_shape(metadata)
        Return the shape of the final output so ChunkedExecutor can decide
        whether to back it with a PersistentResultHandle. Return None to always
        accumulate in RAM.

    checkpoint() / restore(state)
        Serialize / deserialize the reducer's accumulated state so that
        ChunkedExecutor can save progress and resume after interruption.

    merge(other)
        Combine another reducer's partial state into self, enabling parallel
        reduction: run N reducers on N trajectory segments independently, then
        merge in the correct frame order.
    """

    @abstractmethod
    def initialize(self, metadata: dict) -> None:
        """
        Prepare accumulation state.

        Parameters
        ----------
        metadata : dict
            May include: n_atoms, n_structures, n_chunks, operation, form,
            atom_indices, structure_indices. If ChunkedExecutor created a
            PersistentResultHandle for the output, it is available as
            metadata['output_handle'].
        """

    @abstractmethod
    def consume(self, chunk: dict) -> None:
        """
        Process one chunk.

        Parameters
        ----------
        chunk : dict
            Keys: 'coordinates' (np.ndarray float64, nm, shape (n_chunk, n_atoms, 3)),
                  'box' (np.ndarray float64, nm, shape (n_chunk, 3, 3) or None),
                  'time' (np.ndarray float64, ps, shape (n_chunk,) or None),
                  'structure_indices' (np.ndarray int, global frame indices).
            All arrays are read-only views — do not mutate.
        """

    @abstractmethod
    def finalize(self):
        """
        Return the final result after all chunks have been consumed.

        Returns
        -------
        result : np.ndarray or PersistentResultHandle
        """

    # ------------------------------------------------------------------
    # Optional extensions
    # ------------------------------------------------------------------

    def estimate_output_shape(self, metadata: dict):
        """
        Return the shape of the final output array.

        Override to let ChunkedExecutor decide whether to back the output
        with a PersistentResultHandle instead of in-RAM accumulation.

        Returns None by default (always accumulate in RAM).
        """
        return None

    def checkpoint(self) -> dict | None:
        """
        Return a serializable state dict for checkpoint/resume.

        Returns None by default (checkpointing not supported).
        Override to enable ChunkedExecutor checkpointing.
        """
        return None

    def restore(self, state: dict) -> None:
        """
        Restore accumulated state from a checkpoint dict.

        Must be consistent with checkpoint().
        Raises NotImplementedError by default.
        """
        raise NotImplementedError(
            f"{type(self).__name__} does not implement restore(). "
            "Override checkpoint() and restore() to enable checkpoint/resume."
        )

    def merge(self, other: 'Reducer') -> None:
        """
        Merge another reducer's partial state into self.

        Used for parallel reduction: run N reducers on N trajectory segments
        independently, then merge them in frame order.
        The caller is responsible for merging in the correct temporal order
        (earlier frames first).

        Raises NotImplementedError by default.
        """
        raise NotImplementedError(
            f"{type(self).__name__} does not implement merge(). "
            "Override merge() to enable parallel reduction."
        )

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
    """

    @abstractmethod
    def initialize(self, metadata: dict) -> None:
        """
        Prepare accumulation state.

        Parameters
        ----------
        metadata : dict
            May include: n_atoms, n_structures (if known), operation,
            atom_indices, structure_indices.
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

"""
Tests for the Reducer base protocol using a simple CollectorReducer.
"""
import pytest
import numpy as np
from molsysmt._private.execution import Reducer


class CollectorReducer(Reducer):
    """Simple reducer that concatenates coordinate arrays."""

    def initialize(self, metadata):
        self.chunks = []
        self.n_atoms = metadata.get('n_atoms')

    def consume(self, chunk):
        self.chunks.append(chunk['coordinates'].copy())

    def finalize(self):
        return np.concatenate(self.chunks, axis=0)


def _make_chunk(n_structures, n_atoms):
    coords = np.random.rand(n_structures, n_atoms, 3).astype(np.float64)
    coords.flags.writeable = False
    return {
        'coordinates': coords,
        'box': None,
        'time': None,
        'structure_indices': np.arange(n_structures),
    }


def test_reducer_lifecycle():
    reducer = CollectorReducer()
    reducer.initialize({'n_atoms': 10, 'n_structures': 30})

    for i in range(3):
        chunk = _make_chunk(10, 10)
        reducer.consume(chunk)

    result = reducer.finalize()
    assert result.shape == (30, 10, 3)
    assert result.dtype == np.float64


def test_reducer_chunk_is_readonly():
    """Chunks delivered to reducers must be read-only."""
    reducer = CollectorReducer()
    reducer.initialize({'n_atoms': 5})

    chunk = _make_chunk(5, 5)
    assert not chunk['coordinates'].flags.writeable


def test_reducer_is_abstract():
    with pytest.raises(TypeError):
        Reducer()

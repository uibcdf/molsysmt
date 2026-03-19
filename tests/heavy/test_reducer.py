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


def test_reducer_checkpoint_default_returns_none():
    """Default Reducer.checkpoint() must return None."""
    reducer = CollectorReducer()
    reducer.initialize({'n_atoms': 5, 'n_structures': 10})
    reducer.consume(_make_chunk(5, 5))
    assert reducer.checkpoint() is None


def test_reducer_restore_raises_by_default():
    """Default Reducer.restore() must raise NotImplementedError."""
    reducer = CollectorReducer()
    reducer.initialize({'n_atoms': 5, 'n_structures': 10})
    with pytest.raises(NotImplementedError):
        reducer.restore({})


def test_reducer_merge_raises_by_default():
    """Default Reducer.merge() must raise NotImplementedError."""
    r1 = CollectorReducer()
    r2 = CollectorReducer()
    with pytest.raises(NotImplementedError):
        r1.merge(r2)


def test_reducer_estimate_output_shape_default_returns_none():
    """Default Reducer.estimate_output_shape() must return None."""
    reducer = CollectorReducer()
    assert reducer.estimate_output_shape({'n_atoms': 10, 'n_structures': 5}) is None


class CheckpointableReducer(Reducer):
    """Reducer that supports checkpoint/restore/merge."""

    def initialize(self, metadata):
        self.chunks = []

    def consume(self, chunk):
        self.chunks.append(chunk['coordinates'].copy())

    def finalize(self):
        return np.concatenate(self.chunks, axis=0)

    def checkpoint(self):
        return {'chunks': [c.tolist() for c in self.chunks]}

    def restore(self, state):
        self.chunks = [np.array(c) for c in state['chunks']]

    def merge(self, other):
        self.chunks.extend(other.chunks)


def test_reducer_checkpoint_restore_roundtrip():
    """checkpoint() → restore() must reproduce identical partial state."""
    r = CheckpointableReducer()
    r.initialize({'n_atoms': 4, 'n_structures': 8})
    for _ in range(3):
        r.consume(_make_chunk(4, 4))

    state = r.checkpoint()
    r2 = CheckpointableReducer()
    r2.initialize({'n_atoms': 4, 'n_structures': 8})
    r2.restore(state)

    result1 = r.finalize()
    result2 = r2.finalize()
    np.testing.assert_array_equal(result1, result2)


def test_reducer_merge():
    """merge() must combine two partial reducers in frame order."""
    r1 = CheckpointableReducer()
    r1.initialize({'n_atoms': 4, 'n_structures': 8})
    chunk_a = _make_chunk(4, 4)
    r1.consume(chunk_a)

    r2 = CheckpointableReducer()
    r2.initialize({'n_atoms': 4, 'n_structures': 8})
    chunk_b = _make_chunk(4, 4)
    r2.consume(chunk_b)

    r1.merge(r2)
    result = r1.finalize()
    assert result.shape == (8, 4, 3)
    np.testing.assert_array_equal(result[:4], chunk_a['coordinates'])
    np.testing.assert_array_equal(result[4:], chunk_b['coordinates'])

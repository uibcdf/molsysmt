"""
Tests for PersistentResultHandle disk-backed output.
"""
import pytest
import numpy as np
from molsysmt._private.execution import PersistentResultHandle


def test_persistent_result_write_read():
    shape = (100, 50, 3)
    with PersistentResultHandle(shape) as handle:
        data = np.random.rand(*shape).astype(np.float64)
        handle[:] = data
        result = handle.to_memory()
        np.testing.assert_allclose(result, data)


def test_persistent_result_cleanup():
    shape = (10, 5, 3)
    handle = PersistentResultHandle(shape)
    path = handle.path
    assert path.exists()
    handle.cleanup()
    assert not path.exists()


def test_persistent_result_context_manager():
    shape = (20, 10, 3)
    with PersistentResultHandle(shape) as handle:
        path = handle.path
        assert path.exists()
    assert not path.exists()

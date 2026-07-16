"""Tests for fail-fast heavy-execution behavior."""

from types import SimpleNamespace
import warnings

import numpy as np
import pytest

from molsysmt._private.execution import ChunkedExecutor, Reducer
from molsysmt._private.smonitor import MemoryPressureWarning


class _Iterator:
    def __init__(self, chunks):
        self._chunks = chunks

    def __enter__(self):
        return iter(self._chunks)

    def __exit__(self, exc_type, exc_value, traceback):
        return False


class _RecordingReducer(Reducer):
    def initialize(self, metadata):
        self.consumed = 0
        self.finalized = False

    def consume(self, chunk):
        self.consumed += 1

    def finalize(self):
        self.finalized = True
        return self.consumed


class _FailingReducer(_RecordingReducer):
    def consume(self, chunk):
        raise RuntimeError("scientific reducer failed")


def _executor(reducers, n_chunks=1):
    executor = ChunkedExecutor(
        molecular_system=object(),
        form="synthetic",
        operation="test_failure_integrity",
        reducers=reducers,
        chunk_size=1,
        heavy_mode="force",
    )
    chunk = {
        "coordinates": np.zeros((1, 1, 3), dtype=np.float64),
        "box": None,
        "time": None,
        "structure_indices": np.array([0]),
    }
    executor._get_form_iterator = lambda structure_indices, chunk_size: _Iterator([chunk] * n_chunks)
    executor._build_chunk = lambda raw_chunk: raw_chunk
    return executor


def test_heavy_executor_propagates_reducer_exception_without_finalizing():
    first = _RecordingReducer()
    failing = _FailingReducer()
    executor = _executor([first, failing])

    with pytest.raises(RuntimeError, match="scientific reducer failed"):
        executor._execute_heavy(n_atoms=1, n_structures=1)

    assert first.consumed == 1
    assert not first.finalized
    assert not failing.finalized


def test_heavy_executor_propagates_chunk_normalization_exception():
    reducer = _RecordingReducer()
    executor = _executor([reducer])

    def fail_to_build(raw_chunk):
        raise ValueError("invalid chunk shape")

    executor._build_chunk = fail_to_build

    with pytest.raises(ValueError, match="invalid chunk shape"):
        executor._execute_heavy(n_atoms=1, n_structures=1)

    assert reducer.consumed == 0
    assert not reducer.finalized


def test_memory_pressure_warning_rearms_after_pressure_recovers(monkeypatch):
    import molsysmt.configure as config
    import psutil

    reducer = _RecordingReducer()
    executor = _executor([reducer], n_chunks=4)
    rss_values = iter([60, 70, 40, 80])

    class FakeProcess:
        def memory_info(self):
            return SimpleNamespace(rss=next(rss_values))

    monkeypatch.setattr(psutil, "Process", FakeProcess)
    old_telemetry = config.emit_heavy_telemetry
    old_max_ram_usage = config.max_ram_usage
    old_threshold = config.memory_pressure_threshold
    config.emit_heavy_telemetry = True
    config.max_ram_usage = 100
    config.memory_pressure_threshold = 0.5

    try:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            executor._execute_heavy(n_atoms=1, n_structures=4)
    finally:
        config.emit_heavy_telemetry = old_telemetry
        config.max_ram_usage = old_max_ram_usage
        config.memory_pressure_threshold = old_threshold

    pressure_warnings = [
        warning for warning in caught
        if issubclass(warning.category, MemoryPressureWarning)
    ]
    assert len(pressure_warnings) == 2

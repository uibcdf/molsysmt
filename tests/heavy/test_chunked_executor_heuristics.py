"""
Tests for ChunkedExecutor footprint-aware memory heuristics.
"""
import pytest
import numpy as np
import molsysmt as msm
from molsysmt._private.execution.memory_policy import optimize_chunk_size
from molsysmt._private.execution import ChunkedExecutor, Reducer
from .conftest import N_ATOMS, N_STRUCTURES


class DummyReducer(Reducer):
    def initialize(self, metadata):
        pass
    def consume(self, chunk):
        pass
    def finalize(self):
        return True


@pytest.mark.heavy
def test_optimize_chunk_size_math():
    """Verify the mathematical logic of the chunk size optimization formula."""
    # System parameters
    n_atoms = 10000
    n_structures_selected = 5000
    advisory_chunk_size = 100
    max_ram_usage = 8 * 1024**3  # 8 GB
    chunk_memory_fraction = 0.10  # 10% -> 800 MB

    # Footprint of 1 frame: 10000 * 3 * 8 * 1.20 = 288,000 bytes (~281.25 KB)
    # Optimal chunk size: 800,000,000 // 288,000 = 2777 frames
    opt_chunk = optimize_chunk_size(
        n_atoms=n_atoms,
        n_structures_selected=n_structures_selected,
        advisory_chunk_size=advisory_chunk_size,
        max_ram_usage=max_ram_usage,
        chunk_memory_fraction=chunk_memory_fraction,
    )
    assert opt_chunk == 2982

    # If advisory_chunk_size is larger than optimal, it must be respected
    opt_chunk_large = optimize_chunk_size(
        n_atoms=n_atoms,
        n_structures_selected=n_structures_selected,
        advisory_chunk_size=3000,
        max_ram_usage=max_ram_usage,
        chunk_memory_fraction=chunk_memory_fraction,
    )
    assert opt_chunk_large == 3000

    # If the optimal size exceeds the selected structures, it must be capped
    opt_chunk_capped = optimize_chunk_size(
        n_atoms=n_atoms,
        n_structures_selected=1000,
        advisory_chunk_size=advisory_chunk_size,
        max_ram_usage=max_ram_usage,
        chunk_memory_fraction=chunk_memory_fraction,
    )
    assert opt_chunk_capped == 1000

    # If fraction is <= 0 or None, the advisory size must be returned exactly
    opt_chunk_disabled = optimize_chunk_size(
        n_atoms=n_atoms,
        n_structures_selected=n_structures_selected,
        advisory_chunk_size=advisory_chunk_size,
        max_ram_usage=max_ram_usage,
        chunk_memory_fraction=0.0,
    )
    assert opt_chunk_disabled == advisory_chunk_size


@pytest.mark.heavy
def test_chunked_executor_heuristics_integration(pentalanine_h5msm):
    """Verify that ChunkedExecutor dynamically optimizes its chunk size at runtime."""
    import molsysmt.configure as config

    molsys = msm.convert(pentalanine_h5msm, to_form='molsysmt.H5MSMFileHandler')
    try:
        # Configure small RAM usage for testing (e.g. 5 MB)
        # So we can see a precise, calculated optimal chunk size.
        old_max_ram = config.max_ram_usage
        old_fraction = config.chunk_memory_fraction
        
        # 1 frame for 62 atoms footprint: 62 * 3 * 8 * 1.20 = 1785.6 bytes
        # Let's set max_ram_usage to 1,000,000 bytes (1 MB)
        # With a 10% chunk budget = 100,000 bytes.
        # Optimal chunk size = 100,000 // 1785 = 56 frames.
        config.max_ram_usage = 1_000_000
        config.chunk_memory_fraction = 0.10

        try:
            reducer = DummyReducer()
            executor = ChunkedExecutor(
                molecular_system=molsys,
                form='molsysmt.H5MSMFileHandler',
                operation='test_heuristics',
                reducer=reducer,
                chunk_size=10,  # Advisory size
                heavy_mode='force',
                attributes=['coordinates'],
            )

            # Prior to execute, the executor has the advisory chunk size
            assert executor.chunk_size == 10

            # Execute triggers the optimization heuristic
            executor.execute()

            # Verify that chunk_size was optimized to 56 frames (scaled up from 10)
            assert executor.chunk_size == 56

        finally:
            config.max_ram_usage = old_max_ram
            config.chunk_memory_fraction = old_fraction
    finally:
        molsys.close()


@pytest.mark.heavy
def test_chunked_executor_heuristics_disabled(pentalanine_h5msm):
    """Verify that setting chunk_memory_fraction = 0.0 disables optimization."""
    import molsysmt.configure as config

    molsys = msm.convert(pentalanine_h5msm, to_form='molsysmt.H5MSMFileHandler')
    try:
        old_fraction = config.chunk_memory_fraction
        config.chunk_memory_fraction = 0.0

        try:
            reducer = DummyReducer()
            executor = ChunkedExecutor(
                molecular_system=molsys,
                form='molsysmt.H5MSMFileHandler',
                operation='test_heuristics_disabled',
                reducer=reducer,
                chunk_size=15,  # Advisory size
                heavy_mode='force',
                attributes=['coordinates'],
            )

            executor.execute()

            # Optimization is disabled, chunk_size remains exactly 15
            assert executor.chunk_size == 15

        finally:
            config.chunk_memory_fraction = old_fraction
    finally:
        molsys.close()

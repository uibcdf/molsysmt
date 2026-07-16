"""
Tests for ChunkedExecutor — parity between eager and heavy paths.
Uses the pentalanine h5msm fixture (5000 frames, 62 atoms, with coordinates and time).
"""
import pytest
import numpy as np
import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.execution import ChunkedExecutor, Reducer, estimate_footprint, decide_mode

from .conftest import N_ATOMS, N_STRUCTURES


class CoordinatesCollector(Reducer):
    """Collects all coordinates across chunks."""

    def initialize(self, metadata):
        self.all_coords = []

    def consume(self, chunk):
        self.all_coords.append(chunk['coordinates'].copy())

    def finalize(self):
        return np.concatenate(self.all_coords, axis=0)


@pytest.mark.heavy
def test_chunked_executor_heavy_force_parity(pentalanine_h5msm):
    """ChunkedExecutor in heavy mode must produce same coordinates as msm.get."""
    molsys = msm.convert(pentalanine_h5msm, to_form='molsysmt.H5MSMFileHandler')

    # Reference: eager get of all coordinates
    ref_coords = puw.get_value(
        msm.get(molsys, element='atom', selection='all', coordinates=True)
    )
    assert ref_coords.shape == (N_STRUCTURES, N_ATOMS, 3)

    # Heavy result via ChunkedExecutor with small chunk_size (odd to test boundary)
    reducer = CoordinatesCollector()
    executor = ChunkedExecutor(
        molecular_system=molsys,
        form='molsysmt.H5MSMFileHandler',
        operation='test_collect_coordinates',
        reducer=reducer,
        chunk_size=7,
        heavy_mode='force',
        attributes=['coordinates'],
    )
    result = executor.execute()

    assert result.shape == (N_STRUCTURES, N_ATOMS, 3)
    np.testing.assert_allclose(result, ref_coords, atol=1e-5)


@pytest.mark.heavy
def test_chunked_executor_decision_auto_small():
    """Auto mode on a small trajectory should select eager path."""
    fp = estimate_footprint(N_ATOMS, N_STRUCTURES)
    mode = decide_mode(fp, heavy_mode='auto')
    assert mode == 'eager'


@pytest.mark.heavy
def test_chunked_executor_decision_force():
    """force mode always selects heavy regardless of footprint."""
    fp = estimate_footprint(N_ATOMS, N_STRUCTURES)
    mode = decide_mode(fp, heavy_mode='force')
    assert mode == 'heavy'


# ---------------------------------------------------------------------------
# Multi-reducer
# ---------------------------------------------------------------------------

class FrameCountReducer(Reducer):
    """Counts total frames seen across all chunks."""

    def initialize(self, metadata):
        self.n_frames = 0

    def consume(self, chunk):
        self.n_frames += chunk['coordinates'].shape[0]

    def finalize(self):
        return self.n_frames


@pytest.mark.heavy
def test_multi_reducer_returns_list(pentalanine_h5msm):
    """reducers= parameter must return a list of results."""
    molsys = msm.convert(pentalanine_h5msm, to_form='molsysmt.H5MSMFileHandler')
    try:
        collector = CoordinatesCollector()
        counter = FrameCountReducer()

        executor = ChunkedExecutor(
            molecular_system=molsys,
            form='molsysmt.H5MSMFileHandler',
            operation='test_multi_reducer',
            reducers=[collector, counter],
            chunk_size=100,
            heavy_mode='force',
            attributes=['coordinates'],
        )
        results = executor.execute()

        assert isinstance(results, list)
        assert len(results) == 2
        coords, n_frames = results
        assert coords.shape == (N_STRUCTURES, N_ATOMS, 3)
        assert n_frames == N_STRUCTURES
    finally:
        molsys.close()


@pytest.mark.heavy
def test_multi_reducer_single_pass_parity(pentalanine_h5msm):
    """Multi-reducer single pass must match two independent single-reducer passes."""
    molsys = msm.convert(pentalanine_h5msm, to_form='molsysmt.H5MSMFileHandler')
    molsys2 = msm.convert(pentalanine_h5msm, to_form='molsysmt.H5MSMFileHandler')
    try:
        # Single-pass with two reducers
        c1 = CoordinatesCollector()
        c2 = FrameCountReducer()
        executor = ChunkedExecutor(
            molecular_system=molsys,
            form='molsysmt.H5MSMFileHandler',
            operation='test_multi_parity',
            reducers=[c1, c2],
            chunk_size=50,
            heavy_mode='force',
            attributes=['coordinates'],
        )
        coords_multi, count_multi = executor.execute()

        # Single separate pass for reference
        c3 = CoordinatesCollector()
        coords_single = ChunkedExecutor(
            molecular_system=molsys2,
            form='molsysmt.H5MSMFileHandler',
            operation='test_multi_parity_single',
            reducer=c3,
            chunk_size=50,
            heavy_mode='force',
            attributes=['coordinates'],
        ).execute()

        np.testing.assert_array_equal(coords_multi, coords_single)
        assert count_multi == N_STRUCTURES
    finally:
        molsys.close()
        molsys2.close()


# ---------------------------------------------------------------------------
# Checkpoint / resume
# ---------------------------------------------------------------------------

class CheckpointCollector(Reducer):
    """CoordinatesCollector with checkpoint/restore support."""

    def initialize(self, metadata):
        self.all_coords = []

    def consume(self, chunk):
        self.all_coords.append(chunk['coordinates'].copy())

    def finalize(self):
        return np.concatenate(self.all_coords, axis=0)

    def checkpoint(self):
        return {'chunks': [c.tolist() for c in self.all_coords]}

    def restore(self, state):
        self.all_coords = [np.array(c, dtype=np.float64) for c in state['chunks']]

    def merge(self, other):
        self.all_coords.extend(other.all_coords)


@pytest.mark.heavy
def test_checkpoint_resume(tmp_path, pentalanine_h5msm):
    """Checkpoint saved at mid-run and restored must yield same final result."""
    import os
    molsys = msm.convert(pentalanine_h5msm, to_form='molsysmt.H5MSMFileHandler')
    try:
        ckpt_dir = str(tmp_path)
        import molsysmt.configure as config

        with config.context(chunk_memory_fraction=None):
            # --- Pass 1: run with checkpoint every 5 chunks (chunk_size=100 → 50 chunks total)
            r1 = CheckpointCollector()
            executor1 = ChunkedExecutor(
                molecular_system=molsys,
                form='molsysmt.H5MSMFileHandler',
                operation='test_ckpt',
                reducer=r1,
                chunk_size=100,
                heavy_mode='force',
                attributes=['coordinates'],
                checkpoint_interval=5,
                checkpoint_path=ckpt_dir,
            )
            full_result = executor1.execute()

            # Find the last checkpoint file written
            ckpt_files = sorted(
                [f for f in os.listdir(ckpt_dir) if f.endswith('.pkl')],
            )
            assert len(ckpt_files) > 0, "No checkpoint file was written"
            last_ckpt = os.path.join(ckpt_dir, ckpt_files[-1])

            # --- Pass 2: restore from last checkpoint and continue
            r2 = CheckpointCollector()
            executor2 = ChunkedExecutor(
                molecular_system=molsys,
                form='molsysmt.H5MSMFileHandler',
                operation='test_ckpt',
                reducer=r2,
                chunk_size=100,
                heavy_mode='force',
                attributes=['coordinates'],
                restore_from=last_ckpt,
            )
            resumed_result = executor2.execute()

        # Both must cover all frames
        assert full_result.shape == (N_STRUCTURES, N_ATOMS, 3)
        assert resumed_result.shape == (N_STRUCTURES, N_ATOMS, 3)
        np.testing.assert_array_equal(full_result, resumed_result)
    finally:
        molsys.close()


# ---------------------------------------------------------------------------
# ETA adaptive (exponential moving average)
# ---------------------------------------------------------------------------

@pytest.mark.heavy
def test_eta_ema_smoke(pentalanine_h5msm):
    """Executor with telemetry enabled completes without error (EMA path exercised)."""
    import molsysmt.configure as config

    molsys = msm.convert(pentalanine_h5msm, to_form='molsysmt.H5MSMFileHandler')
    try:
        old_telemetry = config.emit_heavy_telemetry
        config.emit_heavy_telemetry = True
        try:
            r = FrameCountReducer()
            result = ChunkedExecutor(
                molecular_system=molsys,
                form='molsysmt.H5MSMFileHandler',
                operation='test_eta_ema',
                reducer=r,
                chunk_size=500,  # 10 chunks for 5000 frames → EMA blends across chunks
                heavy_mode='force',
                attributes=['coordinates'],
            ).execute()
            assert result == N_STRUCTURES
        finally:
            config.emit_heavy_telemetry = old_telemetry
    finally:
        molsys.close()


# ---------------------------------------------------------------------------
# Memory pressure warning
# ---------------------------------------------------------------------------

@pytest.mark.heavy
def test_memory_pressure_warning_emitted(pentalanine_h5msm, monkeypatch):
    """MemoryPressureWarning is emitted when RSS exceeds threshold."""
    import warnings
    import molsysmt.configure as config
    from molsysmt._private.smonitor import MemoryPressureWarning

    molsys = msm.convert(pentalanine_h5msm, to_form='molsysmt.H5MSMFileHandler')
    try:
        # Set threshold to 0.0 so any RSS triggers the warning
        old_threshold = config.memory_pressure_threshold
        old_telemetry = config.emit_heavy_telemetry
        config.memory_pressure_threshold = 0.0
        config.emit_heavy_telemetry = True

        try:
            r = FrameCountReducer()
            executor = ChunkedExecutor(
                molecular_system=molsys,
                form='molsysmt.H5MSMFileHandler',
                operation='test_mem_pressure',
                reducer=r,
                chunk_size=500,
                heavy_mode='force',
                attributes=['coordinates'],
            )
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                executor.execute()

            pressure_warnings = [w for w in caught if issubclass(w.category, MemoryPressureWarning)]
            assert len(pressure_warnings) == 1
        finally:
            config.memory_pressure_threshold = old_threshold
            config.emit_heavy_telemetry = old_telemetry
    finally:
        molsys.close()


@pytest.mark.heavy
def test_memory_pressure_warning_not_emitted_below_threshold(pentalanine_h5msm):
    """MemoryPressureWarning must NOT be emitted when RSS is below threshold."""
    import warnings
    import molsysmt.configure as config
    from molsysmt._private.smonitor import MemoryPressureWarning

    molsys = msm.convert(pentalanine_h5msm, to_form='molsysmt.H5MSMFileHandler')
    try:
        # Set threshold to 1.0 (100%) — essentially never triggers
        old_threshold = config.memory_pressure_threshold
        old_telemetry = config.emit_heavy_telemetry
        config.memory_pressure_threshold = 1.0
        config.emit_heavy_telemetry = True

        try:
            r = FrameCountReducer()
            executor = ChunkedExecutor(
                molecular_system=molsys,
                form='molsysmt.H5MSMFileHandler',
                operation='test_mem_no_pressure',
                reducer=r,
                chunk_size=500,
                heavy_mode='force',
                attributes=['coordinates'],
            )
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                executor.execute()

            pressure_warnings = [w for w in caught if issubclass(w.category, MemoryPressureWarning)]
            assert len(pressure_warnings) == 0, "Unexpected MemoryPressureWarning emitted"
        finally:
            config.memory_pressure_threshold = old_threshold
            config.emit_heavy_telemetry = old_telemetry
    finally:
        molsys.close()


# ---------------------------------------------------------------------------
# Parallel reduction via merge
# ---------------------------------------------------------------------------

@pytest.mark.heavy
def test_parallel_merge(pentalanine_h5msm):
    """Two reducers processing disjoint trajectory halves merge to full result."""
    molsys = msm.convert(pentalanine_h5msm, to_form='molsysmt.H5MSMFileHandler')
    try:
        half = N_STRUCTURES // 2

        # Run first half
        r1 = CheckpointCollector()
        ChunkedExecutor(
            molecular_system=molsys,
            form='molsysmt.H5MSMFileHandler',
            operation='test_merge_first',
            reducer=r1,
            structure_indices=list(range(0, half)),
            chunk_size=50,
            heavy_mode='force',
            attributes=['coordinates'],
        ).execute()

        # Run second half
        r2 = CheckpointCollector()
        ChunkedExecutor(
            molecular_system=molsys,
            form='molsysmt.H5MSMFileHandler',
            operation='test_merge_second',
            reducer=r2,
            structure_indices=list(range(half, N_STRUCTURES)),
            chunk_size=50,
            heavy_mode='force',
            attributes=['coordinates'],
        ).execute()

        # Merge and finalize
        r1.merge(r2)
        merged = r1.finalize()

        # Full single-pass reference
        r_ref = CheckpointCollector()
        ChunkedExecutor(
            molecular_system=molsys,
            form='molsysmt.H5MSMFileHandler',
            operation='test_merge_ref',
            reducer=r_ref,
            chunk_size=50,
            heavy_mode='force',
            attributes=['coordinates'],
        ).execute()
        full = r_ref.finalize()

        assert merged.shape == (N_STRUCTURES, N_ATOMS, 3)
        np.testing.assert_array_equal(merged, full)
    finally:
        molsys.close()

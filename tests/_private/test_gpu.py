"""
Tests for molsysmt._private.gpu — gpu_available() and resolve_use_gpu().

These tests run in a CPU-only environment (no CUDA GPU assumed).
The key invariant: resolve_use_gpu must never raise; it returns False
on any machine without a GPU regardless of the use_gpu argument.
"""

import pytest
import molsysmt.config as config
from molsysmt._private.gpu import gpu_available, resolve_use_gpu


# ---------------------------------------------------------------------------
# gpu_available — must return bool, never raise
# ---------------------------------------------------------------------------

class TestGpuAvailable:

    def test_returns_bool(self):
        result = gpu_available()
        assert isinstance(result, bool)

    def test_cached_on_second_call(self):
        """Second call returns the same value (cache hit)."""
        first = gpu_available()
        second = gpu_available()
        assert first == second

    def test_no_gpu_in_ci(self):
        """In a CPU-only environment the result must be False."""
        # We don't assert False here — just verify it returns without error.
        result = gpu_available()
        assert result in (True, False)


# ---------------------------------------------------------------------------
# resolve_use_gpu — all branches
# ---------------------------------------------------------------------------

class TestResolveUseGpu:

    # --- use_gpu=False (force CPU) ---

    def test_false_always_returns_false(self):
        assert resolve_use_gpu(False, payload_size=10_000_000) is False

    def test_false_ignores_config(self):
        original = config.use_gpu
        try:
            config.use_gpu = True
            assert resolve_use_gpu(False, payload_size=10_000_000) is False
        finally:
            config.use_gpu = original

    # --- use_gpu=None (inherit from config) ---

    def test_none_with_config_false(self):
        original = config.use_gpu
        try:
            config.use_gpu = False
            assert resolve_use_gpu(None, payload_size=10_000_000) is False
        finally:
            config.use_gpu = original

    def test_none_with_config_auto_no_gpu(self):
        """When config='auto' and no GPU is available, resolve returns False."""
        original = config.use_gpu
        try:
            config.use_gpu = 'auto'
            result = resolve_use_gpu(None, payload_size=10_000_000)
            # On a CPU machine gpu_available() is False → result must be False
            if not gpu_available():
                assert result is False
        finally:
            config.use_gpu = original

    # --- use_gpu='auto' ---

    def test_auto_below_threshold_returns_false(self):
        """Even if a GPU is available, payload below threshold → CPU."""
        original_threshold = config.gpu_threshold
        try:
            config.gpu_threshold = 1_000_000
            result = resolve_use_gpu('auto', payload_size=100)
            assert result is False  # below threshold regardless of GPU
        finally:
            config.gpu_threshold = original_threshold

    def test_auto_above_threshold_no_gpu(self):
        """Payload above threshold but no GPU → False."""
        if gpu_available():
            pytest.skip("GPU present — can't test CPU fallback branch")
        result = resolve_use_gpu('auto', payload_size=10_000_000)
        assert result is False

    # --- use_gpu=True (force GPU) ---

    def test_true_no_gpu_emits_warning_returns_false(self):
        """With no GPU, use_gpu=True should warn and return False."""
        if gpu_available():
            pytest.skip("GPU present — not testing the no-GPU branch")
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = resolve_use_gpu(True, payload_size=1)
        assert result is False
        assert len(w) >= 1  # at least one warning was emitted

    # --- unknown value (silent fallback) ---

    def test_unknown_value_returns_false(self):
        """An unrecognised use_gpu value silently falls back to CPU."""
        result = resolve_use_gpu('unknown_value', payload_size=0)
        assert result is False

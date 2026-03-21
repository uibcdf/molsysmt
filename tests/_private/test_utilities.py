"""
Tests for small _private utility modules:
  - memory.py (0% coverage)
  - execfile.py (7% coverage)
"""

import numpy as np
import pytest


# ---------------------------------------------------------------------------
# memory.py
# ---------------------------------------------------------------------------

class TestMemoryOfNdarray:

    def test_gb_units(self):
        from molsysmt._private.memory import memory_of_ndarray
        arr = np.zeros((1024, 1024), dtype=np.float64)
        result = memory_of_ndarray(arr, output='GB')
        assert isinstance(result, float)
        assert result > 0

    def test_mb_units(self):
        from molsysmt._private.memory import memory_of_ndarray
        arr = np.zeros((100, 100), dtype=np.float32)
        result = memory_of_ndarray(arr, output='MB')
        assert isinstance(result, float)
        assert result > 0

    def test_bytes_units(self):
        from molsysmt._private.memory import memory_of_ndarray
        arr = np.zeros(10, dtype=np.float64)
        result = memory_of_ndarray(arr, output='B')
        assert result == 10 * 8  # 10 float64 = 80 bytes

    def test_kb_units(self):
        from molsysmt._private.memory import memory_of_ndarray
        arr = np.zeros(1024, dtype=np.uint8)
        result = memory_of_ndarray(arr, output='KB')
        assert abs(result - 1.0) < 1e-10

    def test_tb_units(self):
        from molsysmt._private.memory import memory_of_ndarray
        arr = np.zeros(1, dtype=np.float64)
        result = memory_of_ndarray(arr, output='TB')
        assert result > 0


class TestMemoryEstimationOfNdarray:

    def test_basic_estimation(self):
        from molsysmt._private.memory import memory_estimation_of_ndarray
        result = memory_estimation_of_ndarray((100, 100), dtype='float64', output='B')
        assert result == 100 * 100 * 8

    def test_gb_estimation(self):
        from molsysmt._private.memory import memory_estimation_of_ndarray
        result = memory_estimation_of_ndarray((1024, 1024, 1024), dtype='float32', output='GB')
        assert isinstance(result, float)
        assert result > 0

    def test_float32_dtype(self):
        from molsysmt._private.memory import memory_estimation_of_ndarray
        result = memory_estimation_of_ndarray((10,), dtype='float32', output='B')
        assert result == 40.0  # 10 * 4 bytes

    def test_3d_shape(self):
        from molsysmt._private.memory import memory_estimation_of_ndarray
        result = memory_estimation_of_ndarray((2, 3, 4), dtype='float64', output='B')
        assert result == 2 * 3 * 4 * 8


# ---------------------------------------------------------------------------
# execfile.py
# ---------------------------------------------------------------------------

class TestExecfile:

    def test_execfile_runs_script(self, tmp_path):
        from molsysmt._private.execfile import execfile
        script = tmp_path / "test_script.py"
        script.write_text("result = 42\n")
        namespace = {}
        execfile(str(script), namespace)
        assert namespace['result'] == 42

    def test_execfile_uses_cache(self, tmp_path):
        from molsysmt._private.execfile import execfile, _CACHE
        script = tmp_path / "cached_script.py"
        script.write_text("x = 1\n")
        ns1 = {}
        execfile(str(script), ns1)
        # Second call should hit cache
        ns2 = {}
        execfile(str(script), ns2)
        assert ns1['x'] == ns2['x'] == 1

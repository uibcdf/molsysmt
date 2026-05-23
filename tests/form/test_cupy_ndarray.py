import pytest
import numpy as np
from molsysmt import pyunitwizard as puw

try:
    import cupy as cp
    CUPY_AVAILABLE = True
except ImportError:
    CUPY_AVAILABLE = False


@pytest.mark.skipif(not CUPY_AVAILABLE, reason="CuPy is not available.")
def test_cupy_ndarray_form_detection_and_conversion():
    import molsysmt as msm

    # Create a GPU coordinate quantity using CuPy
    gpu_val = cp.array([
        [0.0, 0.0, 0.0],
        [1.0, 2.0, 3.0]
    ], dtype=np.float64)
    gpu_qty = puw.quantity(gpu_val, 'nm')

    # Confirm correct form identification
    assert msm.form.get_form(gpu_qty) == 'cupy_ndarray'

    # Convert GPU coordinates to CPU XYZ form
    cpu_xyz = msm.convert(gpu_qty, to_form='XYZ')
    assert msm.form.get_form(cpu_xyz) == 'XYZ'
    assert isinstance(puw.get_value(cpu_xyz), np.ndarray)
    np.testing.assert_allclose(puw.get_value(cpu_xyz), cp.asnumpy(gpu_val))

    # Convert CPU XYZ form to GPU cupy_ndarray form
    gpu_back = msm.convert(cpu_xyz, to_form='cupy_ndarray')
    assert msm.form.get_form(gpu_back) == 'cupy_ndarray'
    assert isinstance(puw.get_value(gpu_back), cp.ndarray)

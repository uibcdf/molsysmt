import pytest
import numpy as np
from molsysmt import pyunitwizard as puw
import molsysmt as msm
from molsysmt.configure import context
from molsysmt._private.smonitor import GpuNotAvailableWarning


def test_least_rmsd_fit_gpu_vacuum():
    """Verify that GPU-accelerated least_rmsd_fit matches CPU references exactly."""
    # Create 10 synthetic coordinate points
    ref_coords_val = np.array([
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [1.0, 1.0, 1.0],
        [2.0, 3.0, 4.0],
        [-1.0, 2.5, 0.0],
        [0.5, -0.5, 2.0],
        [1.2, 0.8, -0.4],
        [-0.5, -0.5, -0.5]
    ], dtype=np.float64)

    # Let's define a translation and a rotation matrix
    translation = np.array([1.5, -2.0, 0.5])
    # 90 degrees rotation around Z-axis: [x, y, z] -> [-y, x, z]
    rotated_coords_val = np.array([[-y, x, z] for x, y, z in ref_coords_val])
    query_coords_val = rotated_coords_val + translation

    # Add frame and unit dimensions
    ref_coords = puw.quantity(ref_coords_val[np.newaxis, :, :], 'nm')
    query_coords = puw.quantity(query_coords_val[np.newaxis, :, :], 'nm')

    # Perform alignment on CPU
    fitted_cpu = msm.structure.least_rmsd_fit(
        query_coords,
        selection='all',
        selection_fit='all',
        reference_molecular_system=ref_coords,
        use_gpu=False
    )

    # Perform alignment on GPU (converts to CPU fallback gracefully or runs CUDA)
    with pytest.warns(GpuNotAvailableWarning, match="GPU acceleration was requested but is not available"):
        fitted_gpu = msm.structure.least_rmsd_fit(
            query_coords,
            selection='all',
            selection_fit='all',
            reference_molecular_system=ref_coords,
            use_gpu=True,
            gpu_backend='cuda'
        )

    # Assert match within precision bounds
    val_cpu = puw.get_value(fitted_cpu)
    val_gpu = puw.get_value(fitted_gpu)
    np.testing.assert_allclose(val_gpu, val_cpu, rtol=1e-5, atol=1e-5)
    np.testing.assert_allclose(val_gpu[0], ref_coords_val, rtol=1e-5, atol=1e-5)


def test_least_rmsd_fit_precision_policies():
    """Verify that the mixed-precision policy ('single' vs 'double') casts coordinates correctly."""
    ref_coords_val = np.array([
        [0.0, 0.0, 0.0],
        [1.0, 1.0, 1.0],
        [2.0, -1.0, 3.0]
    ], dtype=np.float64)
    ref_coords = puw.quantity(ref_coords_val[np.newaxis, :, :], 'nm')

    # Double precision (float64)
    with context(precision='double'):
        fitted_double = msm.structure.least_rmsd_fit(
            ref_coords,
            selection='all',
            selection_fit='all',
            reference_molecular_system=ref_coords,
            use_gpu=False
        )
        assert puw.get_value(fitted_double).dtype == np.float64

    # Single precision (float32)
    with context(precision='single'):
        with pytest.warns(GpuNotAvailableWarning, match="GPU acceleration was requested but is not available"):
            fitted_single = msm.structure.least_rmsd_fit(
                ref_coords,
                selection='all',
                selection_fit='all',
                reference_molecular_system=ref_coords,
                use_gpu=True,
                precision='single'
            )
        assert puw.get_value(fitted_single).dtype == np.float32

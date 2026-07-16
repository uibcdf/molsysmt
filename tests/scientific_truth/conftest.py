"""Governed numerical tolerances for the Scientific Truth Suite."""

import numpy as np
import pytest


@pytest.fixture(scope="session")
def public_six_decimal_atol():
    """Absolute tolerance for public geometry values rounded to six decimals."""

    return 5.0e-7


@pytest.fixture(scope="session")
def float64_kernel_atol():
    """Absolute tolerance for small, well-conditioned float64 analytic kernels."""

    return 1.0e-12


@pytest.fixture(scope="session")
def external_float32_atol():
    """Absolute tolerance for external geometry paths using float32 storage."""

    return 1.0e-6


@pytest.fixture(scope="session")
def rigid_geometry_coordinates_nm():
    """Return two independently specified frames related by a rigid transform."""

    reference = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [1.0, 1.0, 0.0],
            [1.0, 1.0, 1.0],
        ],
        dtype=np.float64,
    )
    rotation = np.array(
        [[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]],
        dtype=np.float64,
    )
    translated = reference @ rotation.T + np.array([2.0, -1.0, 0.5])
    return np.stack([reference, translated])


@pytest.fixture(scope="session")
def triclinic_mic_case_nm():
    """Return coordinates and a row-vector box for an exact triclinic MIC case."""

    box = np.array(
        [[2.0, 0.0, 0.0], [1.0, np.sqrt(3.0), 0.0], [0.0, 0.0, 3.0]],
        dtype=np.float64,
    )
    fractional = np.array([[0.05, 0.05, 0.0], [0.95, 0.95, 0.0]])
    return fractional @ box, box


@pytest.fixture(scope="session")
def trp_cage_pdb_path():
    """Return the catalog path for the 38-model Trp-cage NMR ensemble."""

    import molsysmt as msm

    return str(msm.systems["Trp-Cage"]["1l2y.pdb"])


@pytest.fixture(scope="session")
def pentalanine_trajectory_paths():
    """Return paired MDTraj HDF5 and MolSysMT H5MSM trajectory paths."""

    import molsysmt as msm

    return (
        str(msm.systems["pentalanine"]["traj_pentalanine.h5"]),
        str(msm.systems["pentalanine"]["traj_pentalanine.h5msm"]),
    )

"""
Regression tests for retired GPU arguments falling back to Rust CPU angles.
"""

import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np
import pytest


def test_get_angles_gpu_vacuum():
    """Verify GPU-accelerated valence angles under vacuum conditions (no PBC)."""
    molsys = msm.convert(systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')
    triplets = np.array([[0, 1, 2], [1, 2, 3], [2, 3, 4]], dtype=np.int64)

    # 1. CPU Reference Run
    angles_cpu = msm.structure.get_angles(molsys, triplets=triplets, use_gpu=False)

    # Retired backend names remain accepted and fall back to Rust CPU.
    angles_gpu_cuda = msm.structure.get_angles(
        molsys, triplets=triplets, use_gpu=True, gpu_backend='cuda'
    )

    # 3. Taichi Run (Forces GPU, falls back to CPU cleanly if Taichi is not installed)
    angles_gpu_taichi = msm.structure.get_angles(
        molsys, triplets=triplets, use_gpu=True, gpu_backend='taichi'
    )

    assert angles_cpu.shape == angles_gpu_cuda.shape
    assert np.allclose(puw.get_value(angles_cpu), puw.get_value(angles_gpu_cuda))

    assert angles_cpu.shape == angles_gpu_taichi.shape
    assert np.allclose(puw.get_value(angles_cpu), puw.get_value(angles_gpu_taichi))


def test_get_angles_gpu_orthogonal_pbc():
    """Verify GPU-accelerated valence angles under orthogonal PBC."""
    molsys = msm.convert(systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')
    triplets = np.array([[0, 1, 2], [1, 2, 3], [2, 3, 4]], dtype=np.int64)

    # Set an orthogonal box
    box = np.zeros((5000, 3, 3))
    box[:, 0, 0] = 5.0  # 5 nm box length
    box[:, 1, 1] = 5.0
    box[:, 2, 2] = 5.0
    msm.set(molsys, box=puw.quantity(box, 'nm'))

    angles_cpu = msm.structure.get_angles(
        molsys, triplets=triplets, pbc=True, use_gpu=False
    )
    angles_cuda = msm.structure.get_angles(
        molsys, triplets=triplets, pbc=True, use_gpu=True, gpu_backend='cuda'
    )
    angles_taichi = msm.structure.get_angles(
        molsys, triplets=triplets, pbc=True, use_gpu=True, gpu_backend='taichi'
    )

    assert np.allclose(puw.get_value(angles_cpu), puw.get_value(angles_cuda))
    assert np.allclose(puw.get_value(angles_cpu), puw.get_value(angles_taichi))


def test_get_angles_gpu_triclinic_pbc():
    """Verify GPU-accelerated valence angles under triclinic PBC."""
    molsys = msm.convert(systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')
    triplets = np.array([[0, 1, 2], [1, 2, 3], [2, 3, 4]], dtype=np.int64)

    # Set a triclinic box
    box = np.zeros((5000, 3, 3))
    box[:, 0, 0] = 4.0
    box[:, 1, 0] = 0.5; box[:, 1, 1] = 4.0
    box[:, 2, 0] = 0.5; box[:, 2, 1] = 0.5; box[:, 2, 2] = 4.0
    msm.set(molsys, box=puw.quantity(box, 'nm'))

    angles_cpu = msm.structure.get_angles(
        molsys, triplets=triplets, pbc=True, use_gpu=False
    )
    angles_cuda = msm.structure.get_angles(
        molsys, triplets=triplets, pbc=True, use_gpu=True, gpu_backend='cuda'
    )
    angles_taichi = msm.structure.get_angles(
        molsys, triplets=triplets, pbc=True, use_gpu=True, gpu_backend='taichi'
    )

    assert np.allclose(puw.get_value(angles_cpu), puw.get_value(angles_cuda))
    assert np.allclose(puw.get_value(angles_cpu), puw.get_value(angles_taichi))

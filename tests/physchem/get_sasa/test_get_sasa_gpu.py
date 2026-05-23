"""
Unit and regression tests for GPU-accelerated and native Shrake-Rupley SASA calculations (Numba CUDA & Taichi Lang).
Verifies results against CPU references and the legacy MDTraj engine.
"""

import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np
import pytest


def test_get_sasa_gpu_vacuum():
    """Verify GPU-accelerated and native CPU JIT SASA under vacuum (no PBC)."""
    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')
    molsys = msm.remove(molsys, selection="group_type in ['water', 'ion']")

    # 1. CPU Reference (MDTraj Engine)
    sasa_mdtraj = msm.physchem.get_sasa(molsys, element='molecule', engine='MDTraj')

    # 2. Native CPU JIT (MolSysMT Engine on CPU)
    sasa_cpu_native = msm.physchem.get_sasa(molsys, element='molecule', engine='MolSysMT', use_gpu=False)

    # 3. Numba CUDA GPU
    sasa_gpu_cuda = msm.physchem.get_sasa(
        molsys, element='molecule', engine='MolSysMT', use_gpu=True, gpu_backend='cuda'
    )

    # 4. Taichi GPU
    sasa_gpu_taichi = msm.physchem.get_sasa(
        molsys, element='molecule', engine='MolSysMT', use_gpu=True, gpu_backend='taichi'
    )

    val_mdtraj = puw.get_value(sasa_mdtraj, to_unit='nm**2')
    val_cpu = puw.get_value(sasa_cpu_native, to_unit='nm**2')
    val_cuda = puw.get_value(sasa_gpu_cuda, to_unit='nm**2')
    val_taichi = puw.get_value(sasa_gpu_taichi, to_unit='nm**2')

    # Allow slight tolerances since Shrake-Rupley is a discrete sphere points algorithm
    assert np.allclose(val_mdtraj, val_cpu, rtol=0.04)
    assert np.allclose(val_cpu, val_cuda, rtol=0.01)
    assert np.allclose(val_cpu, val_taichi, rtol=0.01)


def test_get_sasa_gpu_orthogonal_pbc():
    """Verify native and GPU-accelerated SASA calculations under orthogonal PBC."""
    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')
    molsys = msm.remove(molsys, selection="group_type in ['water', 'ion']")

    # Set an orthogonal box
    box = np.zeros((1, 3, 3))
    box[0, 0, 0] = 12.0
    box[0, 1, 1] = 12.0
    box[0, 2, 2] = 12.0
    msm.set(molsys, box=puw.quantity(box, 'nm'))

    sasa_cpu = msm.physchem.get_sasa(molsys, element='molecule', engine='MolSysMT', use_gpu=False)
    sasa_cuda = msm.physchem.get_sasa(molsys, element='molecule', engine='MolSysMT', use_gpu=True, gpu_backend='cuda')
    sasa_taichi = msm.physchem.get_sasa(molsys, element='molecule', engine='MolSysMT', use_gpu=True, gpu_backend='taichi')

    val_cpu = puw.get_value(sasa_cpu, to_unit='nm**2')
    val_cuda = puw.get_value(sasa_cuda, to_unit='nm**2')
    val_taichi = puw.get_value(sasa_taichi, to_unit='nm**2')

    assert np.allclose(val_cpu, val_cuda, rtol=0.01)
    assert np.allclose(val_cpu, val_taichi, rtol=0.01)


def test_get_sasa_gpu_triclinic_pbc():
    """Verify native and GPU-accelerated SASA calculations under triclinic PBC."""
    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')
    molsys = msm.remove(molsys, selection="group_type in ['water', 'ion']")

    # Set a triclinic box
    box = np.zeros((1, 3, 3))
    box[0, 0, 0] = 10.0
    box[0, 1, 0] = 1.0; box[0, 1, 1] = 10.0
    box[0, 2, 0] = 1.0; box[0, 2, 1] = 1.0; box[0, 2, 2] = 10.0
    msm.set(molsys, box=puw.quantity(box, 'nm'))

    sasa_cpu = msm.physchem.get_sasa(molsys, element='molecule', engine='MolSysMT', use_gpu=False)
    sasa_cuda = msm.physchem.get_sasa(molsys, element='molecule', engine='MolSysMT', use_gpu=True, gpu_backend='cuda')
    sasa_taichi = msm.physchem.get_sasa(molsys, element='molecule', engine='MolSysMT', use_gpu=True, gpu_backend='taichi')

    val_cpu = puw.get_value(sasa_cpu, to_unit='nm**2')
    val_cuda = puw.get_value(sasa_cuda, to_unit='nm**2')
    val_taichi = puw.get_value(sasa_taichi, to_unit='nm**2')

    assert np.allclose(val_cpu, val_cuda, rtol=0.01)
    assert np.allclose(val_cpu, val_taichi, rtol=0.01)

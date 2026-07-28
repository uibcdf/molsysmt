"""
Regression tests for retired GPU arguments falling back to Rust CPU contacts.
"""

import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np
import pytest


def test_get_contacts_gpu_vacuum():
    """Verify GPU-accelerated contact search under vacuum conditions (no PBC)."""
    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')
    CA_atoms = msm.select(molsys, selection='atom_name=="CA"')

    # 1. CPU Reference Run
    contacts_cpu = msm.structure.get_contacts(molsys, selection=CA_atoms, threshold='1.2 nm', use_gpu=False)

    # Retired backend names remain accepted and fall back to Rust CPU.
    contacts_gpu_cuda = msm.structure.get_contacts(
        molsys, selection=CA_atoms, threshold='1.2 nm', use_gpu=True, gpu_backend='cuda'
    )

    # 3. Taichi Run (Forces GPU, falls back to CUDA/CPU cleanly if Taichi is not installed)
    contacts_gpu_taichi = msm.structure.get_contacts(
        molsys, selection=CA_atoms, threshold='1.2 nm', use_gpu=True, gpu_backend='taichi'
    )

    assert contacts_cpu.shape == contacts_gpu_cuda.shape
    assert np.all(contacts_cpu == contacts_gpu_cuda)

    assert contacts_cpu.shape == contacts_gpu_taichi.shape
    assert np.all(contacts_cpu == contacts_gpu_taichi)


def test_get_contacts_gpu_cross_system():
    """Verify GPU-accelerated cross-system contact search."""
    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')
    chain_0 = msm.select(molsys, selection="atom_name=='CA' and chain_index==0")
    chain_1 = msm.select(molsys, selection="atom_name=='CA' and chain_index==1")

    # CPU reference
    contacts_cpu = msm.structure.get_contacts(
        molsys, selection=chain_0, selection_2=chain_1, threshold='1.2 nm', use_gpu=False
    )

    # Retired CUDA selector.
    contacts_gpu_cuda = msm.structure.get_contacts(
        molsys, selection=chain_0, selection_2=chain_1, threshold='1.2 nm', use_gpu=True, gpu_backend='cuda'
    )

    # GPU Taichi
    contacts_gpu_taichi = msm.structure.get_contacts(
        molsys, selection=chain_0, selection_2=chain_1, threshold='1.2 nm', use_gpu=True, gpu_backend='taichi'
    )

    assert np.all(contacts_cpu == contacts_gpu_cuda)
    assert np.all(contacts_cpu == contacts_gpu_taichi)


def test_get_contacts_gpu_orthogonal_pbc():
    """Verify GPU-accelerated contacts under orthogonal PBC."""
    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')
    
    # Artificially set an orthogonal box for testing PBC/MIC
    box = np.zeros((1, 3, 3))
    box[0, 0, 0] = 10.0  # 10 nm box length
    box[0, 1, 1] = 10.0
    box[0, 2, 2] = 10.0
    msm.set(molsys, box=puw.quantity(box, 'nm'))

    CA_atoms = msm.select(molsys, selection='atom_name=="CA"')

    contacts_cpu = msm.structure.get_contacts(
        molsys, selection=CA_atoms, threshold='1.2 nm', pbc=True, use_gpu=False
    )
    contacts_cuda = msm.structure.get_contacts(
        molsys, selection=CA_atoms, threshold='1.2 nm', pbc=True, use_gpu=True, gpu_backend='cuda'
    )
    contacts_taichi = msm.structure.get_contacts(
        molsys, selection=CA_atoms, threshold='1.2 nm', pbc=True, use_gpu=True, gpu_backend='taichi'
    )

    assert np.all(contacts_cpu == contacts_cuda)
    assert np.all(contacts_cpu == contacts_taichi)


def test_get_contacts_gpu_triclinic_pbc():
    """Verify GPU-accelerated contacts under non-orthogonal/triclinic PBC."""
    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')
    
    # Set a triclinic box: non-orthogonal vectors
    box = np.zeros((1, 3, 3))
    box[0, 0, 0] = 8.0
    box[0, 1, 0] = 1.0; box[0, 1, 1] = 8.0
    box[0, 2, 0] = 1.0; box[0, 2, 1] = 1.0; box[0, 2, 2] = 8.0
    msm.set(molsys, box=puw.quantity(box, 'nm'))

    CA_atoms = msm.select(molsys, selection='atom_name=="CA"')

    contacts_cpu = msm.structure.get_contacts(
        molsys, selection=CA_atoms, threshold='1.2 nm', pbc=True, use_gpu=False
    )
    contacts_cuda = msm.structure.get_contacts(
        molsys, selection=CA_atoms, threshold='1.2 nm', pbc=True, use_gpu=True, gpu_backend='cuda'
    )
    contacts_taichi = msm.structure.get_contacts(
        molsys, selection=CA_atoms, threshold='1.2 nm', pbc=True, use_gpu=True, gpu_backend='taichi'
    )

    assert np.all(contacts_cpu == contacts_cuda)
    assert np.all(contacts_cpu == contacts_taichi)

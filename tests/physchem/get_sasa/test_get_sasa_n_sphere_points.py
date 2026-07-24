"""
Regression tests for the ``n_sphere_points`` argument of
``molsysmt.physchem.get_sasa`` (Shrake–Rupley sampling density).

The exact per-atom SASA depends on the sampling density, so these tests avoid
hard-coded numeric anchors and instead assert the contract:
- the default reproduces ``n_sphere_points=240`` on both engines,
- changing the density actually changes the result,
- the two engines are unified on the same default density and agree closely.
"""

import molsysmt as msm
from molsysmt import systems
import numpy as np

puw = msm.pyunitwizard


def _system():
    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')
    molsys = msm.remove(molsys, selection="group_type in ['water', 'ion']")
    return molsys


def _total_sasa(molsys, engine, **kwargs):
    sasa = msm.physchem.get_sasa(molsys, element='atom', engine=engine, **kwargs)
    return puw.get_value(sasa, to_unit='nm**2').sum()


def test_get_sasa_default_density_is_240_molsysmt():
    molsys = _system()
    default = _total_sasa(molsys, 'MolSysMT')
    explicit = _total_sasa(molsys, 'MolSysMT', n_sphere_points=240)
    assert np.isclose(default, explicit)


def test_get_sasa_default_density_is_240_mdtraj():
    molsys = _system()
    default = _total_sasa(molsys, 'mdtraj')
    explicit = _total_sasa(molsys, 'mdtraj', n_sphere_points=240)
    assert np.isclose(default, explicit)


def test_get_sasa_n_sphere_points_changes_result_molsysmt():
    molsys = _system()
    # The total SASA is stable across densities (per-atom quantization averages
    # out over a large system), but the per-atom values change measurably.
    coarse = puw.get_value(
        msm.physchem.get_sasa(molsys, element='atom', engine='MolSysMT', n_sphere_points=100),
        to_unit='nm**2')
    fine = puw.get_value(
        msm.physchem.get_sasa(molsys, element='atom', engine='MolSysMT', n_sphere_points=960),
        to_unit='nm**2')
    assert not np.allclose(coarse, fine, atol=1e-6, rtol=0)


def test_get_sasa_engines_agree_at_shared_density():
    molsys = _system()
    native = _total_sasa(molsys, 'MolSysMT', n_sphere_points=240)
    mdtraj = _total_sasa(molsys, 'mdtraj', n_sphere_points=240)
    # Same algorithm and density on both engines: totals agree to a few percent.
    assert np.isclose(native, mdtraj, rtol=0.03)


def test_get_sasa_n_sphere_points_rejects_invalid():
    molsys = _system()
    import pytest
    from molsysmt import ArgumentError
    with pytest.raises(ArgumentError):
        msm.physchem.get_sasa(molsys, engine='MolSysMT', n_sphere_points=0)

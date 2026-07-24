"""
Regression tests for the configurable ``probe_radius`` argument of
``molsysmt.physchem.get_sasa`` (TopoMT-requested capability).

Covers, for both the native ``MolSysMT`` and the ``mdtraj`` engines:
- the default (an explicit ``probe_radius='1.4 angstroms'``) reproduces the
  historical 1.4 angstroms probe,
- a non-default probe radius actually changes the result,
- the physically expected direction for a folded protein: a larger probe occludes
  more crevices and yields a smaller total SASA, a smaller probe yields a larger one.
"""

import molsysmt as msm
from molsysmt import systems
import numpy as np

puw = msm.pyunitwizard


def _system():
    molsys = msm.convert(systems['TcTIM']['1tcd.h5msm'], to_form='molsysmt.MolSys')
    molsys = msm.remove(molsys, selection="group_type in ['water', 'ion']")
    return molsys


def _total_sasa(molsys, engine, probe_radius='1.4 angstroms'):
    sasa = msm.physchem.get_sasa(molsys, element='atom', engine=engine, probe_radius=probe_radius)
    return puw.get_value(sasa, to_unit='nm**2').sum()


def test_get_sasa_probe_radius_default_matches_14_angstroms_molsysmt():
    molsys = _system()
    # The signature default is '1.4 angstroms'; omitting the argument must match it.
    default = puw.get_value(
        msm.physchem.get_sasa(molsys, element='atom', engine='MolSysMT'), to_unit='nm**2').sum()
    explicit = _total_sasa(molsys, 'MolSysMT', probe_radius='1.4 angstroms')
    assert np.isclose(default, explicit)


def test_get_sasa_probe_radius_changes_result_molsysmt():
    molsys = _system()
    small = _total_sasa(molsys, 'MolSysMT', probe_radius='1.0 angstroms')
    default = _total_sasa(molsys, 'MolSysMT', probe_radius='1.4 angstroms')
    large = _total_sasa(molsys, 'MolSysMT', probe_radius='2.0 angstroms')
    # A larger probe buries more area on a folded protein; a smaller one exposes more.
    assert small > default > large


def test_get_sasa_probe_radius_default_matches_mdtraj():
    molsys = _system()
    default = puw.get_value(
        msm.physchem.get_sasa(molsys, element='atom', engine='mdtraj'), to_unit='nm**2').sum()
    explicit = _total_sasa(molsys, 'mdtraj', probe_radius='1.4 angstroms')
    assert np.isclose(default, explicit)


def test_get_sasa_probe_radius_changes_result_mdtraj():
    molsys = _system()
    small = _total_sasa(molsys, 'mdtraj', probe_radius='1.0 angstroms')
    large = _total_sasa(molsys, 'mdtraj', probe_radius='2.0 angstroms')
    assert small > large

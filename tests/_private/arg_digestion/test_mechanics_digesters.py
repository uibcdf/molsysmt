import pytest

from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.argdigest.argument.engine import digest_engine
from molsysmt._private.argdigest.argument.forcefield import digest_forcefield
from molsysmt._private.argdigest.argument.non_bonded_method import digest_non_bonded_method
from molsysmt._private.argdigest.argument.constraints import digest_constraints
from molsysmt._private.argdigest.argument.water_model import digest_water_model
from molsysmt._private.argdigest.argument.rigid_water import digest_rigid_water
from molsysmt._private.argdigest.argument.dispersion_correction import digest_dispersion_correction


def test_digest_engine_accepts_supported_engine_names():
    assert digest_engine('OpenMM') == 'OpenMM'
    assert digest_engine('openmm') == 'OpenMM'
    with pytest.raises(ArgumentError):
        digest_engine('bad')


def test_digest_forcefield_accepts_bool_and_known_forcefields():
    assert digest_forcefield(True, caller='molsysmt.basic.get.get') is True
    assert digest_forcefield('AMBER14') == 'AMBER14'
    with pytest.raises(ArgumentError):
        digest_forcefield('bad-forcefield')


def test_digest_non_bonded_method_and_constraints_accept_form_callers_and_strings():
    assert digest_non_bonded_method('PME', caller='molsysmt.form.openmm_Topology.to_openmm_System') == 'PME'
    assert digest_non_bonded_method('cutoff') == 'cutoff'
    with pytest.raises(ArgumentError):
        digest_non_bonded_method(1)

    assert digest_constraints('hbonds', caller='molsysmt.form.openmm_Topology.to_openmm_System') == 'hbonds'
    assert digest_constraints('none') == 'none'
    with pytest.raises(ArgumentError):
        digest_constraints(1)


def test_digest_water_model_accepts_none_and_known_values():
    assert digest_water_model(True, caller='molsysmt.basic.get.get') is True
    assert digest_water_model(None) is None
    assert digest_water_model('tip3p') == 'TIP3P'
    with pytest.raises(ArgumentError):
        digest_water_model('bad-water')


def test_digest_rigid_water_and_dispersion_correction():
    assert digest_rigid_water(True, caller='molsysmt.form.openmm_Topology.to_openmm_System') is True
    with pytest.raises(ArgumentError):
        digest_rigid_water(True)

    assert digest_dispersion_correction(True, caller='molsysmt.form.openmm_Topology.to_openmm_System') is True
    assert digest_dispersion_correction(False) is False
    with pytest.raises(ArgumentError):
        digest_dispersion_correction('bad')

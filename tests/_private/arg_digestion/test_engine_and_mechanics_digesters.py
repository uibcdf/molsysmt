import pytest

from molsysmt._private.arg_digestion.argument.engine import digest_engine
from molsysmt._private.arg_digestion.argument.forcefield import digest_forcefield
from molsysmt._private.arg_digestion.argument.integrator import digest_integrator
from molsysmt._private.arg_digestion.argument.platform import digest_platform
from molsysmt._private.arg_digestion.argument.non_bonded_method import digest_non_bonded_method
from molsysmt._private.arg_digestion.argument.water_model import digest_water_model
from molsysmt._private.arg_digestion.argument.constraints import digest_constraints
from molsysmt._private.arg_digestion.argument.rigid_water import digest_rigid_water
from molsysmt._private.arg_digestion.argument.dispersion_correction import digest_dispersion_correction
from molsysmt._private.arg_digestion.argument.default_exclusion_rules import digest_default_exclusion_rules
from molsysmt._private.arg_digestion.argument.default_inclusion_rules import digest_default_inclusion_rules
from molsysmt._private.arg_digestion.argument.ewald_error_tolerance import digest_ewald_error_tolerance
from molsysmt._private.smonitor import ArgumentError


def test_engine_and_mechanics_digesters():
    assert digest_engine('LEaP') == 'LEaP'
    assert digest_forcefield('AMBER14') == 'AMBER14'
    assert digest_forcefield(True, caller='molsysmt.basic.get.get') is True
    assert digest_integrator('Langevin') == 'Langevin'
    assert digest_integrator(True, caller='molsysmt.basic.get.get') is True
    assert digest_platform('CPU') == 'CPU'
    assert digest_non_bonded_method('PME') == 'PME'
    assert digest_non_bonded_method(object(), caller='molsysmt.form.openmm_Topology.to_openmm_System') is not None
    assert digest_water_model('tip3p') == 'TIP3P'
    assert digest_water_model(True, caller='molsysmt.basic.get.get') is True
    assert digest_constraints('HBonds') == 'HBonds'
    assert digest_constraints(object(), caller='molsysmt.form.openmm_Topology.to_openmm_System') is not None
    assert digest_rigid_water(True, caller='molsysmt.form.openmm_Topology.to_openmm_System') is True
    assert digest_dispersion_correction(False) is False
    assert digest_default_exclusion_rules(True) is True
    assert digest_default_inclusion_rules(False) is False
    assert digest_ewald_error_tolerance(0.0005) == 0.0005
    assert digest_ewald_error_tolerance(None) is None

    with pytest.raises(ArgumentError):
        digest_engine('unknown')
    with pytest.raises(ArgumentError):
        digest_integrator(object())
    with pytest.raises(ArgumentError):
        digest_platform('OpenCL')

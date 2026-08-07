import numpy as np
import pytest

from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.argdigest.argument.id import digest_id
from molsysmt._private.argdigest.argument.id_step import digest_id_step
from molsysmt._private.argdigest.argument.filename import digest_filename
from molsysmt._private.argdigest.argument.finesse import digest_finesse
from molsysmt._private.argdigest.argument.hydrogen_mass import digest_hydrogen_mass
from molsysmt._private.argdigest.argument.ewald_error_tolerance import digest_ewald_error_tolerance
from molsysmt._private.argdigest.argument.friction import digest_friction


def test_identity_and_scalar_digesters_accept_valid_inputs():
    np.testing.assert_array_equal(digest_id([1, 2, 3]), np.array([1, 2, 3]))
    np.testing.assert_array_equal(digest_id((4, 5)), np.array([4, 5]))
    with pytest.raises(ArgumentError):
        digest_id('abc')

    assert digest_id_step(None) is None
    assert digest_id_step(2) == 2
    with pytest.raises(ArgumentError):
        digest_id_step(1.5)

    assert digest_filename('output.dat') == 'output.dat'
    assert digest_finesse(4) == 4
    with pytest.raises(ArgumentError):
        digest_filename(4)
    with pytest.raises(ArgumentError):
        digest_finesse('fine')


def test_hydrogen_mass_ewald_and_friction_support_form_and_quantity_semantics():
    form_caller = 'molsysmt.form.openmm_Topology.to_openmm_System'
    assert digest_hydrogen_mass(None, caller=form_caller) is None
    assert digest_hydrogen_mass(1.5, caller=form_caller) == 1.5
    with pytest.raises(ArgumentError):
        digest_hydrogen_mass(1.5)

    assert digest_ewald_error_tolerance(None) is None
    assert digest_ewald_error_tolerance(1e-4) == 1e-4
    assert digest_ewald_error_tolerance(5e-5, caller=form_caller) == 5e-5
    with pytest.raises(ArgumentError):
        digest_ewald_error_tolerance('1e-4')

    compare_caller = 'molsysmt.basic.compare.compare'
    assert digest_friction(True, caller=compare_caller) is True
    friction = digest_friction(puw.quantity(1.0, 'ps^-1'))
    assert puw.check(friction, dimensionality={'[T]': -1})
    with pytest.raises(ArgumentError):
        digest_friction(1.0)

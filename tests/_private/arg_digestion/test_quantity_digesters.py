import numpy as np
import pytest

from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.arg_digestion.argument.formal_charge import digest_formal_charge
from molsysmt._private.arg_digestion.argument.kinetic_energy import digest_kinetic_energy
from molsysmt._private.arg_digestion.argument.n_structures import digest_n_structures
from molsysmt._private.arg_digestion.argument.occupancy import digest_occupancy
from molsysmt._private.arg_digestion.argument.partial_charge import digest_partial_charge
from molsysmt._private.arg_digestion.argument.potential_energy import digest_potential_energy
from molsysmt._private.arg_digestion.argument.structure_index import digest_structure_index
from molsysmt._private.arg_digestion.argument.temperature import digest_temperature
from molsysmt._private.arg_digestion.argument.time import digest_time
from molsysmt._private.arg_digestion.argument.total_energy import digest_total_energy
from molsysmt._private.arg_digestion.argument.velocities import digest_velocities


BOOL_CALLER = "molsysmt.basic.get.get"
FORM_CONVERTER_CALLER = "molsysmt.form.file_pdb.to_molsysmt_MolSys.to_molsysmt_MolSys"


@pytest.mark.parametrize(
    ("digester", "value", "unit"),
    [
        (digest_time, 1.0, "picoseconds"),
        (digest_temperature, 300.0, "kelvin"),
        (digest_kinetic_energy, 1.5, "kilojoule/mole"),
        (digest_potential_energy, -2.5, "kilojoule/mole"),
        (digest_total_energy, -1.0, "kilojoule/mole"),
    ],
)
def test_scalar_quantity_digesters_standardize_scalar_inputs(digester, value, unit):
    out = digester(puw.quantity(value, unit))
    assert puw.is_quantity(out)
    assert np.isscalar(puw.get_value(out))


@pytest.mark.parametrize(
    "digester",
    [
        digest_time,
        digest_temperature,
        digest_kinetic_energy,
        digest_potential_energy,
        digest_total_energy,
        digest_velocities,
        digest_formal_charge,
    ],
)
def test_quantity_digesters_support_boolean_query_mode(digester):
    assert digester(True, caller=BOOL_CALLER) is True


def test_time_digester_accepts_quantity_sequences():
    out = digest_time(
        [
            puw.quantity(1.0, "picoseconds"),
            puw.quantity(2.0, "picoseconds"),
        ]
    )
    assert puw.is_quantity(out)
    np.testing.assert_allclose(puw.get_value(out), np.array([1.0, 2.0]))


def test_velocities_digester_normalizes_all_supported_ranks():
    one_vector = puw.quantity([1.0, 2.0, 3.0], "nanometers/picosecond")
    out = digest_velocities(one_vector)
    assert puw.get_value(out).shape == (1, 1, 3)

    many_atoms = puw.quantity([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], "nanometers/picosecond")
    out = digest_velocities(many_atoms)
    assert puw.get_value(out).shape == (1, 2, 3)

    trajectory = puw.quantity(np.ones((2, 3, 3), dtype=np.float32), "nanometers/picosecond")
    out = digest_velocities(trajectory)
    assert puw.get_value(out).shape == (2, 3, 3)


def test_formal_charge_digester_normalizes_one_dimensional_quantities():
    charges = puw.quantity([1.0, -1.0], "elementary_charge")
    out = digest_formal_charge(charges)
    np.testing.assert_allclose(puw.get_value(out), np.array([1.0, -1.0]))


def test_occupancy_digester_normalizes_rank_one_and_rank_two_arrays():
    one = digest_occupancy([0.5, 1.0])
    assert one.shape == (1, 2)

    two = digest_occupancy(np.array([[0.5, 1.0], [1.0, 0.5]]))
    assert two.shape == (2, 2)


def test_partial_charge_digester_accepts_boolean_queries_and_form_bypass():
    assert digest_partial_charge(True, caller=BOOL_CALLER) is True
    token = object()
    assert digest_partial_charge(token, caller=FORM_CONVERTER_CALLER) is token
    with pytest.raises(ArgumentError):
        digest_partial_charge(token)


def test_structure_index_and_n_structures_support_native_and_contains_contexts():
    assert digest_structure_index(3) == 3
    assert digest_n_structures(4, caller="molsysmt.basic.contains.contains") == 4
    assert digest_n_structures(2, caller="molsysmt.structure.get_box_with_shape") == 2


@pytest.mark.parametrize(
    ("digester", "bad_value"),
    [
        (digest_time, puw.quantity([1.0, 2.0], "nanometers")),
        (digest_temperature, puw.quantity(300.0, "picoseconds")),
        (digest_kinetic_energy, puw.quantity(1.0, "kelvin")),
        (digest_potential_energy, puw.quantity(1.0, "nanometer")),
        (digest_total_energy, puw.quantity(1.0, "picoseconds")),
        (digest_velocities, puw.quantity([1.0, 2.0, 3.0], "nanometers")),
        (digest_formal_charge, puw.quantity([1.0], "picoseconds")),
    ],
)
def test_quantity_digesters_reject_wrong_dimensionalities(digester, bad_value):
    with pytest.raises(ArgumentError):
        digester(bad_value)

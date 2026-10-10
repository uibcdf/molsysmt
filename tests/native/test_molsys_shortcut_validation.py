"""Protecting the validated public boundary of native MolSys shortcuts."""

import numpy as np
import pytest

from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError
from molsysmt.native import MolSys


@pytest.fixture
def molsys():
    output = MolSys(n_atoms=4)
    output.structures.coordinates = puw.quantity(
        np.arange(36, dtype=float).reshape(3, 4, 3), "nm"
    )
    return output


@pytest.mark.parametrize("element", ["atom", "atoms", "ATOM"])
def test_get_normalizes_elements_and_scalar_selection(molsys, element):
    assert molsys.get(element=element, selection=2, atom_index=True) == [2]


def test_get_preserves_requested_structure_order_and_units(molsys):
    values = molsys.get(
        element="atom",
        selection=[3, 1],
        structure_indices=[2, 0],
        output_type="dictionary",
        coordinates=True,
    )
    coordinates = values["coordinates"]
    assert coordinates.shape == (2, 2, 3)
    assert puw.get_unit(coordinates) == puw.unit("nm")
    np.testing.assert_array_equal(
        puw.get_value(coordinates),
        [[[33, 34, 35], [27, 28, 29]], [[9, 10, 11], [3, 4, 5]]],
    )


@pytest.mark.parametrize(
    "options",
    [
        {"skip_digestion": "yes"},
        {"output_type": "garbage"},
        {"n_atoms": "no"},
        {"get_missing_bonds": "yes"},
    ],
)
def test_get_rejects_invalid_public_arguments(molsys, options):
    with pytest.raises(ArgumentError):
        molsys.get(**{"n_atoms": True, **options})


def test_get_rejects_unknown_attributes(molsys):
    from argdigest.core.errors import UnknownArgumentError

    with pytest.raises(UnknownArgumentError):
        molsys.get(not_a_molecular_attribute=True)


@pytest.mark.parametrize("method", ["info", "to_form"])
def test_other_shortcuts_reject_nonboolean_skip_flag(molsys, method):
    with pytest.raises(ArgumentError):
        if method == "info":
            molsys.info(skip_digestion="yes")
        else:
            molsys.to_form("molsysmt.MolSys", skip_digestion="yes")


def test_info_normalizes_element_and_scalar_selection(molsys):
    result = molsys.info(element="atoms", selection=2)
    assert len(result.data) == 1
    assert result.data["index"].tolist() == [2]


def test_conversion_normalizes_scalar_indices_without_modifying_source(molsys):
    output = molsys.to_form("molsysmt.Structures", atom_indices=2, structure_indices=1)
    assert output.coordinates.shape == (1, 1, 3)
    assert puw.get_unit(output.coordinates) == puw.unit("nm")
    np.testing.assert_array_equal(puw.get_value(output.coordinates), [[[18, 19, 20]]])
    assert molsys.structures.coordinates.shape == (3, 4, 3)


def test_conversion_rejects_invalid_copy_option(molsys):
    with pytest.raises(ArgumentError):
        molsys.to_form("molsysmt.MolSys", copy_if_all="no")


def test_explicit_trusted_calls_and_copy_semantics_remain_available(molsys):
    assert molsys.get(n_atoms=True, skip_digestion=True) == 4
    assert (
        molsys.to_form("molsysmt.MolSys", copy_if_all=False, skip_digestion=True)
        is molsys
    )
    copied = molsys.to_form("molsysmt.MolSys")
    assert copied is not molsys
    assert not np.shares_memory(
        puw.get_value(copied.structures.coordinates),
        puw.get_value(molsys.structures.coordinates),
    )

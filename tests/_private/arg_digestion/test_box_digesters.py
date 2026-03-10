import numpy as np
import pytest

from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.arg_digestion.argument.box import digest_box
from molsysmt._private.arg_digestion.argument.box_angles import digest_box_angles
from molsysmt._private.arg_digestion.argument.box_lengths import digest_box_lengths
from molsysmt._private.arg_digestion.argument.box_center import digest_box_center
from molsysmt._private.arg_digestion.argument.box_origin import digest_box_origin


def test_digest_box_accepts_boolean_for_get():
    assert digest_box(True, caller='molsysmt.basic.get.get') is True


def test_digest_box_expands_two_dimensional_input():
    box = puw.quantity(np.eye(3), 'nm')
    output = digest_box(box)
    assert puw.get_value(output).shape == (1, 3, 3)


def test_digest_box_accepts_quantity_built_from_nested_lists():
    box = puw.quantity([[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]], 'nm')
    output = digest_box(box)
    assert puw.get_value(output).shape == (1, 3, 3)


def test_digest_box_rejects_wrong_rank():
    with pytest.raises(ArgumentError):
        digest_box(puw.quantity(np.ones((3,)), 'nm'))


@pytest.mark.parametrize('digester', [digest_box_lengths, digest_box_angles])
def test_box_vectors_digesters_accept_boolean_for_get(digester):
    assert digester(True, caller='molsysmt.basic.get.get') is True


@pytest.mark.parametrize(
    ('digester', 'quantity', 'unit_dim'),
    [
        (digest_box_lengths, puw.quantity([1.0, 2.0, 3.0], 'nm'), {'[L]': 1}),
        (digest_box_angles, puw.quantity([90.0, 90.0, 90.0], 'degree'), {}),
    ],
)
def test_box_vector_digesters_standardize_single_structure(digester, quantity, unit_dim):
    output = digester(quantity)
    assert puw.check(output, dimensionality=unit_dim)
    assert puw.get_value(output).shape == (1, 3)


@pytest.mark.parametrize(
    ('digester', 'quantity'),
    [
        (digest_box_lengths, puw.quantity(np.ones((2, 2)), 'nm')),
        (digest_box_angles, puw.quantity(np.ones((2, 2)), 'degree')),
    ],
)
def test_box_vector_digesters_reject_wrong_shape(digester, quantity):
    with pytest.raises(ArgumentError):
        digester(quantity)


@pytest.mark.parametrize('digester', [digest_box_center, digest_box_origin])
def test_box_point_digesters_accept_length_triplets(digester):
    output = digester(puw.quantity([1.0, 2.0, 3.0], 'nm'))
    assert puw.get_value(output).shape == (3,)


@pytest.mark.parametrize('digester', [digest_box_center, digest_box_origin])
def test_box_point_digesters_accept_single_row_matrices(digester):
    output = digester(puw.quantity([[1.0, 2.0, 3.0]], 'nm'))
    assert puw.get_value(output).shape == (3,)


@pytest.mark.parametrize('digester', [digest_box_center, digest_box_origin])
def test_box_point_digesters_reject_wrong_units(digester):
    with pytest.raises(ArgumentError):
        digester(puw.quantity([1.0, 2.0, 3.0], 'ps'))

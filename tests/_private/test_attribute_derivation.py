from types import SimpleNamespace

import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.attribute_derivation import (
    NOT_DERIVABLE,
    can_derive_attribute,
    derive_attribute,
)
from molsysmt.attribute import attributes


def _module_with_box(box):
    def get_box_from_system(item, structure_indices='all', skip_digestion=False):
        if structure_indices is None:
            return None
        if structure_indices == 'all':
            return box
        return box[structure_indices, :, :]

    return SimpleNamespace(
        attributes={'box': True},
        get_box_from_system=get_box_from_system,
    )


def test_catalog_preserves_attribute_dependencies():
    assert attributes['box_lengths']['depends_on'] == ['box']
    assert attributes['box']['dependants'] == [
        'box_shape',
        'box_angles',
        'box_lengths',
        'box_volume',
    ]
    assert attributes['structure_index']['dependants'] == ['n_structures']


def test_box_attributes_are_derived_with_units_and_structure_indices():
    box = puw.quantity(
        np.stack([np.eye(3) * 2.0, np.eye(3) * 3.0]),
        'nanometer',
    )
    module = _module_with_box(box)

    lengths = derive_attribute(
        module,
        None,
        'box_lengths',
        'system',
        structure_indices=[1],
    )
    angles = derive_attribute(module, None, 'box_angles', 'system')
    shape = derive_attribute(module, None, 'box_shape', 'system')
    volume = derive_attribute(module, None, 'box_volume', 'system')

    assert np.allclose(puw.get_value(lengths), [[3.0, 3.0, 3.0]])
    assert puw.get_unit(lengths) == puw.unit('nanometer')
    assert np.allclose(puw.get_value(angles), np.full((2, 3), np.pi / 2), atol=1.0e-6)
    assert puw.get_unit(angles) == puw.unit('radian')
    assert shape == 'cubic'
    assert np.allclose(puw.get_value(volume), [8.0, 27.0])
    assert puw.get_unit(volume) == puw.unit('nanometer**3')


def test_derivation_requires_the_system_level_and_declared_source():
    box = puw.quantity(np.eye(3)[None, :, :], 'nanometer')
    module = _module_with_box(box)

    assert not can_derive_attribute(module, 'box_lengths', 'atom')
    assert derive_attribute(module, None, 'box_lengths', 'atom') is NOT_DERIVABLE

    module.attributes['box'] = False
    assert not can_derive_attribute(module, 'box_lengths', 'system')


def test_derivation_preserves_none_from_the_source_getter():
    module = _module_with_box(None)

    assert derive_attribute(module, None, 'box_volume', 'system') is None


def test_connectivity_attributes_include_system_delivery():
    connectivity_attributes = (
        'bond_index',
        'bonded_atoms',
        'bonded_atom_pairs',
        'inner_bonded_atoms',
        'inner_bonded_atom_pairs',
        'inner_bond_index',
    )

    for attribute in connectivity_attributes:
        assert 'system' in attributes[attribute]['get_from']

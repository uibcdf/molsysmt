"""Testing the shared topology and structures atom-inventory contract."""

import pytest

from molsysmt.attribute import (
    _structural_attributes,
    _topological_attributes,
    is_chemical_state_attribute,
    is_structural_attribute,
    is_topological_attribute,
)


@pytest.mark.parametrize('attribute', ['atom_index', 'n_atoms'])
def test_atom_inventory_is_topological_and_structural(attribute):
    assert is_topological_attribute(attribute)
    assert is_structural_attribute(attribute)
    assert not is_chemical_state_attribute(attribute)


@pytest.mark.parametrize('attribute', ['atom_index', 'n_atoms'])
def test_atom_inventory_occurs_once_in_each_classification(attribute):
    assert _topological_attributes.count(attribute) == 1
    assert _structural_attributes.count(attribute) == 1

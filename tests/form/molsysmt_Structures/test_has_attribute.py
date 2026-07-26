"""Testing instance-aware presence for optional native structure attributes."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.native import Structures


OPTIONAL_ATTRIBUTES = (
    'structure_id',
    'time',
    'box',
    'coordinates',
    'velocities',
    'b_factor',
    'alternate_location',
    'bioassembly',
    'temperature',
    'potential_energy',
    'kinetic_energy',
    'total_energy',
    'occupancy',
)


@pytest.mark.parametrize('attribute', OPTIONAL_ATTRIBUTES)
def test_empty_structures_distinguishes_capability_from_presence(attribute):
    structures = Structures(skip_digestion=True)

    assert msm.has_attribute(structures, attribute, include_none=True)
    assert not msm.has_attribute(structures, attribute)


def test_materialized_optional_structure_attributes_are_present():
    structures = Structures(
        structure_id=[7],
        time=puw.quantity([1.0], 'ps'),
        box=puw.quantity(np.eye(3)[None, :, :], 'nm'),
        coordinates=puw.quantity(np.zeros((1, 2, 3)), 'nm'),
        velocities=puw.quantity(np.ones((1, 2, 3)), 'nm/ps'),
        b_factor=puw.quantity(np.ones((1, 2)), 'nm**2'),
        alternate_location=[{}],
        bioassembly={},
        temperature=puw.quantity([300.0], 'K'),
        potential_energy=puw.quantity([-2.0], 'kJ/mol'),
        kinetic_energy=puw.quantity([1.0], 'kJ/mol'),
        occupancy=np.ones((1, 2)),
        skip_digestion=True,
    )

    for attribute in OPTIONAL_ATTRIBUTES:
        assert msm.has_attribute(structures, attribute)
    assert msm.has_attribute(structures, 'n_bioassemblies')


def test_total_energy_requires_both_energy_components():
    structures = Structures(
        potential_energy=puw.quantity([-2.0], 'kJ/mol'),
        skip_digestion=True,
    )

    assert msm.has_attribute(structures, 'potential_energy')
    assert not msm.has_attribute(structures, 'kinetic_energy')
    assert not msm.has_attribute(structures, 'total_energy')

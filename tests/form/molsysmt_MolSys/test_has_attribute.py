"""Testing composed instance-aware presence for native MolSys."""

import numpy as np

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.form import _dict_modules
from molsysmt.native import MolSys


def test_molsys_declares_the_complete_native_component_union():
    expected = {
        attribute
        for form in (
            'molsysmt.Topology',
            'molsysmt.Structures',
            'molsysmt.MolecularMechanics',
        )
        for attribute, available in _dict_modules[form].attributes.items()
        if available
    }
    expected.add('structure_chemical_state_index')
    observed = {
        attribute
        for attribute, available in _dict_modules['molsysmt.MolSys'].attributes.items()
        if available
    }

    assert observed == expected


def test_molsys_composes_topology_structures_and_mechanics_presence():
    molsys = MolSys(n_atoms=2)

    assert not msm.has_attribute(molsys, 'formal_charge')
    assert not msm.has_attribute(molsys, 'occupancy')
    assert not msm.has_attribute(molsys, 'partial_charge')
    assert not msm.has_attribute(molsys, 'structure_chemical_state_index')

    msm.set(molsys, element='atom', formal_charge=[0, 1])
    molsys.structures.coordinates = puw.quantity(np.zeros((1, 2, 3)), 'nm')
    molsys.structures.occupancy = np.ones((1, 2))
    molsys.molecular_mechanics.partial_charge = [0.1, -0.1]

    assert msm.has_attribute(molsys, 'formal_charge')
    assert msm.has_attribute(molsys, 'occupancy')
    assert msm.has_attribute(molsys, 'partial_charge')
    assert msm.has_attribute(molsys, 'structure_chemical_state_index')

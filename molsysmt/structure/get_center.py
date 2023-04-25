from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt import lib as msmlib
from molsysmt import pyunitwizard as puw
import numpy as np

@digest()
def get_center(molecular_system, selection='all', groups_of_atoms=None, center_of_mass=False, weights=None,
        structure_indices='all', syntax='MolSysMT', engine='MolSysMT'):

    from molsysmt.basic import select, get

    if engine=='MolSysMT':

        coordinates = get(molecular_system, element='system', structure_indices=structure_indices, coordinates=True)
        coordinates_value, coordinates_unit = puw.get_value_and_unit(coordinates)

        if groups_of_atoms is None:
            if is_all(selection):
                atom_indices='all'
            else:
                atom_indices = select(molecular_system, selection=selection, syntax=syntax)
            center = msmlib.structure.get_center(coordinates_value, atom_indices, weights)
        else:
            center = msmlib.structure.get_center_groups(coordinates_value, groups_of_atoms, weights)

        center = puw.quantity(center, coordinates_unit)
        center = puw.standardize(center)

        return center

    else:

        raise NotImplementedMethodError()



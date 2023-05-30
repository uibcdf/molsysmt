from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt import lib as msmlib
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np
import gc

@digest()
def get_center(molecular_system, selection='all', groups_of_atoms=None, center_of_mass=False, weights=None,
        structure_indices='all', syntax='MolSysMT', engine='MolSysMT'):

    from molsysmt.basic import select, get

    if engine=='MolSysMT':

        if groups_of_atoms is None:

            coordinates = get(molecular_system, element='atom', selection=selection,
                    structure_indices=structure_indices, coordinates=True)
            coordinates, length_unit = puw.get_value_and_unit(coordinates)

            if weights is None:
                weights = np.ones((coordinates.shape[1]), dtype=np.float64)

            center = msmlib.structure.get_center(coordinates, weights)
            center = puw.quantity(center, length_unit)

            del(coordinates, length_unit)

        else:

            if weights is None:
                n_groups = len(groups_of_atoms)
                weights = []
                for group_of_atoms in groups_of_atoms:
                    weights.append([1.0 for ii in range(len(group_of_atoms))])
            center = msmlib.structure.get_center_groups(coordinates_value, groups_of_atoms, weights)


        center = puw.standardize(center)

        gc.collect()

        return center

    else:

        raise NotImplementedMethodError()



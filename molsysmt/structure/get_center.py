from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.math import serialized_lists
from molsysmt.lib import com as libcom
from molsysmt import puw
import numpy as np

@digest()
def get_center(molecular_system, selection='all', groups_of_atoms=None, weights=None,
        structure_indices='all', syntax='MolSysMT', engine='MolSysMT'):

    from molsysmt.basic import select, get

    if engine=='MolSysMT':

        if groups_of_atoms is None:
            atom_indices = select(molecular_system, selection=selection, syntax=syntax)
            groups_of_atoms = [atom_indices]

        groups_serialized = serialized_lists(groups_of_atoms, dtype='int64')

        if weights is None:
            weights = np.ones((groups_serialized.n_values))
        elif isinstance(weights, str):
            raise NotImplementedMethodError()

        coordinates = get(molecular_system, element='system', structure_indices=structure_indices, coordinates=True)

        length_units = puw.get_unit(coordinates)
        coordinates = np.asfortranarray(puw.get_value(coordinates), dtype='float64')
        n_atoms = coordinates.shape[1]
        n_structures = coordinates.shape[0]

        com = libcom.center_of_mass(coordinates,
                                    groups_serialized.indices, groups_serialized.values, groups_serialized.starts,
                                    weights, n_structures, n_atoms,
                                    groups_serialized.n_indices, groups_serialized.n_values)

        del(coordinates, groups_serialized)

        return com*length_units

    else:

        raise NotImplementedMethodError()



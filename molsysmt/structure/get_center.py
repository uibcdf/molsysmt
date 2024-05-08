from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt import lib as msmlib
from molsysmt._private.variables import is_all, is_iterable_of_iterables
from molsysmt import pyunitwizard as puw
import numpy as np
import gc

@digest()
def get_center(molecular_system, selection='all', weights=None,
        structure_indices='all', syntax='MolSysMT', engine='MolSysMT', skip_digestion=False):

    from molsysmt.basic import select, get

    if engine=='MolSysMT':

        atom_indices = select(molecular_system, selection=selection)

        if not is_iterable_of_iterables(atom_indices):

            coordinates = get(molecular_system, element='atom', selection=atom_indices,
                    structure_indices=structure_indices, coordinates=True)
            coordinates, length_unit = puw.get_value_and_unit(coordinates)

            if weights is None:
                weights = np.ones((coordinates.shape[1]), dtype=np.float64)

            center = msmlib.structure.get_center(coordinates, weights)
            center = puw.quantity(center, length_unit)

            del(coordinates, length_unit)

        else:

            atoms_per_group = np.array([len(group) for group in atom_indices], dtype=np.int64)
            groups_of_atoms = np.concatenate(atom_indices)
            coordinates = get(molecular_system, element='atom', selection=groups_of_atoms,
                    structure_indices=structure_indices, coordinates=True)
            coordinates, length_unit = puw.get_value_and_unit(coordinates)

            if weights is None:
                weights = np.ones((coordinates.shape[1]), dtype=np.float64)
            else:
                weights = np.concatenate(weights)

            center = msmlib.structure.get_center_groups_of_atoms(coordinates, atoms_per_group, weights)
            center = puw.quantity(center, length_unit)

            del(coordinates, length_unit, groups_of_atoms, weights)

        center = puw.standardize(center)

        gc.collect()

        return center

    else:

        raise NotImplementedMethodError()


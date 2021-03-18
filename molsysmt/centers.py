from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools._digestion import *
from molsysmt.lib import com as libcom
from molsysmt.lib import geometry as libgeometry
from molsysmt import puw
import numpy as np

def center(molecular_system, selection='all', groups_of_atoms=None, weights=None, frame_indices='all', syntaxis='MolSysMT', engine='MolSysMT', parallel=False):

    from molsysmt.multitool import convert, select, get, extract
    from molsysmt._private_tools.math import serialized_lists

    molecular_system = digest_molecular_system(molecular_system)
    engine = digest_engine(engine)

    if engine=='MolSysMT':

        if groups_of_atoms is None:
            atom_indices = select(molecular_system, selection=selection, syntaxis=syntaxis)
            groups_of_atoms = [atom_indices]

        groups_serialized = serialized_lists(groups_of_atoms, dtype='int64')

        if weights is None:
            weights_array = np.ones((groups_serialized.n_values))
        elif weights=='masses':
            raise NotImplementedError
            #weights_array = get(item, selection=groups_serialized.values, masses=True)

        coordinates = get(molecular_system, target='system', frame_indices=frame_indices, coordinates=True)

        length_units = puw.get_unit(coordinates)
        coordinates = np.asfortranarray(puw.get_value(coordinates), dtype='float64')
        n_atoms = coordinates.shape[1]
        n_frames = coordinates.shape[0]

        com = libcom.center_of_mass(coordinates,
                                    groups_serialized.indices, groups_serialized.values, groups_serialized.starts,
                                    weights_array, n_frames, n_atoms,
                                    groups_serialized.n_indices, groups_serialized.n_values)

        del(coordinates, groups_serialized, weights_array)

        return com*length_units

    else:

        raise NotImplementedError(NotImplementedMessage)


def geometric_center(molecular_system, selection='all', groups_of_atoms=None, frame_indices='all', syntaxis='MolSysMT', engine='MolSysMT', parallel=False):

    return center(molecular_system, selection=selection, groups_of_atoms=groups_of_atoms, weights=None, frame_indices=frame_indices, syntaxis=syntaxis,
                  engine=engine, parallel=parallel)

def center_of_mass(molecular_system, selection='all', groups_of_atoms=None, frame_indices='all', syntaxis='MolSysMT', engine='MolSysMT', parallel=False):

    return center(molecular_system, selection=selection, groups_of_atoms=groups_of_atoms, weights='masses', frame_indices=frame_indices, syntaxis=syntaxis,
                  engine=engine, parallel=parallel)

def recenter(molecular_system, selection='all', center_of_selection='all', weights=None, new_coordinates_center=None, frame_indices='all',
             syntaxis='MolSysMT', engine='MolSysMT', in_place=True):

    from molsysmt.multitool import select, get, set, copy
    from molsysmt.geometrical_transformations import translate

    molecular_system = digest_molecular_system(molecular_system)
    frame_indices = digest_frame_indices(frame_indices)
    engine = digest_engine(engine)

    if engine=='MolSysMT':

        coordinates_selection_center = center(molecular_system, selection=center_of_selection, groups_of_atoms=None, weights=weights,
                                              frame_indices=frame_indices, syntaxis=syntaxis, engine=engine)

        if new_coordinates_center is None:
            translation = -coordinates_selection_center
        else:
            translation = new_coordinates_center-coordinates_selection_center

        del(coordinates_selection_center)

        return translate(molecular_system, translation=translation, selection=selection, frame_indices=frame_indices, syntaxis='MolSysMT', in_place=True)

    else:

        raise NotImplementedError()


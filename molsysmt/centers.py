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
        coordinates = _np.asfortranarray(puw.get_value(coordinates), dtype='float64')
        n_atoms = coordinates.shape[1]
        n_frames = coordinates.shape[0]
        n_frame_indices = len(frame_indices)

        com = libcom.center_of_mass(coordinates,
                                    groups_serialized.indices, groups_serialized.values, groups_serialized.starts,
                                    weights_array, frame_indices, n_frames, n_atoms,
                                    groups_serialized.n_indices, groups_serialized.n_values,
                                    n_frame_indices)

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

def recenter(molecular_system, selection='all', selection_center='all', coordinates_center=None, center_of_selection='geometric_center', frame_indices='all',
             syntaxis='MolSysMT', engine='MolSysMT'):

    from molsysmt.multitool import select, get, set, copy

    molecular_system = digest_molecular_system(molecular_system)
    frame_indices = digest_frame_indices(frame_indices)
    engine = digest_engine(engine)

    tmp_molecular_system = copy(molecular_system)
    tmp_molecular_system = digest_molecular_system(molecular_system)

    if engine=='MolSysMT':

        n_atoms = get(molecular_system, n_atoms=True)
        coordinates = get(tmp_item, target='system', coordinates=True, frame_indices=frame_indices)
        n_frames = coordinates.shape[0]
        length_units = puw.get_unit(coordinates)

        if coordinates_center is None:
            coordinates_center = np.zeros([n_frames,3], dtype='float64')*length_units

        if center_of_selection == 'geometric_center':
            coordinates_selection_center = geometric_center(tmp_molecular_system, selection=selection_center, groups_of_atoms=None,
                                           frame_indices=frame_indices, syntaxis=syntaxis, engine=engine)

        translation = coordinates_center - coordinates_selection_center[:,0,:]
        del(coordinates_center, coordinates_selection_center)

        coordinates = np.asfortranarray(puw.get_value(coordinates), dtype='float64')
        translation = np.asfortranarray(puw.get_value(translation), dtype='float64')

        libgeometry.translate(coordinates, translation, frame_indices, n_atoms, n_frames, n_frames)
        #### Tengo que sustituir esto con el método translate de geometrical transformations

        coordinates=np.ascontiguousarray(coordinates)*length_units

        set(tmp_item, coordinates=coordinates, frame_indices=frame_indices)

        del(coordinates, translation, length_units)

        return tmp_item

    else:

        raise NotImplementedError(NotImplementedMessage)


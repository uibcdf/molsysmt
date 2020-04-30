from .utils.engines import digest as _digest_engines
from .utils.forms import digest as _digest_forms
from .lib import com as _libcom
from .lib import geometry as _libgeometry
import numpy as _np
from .utils.exceptions import *

def center(item=None, selection=None, groups_of_atoms=None, weights=None, frame_indices='all',
           syntaxis='MolSysMT', engine='MolSysMT', parallel=False):

    from molsysmt import convert, select, get, extract
    from molsysmt.utils.math import serialized_lists

    engine = _digest_engines(engine)
    form_in, _ = _digest_forms(item, engine)

    if frame_indices is 'all':
        n_frames = get(item, n_frames=True)
        frame_indices = _np.arange(n_frames)
    elif type(frame_indices)==int:
        frame_indices = [frame_indices]

    if engine=='MolSysMT':

        if groups_of_atoms is None:
            atom_indices = select(item, selection=selection, syntaxis=syntaxis)
            groups_of_atoms = [atom_indices]

        groups_serialized = serialized_lists(groups_of_atoms, dtype='int64')

        if weights is None:
            weights_array = _np.ones((groups_serialized.n_values))
        elif weights=='masses':
            weights_array = get(item, selection=groups_serialized.values, masses=True)

        coordinates = get(item, coordinates=True, frame_indices='all')

        length_units = coordinates.unit
        coordinates = _np.asfortranarray(coordinates._value, dtype='float64')
        n_atoms = coordinates.shape[1]
        n_frames = coordinates.shape[0]
        n_frame_indices = len(frame_indices)

        com = _libcom.center_of_mass(coordinates,
                                     groups_serialized.indices, groups_serialized.values, groups_serialized.starts,
                                     weights_array, frame_indices, n_frames, n_atoms,
                                     groups_serialized.n_indices, groups_serialized.n_values,
                                     n_frame_indices)

        del(coordinates, groups_serialized, weights_array)

        return com*length_units

    else:

        raise NotImplementedError(NotImplementedMessage)


def geometric_center(item=None, selection=None, groups_of_atoms=None, frame_indices='all',
                   syntaxis='MolSysMT', engine='MolSysMT', parallel=False):

    return center(item=item, selection=selection, groups_of_atoms=groups_of_atoms,
                  weights=None, frame_indices=frame_indices, syntaxis=syntaxis,
                  engine=engine, parallel=parallel)

def center_of_mass(item=None, selection=None, groups_of_atoms=None, frame_indices='all',
                   syntaxis='MolSysMT', engine='MolSysMT', parallel=False):

    return center(item=item, selection=selection, groups_of_atoms=groups_of_atoms,
                  weights='masses', frame_indices=frame_indices, syntaxis=syntaxis,
                  engine=engine, parallel=parallel)


def recenter(item, selection='all', selection_center='all', coordinates_center=None,
        center_of_selection='geometric_center', frame_indices='all', syntaxis='MolSysMT', engine='MolSysMT'):

    from molsysmt import select, get, duplicate
    from molsysmt import set as _set

    engine = _digest_engines(engine)
    form_in, _ = _digest_forms(item, engine)
    tmp_item = duplicate(item)

    if frame_indices == 'all':
        n_frames = get(item, n_frames=True)
        frame_indices = _np.arange(n_frames)
    elif type(frame_indices)==int:
        frame_indices = [frame_indices]

    if engine=='MolSysMT':

        n_atoms = get(item, n_atoms=True)
        n_frame_indices = len(frame_indices)
        coordinates = get(tmp_item, coordinates=True, frame_indices='all')
        n_frames = coordinates.shape[0]
        length_units = coordinates.unit

        if coordinates_center is None:
            coordinates_center = _np.zeros([n_frame_indices,3],dtype='float64')*length_units

        if center_of_selection == 'geometric_center':
            coordinates_selection_center = geometric_center(item=tmp_item, selection=selection_center, groups_of_atoms=None,
                                           frame_indices=frame_indices, syntaxis=syntaxis, engine=engine)

        translation = coordinates_center - coordinates_selection_center[:,0,:]
        del(coordinates_center, coordinates_selection_center)

        coordinates = _np.asfortranarray(coordinates._value, dtype='float64')
        translation = _np.asfortranarray(translation._value, dtype='float64')

        _libgeometry.translate(coordinates, translation, frame_indices, n_atoms, n_frames,
                n_frame_indices)

        coordinates=_np.ascontiguousarray(coordinates)*length_units

        _set(tmp_item, coordinates=coordinates)

        del(coordinates, translation, length_units)

        return tmp_item

    else:

        raise NotImplementedError(NotImplementedMessage)


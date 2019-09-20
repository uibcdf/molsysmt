from .utils.engines import digest as _digest_engines
from .utils.forms import digest as _digest_forms
from .lib import com as _libcom
from .lib import geometry as _libgeometry
import numpy as _np
from .utils.exceptions import *

def center(item=None, selection=None, selection_groups=None, weights=None, frame_indices='all',
           syntaxis='MDTraj', engine='MolModMT', parallel=False):

    from molmodmt import convert, select, get, extract
    from molmodmt.utils.math import serialized_lists

    engine = _digest_engines(engine)
    form_in, _ = _digest_forms(item, engine)

    if frame_indices == 'all':
        n_frames = get(item, n_frames=True)
        frame_indices = _np.arange(n_frames)
    elif type(frame_indices)==int:
        frame_indices = [frame_indices]

    if engine=='MolModMT':

        if selection_groups is None:
            atom_indices = select(item, selection, syntaxis)
            selection_groups = [atom_indices]

        groups_serialized = serialized_lists(selection_groups, dtype='int64')

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


def geometrical_center(item=None, selection=None, selection_groups=None, frame_indices='all',
                   syntaxis='MDTraj', engine='MolModMT', parallel=False):

    return center(item=item, selection=selection, selection_groups=selection_groups,
                  weights=None, frame_indices=frame_indices, syntaxis=syntaxis,
                  engine=engine, parallel=parallel)

def center_of_mass(item=None, selection=None, selection_groups=None, frame_indices='all',
                   syntaxis='MDTraj', engine='MolModMT', parallel=False):

    return center(item=item, selection=selection, selection_groups=selection_groups,
                  weights='masses', frame_indices=frame_indices, syntaxis=syntaxis,
                  engine=engine, parallel=parallel)


def recenter(item, selection_center=None, selection='all', weights=None, syntaxis='MDTraj', engine='MolModMT'):

    from molmodmt import convert, select, get
    from molmodmt.math import serialize_list_of_lists

    syntaxis = _digest_engines(syntaxis)
    engine = _digest_engines(engine)
    form_in, form_out = _digest_forms(item, engine)
    tmp_item = convert(item, engine)

    if engine=='MolModMT':

        center_to_origin = center(item=tmp_item, selection=selection_center, selection_groups=None,
                                  weights=weigths, frame_indices='all', syntaxis=syntaxis, engine=engine)

        translation = - center_to_origin[:,0,:]
        del(center_to_origin)

        aux = tmp_item.trajectory
        aux.coordinates = _np.asfortranarray(aux.coordinates, dtype='float64')
        _libgeometry.translate(aux.coordinates, translation, aux.n_frames, aux.n_atoms)
        aux.coordinates=_np.ascontiguousarray(self.aux)

        del(translation)

        tmp_item = convert(tmp_item, form_out)
        return tmp_item

    else:

        raise NotImplementedError(NotImplementedMessage)


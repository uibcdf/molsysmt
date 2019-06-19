from .utils.engines import digest as _digest_engines
from .utils.forms import digest as _digest_forms
from .lib import com as _libcom
from .lib import geometry as _libgeometry
import numpy as _np
from .utils.exceptions import *

def center(item=None, selection=None, selection_groups=None, weights=None, frame_indices='all',
           parallel=False, syntaxis='MDTraj', engine='MolModMT'):

    from molmodmt import convert, select, get, extract
    from molmodmt.math import serialized_lists

    syntaxis = _digest_engines(syntaxis)
    engine = _digest_engines(engine)
    form_in, form_out = _digest_forms(item, engine)
    tmp_item = convert(item, engine)

    if engine=='MolModMT':

        if selection_groups is None:
            atom_indices = select(tmp_item, selection, syntaxis)
            selection_groups = [atom_indices]

        groups_serialized = serialized_lists(selection_groups, fortran=False, dtype=int64)

        if frame_indices=='all':
            frame_indices = _np.arange(tmp_item.trajectory.n_frames, dtype=int64)
        else:
            frame_indices = _np.astype(frame_indices, dtype=int64)

        if weights is None:
            weights_array = _np.ones((groups_serialized.n_values))
        elif weights=='masses':
            weights_array = get(tmp_item, selection=groups_serialized.values, masses=True)

        aux = tmp.trajectory
        aux.coordinates = _np.asfortranarray(aux.coordinates, dtype='float64')
        com = _libcom.center_of_mass(aux.coordinates, groups_serialized.values,
                                     groups_serialized.starts, weights_array, frame_indices,
                                     aux.n_frames, aux.n_atoms, groups_serialized.n_values,
                                     groups_serialized.n_lists, frame_indices.shape[0])
        aux.coordinates = _np.ascontiguousarray(aux.coordinates)
        del(tmp_item, groups_serialized, weights_array)

        return com

    else:

        raise NotImplementedError(NotImplementedMessage)



def geometrical_center(item=None, selection=None, selection_groups=None, frame=None,
                                      parallel=False, engine='molmodmt'):

    return center(item=item, selection=selection, selection_groups=selection_groups,
                                weights=None, frame=frame, parallel=parallel, engine=engine)

def center_of_mass(item=None, selection=None, selection_groups=None, frame=None,
                                      parallel=False, engine='molmodmt'):

    return center(item=item, selection=selection, selection_groups=selection_groups,
                                weights='masses', frame=frame, parallel=parallel, engine=engine)


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


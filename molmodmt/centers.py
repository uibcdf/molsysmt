from .utils.engines import digest as _digest_engines
from .utils.forms import digest as _digest_forms

import numpy as _np
from .utils.digest_inputs import _one_system as _digest_one_system
from .utils.digest_inputs import _coordinates as _digest_coordinates
from .lib import com as _libcom
from .utils.exceptions import *

def center(item=None, selection=None, selection_groups=None, weights=None, frame_indices=None,
           parallel=False, syntaxis='MDTraj', engine='MolModMT'):

    from molmodmt import convert, select, get
    from molmodmt.math import serialize_list_of_lists

    syntaxis = _digest_engines(syntaxis)
    engine = _digest_engines(engine)
    form_in, form_out = _digest_forms(item, engine)
    tmp_item = convert(item, engine)

    if engine=='MolModMT':

        if selection_groups is None:




    if engine=='molmodmt':

        if selection_groups is None:

            tmp_item, atom_indices, frame_indices = _digest_one_system(item, selection, frame,
                                                                          form='molmodmt.Trajectory')
            tmp_coors = _digest_coordinates(tmp_item, atom_indices, frame_indices,
                                             form='molmodmt.Trajectory')
            tmp_nframes=tmp_coors.shape[0]
            tmp_natoms =tmp_coors.shape[1]

            if weights is None:
                weights_array = _np.ones((atom_indices.shape[0]))
            elif weights=='masses':
                weights_array = _get(tmp_item, selection=atom_indices, masses=True)

            com = _libcom.center_of_mass(tmp_coors, weights_array, tmp_nframes, tmp_natoms)
            del(tmp_item1, atom_indices1, frame_indices1)
            del(tmp_coors1, tmp_nframes, tmp_natoms)
            return com

        else:

            tmp_item, atom_indices, frame_indices= _digest_one_system(item, selection, frame,
                                                               engine='molmodmt')
            com=[]
            for group in selection_groups:
                tmp_coors = _digest_coordinates(tmp_item, group, frame_indices, engine='molmodmt')
                tmp_nframes=tmp_coors.shape[0]
                tmp_natoms =tmp_coors.shape[1]
                if weights is None:
                    weights_array = _np.ones(tmp_natoms)
                elif weights=='masses':
                    weights_array = _get(tmp_item, selection=group, masses=True)
                tmp_com = _libcom.center_of_mass(tmp_coors, weights_array, tmp_nframes, tmp_natoms)
                com.append(tmp_com.reshape(tmp_coors.shape[0],1,3))
            com=_np.concatenate(com,axis=1)

        del(tmp_item, atom_indices, frame_indices, tmp_coors)
        del(masses)

        return com

    elif engine=='mdtraj':

        if weights=='masses':
            from mdtraj import compute_center_of_mass as _mdtraj_center_of_mass
            tmp_item1, atom_indices1, frame_indices1 = _digest_one_system(item, selection, frame,
                                                                      engine='mdtraj')
            tmp_item = _extract(tmp_item1,atom_indices1)
            com = _mdtraj_center_of_mass(tmp_item)
            del(tmp_item1, tmp_item, atom_indices1, frame_indices1)

            return com

        else:
            raise NotImplementedError(NotImplementedMessage)

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


def recenter(item, selection='all', weights=None, syntaxis='MDTraj', engine='MolModMT'):

    from molmodmt import convert, select, get
    from molmodmt.math import serialize_list_of_lists

    syntaxis = _digest_engines(syntaxis)
    engine = _digest_engines(engine)
    form_in, form_out = _digest_forms(item, engine)
    tmp_item = convert(item, engine)

    if engine=='MolModMT':

        atom_indices = _select(tmp_item, selection, syntaxis)

        if weights=='masses':
            weights_array = get(tmp_item, atom_indices, masses=True)
        elif weights is None:
            weights_array = _np.ones(atom_indices.shape[0], dtype=int)

        aux = tmp_item.trajectory
        aux.coordinates = _np.asfortranarray(aux.coordinates, dtype='float64')
        _libcom.recenter(aux.coordinates, atom_indices, weights_array,
                         aux.n_frames, aux.n_atoms, atom_indices.shape[0])
        aux.coordinates=_np.ascontiguousarray(self.aux)

        return convert(tmp_item, form_out)

    else:

        raise NotImplementedError(NotImplementedMessage)


import numpy as _np
from .multitool import get_form as _get_form, select as _select, get as _get
from .multitool import convert as _convert, extract as _extract
from .utils.digest_inputs import _one_system as _digest_one_system
from .utils.digest_inputs import _coordinates as _digest_coordinates
from .lib import geometry as _libgeometry
from .utils.exceptions import *

def geometrical_center(item=None, selection=None, selection_groups=None, frame=None,
                       pbc=False, parallel=False, engine='molmodmt'):

    if engine=='molmodmt':

        if selection_groups is None:

            tmp_item1, atom_indices1, frame_indices1 = _digest_one_system(item, selection, frame,
                                                                          form='molmodmt.Trajectory')
            tmp_coors1 = _digest_coordinates(tmp_item1, atom_indices1, frame_indices1,
                                             form='molmodmt.Trajectory')
            tmp_nframes=tmp_coors1.shape[0]
            tmp_natoms =tmp_coors1.shape[1]

            masses = _np.ones((atom_indices1.shape[0]))
            com = _libgeometry.center_of_mass(tmp_coors1, masses, tmp_nframes, tmp_natoms)
            del(tmp_item1, atom_indices1, frame_indices1)
            del(tmp_coors1, tmp_nframes, tmp_natoms)
            return com

        else:

            tmp_item1, atom_indices1 , frame_indices1 = _digest_one_system(item, selection, frame,
                                                               engine='molmodmt')
            com=[]
            for group in selection_groups:
                tmp_coors1 = _digest_coordinates(tmp_item1, group, frame_indices1, engine='molmodmt')
                tmp_nframes=tmp_coors1.shape[0]
                tmp_natoms =tmp_coors1.shape[1]
                masses = _np.ones((tmp_coors1.shape[1]))
                tmp_com = _libgeometry.center_of_mass(tmp_coors1, masses,
                                                  tmp_nframes, tmp_natoms)
                com.append(tmp_com.reshape(tmp_coors1.shape[0],1,3))
            com=_np.concatenate(com,axis=1)

        del(tmp_item1, atom_indices1, frame_indices1, tmp_coors1)
        del(masses)

        return com

    else:

        raise NotImplementedError(NotImplementedMessage)


def center_of_mass(item=None, selection=None, selection_groups=None, frame=None,
                   pbc=False, parallel=False, engine='molmodmt'):

    if engine=='molmodmt':

        if selection_groups is None:

            tmp_item1, atom_indices1, frame_indices1 = _digest_one_system(item, selection, frame, engine='molmodmt')
            tmp_coors1 = _digest_coordinates(tmp_item1, atom_indices1, frame_indices1, engine='molmodmt')
            tmp_nframes=tmp_coors1.shape[0]
            tmp_natoms =tmp_coors1.shape[1]

            masses = _get(item, selection=selection, masses=True)

            com = _libgeometry.center_of_mass(tmp_coors1, masses, tmp_nframes, tmp_natoms)

        else:

            tmp_item1, atom_indices1 , frame_indices1 = _digest_one_system(item, selection, frame,
                                                               engine='molmodmt')
            com=[]
            for group in selection_groups:
                tmp_coors1 = _digest_coordinates(tmp_item1, group, frame_indices1, engine='molmodmt')
                tmp_nframes=tmp_coors1.shape[0]
                tmp_natoms =tmp_coors1.shape[1]
                masses = _get(tmp_item1, selection=group, masses=True)
                tmp_com = _libgeometry.center_of_mass(tmp_coors1, masses, tmp_nframes, tmp_natoms)
                com.append(tmp_com.reshape(tmp_coors1.shape[0],1,3))

            com=_np.concatenate(com,axis=1)

        del(tmp_item1, atom_indices1, frame_indices1, tmp_coors1)
        del(masses)

        return com

    elif engine=='mdtraj':

        from mdtraj import compute_center_of_mass as _mdtraj_center_of_mass

        tmp_item1, atom_indices1, frame_indices1 = _digest_one_system(item, selection, frame,
                                                                      engine='mdtraj')
        tmp_item = _extract(tmp_item1,atom_indices1)
        com = _mdtraj_center_of_mass(tmp_item)
        del(tmp_item1, tmp_item, atom_indices1, frame_indices1)

        return com

    else:

        raise NotImplementedError(NotImplementedMessage)



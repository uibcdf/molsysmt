import numpy as _np
from .multitool import get_form as _get_form, get_shape as _get_shape, select as _select, convert as _convert
from .utils.digest_inputs import _one_system as _digest_one_system
from .lib import com as _libcom
from .utils.exceptions import *

def geometrical_center(item=None, selection=None, frame=None,
                       pbc=False, parallel=False, engine='molmodmt'):

    if engine=='molmodmt':

        tmp_item1, atom_indices1, frame_indices1 = _digest_one_system(item, selection, frame, engine='molmodmt')

        tmp_coors1=tmp_item1.trajectory.coordinates[]

        com = _libcom.weighted_center_compact_structure(diff_selection,
                                         tmp_coors1,
                                         tmp_coors2,
                                         tmp_item1.trajectory.box,
                                         tmp_item1.trajectory.invbox,
                                         tmp_item1.trajectory.orthogonal,
                                         pbc,
                                         nelements1,
                                         nelements2,
                                         tmp_item1.trajectory.nframes)

    else:
        raise NotImplementedError(NotImplementedMessage)


def center_of_mass(item=None, selection=None, frame=None, pbc=False,
                   parallel=False, engine='molmodmt'):

    if engine=='molmodmt':

        tmp_item1, atom_indices1, frame_indices1, tmp_item2, atom_indices2, frame_indices2,\
        single_item, diff_selection = _digest_comparison_two_systems(item, selection, frame,\
                                                                       item2, selection2, frame2,\
                                                                       engine='molmodmt')

        com = _libgeometry.distance_titi(diff_selection,
                                                   tmp_coors1,
                                                   tmp_coors2,
                                                   tmp_item1.trajectory.box,
                                                   tmp_item1.trajectory.invbox,
                                                   tmp_item1.trajectory.orthogonal,
                                                   pbc,
                                                   nelements1,
                                                   nelements2,
                                                   tmp_item1.trajectory.nframes)

    elif engine=='mdtraj':

        tmp_item1, atom_indices1, frame_indices1, tmp_item2, atom_indices2, frame_indices2,\
        single_item, single_selection = _digest_comparison_two_systems(item, selection, frame,\
                                                                       item2, selection2, frame2,\
                                                                       engine='mdtraj')

    else:
        raise NotImplementedError(NotImplementedMessage)



import numpy as _np
from .multitool import get_form as _get_form, get_shape as _get_shape, select as _select, convert as _convert
from .utils.digest_inputs import _comparison_two_systems as _digest_comparison_two_systems
from .lib import geometry as _libs_geometry
from .utils.exceptions import *

def distances(item=None, selection=None, selection_groups=None, group_behavior=None, frame=None,
             item2=None, selection2=None, selection_groups2=None, group_behavior2=None, frame2=None,
             pbc=False, parallel=False, engine='native', output_form='matrix'):

    # group_behavior in ['False','center_of_mass','geometric_center','minimum_distance']
    # output_form in ['matrix','dict']

    # selection groups está por si quiero distancias entre centros de masas, necesita
    # hacer un lista de listas frente a otra lista de listas.

    if selection_groups is not None:
        if selection_groups2 is not None:
            selection_groups2=selection_groups

    if engine=='native':

        tmp_item1, atom_indices1, frame_indices1, tmp_item2, atom_indices2, frame_indices2,
        single_item = _digest_comparison_two_systems(item, selection, frame, item2, selection2,
                                                     frame2, engine='mdtraj')

        if (group_behavior is None) and (group_behavior2 is None):
            dists = _libs_geometry.distance (coors1=coors1, coors2=coors2,
                                             selection1=atom_indices1, selection2=atom_indices2,
                                             selection_groups1=selection_groups,
                                             selection_groups2=selection_groups2,
                                             frame1=frame1, frame2=frame2,
                                             pbc=pbc, single_set=single_item)

        raise NotImplementedError(NotImplementedMessage)

    elif engine=='mdtraj':

        tmp_item1, atom_indices1, frame_indices1, tmp_item2, atom_indices2, frame_indices2 = \
        _digest_comparison_two_systems(item, selection, frame, item2, selection2, frame2,
                                       engine='mdtraj')

        if (group_behavior is None) and (group_behavior2 is None):
            if item2 is None:
                from mdtraj import compute_distances as _mdtraj_compute_distances
                tensor1_to_grid, tensor2_to_grid = _np.meshgrid(atom_indices1,atom_indices2)
                pairs_list =_np.vstack([tensor1_to_grid.ravel(), tensor2_to_grid.ravel()]).T
                dists = _mdtraj_compute_distances(tmp_item1,pairs_list,pbc)
                del(_mdtraj_compute_distances,pairs_list)
                if output_form=='matrix':
                    return dists.reshape(len(atom_indices2),len(atom_indices1)).T
                elif output_form=='dict':
                    tmp_dict={}
                    for ii,jj,kk in zip(tensor1_to_grid.ravel(),tensor2_to_grid.ravel(),dists[0]):
                        try:
                            tmp_dict[ii][jj]=kk
                        except:
                            tmp_dict[ii]={}
                            tmp_dict[ii][jj]=kk
                    return tmp_dict
                else:
                    raise NotImplementedError(NotImplementedMessage)
            else:
                raise NotImplementedError(NotImplementedMessage)
        else:
            raise NotImplementedError(NotImplementedMessage)

    else:
        raise NotImplementedError(NotImplementedMessage)



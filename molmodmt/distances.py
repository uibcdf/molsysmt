import numpy as _np
from .multitool import get_form as _get_form, get_shape as _get_shape, select as _select, convert as _convert
from .utils.digest_inputs import _comparison_two_systems as _digest_comparison_two_systems
from .utils.digest_inputs import _coordinates as _digest_coordinates
from .lib import geometry as _libgeometry
from .utils.exceptions import *
from .centers import center_of_mass as _center_of_mass
from .centers import geometrical_center as _geometrical_center

def distances(item=None, selection=None, selection_groups=None, group_behavior=None, frame=None,
             item2=None, selection2=None, selection_groups2=None, group_behavior2=None, frame2=None,
             mode='ti_ti', pbc=False, parallel=False, engine='molmodmt', output_form='matrix'):

    # group_behavior in ['False','center_of_mass','geometric_center','minimum_distance']
    # output_form in ['matrix','dict']

    # selection groups está por si quiero distancias entre centros de masas, necesita
    # hacer un lista de listas frente a otra lista de listas.

    if selection_groups is not None:
        if selection_groups2 is not None:
            selection_groups2=selection_groups

    if engine=='molmodmt':

        tmp_item1, atom_indices1, frame_indices1, tmp_item2, atom_indices2, frame_indices2,\
        single_item, diff_selection = _digest_comparison_two_systems(item, selection, frame,\
                                                                       item2, selection2, frame2,\
                                                                       engine='molmodmt')

        if mode=='ti_ti':

            if tmp_item1.trajectory.nframes!=tmp_item2.trajectory.nframes:
                raise BadCallError(BadCallMessage)

            if selection_groups is None:
                tmp_coors1 = _digest_coordinates(tmp_item1,atom_indices1,frame_indices1)
                nelements1 = tmp_coors1.shape[1]
                nframes1   = tmp_coors1.shape[0]
            else:
                if group_behavior == 'center_of_mass':
                    tmp_coors1 = []
                    for group in selection_groups:
                        tmp_coors1.append(_center_of_mass(tmp_item1,group,frame_indices1))
                    return tmp_coors1
                elif group_behavior == 'geometric_center':
                    tmp_coors1 = []
                    for group in selection_groups:
                        tmp_coors1.append(_geometrical_center(tmp_item1,group,frame_indices1))
                    pass

            if selection_groups2 is None:
                tmp_coors2 = _digest_coordinates(tmp_item2,atom_indices2,frame_indices2)
                nelements2 = tmp_coors2.shape[1]
                nframes2   = tmp_coors2.shape[0]
            else:
                if group_behavior == 'center_of_mass':
                    pass
                elif group_behavior == 'geometric_center':
                    pass

            if (group_behavior is None) and (group_behavior2 is None):
                dists = _libgeometry.distance_titi(diff_selection,
                                                   tmp_coors1,
                                                   tmp_coors2,
                                                   tmp_item1.trajectory.box,
                                                   tmp_item1.trajectory.invbox,
                                                   tmp_item1.trajectory.orthogonal,
                                                   pbc,
                                                   nelements1,
                                                   nelements2,
                                                   nframes1)
                if output_form=='matrix':
                    return dists
                elif output_form=='dict':
                    tmp_dict={}
                    for ii in range(len(atom_indices1)):
                        atom1=atom_indices1[ii]
                        tmp_dict[atom1]={}
                        for jj in range(len(atom_indices2)):
                            atom2=atom_indices2[jj]
                            tmp_dict[atom1][atom2]=dists[:,ii,jj]
                    return tmp_dict
                else:
                    raise NotImplementedError(NotImplementedMessage)


        elif mode=='ti_tj':
            raise NotImplementedError(NotImplementedMessage)
        else:
            raise NotImplementedError(NotImplementedMessage)

    elif engine=='mdtraj':

        tmp_item1, atom_indices1, frame_indices1, tmp_item2, atom_indices2, frame_indices2,\
        single_item, single_selection = _digest_comparison_two_systems(item, selection, frame,\
                                                                       item2, selection2, frame2,\
                                                                       engine='mdtraj')

        if (group_behavior is None) and (group_behavior2 is None):
            if item2 is None:
                from mdtraj import compute_distances as _mdtraj_compute_distances
                tensor1_to_grid, tensor2_to_grid = _np.meshgrid(atom_indices1,atom_indices2)
                pairs_list =_np.vstack([tensor1_to_grid.ravel(), tensor2_to_grid.ravel()]).T
                dists = _mdtraj_compute_distances(tmp_item1,pairs_list,pbc)
                if output_form=='matrix':
                    nframes=dists.shape[0]
                    del(_mdtraj_compute_distances,pairs_list)
                    return dists.reshape(len(atom_indices2),len(atom_indices1),nframes).T
                elif output_form=='dict':
                    tmp_dict={}
                    for kk in range(dists.shape[1]):
                        ii=pairs_list[kk,0]
                        jj=pairs_list[kk,1]
                        try:
                            tmp_dict[ii][jj]=dists[:,kk]
                        except:
                            tmp_dict[ii]={}
                            tmp_dict[ii][jj]=dists[:,kk]
                    del(_mdtraj_compute_distances,pairs_list)
                    return tmp_dict
                else:
                    raise NotImplementedError(NotImplementedMessage)
            else:
                raise NotImplementedError(NotImplementedMessage)
        else:
            raise NotImplementedError(NotImplementedMessage)
    else:
        raise NotImplementedError(NotImplementedMessage)



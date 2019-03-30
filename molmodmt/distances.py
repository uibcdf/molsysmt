import numpy as _np
from .multitool import get_form as _get_form, select as _select, convert as _convert
from .utils.digest_inputs import _comparison_two_systems as _digest_comparison_two_systems
from .utils.digest_inputs import _coordinates as _digest_coordinates
from .utils.digest_inputs import _frameslist as _digest_frames
from .lib import geometry as _libgeometry
from .utils.exceptions import *
from .centers import center_of_mass as _center_of_mass
from .centers import geometrical_center as _geometrical_center

def distances(item=None, selection=None, selection_groups=None, group_behavior=None, frame=None,
             item2=None, selection2=None, selection_groups2=None, group_behavior2=None, frame2=None,
             pbc=False, parallel=False, engine='molmodmt', output_form='matrix'):

    # group_behavior in ['False','center_of_mass','geometric_center','minimum_distance']
    # output_form in ['matrix','dict']

    # selection groups está por si quiero distancias entre centros de masas, necesita
    # hacer un lista de listas frente a otra lista de listas.

    if selection_groups is not None:
        if selection_groups2 is None:
            selection_groups2=selection_groups

    if group_behavior=='minimum_distance' or group_behavior2=='minimum_distance':

        if group_behavior=='minimum_distance' and group_behavior2=='minimum_distance':

            num_groups1=len(selection_groups)
            num_groups2=len(selection_groups2)
            frame_indices = _digest_frames(item, frame)
            num_frames=len(frame_indices)
            dists = _np.zeros((num_frames,num_groups1,num_groups2),dtype=float)
            for ii in range(num_groups1):
                group1 = selection_groups[ii]
                for jj in range(num_groups2):
                    group2 = selection_groups2[jj]
                    _, min_dist = min_distances(item=item, selection=group1, frame=frame,
                                                item2=item2, selection2=group2, frame2=frame2,
                                                pbc=pbc, parallel=parallel)
                    dists[:,ii,jj]=min_dist
            del(num_groups1,num_groups2,frame_indices,num_frames,group1,group2)
            return dists
        else:
            raise NotImplementedError(NotImplementedMessage)

    if engine=='molmodmt':

        tmp_item1, atom_indices1, frame_indices1, tmp_item2, atom_indices2, frame_indices2,\
        single_item, diff_selection = _digest_comparison_two_systems(item, selection, frame,
                                                                     item2, selection2, frame2,
                                                                      form='molmodmt.Trajectory')

        if tmp_item1.nframes!=tmp_item2.nframes:
            raise BadCallError(BadCallMessage)

        if selection_groups is None:
            tmp_coors1 = _digest_coordinates(tmp_item1,atom_indices1,frame_indices1)
        else:
            if group_behavior == 'center_of_mass':
                tmp_coors1 = _center_of_mass(tmp_item1,selection_groups=selection_groups,
                                             frame=frame_indices1)
            elif group_behavior == 'geometric_center':
                tmp_coors1 = _geometrical_center(tmp_item1,selection_groups=selection_groups,
                                    frame=frame_indices1)

            atom_indices1=list(range(tmp_coors1.shape[1]))

        nelements1 = tmp_coors1.shape[1]
        nframes1   = tmp_coors1.shape[0]

        if selection_groups2 is None:
            tmp_coors2 = _digest_coordinates(tmp_item2,atom_indices2,frame_indices2)
        else:
            if group_behavior == 'center_of_mass':
                tmp_coors2 = _center_of_mass(tmp_item2,selection_groups=selection_groups2,
                                             frame=frame_indices2)
            elif group_behavior == 'geometric_center':
                tmp_coors2 = _geometrical_center(tmp_item2,selection_groups=selection_groups2,
                                    frame=frame_indices2)
            atom_indices2=list(range(tmp_coors2.shape[1]))

        nelements2 = tmp_coors2.shape[1]
        nframes2   = tmp_coors2.shape[0]

        dists = _libgeometry.distance(diff_selection,
                                           tmp_coors1,
                                           tmp_coors2,
                                           tmp_item1.box,
                                           tmp_item1.invbox,
                                           tmp_item1.orthogonal,
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

    elif engine=='mdtraj':

        tmp_item1, atom_indices1, frame_indices1, tmp_item2, atom_indices2, frame_indices2,\
        single_item, single_selection = _digest_comparison_two_systems(item, selection, frame,\
                                                                       item2, selection2, frame2,\
                                                                       form='mdtraj.Trajectory')

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

def min_distances(item=None, selection=None, selection_groups=None, group_behavior=None, frame=None,
                  item2=None, selection2=None, selection_groups2=None, group_behavior2=None, frame2=None,
                  pbc=False, parallel=False, engine='molmodmt'):

    all_dists= distances(item=item, selection=selection, selection_groups=selection_groups,
                         group_behavior=group_behavior, frame=frame,
                         item2=item2, selection2=selection2, selection_groups2=selection_groups2,
                         group_behavior2=group_behavior2, frame2=frame2,
                         pbc=pbc, parallel=parallel, engine=engine, output_form='matrix')

    shape_matrix=all_dists[0,:,:].shape
    num_frames=all_dists.shape[0]
    min_pairs=_np.empty((num_frames,2),dtype=int)
    min_dists=_np.empty((num_frames),dtype=float)
    for indice_frame in range(num_frames):
        ii = _np.argmin(all_dists[indice_frame,:,:])
        tmp_pair = _np.unravel_index(ii,shape_matrix)
        min_pairs[indice_frame,0] = tmp_pair[0]
        min_pairs[indice_frame,1] = tmp_pair[1]
        min_dists[indice_frame] = all_dists[indice_frame,tmp_pair[0],tmp_pair[1]]

    del(all_dists, shape_matrix, num_frames, indice_frame, ii)

    return min_pairs, min_dists


def contact_map(item=None, selection=None, selection_groups=None, group_behavior=None, frame=None,
                item2=None, selection2=None, selection_groups2=None, group_behavior2=None, frame2=None,
                threshold=None, pbc=False, parallel=False, engine='molmodmt'):

    all_dists= distances(item=item, selection=selection, selection_groups=selection_groups,
                         group_behavior=group_behavior, frame=frame,
                         item2=item2, selection2=selection2, selection_groups2=selection_groups2,
                         group_behavior2=group_behavior2, frame2=frame2,
                         pbc=pbc, parallel=parallel, engine=engine, output_form='matrix')

    if threshold is None:
        raise BadCallError(BadCallMessage)

    num_frames=all_dists.shape[0]
    contact_map=_np.empty(all_dists.shape,dtype=bool)
    for indice_frame in range(num_frames):
        contact_map[indice_frame,:,:]=(all_dists[indice_frame,:,:]<=threshold)

    del(all_dists, num_frames, indice_frame)

    return contact_map

def neighbors_lists(item=None, selection=None, selection_groups=None, group_behavior=None, frame=None,
                    item2=None, selection2=None, selection_groups2=None, group_behavior2=None, frame2=None,
                    threshold=None, num_neighbors=None, pbc=False, parallel=False, engine='molmodmt'):

    all_dists= distances(item=item, selection=selection, selection_groups=selection_groups,
                         group_behavior=group_behavior, frame=frame,
                         item2=item2, selection2=selection2, selection_groups2=selection_groups2,
                         group_behavior2=group_behavior2, frame2=frame2,
                         pbc=pbc, parallel=parallel, engine=engine, output_form='matrix')

    if (threshold is None) and (num_neighbors is None):
        raise BadCallError(BadCallMessage)

    num_frames=all_dists.shape[0]
    num_first_elements=all_dists.shape[1]
    neighbors=[]

    if threshold is not None:
        for indice_frame in range(num_frames):
            neighbors_frame=[]
            for ii in range(num_first_elements):
                tmp_neighbors = _np.argwhere(all_dists[indice_frame,ii,:]<=threshold)[:,0]
                tmp_dists = all_dists[indice_frame,ii,tmp_neighbors]
                sorted_indices = _np.argsort(tmp_dists)
                neighbors_frame.append([tmp_neighbors[sorted_indices],tmp_dists[sorted_indices]])
            neighbors.append(neighbors_frame)
        del(sorted_indices)
    elif num_neighbors is not None:
        for indice_frame in range(num_frames):
            neighbors_frame=[]
            for ii in range(num_first_elements):
                tmp_neighbors = _np.argsort(all_dists[indice_frame,ii,:])[:num_neighbors]
                tmp_dists = all_dists[indice_frame,ii,tmp_neighbors]
                neighbors_frame.append([_np.array(tmp_neighbors,dtype=int),tmp_dists])
            neighbors.append(neighbors_frame)

    del(all_dists, num_frames, indice_frame)
    del(tmp_neighbors,tmp_dists)

    return _np.array(neighbors)



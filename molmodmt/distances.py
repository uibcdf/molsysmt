import numpy as _np
#from .multitool import get_form as _get_form, select as _select, convert as _convert
#from .utils.digest_inputs import _comparison_two_systems as _digest_comparison_two_systems
#from .utils.digest_inputs import _coordinates as _digest_coordinates
#from .utils.digest_inputs import _frameslist as _digest_frames
#from .utils.digest_inputs import _frameslist as _digest_frames
from .lib import geometry as _libgeometry
from .utils.exceptions import *
from .centers import center_of_mass as _center_of_mass
from .centers import geometrical_center as _geometrical_center
from .utils.engines import digest as _digest_engines
from .utils.frame_indices import digest as _digest_frame_indices

def distance(item_1=None, selection_1=None, selection_groups_1=None, group_behavior_1=None, frame_indices_1="all",
             item_2=None, selection_2=None, selection_groups_2=None, group_behavior_2=None, frame_indices_2=None,
             pbc=False, parallel=False, output_form='ndarray', engine='MolModMT', syntaxis='MDTraj'):

    # group_behavior in ['None','center_of_mass','geometric_center','minimum_distance']
    # output_form in ['ndarray','dict']

    # selection groups está por si quiero distancias entre centros de masas, necesita
    # hacer un lista de listas frente a otra lista de listas.

    from molmodmt import convert, select, get, extract

    engine = _digest_engines(engine)
    frame_indices_2 = frame_indices_1

    if group_behavior_1=='minimum_distance' or group_behavior2=='minimum_distance':
        if group_behavior_1=='minimum_distance' and group_behavior2=='minimum_distance':

            num_groups_1=len(selection_groups_1)
            num_groups_2=len(selection_groups_2)
            frame_indices = _digest_frame_indices(item, frame_indices_1)
            num_frames=len(frame_indices)
            dists = _np.zeros((num_frames, num_groups_1, num_groups_2),dtype=float)
            for ii in range(num_groups_1):
                group1 = selection_groups_2[ii]
                for jj in range(num_groups_2):
                    group2 = selection_groups_2[jj]
                    _, min_dist = min_distances(item_1=item_1, selection_1=group1,
                                                frame_indices_1=frame_indices_1,
                                                item_2=item_2, selection_2=group2,
                                                pbc=pbc, parallel=parallel, engine=engine)
                    dists[:,ii,jj]=min_dist
            del(num_groups1,num_groups2,frame_indices,num_frames,group1,group2)
            return dists
        else:
            raise NotImplementedError(NotImplementedMessage)

    if engine=='MolModMT':

        diff_set = True
        same_item = False
        same_selection = False
        same_groups = False

        if item_2 is None:

            item_2 = item_1
            same_item = True

            if (selection_1 is not None) and (selection_2 is None):
                if (selection_groups_2 is None):
                    selection_2 = selection_1
                    same_selection = True
                    diff_set = False

            if selection_groups_1 is not None:
                if (selection_2 is None) and (selection_groups_2 is None):
                    selection_groups_2=selection_groups_1
                    same_groups = True
                    diff_set = False

        if selection_1 is not None:

            atom_indices_1 = select(item_1, selection=selection_1, syntaxis=syntaxis)
            coordinates_1 = get(item_1, element='atom', indices=atom_indices_1,
                            frame_indices=frame_indices_1, coordinates=True)
        else:

            if group_behavior == 'center_of_mass':
                coordinates_1 = _center_of_mass(item_1, selection_groups=selection_groups_1,
                                                frame_indices=frame_indices_1)
            elif group_behavior == 'geometrical_center':
                coordinates_1 = _geometrical_center(item_1,selection_groups=selection_groups_1,
                                                    frame=frame_indices_1)
            atom_indices_1 = list(len(coordinates_1.shape[1]))

        if selection_2 is not None:

            if same_selection:
                atom_indices_2 = _np.copy(atom_indices_1)
                coordinates_2 = _np.copy(coordinates_1)
            else:
                atom_indices_2 = select(item_2, selection=selection_2, syntaxis=syntaxis)
                coordinates_2 = get(item_2, element='atom', indices=atom_indices_2,
                                    frame_indices=frame_indices_2, coordinates=True)

        else:

            if same_groups:
                atom_indices_2 = _np.copy(atom_indices_1)
                coordinates_2 = _np.copy(coordinates_1)
            else:

                if group_behavior == 'center_of_mass':
                    coordinates_2 = _center_of_mass(item_2, selection_groups=selection_groups_2,
                                                frame_indices=frame_indices_2)
                elif group_behavior == 'geometrical_center':
                    coordinates_2 = _geometrical_center(item_2,selection_groups=selection_groups_2,
                                                frame=frame_indices_2)
                atom_indices_2 = list(len(coordinates_2.shape[1]))

        box, box_shape = get(item_1, box=True, box_shape=True, frame_indices=frame_indices_1)
        orthogonal = 0
        if box_shape=='cubic': orthogonal = 1

        length_units = coordinates_1.unit
        coordinates_1 = _np.asfortranarray(coordinates_1._value, dtype='float64')
        coordinates_2 = _np.asfortranarray(coordinates_2._value, dtype='float64')
        nframes = coordinates_1.shape[0]
        nelements1 = coordinates_1.shape[1]
        nelements2 = coordinates_2.shape[1]

        dists = _libgeometry.distance(int(diff_set),
                                      coordinates_1,
                                      coordinates_2,
                                      box,
                                      orthogonal,
                                      int(pbc),
                                      nelements1,
                                      nelements2,
                                      nframes)

        dists = dists*length_units

        if output_form=='ndarray':
             return dists
        elif output_form=='dict':
            tmp_dict={}
            for ii in range(len(atom_indices_1)):
                atom1=atom_indices_1[ii]
                tmp_dict[atom1]={}
                for jj in range(len(atom_indices_2)):
                    atom2=atom_indices_2[jj]
                    tmp_dict[atom1][atom2]=dists[:,ii,jj]
            return tmp_dict
        else:
            raise NotImplementedError(NotImplementedMessage)

    elif engine=='MDTraj':

        #tmp_item1, atom_indices1, frame_indices1, tmp_item2, atom_indices2, frame_indices2,\
        #single_item, single_selection = _digest_comparison_two_systems(item, selection, frame,\
        #                                                               item2, selection2, frame2,\
        #                                                               form='mdtraj.Trajectory')

        #if (group_behavior is None) and (group_behavior2 is None):
        #    if item2 is None:
        #        from mdtraj import compute_distances as _mdtraj_compute_distances
        #        tensor1_to_grid, tensor2_to_grid = _np.meshgrid(atom_indices1,atom_indices2)
        #        pairs_list =_np.vstack([tensor1_to_grid.ravel(), tensor2_to_grid.ravel()]).T
        #        dists = _mdtraj_compute_distances(tmp_item1,pairs_list,pbc)
        #        if output_form=='matrix':
        #            nframes=dists.shape[0]
        #            del(_mdtraj_compute_distances,pairs_list)
        #            return dists.reshape(len(atom_indices2),len(atom_indices1),nframes).T
        #        elif output_form=='dict':
        #            tmp_dict={}
        #            for kk in range(dists.shape[1]):
        #                ii=pairs_list[kk,0]
        #                jj=pairs_list[kk,1]
        #                try:
        #                    tmp_dict[ii][jj]=dists[:,kk]
        #                except:
        #                    tmp_dict[ii]={}
        #                    tmp_dict[ii][jj]=dists[:,kk]
        #            del(_mdtraj_compute_distances,pairs_list)
        #            return tmp_dict
        #        else:
        #            raise NotImplementedError(NotImplementedMessage)
        #    else:
        #        raise NotImplementedError(NotImplementedMessage)
        #else:
        #    raise NotImplementedError(NotImplementedMessage)

        raise NotImplementedError(NotImplementedMessage)
    else:
        raise NotImplementedError(NotImplementedMessage)

def distance_atoms_pairs(item=None, atoms_pairs_list=None, frame=None, pbc=False, parallel=False,
                         engine='molmodmt'):

    pass

def minimum_distance(item_1=None, selection_1=None, selection_groups_1=None, group_behavior_1=None, frame_indices_1="all",
                     item_2=None, selection_2=None, selection_groups_2=None, group_behavior_2=None, frame_indices_2=None,
                     pbc=False, parallel=False, engine='MolModMT', syntaxis='MDTraj'):

    all_dists = distance(item_1=item_1, selection_1=selection_1,
                         selection_groups_1=selection_groups_1, group_behavior_1=group_behavior_1,
                         frame_indices_1=frame_indices_1,
                         item_2=item_2, selection_2=selection_2,
                         selection_groups_2=selection_groups_2, group_behavior_2=group_behavior_2,
                         frame_indices_2=frame_indices_2,
                         pbc=pbc, parallel=parallel, output_form='ndarray', engine=engine,
                         syntaxis=syntaxis):

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


def contact_map(item_1=None, selection_1=None, selection_groups_1=None, group_behavior_1=None, frame_indices_1="all",
                item_2=None, selection_2=None, selection_groups_2=None, group_behavior_2=None, frame_indices_2=None,
                pbc=False, parallel=False, engine='MolModMT', syntaxis='MDTraj'):

    all_dists = distance(item_1=item_1, selection_1=selection_1,
                         selection_groups_1=selection_groups_1, group_behavior_1=group_behavior_1,
                         frame_indices_1=frame_indices_1,
                         item_2=item_2, selection_2=selection_2,
                         selection_groups_2=selection_groups_2, group_behavior_2=group_behavior_2,
                         frame_indices_2=frame_indices_2,
                         pbc=pbc, parallel=parallel, output_form='ndarray', engine=engine,
                         syntaxis=syntaxis):

    if threshold is None:
        raise BadCallError(BadCallMessage)

    num_frames=all_dists.shape[0]
    contact_map=_np.empty(all_dists.shape,dtype=bool)
    for indice_frame in range(num_frames):
        contact_map[indice_frame,:,:]=(all_dists[indice_frame,:,:]<=threshold)

    del(all_dists, num_frames, indice_frame)

    return contact_map

def neighbors_lists(item_1=None, selection_1=None, selection_groups_1=None, group_behavior_1=None, frame_indices_1="all",
                    item_2=None, selection_2=None, selection_groups_2=None, group_behavior_2=None, frame_indices_2=None,
                    pbc=False, parallel=False, engine='MolModMT', syntaxis='MDTraj'):

    all_dists = distance(item_1=item_1, selection_1=selection_1,
                         selection_groups_1=selection_groups_1, group_behavior_1=group_behavior_1,
                         frame_indices_1=frame_indices_1,
                         item_2=item_2, selection_2=selection_2,
                         selection_groups_2=selection_groups_2, group_behavior_2=group_behavior_2,
                         frame_indices_2=frame_indices_2,
                         pbc=pbc, parallel=parallel, output_form='ndarray', engine=engine,
                         syntaxis=syntaxis):

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


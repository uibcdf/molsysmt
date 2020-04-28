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

def distance(item_1=None, selection_1="all", selection_groups_1=None, group_behavior_1=None, frame_indices_1="all",
             item_2=None, selection_2=None, selection_groups_2=None, group_behavior_2=None, frame_indices_2=None,
             pairs=False, crossed_frames=False, pbc=False, parallel=False, output_form='tensor', engine='MolSysMT',
             syntaxis='MDTraj'):

    # group_behavior in
    # ['center_of_mass','geometric_center','minimum_distance','maximum_distance']
    # output_form in ['tensor','dict']

    # crossed_frames es para cuando queremos calcular lista de frames1 contra lista de frames 2
    # (todos con todos), si crossed_frames=False entonces es sólo el primer frame de lista 1 contra
    # el primer frame de lista 2, el segundo contra el segundo, etc.

    # selection groups está por si quiero distancias entre centros de masas, necesita
    # hacer un lista de listas frente a otra lista de listas.

    from molsysmt import convert, select, get, extract

    engine = _digest_engines(engine)

    if group_behavior_1=='minimum_distance' or group_behavior_2=='minimum_distance':
        if group_behavior_1=='minimum_distance' and group_behavior_2=='minimum_distance':
            raise NotImplementedError(NotImplementedMessage)
            #num_groups_1=len(selection_groups_1)
            #num_groups_2=len(selection_groups_2)
            #frame_indices = _digest_frame_indices(item, frame_indices_1)
            #num_frames=len(frame_indices)
            #dists = _np.zeros((num_frames, num_groups_1, num_groups_2),dtype=float)
            #for ii in range(num_groups_1):
            #    group1 = selection_groups_2[ii]
            #    for jj in range(num_groups_2):
            #        group2 = selection_groups_2[jj]
            #        _, min_dist = min_distances(item_1=item_1, selection_1=group1,
            #                                    frame_indices_1=frame_indices_1,
            #                                    item_2=item_2, selection_2=group2,
            #                                    pbc=pbc, parallel=parallel, engine=engine)
            #        dists[:,ii,jj]=min_dist
            #del(num_groups1,num_groups2,frame_indices,num_frames,group1,group2)
            #return dists
        else:
            raise NotImplementedError(NotImplementedMessage)

    if engine=='MolSysMT':

        diff_set = True
        same_item = False
        same_selection = False
        same_groups = False
        same_frames = False

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

        else:
            if (selection_1 is not None) and (selection_2 is None):
                if (selection_groups_2 is None):
                    selection_2 = selection_1

        if frame_indices_2 is None:
            frame_indices_2 = frame_indices_1
            same_frames = True
        else:
            diff_set = True

        frame_indices_1 = _digest_frame_indices(item_1, frame_indices_1)
        frame_indices_2 = _digest_frame_indices(item_2, frame_indices_2)

        if selection_1 is not None:

            atom_indices_1 = select(item_1, selection=selection_1, syntaxis=syntaxis)
            coordinates_1 = get(item_1, target='atom', indices=atom_indices_1,
                            frame_indices=frame_indices_1, coordinates=True)
        else:

            if group_behavior_1 == 'center_of_mass':
                coordinates_1 = _center_of_mass(item_1, selection_groups=selection_groups_1,
                                                frame_indices=frame_indices_1)
                atom_indices_1 = list(len(coordinates_1.shape[1]))
            elif group_behavior_1 == 'geometrical_center':
                coordinates_1 = _geometrical_center(item_1,selection_groups=selection_groups_1,
                                                    frame=frame_indices_1)
                atom_indices_1 = list(len(coordinates_1.shape[1]))
            else:
                raise ValueError("Value of argument group_behavior_1 not recognized.")

        if selection_2 is not None:

            atom_indices_2 = select(item_2, selection=selection_2, syntaxis=syntaxis)
            coordinates_2 = get(item_2, target='atom', indices=atom_indices_2,
                                frame_indices=frame_indices_2, coordinates=True)
        else:

            if same_groups and same_frames:
                atom_indices_2 = _np.copy(atom_indices_1)
                coordinates_2 = _np.copy(coordinates_1)
            else:
                if group_behavior_2 == 'center_of_mass':
                    coordinates_2 = _center_of_mass(item_2, selection_groups=selection_groups_2,
                                                frame_indices=frame_indices_2)
                    atom_indices_2 = list(len(coordinates_2.shape[1]))
                elif group_behavior_2 == 'geometrical_center':
                    coordinates_2 = _geometrical_center(item_2,selection_groups=selection_groups_2,
                                                frame=frame_indices_2)
                else:
                    raise ValueError("Value of argument group_behavior_2 not recognized.")


        length_units = coordinates_1.unit
        coordinates_1 = _np.asfortranarray(coordinates_1._value, dtype='float64')
        coordinates_2 = _np.asfortranarray(coordinates_2._value, dtype='float64')
        nframes_1 = coordinates_1.shape[0]
        nframes_2 = coordinates_2.shape[0]
        nelements1 = coordinates_1.shape[1]
        nelements2 = coordinates_2.shape[1]

        if (nframes_1!=len(frame_indices_1)):
            raise NotImplementedError("Coordinates extraction from item_1 not implemented for frame_indices_1")
        if (nframes_2!=len(frame_indices_2)):
            raise NotImplementedError("Coordinates extraction from item_2 not implemented for frame_indices_2")

        box, box_shape = get(item_1, target='system', box=True, box_shape=True, frame_indices=frame_indices_1)

        orthogonal = 0
        if box_shape == 'cubic':
            orthogonal =1

        if box is None:
            box= _np.zeros([nframes_1,3,3])*length_units

        box = _np.asfortranarray(box._value, dtype='float64')

        if crossed_frames is False:
            if nframes_1 != nframes_2:
                raise ValueError("Both frame_indices_1 and frame_indices_2 need the same number of frames.")
            else:
                if pairs is False:
                    dists = _libgeometry.distance(int(diff_set),
                                                  coordinates_1,
                                                  coordinates_2,
                                                  box,
                                                  orthogonal,
                                                  int(pbc),
                                                  nelements1,
                                                  nelements2,
                                                  nframes_1)
                else:
                    if nframes_1 != nframes_2:
                        raise ValueError("Both selection_1 and selection_2 need the same number of atoms.")
                    else:
                        dists = _libgeometry.distance_pairs(coordinates_1,
                                                            coordinates_2,
                                                            box,
                                                            orthogonal,
                                                            int(pbc),
                                                            nelements1,
                                                            nelements2,
                                                            nframes_1)
        else:
            raise NotImplementedError(NotImplementedMessage)

        del(coordinates_1, coordinates_2, box)

        dists = dists*length_units

        if output_form=='tensor':
             return dists
        elif output_form=='dict':
            if pairs is False:
                if crossed_frames is False:
                    tmp_dict={}
                    for ii in range(len(atom_indices_1)):
                        atom1=atom_indices_1[ii]
                        tmp_dict[atom1]={}
                        for jj in range(len(atom_indices_2)):
                            atom2=atom_indices_2[jj]
                            tmp_dict[atom1][atom2]={}
                            for kk in range(len(frame_indices_1)):
                                frame_index_1 = frame_indices_1[kk]
                                tmp_dict[atom1][atom2][frame_index_1]=dists[kk,ii,jj]
                    return tmp_dict
                else:
                    raise NotImplementedError(NotImplementedMessage)
            else:
                if crossed_frames is False:
                    tmp_dict={}
                    for ii in range(len(atom_indices_1)):
                        atom1=atom_indices_1[ii]
                        atom2=atom_indices_2[ii]
                        if atom1 not in tmp_dict:
                            tmp_dict[atom1]={}
                        if atom2 not in tmp_dict[atom1]:
                            tmp_dict[atom1][atom2]={}
                        for kk in range(len(frame_indices_1)):
                            frame_index_1 = frame_indices_1[kk]
                            tmp_dict[atom1][atom2][frame_index_1]=dists[kk,ii]
                    return tmp_dict
                else:
                    raise NotImplementedError(NotImplementedMessage)
 
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

def minimum_distance(item_1=None, selection_1="all", selection_groups_1=None, group_behavior_1=None,
                     as_entity_1=True, frame_indices_1="all",
                     item_2=None, selection_2=None, selection_groups_2=None, group_behavior_2=None,
                     as_entity_2=True, frame_indices_2=None,
                     pairs=False, pbc=False, parallel=False, engine='MolSysMT', syntaxis='MDTraj'):

    all_dists = distance(item_1=item_1, selection_1=selection_1,
                         selection_groups_1=selection_groups_1, group_behavior_1=group_behavior_1,
                         frame_indices_1=frame_indices_1,
                         item_2=item_2, selection_2=selection_2,
                         selection_groups_2=selection_groups_2, group_behavior_2=group_behavior_2,
                         frame_indices_2=frame_indices_2,
                         pairs=pairs, pbc=pbc, parallel=parallel, output_form='tensor', engine=engine,
                         syntaxis=syntaxis)

    if pairs is False:

        nframes, nelements_1, nelements_2 = all_dists.shape
        length_units = all_dists.unit

        if (as_entity_1 is True) and (as_entity_2 is True):

            pairs=_np.empty((nframes,2),dtype=int)
            dists=_np.empty((nframes),dtype=float)
            for indice_frame in range(nframes):
                ii,jj = _np.unravel_index(all_dists[indice_frame,:,:].argmin(), all_dists[indice_frame,:,:].shape)
                pairs[indice_frame,0] = ii
                pairs[indice_frame,1] = jj
                dists[indice_frame] = all_dists[indice_frame,ii,jj]._value

            del(all_dists)

            dists=dists*length_units

            return pairs, dists

        elif (as_entity_1 is False) and (as_entity_2 is True):

            pairs=_np.empty((nframes, nelements_1), dtype=int)
            dists=_np.empty((nframes, nelements_1), dtype=float)
            for indice_frame in range(nframes):
                for ii in range(nelements_1):
                    jj = all_dists[indice_frame,ii,:].argmin()
                    pairs[indice_frame,ii]=jj
                    dists[indice_frame,ii]=all_dists[indice_frame,ii,jj]._value

            del(all_dists)

            dists=dists*length_units

            return pairs, dists

        elif (as_entity_1 is True) and (as_entity_2 is False):

            pairs=_np.empty((nframes, nelements_2), dtype=int)
            dists=_np.empty((nframes, nelements_2), dtype=float)
            for indice_frame in range(nframes):
                for ii in range(nelements_2):
                    jj = all_dists[indice_frame,:,ii].argmin()
                    pairs[indice_frame,ii]=jj
                    dists[indice_frame,ii]=all_dists[indice_frame,jj,ii]._value

            del(all_dists)

            dists=dists*length_units

            return pairs, dists

        else:
            raise ValueError("If both input arguments 'as_entity_1' and 'as_entity_2' are False, the method you are looking for is molsysmt.distance()")

    else:

        nframes, nelements = all_dists.shape
        length_units = all_dists.unit

        if (as_entity_1 is True) and (as_entity_2 is True):

            pairs=_np.empty((nframes),dtype=int)
            dists=_np.empty((nframes),dtype=float)
            for indice_frame in range(nframes):
                ii = all_dists[indice_frame,:].argmin()
                pairs[indice_frame] = ii
                dists[indice_frame] = all_dists[indice_frame,ii]._value

            del(all_dists)

            dists=dists*length_units

            return pairs, dists

        else:
            raise ValueError("If 'pairs=True' both input arguments 'as_entity_1' and 'as_entity_2' need to be True")

def maximum_distance(item_1=None, selection_1="all", selection_groups_1=None, group_behavior_1=None,
                     as_entity_1=True, frame_indices_1="all",
                     item_2=None, selection_2=None, selection_groups_2=None, group_behavior_2=None,
                     as_entity_2=True, frame_indices_2=None,
                     pairs=False, pbc=False, parallel=False, engine='MolSysMT', syntaxis='MDTraj'):

    all_dists = distance(item_1=item_1, selection_1=selection_1,
                         selection_groups_1=selection_groups_1, group_behavior_1=group_behavior_1,
                         frame_indices_1=frame_indices_1,
                         item_2=item_2, selection_2=selection_2,
                         selection_groups_2=selection_groups_2, group_behavior_2=group_behavior_2,
                         frame_indices_2=frame_indices_2,
                         pairs=pairs, pbc=pbc, parallel=parallel, output_form='tensor', engine=engine,
                         syntaxis=syntaxis)

    if pairs is False:

        nframes, nelements_1, nelements_2 = all_dists.shape
        length_units = all_dists.unit

        if (as_entity_1 is True) and (as_entity_2 is True):

            pairs=_np.empty((nframes,2),dtype=int)
            dists=_np.empty((nframes),dtype=float)
            for indice_frame in range(nframes):
                ii,jj = _np.unravel_index(all_dists[indice_frame,:,:].argmax(), all_dists[indice_frame,:,:].shape)
                pairs[indice_frame,0] = ii
                pairs[indice_frame,1] = jj
                dists[indice_frame] = all_dists[indice_frame,ii,jj]._value

            del(all_dists)

            dists=dists*length_units

            return pairs, dists

        elif (as_entity_1 is False) and (as_entity_2 is True):

            pairs=_np.empty((nframes, nelements_1), dtype=int)
            dists=_np.empty((nframes, nelements_1), dtype=float)
            for indice_frame in range(nframes):
                for ii in range(nelements_1):
                    jj = all_dists[indice_frame,ii,:].argmax()
                    pairs[indice_frame,ii]=jj
                    dists[indice_frame,ii]=all_dists[indice_frame,ii,jj]._value

            del(all_dists)

            dists=dists*length_units

            return pairs, dists

        elif (as_entity_1 is True) and (as_entity_2 is False):

            pairs=_np.empty((nframes, nelements_2), dtype=int)
            dists=_np.empty((nframes, nelements_2), dtype=float)
            for indice_frame in range(nframes):
                for ii in range(nelements_2):
                    jj = all_dists[indice_frame,:,ii].argmax()
                    pairs[indice_frame,ii]=jj
                    dists[indice_frame,ii]=all_dists[indice_frame,jj,ii]._value

            del(all_dists)

            dists=dists*length_units

            return pairs, dists

        else:
            raise ValueError("If both input arguments 'as_entity_1' and 'as_entity_2' are False, the\
                    method you are looking for is molsysmt.distance()")

    else:

        nframes, nelements = all_dists.shape
        length_units = all_dists.unit

        if (as_entity_1 is True) and (as_entity_2 is True):

            pairs=_np.empty((nframes),dtype=int)
            dists=_np.empty((nframes),dtype=float)
            for indice_frame in range(nframes):
                ii = all_dists[indice_frame,:].argmax()
                pairs[indice_frame] = ii
                dists[indice_frame] = all_dists[indice_frame,ii]._value

            del(all_dists)

            dists=dists*length_units

            return pairs, dists

        else:
            raise ValueError("If 'pairs=True' both input arguments 'as_entity_1' and 'as_entity_2' need to be True")


def contact_map(item_1=None, selection_1="all", selection_groups_1=None, group_behavior_1=None, frame_indices_1="all",
                item_2=None, selection_2=None, selection_groups_2=None, group_behavior_2=None, frame_indices_2=None,
                threshold=None, pbc=False, parallel=False, engine='MolSysMT', syntaxis='MDTraj'):

    all_dists = distance(item_1=item_1, selection_1=selection_1,
                         selection_groups_1=selection_groups_1, group_behavior_1=group_behavior_1,
                         frame_indices_1=frame_indices_1,
                         item_2=item_2, selection_2=selection_2,
                         selection_groups_2=selection_groups_2, group_behavior_2=group_behavior_2,
                         frame_indices_2=frame_indices_2,
                         pbc=pbc, parallel=parallel, output_form='tensor', engine=engine,
                         syntaxis=syntaxis)

    if threshold is None:
        raise BadCallError(BadCallMessage)

    num_frames=all_dists.shape[0]
    contact_map=_np.empty(all_dists.shape,dtype=bool)
    for indice_frame in range(num_frames):
        contact_map[indice_frame,:,:]=(all_dists[indice_frame,:,:]<=threshold)

    del(all_dists, num_frames, indice_frame)

    return contact_map

def neighbors_lists(item_1=None, selection_1="all", selection_groups_1=None, group_behavior_1=None, frame_indices_1="all",
                    item_2=None, selection_2=None, selection_groups_2=None, group_behavior_2=None, frame_indices_2=None,
                    threshold=None, num_neighbors=None,
                    pbc=False, parallel=False, engine='MolSysMT', syntaxis='MDTraj'):

    if (threshold is None) and (num_neighbors is None):
        raise BadCallError(BadCallMessage)

    all_dists = distance(item_1=item_1, selection_1=selection_1,
                         selection_groups_1=selection_groups_1, group_behavior_1=group_behavior_1,
                         frame_indices_1=frame_indices_1,
                         item_2=item_2, selection_2=selection_2,
                         selection_groups_2=selection_groups_2, group_behavior_2=group_behavior_2,
                         frame_indices_2=frame_indices_2,
                         pbc=pbc, parallel=parallel, output_form='tensor', engine=engine,
                         syntaxis=syntaxis)


    nframes, nelements_1, nelements_2 = all_dists.shape
    length_units = all_dists.unit


    if num_neighbors is not None and threshold is None:

        neighs=_np.empty((nframes, nelements_1, num_neighbors), dtype=int)
        dists=_np.empty((nframes, nelements_1, num_neighbors), dtype=float)

        for indice_frame in range(nframes):
            for ii in range(nelements_1):
                neighs_aux = _np.argpartition(all_dists[indice_frame,ii,:], num_neighbors-1)[:num_neighbors]
                dists_aux = all_dists[indice_frame,ii,neighs_aux]
                #good_order = _np.argsort(dists_aux)
                #neighs_aux = neighs_aux[good_order]
                #dists_aux = dists_aux[good_order]
                neighs[indice_frame,ii,:]=neighs_aux
                dists[indice_frame,ii,:]=dists_aux

        del(all_dists)

        dists=dists*length_units

        return neighs, dists

    elif threshold is not None and num_neighbors is None:

        neighs=_np.empty((nframes, nelements_1), dtype=object)
        dists=_np.empty((nframes, nelements_1), dtype=object)

        for indice_frame in range(nframes):
            for ii in range(nelements_1):
                neighs_aux = _np.argwhere(all_dists[indice_frame,ii,:]<=threshold)[:,0]
                dists_aux = all_dists[indice_frame,ii,neighs_aux]
                good_order = _np.argsort(dists_aux)
                neighs_aux = neighs_aux[good_order]
                dists_aux = dists_aux[good_order]
                neighs[indice_frame,ii]=_np.array(neighs_aux,dtype=int)
                dists[indice_frame,ii]=_np.array(dists_aux,dtype=float)

        del(all_dists)

        dists=dists*length_units

        return neighs, dists


    else:
        raise ValueError("Use either threshold or num_neighbors, but not both at the same time")



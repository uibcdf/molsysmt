from molsysmt._private_tools._digestion import *
from molsysmt._private_tools.exceptions import *
from molsysmt.lib import geometry as libgeometry
from molsysmt import puw
import numpy as np

def distance(molecular_system_1, selection_1="all", groups_of_atoms_1=None, group_behavior_1=None, frame_indices_1="all",
             molecular_system_2=None, selection_2=None, groups_of_atoms_2=None, group_behavior_2=None, frame_indices_2=None,
             pairs=False, crossed_frames=False, pbc=False, parallel=False, output_form='tensor', engine='MolSysMT', syntaxis='MolSysMT'):

    # group_behavior in
    # ['center_of_mass','geometric_center','minimum_distance','maximum_distance']
    # output_form in ['tensor','dict']

    # crossed_frames es para cuando queremos calcular lista de frames1 contra lista de frames 2
    # (todos con todos), si crossed_frames=False entonces es sólo el primer frame de lista 1 contra
    # el primer frame de lista 2, el segundo contra el segundo, etc.

    # selection groups está por si quiero distancias entre centros de masas, necesita
    # hacer un lista de listas frente a otra lista de listas.

    from molsysmt.multitool import convert, select, get, extract
    from molsysmt.centers import center_of_mass, geometric_center

    molecular_system_1 = digest_molecular_system(molecular_system_1)
    if molecular_system_2 is not None:
        molecular_system_2 = digest_molecular_system(molecular_system_2)

    engine = digest_engine(engine)
    frame_indices_1 = digest_frame_indices(frame_indices_1)
    frame_indices_2 = digest_frame_indices(frame_indices_2)

    if group_behavior_1=='minimum_distance' or group_behavior_2=='minimum_distance':
        if group_behavior_1=='minimum_distance' and group_behavior_2=='minimum_distance':
            raise NotImplementedError(NotImplementedMessage)
            #num_groups_1=len(groups_of_atoms_1)
            #num_groups_2=len(groups_of_atoms_2)
            #frame_indices = _digest_frame_indices(item, frame_indices_1)
            #num_frames=len(frame_indices)
            #dists = np.zeros((num_frames, num_groups_1, num_groups_2),dtype=float)
            #for ii in range(num_groups_1):
            #    group1 = groups_of_atoms_2[ii]
            #    for jj in range(num_groups_2):
            #        group2 = groups_of_atoms_2[jj]
            #        _, min_dist = min_distances(molecular_system_1=molecular_system_1, selection_1=group1,
            #                                    frame_indices_1=frame_indices_1,
            #                                    molecular_system_2=molecular_system_2, selection_2=group2,
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

        if groups_of_atoms_1 is not None:

            selection_1=None

        if molecular_system_2 is None:

            molecular_system_2 = molecular_system_1
            same_item = True

            if (selection_1 is not None) and (selection_2 is None):
                if (groups_of_atoms_2 is None):
                    selection_2 = selection_1
                    same_selection = True
                    diff_set = False

            if groups_of_atoms_1 is not None:
                if (selection_2 is None) and (groups_of_atoms_2 is None):
                    groups_of_atoms_2=groups_of_atoms_1
                    same_groups = True
                    diff_set = False

        else:
            if (selection_1 is not None) and (selection_2 is None):
                if (groups_of_atoms_2 is None):
                    selection_2 = selection_1

        if frame_indices_2 is None:
            frame_indices_2 = frame_indices_1
            same_frames = True
        else:
            diff_set = True

        if selection_1 is not None:

            if group_behavior_1 == 'center_of_mass':
                coordinates_1 = center_of_mass(molecular_system_1, selection=selection_1, frame_indices=frame_indices_1)
                atom_indices_1 = [0]
            elif group_behavior_1 == 'geometric_center':
                coordinates_1 = geometric_center(molecular_system_1, selection=selection_1, frame_indices=frame_indices_1)
                atom_indices_1 = [0]
            else:
                atom_indices_1 = select(molecular_system_1, selection=selection_1, syntaxis=syntaxis)
                coordinates_1 = get(molecular_system_1, target='atom', indices=atom_indices_1, frame_indices=frame_indices_1, coordinates=True)
        else:

            if group_behavior_1 == 'center_of_mass':
                coordinates_1 = center_of_mass(molecular_system_1, groups_of_atoms=groups_of_atoms_1, frame_indices=frame_indices_1)
                atom_indices_1 = np.range(coordinates_1.shape[1])
            elif group_behavior_1 == 'geometric_center':
                coordinates_1 = geometric_center(molecular_system_1, groups_of_atoms=groups_of_atoms_1, frame_indices=frame_indices_1)
                atom_indices_1 = np.arange(coordinates_1.shape[1])
            else:
                raise ValueError("Value of argument group_behavior_1 not recognized.")

        if selection_2 is not None:

            if group_behavior_2 == 'center_of_mass':
                coordinates_2 = center_of_mass(molecular_system_2, selection=selection_2, frame_indices=frame_indices_2)
                atom_indices_2 = [0]
            elif group_behavior_2 == 'geometric_center':
                coordinates_2 = geometric_center(molecular_system_2, selection=selection_2, frame_indices=frame_indices_2)
                atom_indices_2 = [0]
            else:
                atom_indices_2 = select(molecular_system_2, selection=selection_2, syntaxis=syntaxis)
                coordinates_2 = get(molecular_system_2, target='atom', indices=atom_indices_2, frame_indices=frame_indices_2, coordinates=True)

        else:

            if same_groups and same_frames:
                atom_indices_2 = atom_indices_1
                coordinates_2 = coordinates_1
            else:
                if group_behavior_2 == 'center_of_mass':
                    coordinates_2 = center_of_mass(molecular_system_2, groups_of_atoms=groups_of_atoms_2, frame_indices=frame_indices_2)
                    atom_indices_2 = np.arange(coordinates_2.shape[1])
                elif group_behavior_2 == 'geometric_center':
                    coordinates_2 = geometric_center(molecular_system_2, groups_of_atoms=groups_of_atoms_2, frame_indices=frame_indices_2)
                    atom_indices_2 = np.arange(coordinates_2.shape[1])
                else:
                    raise ValueError("Value of argument group_behavior_2 not recognized.")

        length_units = puw.get_unit(coordinates_1)
        coordinates_1 = np.asfortranarray(puw.get_value(coordinates_1), dtype='float64')
        coordinates_2 = np.asfortranarray(puw.get_value(coordinates_2), dtype='float64')
        nframes_1 = coordinates_1.shape[0]
        nframes_2 = coordinates_2.shape[0]
        nelements1 = coordinates_1.shape[1]
        nelements2 = coordinates_2.shape[1]

        box, box_shape = get(molecular_system_1, target='system', box=True, box_shape=True, frame_indices=frame_indices_1)

        orthogonal = 0
        if box_shape is None:
            orthogonal =1
            if pbc:
                raise ValueError("The system has no PBC box. The input argument 'pbc' can not be True.")
        elif box_shape == 'cubic':
            orthogonal =1

        if box is None:
            box= np.zeros([nframes_1, 3, 3])*length_units

        box = np.asfortranarray(puw.get_value(box), dtype='float64')

        if crossed_frames is False:
            if nframes_1 != nframes_2:
                raise ValueError("Both frame_indices_1 and frame_indices_2 need the same number of frames.")
            else:
                if pairs is False:
                    dists = libgeometry.distance(int(diff_set), coordinates_1, coordinates_2, box, orthogonal, int(pbc),
                                                 nelements1, nelements2, nframes_1)
                else:
                    if nframes_1 != nframes_2:
                        raise ValueError("Both selection_1 and selection_2 need the same number of atoms.")
                    else:
                        dists = libgeometry.distance_pairs(coordinates_1, coordinates_2, box, orthogonal, int(pbc),
                                                           nelements1, nelements2, nframes_1)
        else:
            raise NotImplementedError(NotImplementedMessage)

        del(coordinates_1, coordinates_2, box)

        dists = dists*length_units

        if output_form=='tensor':
             return dists
        elif output_form=='dict':
            if frame_indices_1 is 'all':
                frame_indices_1 = np.arange(nframes_1)
            if frame_indices_2 is 'all':
                frame_indices_2 = np.arange(nframes_2)
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
        #        tensor1_to_grid, tensor2_to_grid = np.meshgrid(atom_indices1,atom_indices2)
        #        pairs_list =np.vstack([tensor1_to_grid.ravel(), tensor2_to_grid.ravel()]).T
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

def minimum_distance(molecular_system_1, selection_1="all", groups_of_atoms_1=None, group_behavior_1=None, as_entity_1=True, frame_indices_1="all",
                     molecular_system_2=None, selection_2=None, groups_of_atoms_2=None, group_behavior_2=None, as_entity_2=True, frame_indices_2=None,
                     pairs=False, pbc=False, parallel=False, engine='MolSysMT', syntaxis='MolSysMT'):

    all_dists = distance(molecular_system_1=molecular_system_1, selection_1=selection_1, groups_of_atoms_1=groups_of_atoms_1,
                         group_behavior_1=group_behavior_1, frame_indices_1=frame_indices_1,
                         molecular_system_2=molecular_system_2, selection_2=selection_2, groups_of_atoms_2=groups_of_atoms_2,
                         group_behavior_2=group_behavior_2, frame_indices_2=frame_indices_2,
                         pairs=pairs, pbc=pbc, parallel=parallel, output_form='tensor', engine=engine, syntaxis=syntaxis)

    if pairs is False:

        nframes, nelements_1, nelements_2 = all_dists.shape
        length_units = puw.get_unit(all_dists)
        all_dists = puw.get_value(all_dists)

        if (as_entity_1 is True) and (as_entity_2 is True):

            pairs=np.empty((nframes,2),dtype=int)
            dists=np.empty((nframes),dtype=float)
            for indice_frame in range(nframes):
                ii,jj = np.unravel_index(all_dists[indice_frame,:,:].argmin(), all_dists[indice_frame,:,:].shape)
                pairs[indice_frame,0] = ii
                pairs[indice_frame,1] = jj
                dists[indice_frame] = all_dists[indice_frame,ii,jj]

            del(all_dists)

            dists=dists*length_units

            return pairs, dists

        elif (as_entity_1 is False) and (as_entity_2 is True):

            pairs=np.empty((nframes, nelements_1), dtype=int)
            dists=np.empty((nframes, nelements_1), dtype=float)
            for indice_frame in range(nframes):
                for ii in range(nelements_1):
                    jj = all_dists[indice_frame,ii,:].argmin()
                    pairs[indice_frame,ii]=jj
                    dists[indice_frame,ii]=all_dists[indice_frame,ii,jj]

            del(all_dists)

            dists=dists*length_units

            return pairs, dists

        elif (as_entity_1 is True) and (as_entity_2 is False):

            pairs=np.empty((nframes, nelements_2), dtype=int)
            dists=np.empty((nframes, nelements_2), dtype=float)
            for indice_frame in range(nframes):
                for ii in range(nelements_2):
                    jj = all_dists[indice_frame,:,ii].argmin()
                    pairs[indice_frame,ii]=jj
                    dists[indice_frame,ii]=all_dists[indice_frame,jj,ii]

            del(all_dists)

            dists=dists*length_units

            return pairs, dists

        else:
            raise ValueError("If both input arguments 'as_entity_1' and 'as_entity_2' are False, the method you are looking for is molsysmt.distance()")

    else:

        nframes, nelements = all_dists.shape
        length_units = puw.get_unit(all_dists)
        all_dists = puw.get_value(all_dists)

        if (as_entity_1 is True) and (as_entity_2 is True):

            pairs=np.empty((nframes),dtype=int)
            dists=np.empty((nframes),dtype=float)
            for indice_frame in range(nframes):
                ii = all_dists[indice_frame,:].argmin()
                pairs[indice_frame] = ii
                dists[indice_frame] = all_dists[indice_frame,ii]

            del(all_dists)

            dists=dists*length_units

            return pairs, dists

        else:
            raise ValueError("If 'pairs=True' both input arguments 'as_entity_1' and 'as_entity_2' need to be True")

def maximum_distance(molecular_system_1, selection_1="all", groups_of_atoms_1=None, group_behavior_1=None,
                     as_entity_1=True, frame_indices_1="all",
                     molecular_system_2=None, selection_2=None, groups_of_atoms_2=None, group_behavior_2=None,
                     as_entity_2=True, frame_indices_2=None,
                     pairs=False, pbc=False, parallel=False, engine='MolSysMT', syntaxis='MDTraj'):

    all_dists = distance(molecular_system_1=molecular_system_1, selection_1=selection_1, groups_of_atoms_1=groups_of_atoms_1,
                         group_behavior_1=group_behavior_1, frame_indices_1=frame_indices_1,
                         molecular_system_2=molecular_system_2, selection_2=selection_2, groups_of_atoms_2=groups_of_atoms_2,
                         group_behavior_2=group_behavior_2, frame_indices_2=frame_indices_2,
                         pairs=pairs, pbc=pbc, parallel=parallel, output_form='tensor', engine=engine, syntaxis=syntaxis)

    if pairs is False:

        nframes, nelements_1, nelements_2 = all_dists.shape
        length_units = puw.get_unit(all_dists)
        all_dists = puw.get_value(all_dists)

        if (as_entity_1 is True) and (as_entity_2 is True):

            pairs=np.empty((nframes,2),dtype=int)
            dists=np.empty((nframes),dtype=float)
            for indice_frame in range(nframes):
                ii,jj = np.unravel_index(all_dists[indice_frame,:,:].argmax(), all_dists[indice_frame,:,:].shape)
                pairs[indice_frame,0] = ii
                pairs[indice_frame,1] = jj
                dists[indice_frame] = all_dists[indice_frame,ii,jj]

            del(all_dists)

            dists=dists*length_units

            return pairs, dists

        elif (as_entity_1 is False) and (as_entity_2 is True):

            pairs=np.empty((nframes, nelements_1), dtype=int)
            dists=np.empty((nframes, nelements_1), dtype=float)
            for indice_frame in range(nframes):
                for ii in range(nelements_1):
                    jj = all_dists[indice_frame,ii,:].argmax()
                    pairs[indice_frame,ii]=jj
                    dists[indice_frame,ii]=all_dists[indice_frame,ii,jj]

            del(all_dists)

            dists=dists*length_units

            return pairs, dists

        elif (as_entity_1 is True) and (as_entity_2 is False):

            pairs=np.empty((nframes, nelements_2), dtype=int)
            dists=np.empty((nframes, nelements_2), dtype=float)
            for indice_frame in range(nframes):
                for ii in range(nelements_2):
                    jj = all_dists[indice_frame,:,ii].argmax()
                    pairs[indice_frame,ii]=jj
                    dists[indice_frame,ii]=all_dists[indice_frame,jj,ii]

            del(all_dists)

            dists=dists*length_units

            return pairs, dists

        else:
            raise ValueError("If both input arguments 'as_entity_1' and 'as_entity_2' are False, the\
                    method you are looking for is molsysmt.distance()")

    else:

        nframes, nelements = all_dists.shape
        length_units = puw.get_unit(all_dists)
        all_dists = puw.get_value(all_dists)

        if (as_entity_1 is True) and (as_entity_2 is True):

            pairs=np.empty((nframes),dtype=int)
            dists=np.empty((nframes),dtype=float)
            for indice_frame in range(nframes):
                ii = all_dists[indice_frame,:].argmax()
                pairs[indice_frame] = ii
                dists[indice_frame] = all_dists[indice_frame,ii]

            del(all_dists)

            dists=dists*length_units

            return pairs, dists

        else:
            raise ValueError("If 'pairs=True' both input arguments 'as_entity_1' and 'as_entity_2' need to be True")


def contact_map(molecular_system_1, selection_1="all", groups_of_atoms_1=None, group_behavior_1=None, frame_indices_1="all",
                molecular_system_2=None, selection_2=None, groups_of_atoms_2=None, group_behavior_2=None, frame_indices_2=None,
                threshold=None, pbc=False, parallel=False, engine='MolSysMT', syntaxis='MolSysMT'):

    all_dists = distance(molecular_system_1=molecular_system_1, selection_1=selection_1, groups_of_atoms_1=groups_of_atoms_1,
                         group_behavior_1=group_behavior_1, frame_indices_1=frame_indices_1,
                         molecular_system_2=molecular_system_2, selection_2=selection_2, groups_of_atoms_2=groups_of_atoms_2,
                         group_behavior_2=group_behavior_2, frame_indices_2=frame_indices_2,
                         pbc=pbc, parallel=parallel, output_form='tensor', engine=engine, syntaxis=syntaxis)

    if threshold is None:
        raise BadCallError(BadCallMessage)

    length_units = puw.get_unit(all_dists)
    threshold = puw.get_value(threshold, in_units=length_units)
    all_dists = puw.get_value(all_dists)

    num_frames=all_dists.shape[0]
    contact_map=np.empty(all_dists.shape, dtype=bool)
    for indice_frame in range(num_frames):
        contact_map[indice_frame,:,:]=(all_dists[indice_frame,:,:]<=threshold)

    del(all_dists, num_frames, indice_frame, length_units)

    return contact_map

def neighbors_lists(molecular_system_1, selection_1="all", groups_of_atoms_1=None, group_behavior_1=None, frame_indices_1="all",
                    molecular_system_2=None, selection_2=None, groups_of_atoms_2=None, group_behavior_2=None, frame_indices_2=None,
                    threshold=None, num_neighbors=None, pbc=False, parallel=False, engine='MolSysMT', syntaxis='MolSysMT'):

    if (threshold is None) and (num_neighbors is None):
        raise BadCallError(BadCallMessage)

    same_set = False

    same_items = False
    same_selections = False
    same_groups = False
    same_frames = False

    if groups_of_atoms_1 is not None:
        selection_1=None

    if molecular_system_2 is None:
        same_items = True
        if (selection_1 is not None) and (selection_2 is None) and (groups_of_atoms_2 is None):
            same_selections = True
        elif (groups_of_atoms_1 is not None) and (selection_2 is None) and (groups_of_atoms_2 is None):
            same_groups = True
    else:
        if (selection_1 is not None) and (selection_2 is None) and (groups_of_atoms_2 is None):
            same_selections=True
        elif (groups_of_atoms_1 is not None) and (selection_2 is None) and (groups_of_atoms_2 is None):
            same_groups = True

    if frame_indices_2 is None:
        same_frames = True

    same_set= same_items and (same_selections or same_groups) and same_frames

    all_dists = distance(molecular_system_1=molecular_system_1, selection_1=selection_1, groups_of_atoms_1=groups_of_atoms_1,
                         group_behavior_1=group_behavior_1, frame_indices_1=frame_indices_1,
                         molecular_system_2=molecular_system_2, selection_2=selection_2, groups_of_atoms_2=groups_of_atoms_2,
                         group_behavior_2=group_behavior_2, frame_indices_2=frame_indices_2,
                         pbc=pbc, parallel=parallel, output_form='tensor', engine=engine, syntaxis=syntaxis)

    nframes, nelements_1, nelements_2 = all_dists.shape
    length_units = puw.get_unit(all_dists)
    all_dists = puw.get_value(all_dists)

    if num_neighbors is not None and threshold is None:

        neighs=np.empty((nframes, nelements_1, num_neighbors), dtype=int)
        dists=np.empty((nframes, nelements_1, num_neighbors), dtype=float)

        offset = 0
        if same_set:
            offset = 1

        for indice_frame in range(nframes):
            for ii in range(nelements_1):
                neighs_aux = np.argpartition(all_dists[indice_frame,ii,:], num_neighbors-1+offset)[:num_neighbors+offset]
                dists_aux = all_dists[indice_frame,ii,neighs_aux]
                good_order = np.argsort(dists_aux)
                neighs_aux = neighs_aux[good_order]
                dists_aux = dists_aux[good_order]
                neighs[indice_frame,ii,:]=neighs_aux[offset:]
                dists[indice_frame,ii,:]=dists_aux[offset:]
                if same_set:
                    if dists_aux[0] > 0.01:
                        raise ValueError("Error in algorithm, sets are different.")

        del(all_dists)

        dists=dists*length_units

        return neighs, dists

    elif threshold is not None and num_neighbors is None:

        threshold = puw.get_value(threshold, in_units=length_units)

        neighs=np.empty((nframes, nelements_1), dtype=object)
        dists=np.empty((nframes, nelements_1), dtype=object)

        offset = 0
        if same_set:
            offset = 1

        for indice_frame in range(nframes):
            for ii in range(nelements_1):
                neighs_aux = np.argwhere(all_dists[indice_frame,ii,:]<=threshold)[:,0]
                dists_aux = all_dists[indice_frame,ii,neighs_aux]
                good_order = np.argsort(dists_aux)
                neighs_aux = neighs_aux[good_order]
                dists_aux = dists_aux[good_order]
                neighs[indice_frame,ii]=np.array(neighs_aux,dtype=int)[offset:]
                dists[indice_frame,ii]=np.array(dists_aux,dtype=float)[offset:]
                if same_set:
                    if dists_aux[0] > 0.01:
                        raise ValueError("Error in algorithm, sets are different.")

        del(all_dists)

        dists=dists*length_units

        return neighs, dists

    else:

        raise ValueError("Use either threshold or num_neighbors, but not both at the same time")


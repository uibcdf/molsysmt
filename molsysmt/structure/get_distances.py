from molsysmt._private_tools._digestion import *
from molsysmt._private_tools.exceptions import *
from molsysmt.basic import select, get
from molsysmt.lib import geometry as libgeometry
from molsysmt import puw
import numpy as np

def get_distances(molecular_system, selection="all", groups_of_atoms=None, group_behavior=None, frame_indices="all",
             selection_2=None, groups_of_atoms_2=None, group_behavior_2=None, frame_indices_2=None,
             pairs=False, crossed_frames=False, pbc=False, parallel=False, output_form='tensor',
             output_atom_indices=False, output_frame_indices=False, engine='MolSysMT', syntaxis='MolSysMT'):

    from molsysmt.structure.get_center_of_mass import get_center_of_mass
    from molsysmt.structure.get_geometric_center import get_geometric_center

    # group_behavior in
    # ['center_of_mass','geometric_center','minimum_distance','maximum_distance']
    # output_form in ['tensor','dict']

    # crossed_frames es para cuando queremos calcular lista de frames1 contra lista de frames 2
    # (todos con todos), si crossed_frames=False entonces es sólo el primer frame de lista 1 contra
    # el primer frame de lista 2, el segundo contra el segundo, etc.

    # selection groups está por si quiero distancias entre centros de masas, necesita
    # hacer un lista de listas frente a otra lista de listas.

    molecular_system = digest_molecular_system(molecular_system)

    engine = digest_engine(engine)
    frame_indices = digest_frame_indices(frame_indices)
    frame_indices_2 = digest_frame_indices(frame_indices_2)

    if group_behavior=='minimum_distance' or group_behavior_2=='minimum_distance':
        if group_behavior=='minimum_distance' and group_behavior_2=='minimum_distance':
            raise NotImplementedError(NotImplementedMessage)
            #num_groups_1=len(groups_of_atoms)
            #num_groups_2=len(groups_of_atoms_2)
            #frame_indices = _digest_frame_indices(item, frame_indices)
            #num_frames=len(frame_indices)
            #dists = np.zeros((num_frames, num_groups_1, num_groups_2),dtype=float)
            #for ii in range(num_groups_1):
            #    group1 = groups_of_atoms_2[ii]
            #    for jj in range(num_groups_2):
            #        group2 = groups_of_atoms_2[jj]
            #        _, min_dist = min_distances(molecular_system=molecular_system, selection=group1,
            #                                    frame_indices=frame_indices,
            #                                    selection_2=group2,
            #                                    pbc=pbc, parallel=parallel, engine=engine)
            #        dists[:,ii,jj]=min_dist
            #del(num_groups1,num_groups2,frame_indices,num_frames,group1,group2)
            #return dists
        else:
            raise NotImplementedError(NotImplementedMessage)

    if engine=='MolSysMT':

        diff_set = True
        same_selection = False
        same_groups = False
        same_frames = False

        if groups_of_atoms is not None:

            selection=None

        if (selection is not None) and (selection_2 is None):
            if (groups_of_atoms_2 is None):
                selection_2 = selection
                same_selection = True
                diff_set = False

        if groups_of_atoms is not None:
            if (selection_2 is None) and (groups_of_atoms_2 is None):
                groups_of_atoms_2=groups_of_atoms
                same_groups = True
                diff_set = False

        if frame_indices_2 is None:
            frame_indices_2 = frame_indices
            same_frames = True
        else:
            diff_set = True

        if selection is not None:

            if group_behavior == 'center_of_mass':
                coordinates_1 = get_center_of_mass(molecular_system, selection=selection, frame_indices=frame_indices)
                atom_indices_1 = [0]
            elif group_behavior == 'geometric_center':
                coordinates_1 = get_geometric_center(molecular_system, selection=selection, frame_indices=frame_indices)
                atom_indices_1 = [0]
            else:
                atom_indices_1 = select(molecular_system, selection=selection, syntaxis=syntaxis)
                coordinates_1 = get(molecular_system, target='atom', indices=atom_indices_1, frame_indices=frame_indices, coordinates=True)
        else:

            if group_behavior == 'center_of_mass':
                coordinates_1 = get_center_of_mass(molecular_system, groups_of_atoms=groups_of_atoms, frame_indices=frame_indices)
                atom_indices_1 = np.range(coordinates_1.shape[1])
            elif group_behavior == 'geometric_center':
                coordinates_1 = get_geometric_center(molecular_system, groups_of_atoms=groups_of_atoms, frame_indices=frame_indices)
                atom_indices_1 = np.arange(coordinates_1.shape[1])
            else:
                raise ValueError("Value of argument group_behavior not recognized.")

        if selection_2 is not None:

            if group_behavior_2 == 'center_of_mass':
                coordinates_2 = get_center_of_mass(molecular_system, selection=selection_2, frame_indices=frame_indices_2)
                atom_indices_2 = [0]
            elif group_behavior_2 == 'geometric_center':
                coordinates_2 = get_geometric_center(molecular_system, selection=selection_2, frame_indices=frame_indices_2)
                atom_indices_2 = [0]
            else:
                atom_indices_2 = select(molecular_system, selection=selection_2, syntaxis=syntaxis)
                coordinates_2 = get(molecular_system, target='atom', indices=atom_indices_2, frame_indices=frame_indices_2, coordinates=True)

        else:

            if same_groups and same_frames:
                atom_indices_2 = atom_indices_1
                coordinates_2 = coordinates_1
            else:
                if group_behavior_2 == 'center_of_mass':
                    coordinates_2 = get_center_of_mass(molecular_system, groups_of_atoms=groups_of_atoms_2, frame_indices=frame_indices_2)
                    atom_indices_2 = np.arange(coordinates_2.shape[1])
                elif group_behavior_2 == 'geometric_center':
                    coordinates_2 = get_geometric_center(molecular_system, groups_of_atoms=groups_of_atoms_2, frame_indices=frame_indices_2)
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

        if pbc:

            box, box_shape = get(molecular_system, target='system', box=True, box_shape=True, frame_indices=frame_indices)

            orthogonal = 0
            if box_shape is None:
                raise ValueError("The system has no PBC box. The input argument 'pbc' can not be True.")
            elif box_shape == 'cubic':
                orthogonal =1

        else:

            box= np.zeros([nframes_1, 3, 3])*length_units
            orthogonal = 1

        box = np.asfortranarray(puw.get_value(box), dtype='float64')

        if crossed_frames is False:
            if nframes_1 != nframes_2:
                raise ValueError("Both frame_indices and frame_indices_2 need the same number of frames.")
            else:
                if pairs is False:
                    dists = libgeometry.distance(int(diff_set), coordinates_1, coordinates_2, box, orthogonal, int(pbc),
                                                 nelements1, nelements2, nframes_1)
                else:
                    if nframes_1 != nframes_2:
                        raise ValueError("Both selection and selection_2 need the same number of atoms.")
                    else:
                        dists = libgeometry.distance_pairs(coordinates_1, coordinates_2, box, orthogonal, int(pbc),
                                                           nelements1, nelements2, nframes_1)
        else:
            raise NotImplementedError(NotImplementedMessage)

        del(coordinates_1, coordinates_2, box)

        dists = dists*length_units

        if output_form=='tensor':
            if output_frame_indices:

                if frame_indices is 'all':
                    frame_indices = np.arange(nframes_1)
                if frame_indices_2 is 'all':
                    frame_indices_2 = np.arange(nframes_2)

                if output_atom_indices:
                    return atom_indices_1, frame_indices, atom_indices_2, frame_indices_2, dists
                else:
                    return frame_indices, frame_indices_2, dists

            elif output_atom_indices:
                return atom_indices_1, atom_indices_2, dists
            else:
                return dists

        elif output_form=='dict':
            if frame_indices is 'all':
                frame_indices = np.arange(nframes_1)
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
                            for kk in range(len(frame_indices)):
                                frame_index_1 = frame_indices[kk]
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
                        for kk in range(len(frame_indices)):
                            frame_index_1 = frame_indices[kk]
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


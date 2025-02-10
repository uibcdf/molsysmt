from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from copy import copy
import numpy as np

def get_luzard_chandler_hbonds(molecular_system, selection='all', acceptors=None, donors=None, structure_indices='all',
        molecular_system_2=None, selection_2=None, acceptors_2=None, donors_2=None, structure_indices_2=None,
        distance_threshold='3.5 angstroms', angle_threshold='30 degrees', pbc=True, syntax='MolSysMT'):

    from molsysmt.basic import select, get
    from .get_acceptor_atoms import get_acceptor_atoms
    from .get_donor_atoms import get_donor_atoms
    from molsysmt.structure import get_neighbors, get_angles
    from molsysmt import pyunitwizard as puw

    angle_threshold = puw.standardize(angle_threshold)

    if is_all(structure_indices):
        n_structures=get(molecular_system, n_structures=True)
        structure_indices=np.arange(n_structures)
    elif isinstance(structure_indices,(int,np.int64)):
        structure_indices=[structure_indices]

    if (molecular_system_2 is None):

        if acceptors is None:
            acceptors = get_acceptor_atoms(molecular_system, selection=selection, syntax=syntax)
        else:
            acceptors = select(molecular_system, selection=selection, mask=acceptors, syntax=syntax)

        if donors is None:
            donors = get_donor_atoms(molecular_system, selection=selection, syntax=syntax)
        else:
            donors = select(molecular_system, selection=selection, mask=donors, syntax=syntax)

        n_acceptors = acceptors.shape[0]
        n_donors = donors.shape[0]

        if (selection_2 is None) and (acceptors_2 is None) and (donors_2 is None):

            output_atoms=[]
            output_distances=[]
            output_angles=[]

            neighs, distances = get_neighbors(molecular_system, selection=donors[:,0], selection_2=acceptors,
                structure_indices=structure_indices, structure_indices_2=structure_indices_2,
                threshold=distance_threshold, pbc=pbc)

            for ll,mm in enumerate(structure_indices):

                tmp_atoms=[]
                tmp_distances=[]
                tmp_angles=[]

                for ii in range(n_donors):
                    atom_d = donors[ii,0]
                    atom_h = donors[ii,1]
                    for jj, dist in zip(neighs[ll,ii], distances[ll,ii]):
                        if atom_d!=acceptors[jj]:
                            tmp_atoms.append([atom_d, atom_h, acceptors[jj]])
                            tmp_distances.append(dist)

                tmp_atoms = np.array(tmp_atoms)
                tmp_distances = puw.utils.sequences.concatenate(tmp_distances, value_type='numpy.ndarray')

                tmp_angles = get_angles(molecular_system, tmp_atoms[:,[1,0,2]], pbc=pbc,
                        structure_indices=mm)[0]
                mask = tmp_angles<angle_threshold

                output_atoms.append(tmp_atoms[mask,:])
                output_distances.append(tmp_distances[mask])
                output_angles.append(tmp_angles[mask])

            output_atoms=np.array(output_atoms)
            output_distances=puw.utils.sequences.concatenate(output_distances, value_type='numpy.ndarray')
            output_angles=puw.utils.sequences.concatenate(output_angles, value_type='numpy.ndarray')


            return output_atoms, output_distances, output_angles

        else:

            if selection_2 is None:
                selection_2 = selection

            if acceptors_2 is None:
                acceptors_2 = get_acceptor_atoms(molecular_system, selection=selection_2, syntax=syntax)
            else:
                acceptors_2 = select(molecular_system, selection=selection_2, mask=acceptors_2, syntax=syntax)

            if donors_2 is None:
                donors_2 = get_donor_atoms(molecular_system, selection=selection_2, syntax=syntax)
            else:
                donors_2 = select(molecular_system, selection=selection_2, mask=donors_2, syntax=syntax)

            n_acceptors_2 = acceptors_2.shape[0]
            n_donors_2 = donors_2.shape[0]

            output_atoms=[]
            output_distances=[]
            output_angles=[]

            neighs, distances = get_neighbors(molecular_system, selection=donors[:,0],
                    selection_2=acceptors_2, structure_indices=structure_indices,
                    structure_indices_2=structure_indices_2, threshold=distance_threshold, pbc=pbc)

            neighs_2, distances_2 = get_neighbors(molecular_system, selection=donors_2[:,0],
                    selection_2=acceptors, structure_indices=structure_indices,
                    structure_indices_2=structure_indices_2, threshold=distance_threshold, pbc=pbc)

            for ll,mm in enumerate(structure_indices):

                tmp_atoms=[]
                tmp_distances=[]

                for ii in range(n_donors):
                    atom_d = donors[ii,0]
                    atom_h = donors[ii,1]
                    for jj, dist in zip(neighs[ll,ii], distances[ll,ii]):
                        if atom_d!=acceptors_2[jj]:
                            tmp_atoms.append([atom_d, atom_h, acceptors_2[jj]])
                            tmp_distances.append(dist)

                for ii in range(n_donors_2):
                    atom_d = donors_2[ii,0]
                    atom_h = donors_2[ii,1]
                    for jj, dist in zip(neighs_2[ll,ii], distances_2[ll,ii]):
                        if atom_d!=acceptors[jj]:
                            tmp_atoms.append([atom_d, atom_h, acceptors[jj]])
                            tmp_distances.append(dist)

                tmp_atoms = np.array(tmp_atoms)
                tmp_distances = puw.utils.sequences.concatenate(tmp_distances, value_type='numpy.ndarray')

                tmp_angles = get_angles(molecular_system, tmp_atoms[:,[1,0,2]], pbc=pbc,
                        structure_indices=mm)[0]
                mask = tmp_angles<angle_threshold

                output_atoms.append(tmp_atoms[mask,:])
                output_distances.append(tmp_distances[mask])
                output_angles.append(tmp_angles[mask])

            output_atoms=np.array(output_atoms)
            output_distances=puw.utils.sequences.concatenate(output_distances, value_type='numpy.ndarray')
            output_angles=puw.utils.sequences.concatenate(output_angles, value_type='numpy.ndarray')

            return output_atoms, output_distances, output_angles

    pass


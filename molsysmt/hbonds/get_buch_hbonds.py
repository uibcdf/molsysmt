from molsysmt._private.digestion import digest
from copy import copy
import numpy as np

def get_buch_hbonds(molecular_system, selection='all', acceptors=None, donors=None, structure_indices='all',
        molecular_system_2=None, selection_2=None, acceptors_2=None, donors_2=None, structure_indices_2=None,
        threshold='2.3 angstroms', pbc=True, syntax='MolSysMT'):

    from molsysmt.basic import select
    from .get_acceptor_atoms import get_acceptor_atoms
    from .get_donor_atoms import get_donor_atoms
    from molsysmt.structure import get_neighbors
    from molsysmt import pyunitwizard as puw

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

            neighs, distances = get_neighbors(molecular_system, selection=donors[:,1], selection_2=acceptors,
                structure_indices=structure_indices, structure_indices_2=structure_indices_2,
                threshold=threshold, pbc=pbc)

            output_atoms=[]
            output_distances=[]

            for structure_index in range(len(neighs)):
                tmp_atoms=[]
                tmp_distances=[]
                for ii in range(n_donors):
                    atom_d = donors[ii,0]
                    atom_h = donors[ii,1]
                    for jj, dist in zip(neighs[structure_index,ii], distances[structure_index,ii]):
                        if atom_d!=acceptors[jj]:
                            tmp_atoms.append([atom_d, atom_h, acceptors[jj]])
                            tmp_distances.append(dist)
                output_atoms.append(np.array(tmp_atoms))
                output_distances.append(puw.concatenate(tmp_distances, type_value='numpy.ndarray'))

            output_atoms=np.array(output_atoms)
            output_distances=puw.concatenate(output_distances, type_value='numpy.ndarray')

            return output_atoms, output_distances

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

            neighs, distances = get_neighbors(molecular_system, selection=donors[:,1],
                    selection_2=acceptors_2, structure_indices=structure_indices,
                    structure_indices_2=structure_indices_2, threshold=threshold, pbc=pbc)

            neighs_2, distances_2 = get_neighbors(molecular_system, selection=donors_2[:,1],
                    selection_2=acceptors, structure_indices=structure_indices,
                    structure_indices_2=structure_indices_2, threshold=threshold, pbc=pbc)

            output_atoms=[]
            output_distances=[]

            for structure_index in range(len(neighs)):

                tmp_atoms=[]
                tmp_distances=[]

                for ii in range(n_donors):
                    atom_d = donors[ii,0]
                    atom_h = donors[ii,1]
                    for jj, dist in zip(neighs[structure_index,ii], distances[structure_index,ii]):
                        if atom_d!=acceptors_2[jj]:
                            tmp_atoms.append([atom_d, atom_h, acceptors_2[jj]])
                            tmp_distances.append(dist)

                for ii in range(n_donors_2):
                    atom_d = donors_2[ii,0]
                    atom_h = donors_2[ii,1]
                    for jj, dist in zip(neighs_2[structure_index,ii], distances_2[structure_index,ii]):
                        if atom_d!=acceptors[jj]:
                            tmp_atoms.append([atom_d, atom_h, acceptors[jj]])
                            tmp_distances.append(dist)

                output_atoms.append(np.array(tmp_atoms))
                output_distances.append(puw.concatenate(tmp_distances, type_value='numpy.ndarray'))

            output_atoms=np.array(output_atoms)
            output_distances=puw.concatenate(output_distances, type_value='numpy.ndarray')

            return output_atoms, output_distances

    pass


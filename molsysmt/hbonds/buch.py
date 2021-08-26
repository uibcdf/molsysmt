# Source: V. J. Buch. J. Chem. Phys. 96, 3814-3823 (1992)

from molsysmt._private_tools._digestion import *
from molsysmt._private_tools.exceptions import *
from molsysmt.basic import select
from molsysmt import puw
import numpy as np

def buch(molecular_system, selection='all', selection_2=None, frame_indices='all', threshold='2.3 angstroms',
        acceptors=None, donors=None, pbc=False, optimize=False, output_form='dict', engine='MolSysMT', syntaxis='MolSysMT'):


    from molsysmt.hbonds.donors_and_acceptors import get_acceptor_atoms, get_donor_atoms
    from molsysmt.structure import get_neighbors

    molecular_system = digest_molecular_system(molecular_system)
    engine = digest_engine(engine)
    frame_indices = digest_frame_indices(frame_indices)

    output = None

    if selection_2 is None:

        if acceptors is None:
            acceptors_1 = get_acceptor_atoms(molecular_system, selection=selection, engine=engine, syntaxis=syntaxis)
        else:
            acceptors_1 = select(molecular_system, selection=selection, mask=acceptors, syntaxis=syntaxis)

        if donors is None:
            donors_1 = get_donor_atoms(molecular_system, selection=selection, engine=engine, syntaxis=syntaxis)
        else:
            donors_1 = select(molecular_system, selection=selection, mask=donors, syntaxis=syntaxis)

        neighs, _ = get_neighbors(molecular_system, selection=acceptors_1, selection_2=donors_1[0],
                frame_indices=frame_indices, threshold=threshold, pbc=pbc, engine=engine, syntaxis=syntaxis)

        if output_form == 'dict':

            output = {}

            n_acceptors = len(acceptors_1)
            for frame_index in range(neighs.shape[0]):
                for ii in range(n_acceptors):
                    for donor_index in neighs[frame_index][ii]:
                        hbond_id = tuple(donors_1[donor_index].tolist()+[acceptors_1[ii]])
                        try:
                            output[hbond_id].append(frame_index)
                        except:
                            output[hbond_id]=[frame_index]

        else:

            raise NotImplementedError

    else:

        if acceptors is None:
            acceptors_1 = get_acceptor_atoms(molecular_system, selection=selection, engine=engine, syntaxis=syntaxis)
            acceptors_2 = get_acceptor_atoms(molecular_system, selection=selection_2, engine=engine, syntaxis=syntaxis)
        else:
            acceptors_1 = select(molecular_system, selection=selection, mask=acceptors, syntaxis=syntaxis)
            acceptors_2 = select(molecular_system, selection=selection_2, mask=acceptors, syntaxis=syntaxis)

        if donors is None:
            donors_1 = get_donor_atoms(molecular_system, selection=selection, engine=engine, syntaxis=syntaxis)
            donors_2 = get_donor_atoms(molecular_system, selection=selection_2, engine=engine, syntaxis=syntaxis)
        else:
            donors_1 = select(molecular_system, selection=selection, mask=donors, syntaxis=syntaxis)
            donors_2 = select(molecular_system, selection=selection_2, mask=donors, syntaxis=syntaxis)

        neighs, _ = get_neighbors(molecular_system, selection=acceptors_1, selection_2=donors_2[0],
                frame_indices=frame_indices, threshold=threshold, pbc=pbc, engine=engine, syntaxis=syntaxis)

        neighs_2, _ = get_neighbors(molecular_system, selection=acceptors_2, selection_2=donors_1[0],
                frame_indices=frame_indices, threshold=threshold, pbc=pbc, engine=engine, syntaxis=syntaxis)

        if output_form == 'dict':

            output = {}

            n_acceptors = len(acceptors_1)
            for frame_index in range(neighs.shape[0]):
                for ii in range(n_acceptors):
                    for donor_index in neighs[frame_index][ii]:
                        hbond_id = tuple(donors_2[donor_index].tolist()+[acceptors_1[ii]])
                        try:
                            output[hbond_id].append(frame_index)
                        except:
                            output[hbond_id]=[frame_index]

            n_acceptors = len(acceptors_2)
            for frame_index in range(neighs_2.shape[0]):
                for ii in range(n_acceptors):
                    for donor_index in neighs_2[frame_index][ii]:
                        hbond_id = tuple(donors_1[donor_index].tolist()+[acceptors_2[ii]])
                        try:
                            output[hbond_id].append(frame_index)
                        except:
                            output[hbond_id]=[frame_index]

        else:

            raise NotImplementedError()

    return output


# Source: V. J. Buch. J. Chem. Phys. 96, 3814-3823 (1992)

from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from molsysmt.basic import select
from molsysmt import pyunitwizard as puw
import numpy as np

def get_hbonds(molecular_system, selection='all', selection_2=None, structure_indices='all', threshold='2.3 angstroms',
        acceptors=None, donors=None, pbc=False, optimize=False, output_form='dict',
        engine='MolSysMT', syntax='MolSysMT', method='Buch'):
    """
    To be written soon...
    """

    from molsysmt.hbonds.donors_and_acceptors import get_acceptor_atoms, get_donor_atoms
    from molsysmt.structure import get_neighbors

    molecular_system = digest_molecular_system(molecular_system)
    engine = digest_engine(engine)
    structure_indices = digest_structure_indices(structure_indices)

    output = None

    if selection_2 is None:

        if acceptors is None:
            acceptors_1 = get_acceptor_atoms(molecular_system, selection=selection, engine=engine, syntax=syntax)
        else:
            acceptors_1 = select(molecular_system, selection=selection, mask=acceptors, syntax=syntax)

        if donors is None:
            donors_1 = get_donor_atoms(molecular_system, selection=selection, engine=engine, syntax=syntax)
        else:
            donors_1 = select(molecular_system, selection=selection, mask=donors, syntax=syntax)

        neighs, _ = get_neighbors(molecular_system, selection=acceptors_1, selection_2=donors_1[0],
                structure_indices=structure_indices, threshold=threshold, pbc=pbc, engine=engine, syntax=syntax)

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
            acceptors_1 = get_acceptor_atoms(molecular_system, selection=selection, engine=engine, syntax=syntax)
            acceptors_2 = get_acceptor_atoms(molecular_system, selection=selection_2, engine=engine, syntax=syntax)
        else:
            acceptors_1 = select(molecular_system, selection=selection, mask=acceptors, syntax=syntax)
            acceptors_2 = select(molecular_system, selection=selection_2, mask=acceptors, syntax=syntax)

        if donors is None:
            donors_1 = get_donor_atoms(molecular_system, selection=selection, engine=engine, syntax=syntax)
            donors_2 = get_donor_atoms(molecular_system, selection=selection_2, engine=engine, syntax=syntax)
        else:
            donors_1 = select(molecular_system, selection=selection, mask=donors, syntax=syntax)
            donors_2 = select(molecular_system, selection=selection_2, mask=donors, syntax=syntax)

        neighs, _ = get_neighbors(molecular_system, selection=acceptors_1, selection_2=donors_2[0],
                structure_indices=structure_indices, threshold=threshold, pbc=pbc, engine=engine, syntax=syntax)

        neighs_2, _ = get_neighbors(molecular_system, selection=acceptors_2, selection_2=donors_1[0],
                structure_indices=structure_indices, threshold=threshold, pbc=pbc, engine=engine, syntax=syntax)

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


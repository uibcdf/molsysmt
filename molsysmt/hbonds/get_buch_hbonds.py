from molsysmt._private.argdigest import arg_digest
from copy import copy
import numpy as np

@arg_digest()
def get_buch_hbonds(molecular_system, selection='all', acceptors=None, donors=None, structure_indices='all',
        molecular_system_2=None, selection_2=None, acceptors_2=None, donors_2=None, structure_indices_2=None,
        distance_threshold='2.3 angstroms', pbc=True, syntax='MolSysMT', skip_digestion=False):
    """
    Calculating hydrogen bonds using the Buch geometric criteria.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    acceptors : numpy.ndarray, list, or tuple, default=None
        Precomputed atom indices of hydrogen bond acceptors.
    donors : numpy.ndarray, list, or tuple, default=None
        Precomputed atom indices of hydrogen bond donors.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    molecular_system_2 : object, default=None
        Argument molecular_system_2.
    selection_2 : str, list, tuple, or numpy.ndarray, default=None
        Second selection string or boolean/integer array.
    acceptors_2 : numpy.ndarray, list, or tuple, default=None
        Precomputed acceptor atom indices for selection_2.
    donors_2 : numpy.ndarray, list, or tuple, default=None
        Precomputed donor atom indices for selection_2.
    structure_indices_2 : int, list, tuple, or numpy.ndarray, default=None
        Structure indices (0-based) for the second selection.
    distance_threshold : object, default='2.3 angstroms'
        Argument distance_threshold.
    pbc : bool, default=True
        Whether to take periodic boundary conditions into account.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    tuple
        `(atoms, distances)` arrays per structure for the detected H-bonds.
    """

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

            offsets, indices, distances = get_neighbors(molecular_system, selection=donors[:,1],
                selection_2=acceptors, structure_indices=structure_indices,
                structure_indices_2=structure_indices_2, threshold=distance_threshold, pbc=pbc,
                output_type='csr')

            output_atoms=[]
            output_distances=[]

            n_structures = (len(offsets) - 1) // n_donors
            for structure_index in range(n_structures):
                tmp_atoms=[]
                tmp_distances=[]
                for ii in range(n_donors):
                    atom_d = donors[ii,0]
                    atom_h = donors[ii,1]
                    w = structure_index * n_donors + ii
                    for p in range(offsets[w], offsets[w+1]):
                        jj = indices[p]
                        if atom_d!=acceptors[jj]:
                            tmp_atoms.append([atom_d, atom_h, acceptors[jj]])
                            tmp_distances.append(distances[p])
                output_atoms.append(np.array(tmp_atoms))
                output_distances.append(puw.utils.sequences.concatenate(tmp_distances, value_type='numpy.ndarray'))

            output_atoms=np.array(output_atoms)
            output_distances=puw.utils.sequences.concatenate(output_distances, value_type='numpy.ndarray')

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

            offsets, indices, distances = get_neighbors(molecular_system, selection=donors[:,1],
                    selection_2=acceptors_2, structure_indices=structure_indices,
                    structure_indices_2=structure_indices_2, threshold=distance_threshold, pbc=pbc,
                    output_type='csr')

            offsets_2, indices_2, distances_2 = get_neighbors(molecular_system, selection=donors_2[:,1],
                    selection_2=acceptors, structure_indices=structure_indices,
                    structure_indices_2=structure_indices_2, threshold=distance_threshold, pbc=pbc,
                    output_type='csr')

            output_atoms=[]
            output_distances=[]

            n_structures = (len(offsets) - 1) // n_donors
            for structure_index in range(n_structures):

                tmp_atoms=[]
                tmp_distances=[]

                for ii in range(n_donors):
                    atom_d = donors[ii,0]
                    atom_h = donors[ii,1]
                    w = structure_index * n_donors + ii
                    for p in range(offsets[w], offsets[w+1]):
                        jj = indices[p]
                        if atom_d!=acceptors_2[jj]:
                            tmp_atoms.append([atom_d, atom_h, acceptors_2[jj]])
                            tmp_distances.append(distances[p])

                for ii in range(n_donors_2):
                    atom_d = donors_2[ii,0]
                    atom_h = donors_2[ii,1]
                    w = structure_index * n_donors_2 + ii
                    for p in range(offsets_2[w], offsets_2[w+1]):
                        jj = indices_2[p]
                        if atom_d!=acceptors[jj]:
                            tmp_atoms.append([atom_d, atom_h, acceptors[jj]])
                            tmp_distances.append(distances_2[p])

                output_atoms.append(np.array(tmp_atoms))
                output_distances.append(puw.utils.sequences.concatenate(tmp_distances, value_type='numpy.ndarray'))

            output_atoms=np.array(output_atoms)
            output_distances=puw.utils.sequences.concatenate(output_distances, value_type='numpy.ndarray')

            return output_atoms, output_distances

    pass

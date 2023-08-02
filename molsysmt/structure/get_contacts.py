from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
import numpy as np
import gc

#@digest()
def get_contacts(molecular_system, selection=None, center_of_atoms=False, weights=None, structure_indices="all",
                 selection_2=None, center_of_atoms_2=False, weights_2=None, structure_indices_2=None,
                 threshold='12 angstroms', pbc=False, syntax='MolSysMT', output_type='map', output_indices=None):

    """
    To be written soon...
    """

    from molsysmt.structure.get_distances import get_distances
    from molsysmt.basic import select

    atom_indices = select(molecular_system, selection=selection, syntax=syntax)

    if selection_2 is None:
        atom_indices_2 = None
    else:
        atom_indices_2 = select(molecular_system, selection=selection_2, syntax=syntax)

    all_dists = get_distances(molecular_system=molecular_system, selection=atom_indices,
                center_of_atoms=center_of_atoms, weights=weights, structure_indices=structure_indices,
                selection_2=atom_indices_2, center_of_atoms_2=center_of_atoms_2, weights_2=weights_2,
                structure_indices_2=structure_indices_2, pbc=pbc)

    length_units = puw.get_unit(all_dists)
    threshold = puw.get_value(threshold, to_unit=length_units)
    all_dists = puw.get_value(all_dists)

    num_structures=all_dists.shape[0]
    contact_map=np.empty(all_dists.shape, dtype=bool)
    for indice_structure in range(num_structures):
        contact_map[indice_structure,:,:]=(all_dists[indice_structure,:,:]<=threshold)

    del(all_dists, num_structures, indice_structure, length_units)

    gc.collect()

    if output_type=='map':
        return contact_map
    elif output_type=='pairs':

        pairs = []
        n_contact_maps = contact_map.shape[0]

        for ii in range(n_contact_maps):
            aux_pairs = np.nonzero(np.triu(contact_map[ii],k=1)==True)
            aux_pairs = np.column_stack(aux_pairs)
            pairs.append(aux_pairs)

        if output_indices is None:
            return pairs
        elif output_indices=='atom_index':
            if atom_indices_2 is None:
                for ii in range(n_contact_maps):
                    pairs[ii]=atom_indices[pairs[ii]]
            else:
                for ii in range(n_contact_maps):
                    pairs[ii]=np.column_stack(atom_indices[pairs[ii][:,0]],
                            atom_indices_2[pairs[ii][:,1]])
            return pairs

    pass


from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_iterable_of_pairs
from molsysmt import pyunitwizard as puw
import numpy as np
import gc

@digest()
def get_contacts(molecular_system, selection=None, center_of_atoms=False, weights=None, structure_indices="all",
                 selection_2=None, center_of_atoms_2=False, weights_2=None, structure_indices_2=None,
                 threshold='12 angstroms', pairs=False, pbc=True, syntax='MolSysMT',
                 output_type='numpy.ndarray', output_indices=None, skip_digestion=False):

    """
    To be written soon...
    """

    from molsysmt.structure.get_distances import get_distances
    from molsysmt.basic import select
    from molsysmt.pbc import has_pbc

    if pbc:
        pbc=has_pbc(molecular_system)

    if pairs and (selection_2 is None):
        if is_iterable_of_pairs(selection):
            if not isinstance(selection, np.ndarray):
                selection=np.array(selection)
            selection_2 = selection[:,1]
            selection = selection[:,0]

    atom_indices = select(molecular_system, selection=selection, syntax=syntax)

    if selection_2 is None:
        atom_indices_2 = None
    else:
        atom_indices_2 = select(molecular_system, selection=selection_2, syntax=syntax)

    all_dists = get_distances(molecular_system=molecular_system, selection=atom_indices,
                center_of_atoms=center_of_atoms, weights=weights, structure_indices=structure_indices,
                selection_2=atom_indices_2, center_of_atoms_2=center_of_atoms_2, weights_2=weights_2,
                structure_indices_2=structure_indices_2, pairs=pairs, pbc=pbc)

    length_units = puw.get_unit(all_dists)
    threshold = puw.get_value(threshold, to_unit=length_units)
    all_dists = puw.get_value(all_dists)

    num_structures=all_dists.shape[0]
    contact_map=np.empty(all_dists.shape, dtype=bool)


    for indice_structure in range(num_structures):
        if pairs:
            contact_map[indice_structure,:]=(all_dists[indice_structure,:]<=threshold)
        else:
            contact_map[indice_structure,:,:]=(all_dists[indice_structure,:,:]<=threshold)

    del(all_dists, num_structures, indice_structure, length_units)

    gc.collect()

    output = None

    if output_type=='numpy.ndarray':

        output = contact_map

    elif output_type in ['pairs', 'sorted pairs']:

        output = []
        n_contact_maps = contact_map.shape[0]

        if pairs:

            if output_indices=='selection':
                for ii in range(n_contact_maps):
                    aux_pairs = np.nonzero(contact_map[ii,:]==True)[0]
                    output.append(aux_pairs.tolist())
            elif output_indices=='atom':
                for ii in range(n_contact_maps):
                    aux_pairs = np.nonzero(contact_map[ii,:]==True)[0]
                    output.append([[selection[ii],selection_2[ii]] for ii in aux_pairs])

        else:

            if selection_2 is None:
                for ii in range(n_contact_maps):
                    aux_pairs = np.nonzero(np.triu(contact_map[ii],k=1)==True)
                    aux_pairs = np.column_stack(aux_pairs).tolist()
                    output.append(aux_pairs)
            else:
                for ii in range(n_contact_maps):
                    aux_pairs = np.nonzero(contact_map[ii])
                    aux_pairs = np.column_stack(aux_pairs).tolist()
                    output.append(aux_pairs)

            if output_indices=='atom':

                atom_indices = np.array(atom_indices)

                if atom_indices_2 is None:
                    for ii in range(n_contact_maps):
                        output[ii]=atom_indices[output[ii]].tolist()
                else:
                    atom_indices_2 = np.array(atom_indices_2)
                    for ii in range(n_contact_maps):
                        aux_pairs = np.array(output[ii])
                        output[ii]=np.column_stack([atom_indices[aux_pairs[:,0]],
                                atom_indices_2[aux_pairs[:,1]]]).tolist()

        if output_type=='sorted pairs':
            for ii in range(n_contact_maps):
                output[ii] = sorted(output[ii])

    return output




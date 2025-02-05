from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
from molsysmt._private.lists import sorted_list_of_pairs
import numpy as np

@digest()
def get_neighbors(molecular_system, selection="all", structure_indices="all", center_of_atoms=False, weights=None,
                  molecular_system_2=None, selection_2=None, structure_indices_2=None, center_of_atoms_2=False, weights_2=None,
                  threshold=None, n_neighbors=None, pairs=False, mutual_only=False, pbc=True, output_type='numpy.ndarray',
                  output_indices=None, output_structure_indices=None,
                  sorted=True, engine='MolSysMT', syntax='MolSysMT', skip_digestion=False):
    """
    To be written soon...
    """

    from . import get_distances
    from molsysmt.basic import select
    from molsysmt.pbc import has_pbc

    if pbc:
        pbc=has_pbc(molecular_system)

    same_set = False

    same_selections = False
    same_structures = False

    if (selection is not None) and (selection_2 is None):
        same_selections = True

    if structure_indices_2 is None:
        same_structures = True

    same_set= same_selections and same_structures

    output_get_distances = get_distances(molecular_system=molecular_system, selection=selection,
               structure_indices=structure_indices, center_of_atoms=center_of_atoms, weights=weights,
               selection_2=selection_2, structure_indices_2=structure_indices_2, center_of_atoms_2=center_of_atoms_2,
               output_type='numpy.ndarray', output_indices=output_indices, output_structure_indices=output_structure_indices,
               weights_2=weights_2, pbc=pbc, engine=engine, syntax=syntax)

    if output_indices is None and output_structure_indices is None:
        all_dists = output_get_distances
    else:
        all_dists = output_get_distances[-1]

    nstructures, nelements_1, nelements_2 = all_dists.shape
    length_units = puw.get_unit(all_dists)
    all_dists = puw.get_value(all_dists)

    if n_neighbors is not None and threshold is None:

        neighs=np.empty((nstructures, nelements_1, n_neighbors), dtype=int)
        dists=np.empty((nstructures, nelements_1, n_neighbors), dtype=float)

        offset = 0
        if same_set:
            offset = 1

        for indice_structure in range(nstructures):
            for ii in range(nelements_1):
                neighs_aux = np.argpartition(all_dists[indice_structure,ii,:], n_neighbors-1+offset)[:n_neighbors+offset]
                dists_aux = all_dists[indice_structure,ii,neighs_aux]
                good_order = np.argsort(dists_aux)
                neighs_aux = neighs_aux[good_order]
                dists_aux = dists_aux[good_order]
                neighs[indice_structure,ii,:]=neighs_aux[offset:]
                dists[indice_structure,ii,:]=dists_aux[offset:]
                if same_set:
                    if dists_aux[0] > 0.01:
                        raise ValueError("Error in algorithm, sets are different.")

        del(all_dists)

        dists=dists*length_units

    elif threshold is not None and n_neighbors is None:

        threshold = puw.get_value(threshold, to_unit=length_units)

        neighs=np.empty((nstructures, nelements_1), dtype=object)
        dists=np.empty((nstructures, nelements_1), dtype=object)

        offset = 0
        if same_set:
            offset = 1

        for indice_structure in range(nstructures):
            for ii in range(nelements_1):
                neighs_aux = np.argwhere(all_dists[indice_structure,ii,:]<=threshold)[:,0]
                dists_aux = all_dists[indice_structure,ii,neighs_aux]
                good_order = np.argsort(dists_aux)
                neighs_aux = neighs_aux[good_order]
                dists_aux = dists_aux[good_order]
                neighs[indice_structure,ii]=neighs_aux[offset:]
                dists[indice_structure,ii]=dists_aux[offset:]
                if same_set:
                    if dists_aux[0] > 0.01:
                        raise ValueError("Error in algorithm, sets are different.")

        del(all_dists)

        dists=dists*length_units

    else:

        raise ValueError("Use either threshold or n_neighbors, but not both at the same time")

    if output_type == 'numpy.ndarray':
        if output_indices is None and output_structure_indices is None:
            return neighs, dists
        else:
            raise NotImplementedError
    elif output_type == 'pairs':
        with_output_indices = False
        if output_indices is not None:
            with_output_indices = True
            if len(output_get_distances)==2:
                aux_indices_1 = output_get_distances[0]
                aux_indices_2 = aux_indices_1
            elif len(output_get_distances)==3:
                aux_indices_1 = output_get_distances[0]
                aux_indices_2 = output_get_distances[1]
            else:
                raise NotImplementedError
        if output_indices is not None:
            neighs_pairs = []
            dists_pairs = []
            for ii in range(nstructures):
                aux_pairs = []
                aux_dists = []
                for jj in range(nelements_1):
                    for kk in range(len(neighs[ii,jj])):
                        aux_dists.append(dists[ii,jj][kk])
                        if with_output_indices:
                            aux_pairs.append([aux_indices_1[jj], aux_indices_2[neighs[ii,jj][kk]]])
                        else:
                            aux_pairs.append([jj, neighs[ii,jj][kk]])
                if mutual_only:
                    tmp_pairs = []
                    tmp_dists = []
                    for pair, dist in zip(aux_pairs, aux_dists):
                        if ([pair[1], pair[0]] in aux_pairs) and (pair[0]<pair[1]):
                            tmp_pairs.append(pair)
                            tmp_dists.append(dist)
                    aux_pairs = tmp_pairs
                    aux_dists = tmp_dists
                if len(aux_dists)>0:
                    aux_dists = puw.concatenate(aux_dists, type_value='list')
                if sorted:
                    aux_pairs, aux_dists = sorted_list_of_pairs(aux_pairs, aux_dists)
                neighs_pairs.append(aux_pairs)
                dists_pairs.append(aux_dists)
            return neighs_pairs, dists_pairs
        else:
            raise NotImplementedError

    raise ValueError

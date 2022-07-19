from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from molsysmt import puw
import numpy as np

def get_neighbors(molecular_system, selection="all", groups_of_atoms=None, group_behavior=None, structure_indices="all",
                  molecular_system_2=None, selection_2=None, groups_of_atoms_2=None, group_behavior_2=None, structure_indices_2=None,
                  threshold=None, num_neighbors=None, atom_indices=False, pbc=False, parallel=False,
                  engine='MolSysMT', syntax='MolSysMT', check=True):

    if check:

        digest_single_molecular_system(molecular_system)
        if molecular_system_2 is not None:
            digest_single_molecular_system(molecular_system_2)

        syntax = digest_syntax(syntax)
        selection = digest_selection(selection, syntax)
        selection_2 = digest_selection(selection_2, syntax)

        structure_indices = digest_structure_indices(structure_indices)
        if structure_indices_2 is not None:
            structure_indices_2 = digest_structure_indices(structure_indices_2)

        engine = digest_engine(engine)

    from . import get_distances

    if (threshold is None) and (num_neighbors is None):
        raise BadCallError(BadCallMessage)

    same_set = False

    same_selections = False
    same_groups = False
    same_structures = False

    if groups_of_atoms is not None:
        selection=None

    if (selection is not None) and (selection_2 is None) and (groups_of_atoms_2 is None):
        same_selections = True
    elif (groups_of_atoms is not None) and (selection_2 is None) and (groups_of_atoms_2 is None):
        same_groups = True

    if structure_indices_2 is None:
        same_structures = True

    same_set= (same_selections or same_groups) and same_structures

    if atom_indices:

        atom_indices_1, atom_indices_2, all_dists = get_distances(molecular_system=molecular_system, selection=selection, groups_of_atoms=groups_of_atoms,
                                                    group_behavior=group_behavior, structure_indices=structure_indices,
                                                    molecular_system_2=molecular_system_2, selection_2=selection_2, groups_of_atoms_2=groups_of_atoms_2,
                                                    group_behavior_2=group_behavior_2, structure_indices_2=structure_indices_2,
                                                    pbc=pbc, parallel=parallel, output_form='tensor', engine=engine, syntax=syntax, check=False)

    else:

        all_dists = get_distances(molecular_system=molecular_system, selection=selection, groups_of_atoms=groups_of_atoms,
                            group_behavior=group_behavior, structure_indices=structure_indices,
                            selection_2=selection_2, groups_of_atoms_2=groups_of_atoms_2,
                            group_behavior_2=group_behavior_2, structure_indices_2=structure_indices_2,
                            pbc=pbc, parallel=parallel, output_form='tensor', engine=engine, syntax=syntax, check=False)

    nstructures, nelements_1, nelements_2 = all_dists.shape
    length_units = puw.get_unit(all_dists)
    all_dists = puw.get_value(all_dists)

    if num_neighbors is not None and threshold is None:

        neighs=np.empty((nstructures, nelements_1, num_neighbors), dtype=int)
        dists=np.empty((nstructures, nelements_1, num_neighbors), dtype=float)

        offset = 0
        if same_set:
            offset = 1

        for indice_structure in range(nstructures):
            for ii in range(nelements_1):
                neighs_aux = np.argpartition(all_dists[indice_structure,ii,:], num_neighbors-1+offset)[:num_neighbors+offset]
                dists_aux = all_dists[indice_structure,ii,neighs_aux]
                good_order = np.argsort(dists_aux)
                neighs_aux = neighs_aux[good_order]
                dists_aux = dists_aux[good_order]
                if atom_indices:
                    neighs[indice_structure,ii,:]=atom_indices_2[neighs_aux[offset:]]
                else:
                    neighs[indice_structure,ii,:]=neighs_aux[offset:]
                dists[indice_structure,ii,:]=dists_aux[offset:]
                if same_set:
                    if dists_aux[0] > 0.01:
                        raise ValueError("Error in algorithm, sets are different.")

        del(all_dists)

        dists=dists*length_units

        return neighs, dists

    elif threshold is not None and num_neighbors is None:

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
                if atom_indices:
                    neighs[indice_structure,ii]=atom_indices_2[np.array(neighs_aux,dtype=int)[offset:]]
                else:
                    neighs[indice_structure,ii]=np.array(neighs_aux,dtype=int)[offset:]
                dists[indice_structure,ii]=np.array(dists_aux,dtype=float)[offset:]
                if same_set:
                    if dists_aux[0] > 0.01:
                        raise ValueError("Error in algorithm, sets are different.")

        del(all_dists)

        dists=dists*length_units

        return neighs, dists

    else:

        raise ValueError("Use either threshold or num_neighbors, but not both at the same time")


from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
import numpy as np
import gc

@digest()
def get_contacts(molecular_system, selection=None, groups_of_atoms=None, group_behavior=None, structure_indices="all",
                 selection_2=None, groups_of_atoms_2=None, group_behavior_2=None, structure_indices_2=None,
                 threshold='12 angstroms', pbc=False,
                 engine='MolSysMT', syntax='MolSysMT'):

    from molsysmt.structure.get_distances import get_distances

    all_dists = get_distances(molecular_system=molecular_system, selection=selection, groups_of_atoms=groups_of_atoms,
                group_behavior=group_behavior, structure_indices=structure_indices,
                selection_2=selection_2, groups_of_atoms_2=groups_of_atoms_2,
                group_behavior_2=group_behavior_2, structure_indices_2=structure_indices_2,
                pbc=pbc, engine=engine, syntax=syntax)

    length_units = puw.get_unit(all_dists)
    threshold = puw.get_value(threshold, to_unit=length_units)
    all_dists = puw.get_value(all_dists)

    num_structures=all_dists.shape[0]
    contact_map=np.empty(all_dists.shape, dtype=bool)
    for indice_structure in range(num_structures):
        contact_map[indice_structure,:,:]=(all_dists[indice_structure,:,:]<=threshold)

    del(all_dists, num_structures, indice_structure, length_units)
    gc.collect()

    return contact_map


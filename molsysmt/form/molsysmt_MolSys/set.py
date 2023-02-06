from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

###### Set

## Atom

@digest(form='molsysmt.MolSys')
def set_atom_name_to_atom(item, indices='all', structure_indices='all', value=None):

    from ..molsysmt_Topology import set_atom_name_to_atom as aux_set

    return aux_set(item.topology, indices=indices, structure_indices=structure_indices, value=value)

@digest(form='molsysmt.MolSys')
def set_coordinates_to_atom(item, indices='all', structure_indices='all', value=None):

    from ..molsysmt_Structures import set_coordinates_to_atom as molsysmt_Structures_set_coordinates_to_atom
    from ..molsysmt_Topology import get_n_atoms_from_system as molsysmt_Topology_get_n_atoms_from_system

    if is_all(indices):
        n_atoms = molsysmt_Topology_get_n_atoms_from_system(item.topology)
        if n_atoms!=value.shape[1]:
            raise ValueError('Coordinates has a different atoms number.')

    return molsysmt_Structures_set_coordinates_to_atom(item.structures, indices=indices, structure_indices=structure_indices,
                value=value)

## System

@digest(form='molsysmt.MolSys')
def set_structure_id_to_system(item, structure_indices='all', value=None):

    from ..molsysmt_Structures import set_structure_id_to_system as molsysmt_Structures_set_structure_id_to_system

    return molsysmt_Structures_set_structure_id_to_system(item.structures, structure_indices=structure_indices, value=value)

@digest(form='molsysmt.MolSys')
def set_time_to_system(item, structure_indices='all', value=None):

    from ..molsysmt_Structures import set_time_to_system as molsysmt_Structures_set_time_to_system

    return molsysmt_Structures_set_time_to_system(item.structures, structure_indices=structure_indices, value=value)

@digest(form='molsysmt.MolSys')
def set_box_to_system(item, structure_indices='all', value=None):

    from ..molsysmt_Structures import set_box_to_system as molsysmt_Structures_set_box_to_system

    return molsysmt_Structures_set_box_to_system(item.structures, structure_indices=structure_indices, value=value)

@digest(form='molsysmt.MolSys')
def set_coordinates_to_system(item, indices='all', structure_indices='all', value=None):

    return set_coordinates_to_atom(item, indices='all', structure_indices=structure_indices,
            value=value)


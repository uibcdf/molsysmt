from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

###### Set

## Atom

@arg_digest(form='molsysmt.Structures')
def set_coordinates_to_atom(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

    item.set_coordinates(indices=indices, structure_indices=structure_indices, value=value,
                         skip_digestion=True)

@arg_digest(form='molsysmt.Structures')
def set_velocities_to_atom(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

    item.set_velocities(indices=indices, structure_indices=structure_indices, value=value,
                         skip_digestion=True)

@arg_digest(form='molsysmt.Structures')
def set_occupancy_to_atom(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

    item.set_occupancy(indices=indices, structure_indices=structure_indices, value=value,
                       skip_digestion=True)

@arg_digest(form='molsysmt.Structures')
def set_b_factor_to_atom(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

    item.set_b_factor(indices=indices, structure_indices=structure_indices, value=value,
                      skip_digestion=True)

## System

@arg_digest(form='molsysmt.Structures')
def set_structure_id_to_system(item, structure_indices='all', value=None, skip_digestion=False):

    item.set_structure_id(structure_indices=structure_indices, value=value, skip_digestion=True)

@arg_digest(form='molsysmt.Structures')
def set_time_to_system(item, structure_indices='all', value=None, skip_digestion=False):

    item.set_time(structure_indices=structure_indices, value=value, skip_digestion=True)

@arg_digest(form='molsysmt.Structures')
def set_box_to_system(item, structure_indices='all', value=None, skip_digestion=False):

    item.set_box(structure_indices=structure_indices, value=value, skip_digestion=True)

@arg_digest(form='molsysmt.Structures')
def set_coordinates_to_system(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

    return set_coordinates_to_atom(item, indices='all', structure_indices=structure_indices,
            value=value, skip_digestion=True)

@arg_digest(form='molsysmt.Structures')
def set_velocities_to_system(item, indices='all', structure_indices='all', value=None, skip_digestion=False):

    return set_velocities_to_atom(item, indices='all', structure_indices=structure_indices,
            value=value, skip_digestion=True)


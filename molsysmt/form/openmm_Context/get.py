#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.execfile import execfile
from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

form='openmm.Context'


## From atom

@digest(form=form)
def get_atom_id_from_atom(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_atom_name_from_atom(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_atom_type_from_atom(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_group_index_from_atom(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_component_index_from_atom(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_chain_index_from_atom(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_molecule_index_from_atom(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_entity_index_from_atom(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_inner_bonded_atoms_from_atom(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_n_inner_bonds_from_atom(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all'):

    coordinates = item.getState(getPositions=True).getPositions(asNumpy=True)
    unit = puw.get_unit(coordinates)
    coordinates = puw.get_value(coordinates)
    coordinates = coordinates.reshape(1, coordinates.shape[0], coordinates.shape[1])

    if not is_all(structure_indices):
        coordinates = coordinates[structure_indices,:,:]

    if not is_all(indices):
        coordinates = coordinates[:,indices,:]

    coordinates = coordinates * unit
    coordinates = puw.standardize(coordinates)

    return coordinates


## From group

@digest(form=form)
def get_group_id_from_group(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_group_name_from_group(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_group_type_from_group(item, indices='all'):

    raise NotWithThisFormError()


## From component

@digest(form=form)
def get_component_id_from_component(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_component_name_from_component(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_component_type_from_component(item, indices='all'):

    raise NotWithThisFormError()


## From molecule

@digest(form=form)
def get_molecule_id_from_molecule(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_molecule_name_from_molecule(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_molecule_type_from_molecule(item, indices='all'):

    raise NotWithThisFormError()


## From chain

@digest(form=form)
def get_chain_id_from_chain(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_chain_name_from_chain(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_chain_type_from_chain(item, indices='all'):

    raise NotWithThisFormError()


## From entity

@digest(form=form)
def get_entity_id_from_entity(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_entity_name_from_entity(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_entity_type_from_entity(item, indices='all'):

    raise NotWithThisFormError()


## From system

@digest(form=form)
def get_n_atoms_from_system(item):

    return item.getSystem().getNumParticles()

@digest(form=form)
def get_n_groups_from_system(item):

    raise NotWithThisFormError()

@digest(form=form)
def get_n_components_from_system(item):

    raise NotWithThisFormError()

@digest(form=form)
def get_n_chains_from_system(item):

    raise NotWithThisFormError()

@digest(form=form)
def get_n_molecules_from_system(item):

    raise NotWithThisFormError()

@digest(form=form)
def get_n_entities_from_system(item):

    raise NotWithThisFormError()

@digest(form=form)
def get_n_bonds_from_system(item):

    raise NotWithThisFormError()

@digest(form=form)
def get_box_from_system(item, structure_indices='all'):

    box=item.getState().getPeriodicBoxVectors(asNumpy=True)

    if box is not None:
        box_unit = box.unit
        box = np.array(box._value)
        box = box.reshape(1, box.shape[0], box.shape[1])
        box = box * box_unit

    output=None

    if box is not None:
        if is_all(structure_indices):
            output=box
        else:
            output=box[structure_indices,:,:]

    return output

@digest(form=form)
def get_time_from_system(item, structure_indices='all'):

    output = item.getState().getTime()
    value = puw.get_value(output)
    unit = puw.get_unit(output)
    output = np.array([value])*unit
    output = puw.standardize(output)

    return output

@digest(form=form)
def get_structure_id_from_system(item, structure_indices='all'):

    return None

@digest(form=form)
def get_n_structures_from_system(item, structure_indices='all'):

    if is_all(structure_indices):
        return 1
    else:
        len(structure_indices)

@digest(form=form)
def get_bonded_atoms_from_system(item):

    raise NotWithThisFormError()


## From bond

@digest(form=form)
def get_bond_order_from_bond(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_bond_type_from_bond(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_bonded_atoms_from_bond(item, indices='all'):

    raise NotWithThisFormError()


#######################################################################################
######### DO NOT TOUCH THE FOLLOWING LINES, JUST INCLUDE THEM AS THEY ARE #############
#######################################################################################

from os import path
this_folder = path.dirname(path.abspath(__file__))
common_get = path.join(this_folder, '../../_private/common_get.py')
execfile(common_get, globals(), locals())
del(path, this_folder, common_get)


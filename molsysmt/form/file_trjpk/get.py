#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.execfile import execfile
from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import pickle

form='file:trjpk'


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

    fff = open(item, 'rb')
    _ = pickle.load(fff)
    _ = pickle.load(fff)
    coordinates = pickle.load(fff)
    fff.close()

    if coordinates is not None:
        if not is_all(structure_indices):
            coordinates = coordinates[structure_indices, :, :]
        if not _is_all(indices):
            coordinates = coordinates[:, indices, :]
        coordinates = puw.quantity(coordinates, to_unit='nm')

    return coordinates


## From group

@digest(form=form)
def get_group_id_from_group(item, indices='all'):

    raise NotImplementedMethodError()

@digest(form=form)
def get_group_name_from_group(item, indices='all'):

    raise NotImplementedMethodError()

@digest(form=form)
def get_group_type_from_group(item, indices='all'):

    raise NotImplementedMethodError()


## From component

@digest(form=form)
def get_component_id_from_group(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_component_name_from_group(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_component_type_from_group(item, indices='all'):

    raise NotWithThisFormError()


## From molecule

@digest(form=form)
def get_molecule_id_from_group(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_molecule_name_from_group(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_molecule_type_from_group(item, indices='all'):

    raise NotWithThisFormError()


## From chain

@digest(form=form)
def get_chain_id_from_group(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_chain_name_from_group(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_chain_type_from_group(item, indices='all'):

    raise NotWithThisFormError()


## From entity

@digest(form=form)
def get_entity_id_from_group(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_entity_name_from_group(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_entity_type_from_group(item, indices='all'):

    raise NotWithThisFormError()


## From system

@digest(form=form)
def get_n_atoms_from_system(item):

    fff = open(item, 'rb')
    n_atoms = pickle.load(fff)
    fff.close()

    return n_atoms

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
def get_n_structures_from_system(item):

    fff = open(item, 'rb')
    _ = pickle.load(fff)
    n_structures = pickle.load(fff)
    fff.close()

    return n_structures

@digest(form=form)
def get_box_from_system(item, structure_indices='all'):

    fff = open(item, 'rb')
    _ = pickle.load(fff)
    _ = pickle.load(fff)
    _ = pickle.load(fff)
    box = pickle.load(fff)
    fff.close()

    if box is not None:
        if not is_all(structure_indices):
            box = box[structure_indices, :, :]

        box = puw.quantity(box, to_unit='nm')

    return box

@digest(form=form)
def get_time_from_system(item, structure_indices='all'):

    fff = open(item, 'rb')
    _ = pickle.load(fff)
    _ = pickle.load(fff)
    _ = pickle.load(fff)
    _ = pickle.load(fff)
    time = pickle.load(fff)
    fff.close()

    if time is not None:
        if not is_all(structure_indices):
            time = time[structure_indices]

        time = puw.quantity(time, to_unit='nm')

    return time

@digest(form=form)
def get_step_from_system(item, structure_indices='all'):

    fff = open(item, 'rb')
    _ = pickle.load(fff)
    _ = pickle.load(fff)
    _ = pickle.load(fff)
    _ = pickle.load(fff)
    _ = pickle.load(fff)
    step = pickle.load(fff)
    fff.close()

    if step is not None:
        if not is_all(structure_indices):
            step = step[structure_indices]

    return step


#######################################################################################
######### DO NOT TOUCH THE FOLLOWING LINES, JUST INCLUDE THEM AS THEY ARE #############
#######################################################################################

from os import path
this_folder = path.dirname(path.abspath(__file__))
common_get = path.join(this_folder, '../../_private/common_get.py')
execfile(common_get, globals(), locals())
del(path, this_folder, common_get)


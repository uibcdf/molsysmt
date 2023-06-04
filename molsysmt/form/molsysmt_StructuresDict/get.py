#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.execfile import execfile
from molsysmt._private.exceptions import NotWithThisFormError, NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np

form='molsysmt.StructuresDict'


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

    tmp_coordinates = item['coordinates']

    if not is_all(structure_indices):
        tmp_coordinates = tmp_coordinates[structure_indices,:,:]

    if not is_all(indices):
        tmp_coordinates = tmp_coordinates[:,indices,:]

    return tmp_coordinates.astype(np.float64)


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

    output = None

    if 'coordinates' in item:
        output = item['coordinates'].shape[1]

    return output

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

    output = None

    if 'coordinates' in item:
        output=item['coordinates'].shape[0]
    elif 'box' in item:
        len_shape = len(item['box'].shape)
        if len_shape==3:
            output=item['box'].shape[0]
        elif len_shape==2:
            output=1

    return output

@digest(form=form)
def get_box_from_system(item, structure_indices='all'):

    output=None

    if 'box' in item:

        len_shape = len(item['box'].shape)

        if len_shape==3:
            if is_all(structure_indices):
                output=item['box']
            else:
                output=item['box'][structure_indices,:,:]
        elif len_shape==2:
            if is_all(structure_indices):
                n_structures=get_n_structures_from_system(item)
            else:
                n_structures=len(structure_indices)
            output=np.tile(item['box'], (n_structures, 1, 1))

    return output.astype(np.float64)

@digest(form=form)
def get_structure_id_from_system(item, structure_indices='all'):

    output = None
    if is_all(structure_indices):
        output = item['structure_id']
    else:
        output = item['structure_id'][structure_indices]
    return output

@digest(form=form)
def get_time_from_system(item, structure_indices='all'):

    output = None
    if is_all(structure_indices):
        output = item['time']
    else:
        output = item['time'][structure_indices]
    return output


#######################################################################################
######### DO NOT TOUCH THE FOLLOWING LINES, JUST INCLUDE THEM AS THEY ARE #############
#######################################################################################

from os import path
this_folder = path.dirname(path.abspath(__file__))
common_get = path.join(this_folder, '../../_private/common_get.py')
execfile(common_get, globals(), locals())
del(path, this_folder, common_get)


#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.execfile import execfile
from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np

form='MDAnalysis.Topology'


## From atom

@digest(form=form)
def get_atom_id_from_atom(item, indices='all'):

    output = item.ids.values
    if not is_all(indices):
        output = output[indices]
    return output

@digest(form=form)
def get_atom_name_from_atom(item, indices='all'):

    output = item.names.values
    if not is_all(indices):
        output = output[indices]
    return output

@digest(form=form)
def get_atom_type_from_atom(item, indices='all'):

    output = item.types.values
    if not is_all(indices):
        output = output[indices]
    return output

@digest(form=form)
def get_group_index_from_atom(item, indices='all'):

    if is_all(indices):
        n_atoms = get_n_atoms_from_system(item)
        indices = np.arange(n_atoms)

    output = item.tt.atoms2residues(indices)

    return output

@digest(form=form)
def get_component_index_from_atom(item, indices='all'):

    if is_all(indices):
        n_atoms = get_n_atoms_from_system(item)
        indices = np.arange(n_atoms)

    output = item.tt.atoms2segments(indices)

    return output

@digest(form=form)
def get_chain_index_from_atom(item, indices='all'):

    if is_all(indices):
        n_atoms = get_n_atoms_from_system(item)
        indices = np.arange(n_atoms)

    output = item.tt.atoms2segments(indices)

    return output

@digest(form=form)
def get_molecule_index_from_atom(item, indices='all'):

    raise NotImplementedMethodError()

@digest(form=form)
def get_entity_index_from_atom(item, indices='all'):

    raise NotImplementedMethodError()

@digest(form=form)
def get_inner_bonded_atoms_from_atom(item, indices='all'):

    raise NotImplementedMethodError()

@digest(form=form)
def get_n_inner_bonds_from_atom(item, indices='all'):

    raise NotImplementedMethodError()

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
def get_component_id_from_component(item, indices='all'):

    raise NotImplementedMethodError()

@digest(form=form)
def get_component_name_from_component(item, indices='all'):

    raise NotImplementedMethodError()

@digest(form=form)
def get_component_type_from_component(item, indices='all'):

    raise NotImplementedMethodError()

## From molecule

@digest(form=form)
def get_molecule_id_from_molecule(item, indices='all'):

    raise NotImplementedMethodError()

@digest(form=form)
def get_molecule_name_from_molecule(item, indices='all'):

    raise NotImplementedMethodError()

@digest(form=form)
def get_molecule_type_from_molecule(item, indices='all'):

    raise NotImplementedMethodError()

## From chain

@digest(form=form)
def get_chain_id_from_chain(item, indices='all'):

    raise NotImplementedMethodError()

@digest(form=form)
def get_chain_name_from_chain(item, indices='all'):

    raise NotImplementedMethodError()

@digest(form=form)
def get_chain_type_from_chain(item, indices='all'):

    raise NotImplementedMethodError()

## From entity

@digest(form=form)
def get_entity_id_from_entity(item, indices='all'):

    raise NotImplementedMethodError()

@digest(form=form)
def get_entity_name_from_entity(item, indices='all'):

    raise NotImplementedMethodError()

@digest(form=form)
def get_entity_type_from_entity(item, indices='all'):

    raise NotImplementedMethodError()

## From system

@digest(form=form)
def get_n_atoms_from_system(item):

    return item.n_atoms

@digest(form=form)
def get_n_groups_from_system(item):

    return item.n_residues

@digest(form=form)
def get_n_components_from_system(item):

    raise NotImplementedMethodError()

@digest(form=form)
def get_n_chains_from_system(item):

    return item.n_segments

@digest(form=form)
def get_n_molecules_from_system(item):

    raise NotImplementedMethodError()

@digest(form=form)
def get_n_entities_from_system(item):

    raise NotImplementedMethodError()

@digest(form=form)
def get_n_bonds_from_system(item):

    return len(item.bonds.values)

@digest(form=form)
def get_n_structures_from_system(item, structure_indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_box_from_system(item, structure_indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_time_from_system(item, structure_indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_structure_id_from_system(item, structure_indices='all'):

    raise NotWithThisFormError()


## From bond

@digest(form=form)
def get_bond_order_from_bond(item, indices='all'):

    raise NotImplementedMethodError()

@digest(form=form)
def get_bond_type_from_bond(item, indices='all'):

    raise NotImplementedMethodError()

@digest(form=form)
def get_atom_index_from_bond(item, indices='all'):

    raise NotImplementedMethodError()


#######################################################################################
######### DO NOT TOUCH THE FOLLOWING LINES, JUST INCLUDE THEM AS THEY ARE #############
#######################################################################################

from os import path
this_folder = path.dirname(path.abspath(__file__))
common_get = path.join(this_folder, '../../_private/common_get.py')
execfile(common_get, globals(), locals())
del(path, this_folder, common_get)


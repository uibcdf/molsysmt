#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.execfile import execfile
from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.digestion import digest

form='molsysmt.MSMH5FileHandler'


## From atom

@digest(form=form)
def get_atom_id_from_atom(item, indices='all'):

    output = item.file['topology']['atoms']['id'][:].astype('int64')

    if not is_all(indices):
        output = output[indices]

    return output

@digest(form=form)
def get_atom_name_from_atom(item, indices='all'):

    output = item.file['topology']['atoms']['name'][:].astype('str')

    if not is_all(indices):
        output = output[indices]

    return output

@digest(form=form)
def get_atom_type_from_atom(item, indices='all'):

    output = item.file['topology']['atoms']['type'][:].astype('str')

    if not is_all(indices):
        output = output[indices]

    return output

@digest(form=form)
def get_group_index_from_atom(item, indices='all'):

    output = item.file['topology']['atoms']['group_index'][:].astype('int')

    if not is_all(indices):
        output = output[indices]

    return output

@digest(form=form)
def get_component_index_from_atom(item, indices='all'):

    group_index = get_group_index_from_atom(item, indices)
    component_index_from_group = item.file['topology']['groups']['component_index'][:].astype('int')
    output = component_index_from_group[group_index]

    return output

@digest(form=form)
def get_chain_index_from_atom(item, indices='all'):

    output = item.file['topology']['atoms']['chain_index'][:].astype('int')

    if not is_all(indices):
        output = output[indices]

    return output

@digest(form=form)
def get_molecule_index_from_atom(item, indices='all'):

    component_index = get_component_index_from_atom(item, indices)
    molecule_index_from_component = item.file['topology']['components']['molecule_index'][:].astype('int')
    output = molecule_index_from_component[component_index]

    return output

@digest(form=form)
def get_entity_index_from_atom(item, indices='all'):

    molecule_index = get_molecule_index_from_atom(item, indices)
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    output = entity_index_from_molecule[molecule_index]

    return output

@digest(form=form)
def get_inner_bonded_atoms_from_atom(item, indices='all'):

    if is_all(indices):

        output = get_bonded_atoms_from_bond(item, indices='all')

    else:

        bond_indices = get_inner_bond_index_from_atom (item, indices=indices)
        output = get_bonded_atoms_from_bond(item, indices=bond_indices)
        del(bond_indices)

    output = output[np.lexsort((output[:, 1], output[:, 0]))]

    return(output)

@digest(form=form)
def get_n_inner_bonds_from_atom(item, indices='all'):

    bond_indices = get_inner_bond_index_from_atom(item, indices=indices)
    output = bond_indices.shape[0]
    del(bond_indices)
    return(output)

@digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all'):

    if is_all(structure_indices):
        if is_all(indices):
            output = item.file['structures']['coordinates'][:,:,:].astype('float')
        else:
            output = item.file['structures']['coordinates'][:,indices,:].astype('float')
    else:
        output = []
        for ii in structure_indices:
            output.append(item.file['structures']['coordinates'][ii,indices,:].astype('float'))
        output = np.array(output)

    return output

## From group

@digest(form=form)
def get_group_id_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_group_name_from_group(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_group_type_from_group(item, indices='all'):

    raise NotImplementedError

## From component

@digest(form=form)
def get_component_id_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_component_name_from_component(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_component_type_from_component(item, indices='all'):

    raise NotImplementedError

## From molecule

@digest(form=form)
def get_molecule_id_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_molecule_name_from_molecule(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_molecule_type_from_molecule(item, indices='all'):

    raise NotImplementedError


## From chain

@digest(form=form)
def get_chain_id_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_chain_name_from_chain(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_chain_type_from_chain(item, indices='all'):

    raise NotImplementedError


## From entity

@digest(form=form)
def get_entity_id_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_entity_name_from_entity(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_entity_type_from_entity(item, indices='all'):

    raise NotImplementedError


## From system

@digest(form=form)
def get_n_atoms_from_system(item):

    output = item.file['topology']['atoms'].attrs['n_atoms']

    if output == 0:
        output = item.file['structures'].attrs['n_atoms']

    return output

@digest(form=form)
def get_n_groups_from_system(item):

    output = item.file['topology']['groups'].attrs['n_groups']

    return output

@digest(form=form)
def get_n_components_from_system(item):

    output = item.file['topology']['components'].attrs['n_components']

    return output

@digest(form=form)
def get_n_chains_from_system(item):

    output = item.file['topology']['chains'].attrs['n_chains']

    return output

@digest(form=form)
def get_n_molecules_from_system(item):

    output = item.file['topology']['molecules'].attrs['n_molecules']

    return output

@digest(form=form)
def get_n_entities_from_system(item):

    output = item.file['topology']['entities'].attrs['n_entities']

    return output

@digest(form=form)
def get_n_bonds_from_system(item):

    output = item.file['topology']['bonds'].attrs['n_bonds']

    return output

@digest(form=form)
def get_n_structures_from_system(item, structure_indices='all'):

    output = item.file['structures'].attrs['n_structures_written']

    return output

@digest(form=form)
def get_box_from_system(item, structure_indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_time_from_system(item, structure_indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_structure_id_from_system(item, structure_indices='all'):

    raise NotImplementedError


## From bond

@digest(form=form)
def get_bond_order_from_bond(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_bond_type_from_bond(item, indices='all'):

    raise NotImplementedError

@digest(form=form)
def get_bonded_atoms_from_bond(item, indices='all'):

    raise NotImplementedError


#######################################################################################
######### DO NOT TOUCH THE FOLLOWING LINES, JUST INCLUDE THEM AS THEY ARE #############
#######################################################################################

from os import path
this_folder = path.dirname(path.abspath(__file__))
common_get = path.join(this_folder, '../../_private/common_get.py')
execfile(common_get, globals(), locals())
del(path, this_folder, common_get)


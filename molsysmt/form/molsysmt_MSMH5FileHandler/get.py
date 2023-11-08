#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.execfile import execfile
from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw

form='molsysmt.MSMH5FileHandler'


## From atom

@digest(form=form)
def get_atom_id_from_atom(item, indices='all'):

    if is_all(indices):
        output = item.file['topology']['atoms']['id'][:].astype('int64')
    else:
        output = item.file['topology']['atoms']['id'][indices].astype('int64')

    return output

@digest(form=form)
def get_atom_name_from_atom(item, indices='all'):

    if is_all(indices):
        output = item.file['topology']['atoms']['name'][:].astype('str')
    else:
        output = item.file['topology']['atoms']['name'][indices].astype('str')

    return output

@digest(form=form)
def get_atom_type_from_atom(item, indices='all'):

    if is_all(indices):
        output = item.file['topology']['atoms']['type'][:].astype('str')
    else:
        output = item.file['topology']['atoms']['type'][indices].astype('str')

    return output

@digest(form=form)
def get_group_index_from_atom(item, indices='all'):

    if is_all(indices):
        output = item.file['topology']['atoms']['group_index'][:].astype('int')
    else:
        output = item.file['topology']['atoms']['group_index'][indices].astype('int')

    return output

@digest(form=form)
def get_component_index_from_atom(item, indices='all'):

    group_index = get_group_index_from_atom(item, indices)
    output = item.file['topology']['groups']['component_index'][group_index].astype('int')

    return output

@digest(form=form)
def get_chain_index_from_atom(item, indices='all'):

    if is_all(indices):
        output = item.file['topology']['atoms']['chain_index'][:].astype('int')
    else:
        output = item.file['topology']['atoms']['chain_index'][indices].astype('int')

    return output

@digest(form=form)
def get_molecule_index_from_atom(item, indices='all'):

    component_index = get_component_index_from_atom(item, indices)
    output = item.file['topology']['components']['molecule_index'][component_index].astype('int')

    return output

@digest(form=form)
def get_entity_index_from_atom(item, indices='all'):

    molecule_index = get_molecule_index_from_atom(item, indices)
    output = item.file['topology']['molecules']['entity_index'][molecule_index].astype('int')

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

    output = puw.quantity(output, item.file.attrs['length_unit'], standardized=True)

    return output

@digest(form=form)
def get_velocities_from_atom(item, indices='all', structure_indices='all'):

    if is_all(structure_indices):
        if is_all(indices):
            output = item.file['structures']['velocities'][:,:,:].astype('float')
        else:
            output = item.file['structures']['velocities'][:,indices,:].astype('float')
    else:
        output = []
        for ii in structure_indices:
            output.append(item.file['structures']['velocities'][ii,indices,:].astype('float'))
        output = np.array(output)

    output = puw.quantity(output, item.file.attrs['length_unit']+'/'+item.file.attrs['time_unit'], standardized=True)

    return output

## From group

@digest(form=form)
def get_group_id_from_group(item, indices='all'):

    if is_all(indices):
        output = item.file['topology']['groups']['id'][:].astype('int64')
    else:
        output = item.file['topology']['groups']['id'][indices].astype('int64')

    return output

@digest(form=form)
def get_group_name_from_group(item, indices='all'):

    if is_all(indices):
        output = item.file['topology']['groups']['name'][:].astype('str')
    else:
        output = item.file['topology']['groups']['name'][indices].astype('str')

    return output

@digest(form=form)
def get_group_type_from_group(item, indices='all'):

    if is_all(indices):
        output = item.file['topology']['groups']['type'][:].astype('str')
    else:
        output = item.file['topology']['groups']['type'][indices].astype('str')

    return output

## From component

@digest(form=form)
def get_component_id_from_component(item, indices='all'):

    if is_all(indices):
        output = item.file['topology']['components']['id'][:].astype('int64')
    else:
        output = item.file['topology']['components']['id'][indices].astype('int64')

    return output

@digest(form=form)
def get_component_name_from_component(item, indices='all'):

    if is_all(indices):
        output = item.file['topology']['components']['name'][:].astype('str')
    else:
        output = item.file['topology']['components']['name'][indices].astype('str')

    return output

@digest(form=form)
def get_component_type_from_component(item, indices='all'):

    if is_all(indices):
        output = item.file['topology']['components']['type'][:].astype('str')
    else:
        output = item.file['topology']['components']['type'][indices].astype('str')

    return output

## From molecule

@digest(form=form)
def get_molecule_id_from_molecule(item, indices='all'):

    if is_all(indices):
        output = item.file['topology']['molecules']['id'][:].astype('int')
    else:
        output = item.file['topology']['molecules']['id'][indices].astype('int')

    return output

@digest(form=form)
def get_molecule_name_from_molecule(item, indices='all'):

    if is_all(indices):
        output = item.file['topology']['molecules']['name'][:].astype('str')
    else:
        output = item.file['topology']['molecules']['name'][indices].astype('str')

    return output

@digest(form=form)
def get_molecule_type_from_molecule(item, indices='all'):

    if is_all(indices):
        output = item.file['topology']['molecules']['type'][:].astype('str')
    else:
        output = item.file['topology']['molecules']['type'][indices].astype('str')

    return output

## From chain

@digest(form=form)
def get_chain_id_from_chain(item, indices='all'):

    if is_all(indices):
        output = item.file['topology']['chains']['id'][:].astype('int')
    else:
        output = item.file['topology']['chains']['id'][indices].astype('int')

    return output

@digest(form=form)
def get_chain_name_from_chain(item, indices='all'):

    if is_all(indices):
        output = item.file['topology']['chains']['name'][:].astype('str')
    else:
        output = item.file['topology']['chains']['name'][indices].astype('str')

    return output

@digest(form=form)
def get_chain_type_from_chain(item, indices='all'):

    if is_all(indices):
        output = item.file['topology']['chains']['type'][:].astype('str')
    else:
        output = item.file['topology']['chains']['type'][indices].astype('str')

    return output

## From entity

@digest(form=form)
def get_entity_id_from_entity(item, indices='all'):

    if is_all(indices):
        output = item.file['topology']['entities']['id'][:].astype('int')
    else:
        output = item.file['topology']['entities']['id'][indices].astype('int')

    return output

@digest(form=form)
def get_entity_name_from_entity(item, indices='all'):

    if is_all(indices):
        output = item.file['topology']['entities']['name'][:].astype('str')
    else:
        output = item.file['topology']['entities']['name'][indices].astype('str')

    return output

@digest(form=form)
def get_entity_type_from_entity(item, indices='all'):

    if is_all(indices):
        output = item.file['topology']['entities']['type'][:].astype('str')
    else:
        output = item.file['topology']['entities']['type'][indices].astype('str')

    if not is_all(indices):
        output = output[indices]

    return output

## From system

@digest(form=form)
def get_n_atoms_from_system(item):

    output = item.file['topology'].attrs['n_atoms']

    if output==0:
        output = item.file['structures'].attrs['n_atoms']

    return output

@digest(form=form)
def get_n_groups_from_system(item):

    output = item.file['topology'].attrs['n_groups']

    return output

@digest(form=form)
def get_n_components_from_system(item):

    output = item.file['topology'].attrs['n_components']

    return output

@digest(form=form)
def get_n_chains_from_system(item):

    output = item.file['topology'].attrs['n_chains']

    return output

@digest(form=form)
def get_n_molecules_from_system(item):

    output = item.file['topology'].attrs['n_molecules']

    return output

@digest(form=form)
def get_n_entities_from_system(item):

    output = item.file['topology'].attrs['n_entities']

    return output

@digest(form=form)
def get_n_bonds_from_system(item):

    output = item.file['topology'].attrs['n_bonds']

    return output

@digest(form=form)
def get_n_structures_from_system(item, structure_indices='all'):

    output = item.file['structures'].attrs['n_structures_written']

    return output

@digest(form=form)
def get_box_from_system(item, structure_indices='all'):

    if item.file['structures'].attrs['constant_box']:
        if is_all(structure_indices):
            n_structures = item.file['structures'].attrs['n_structures_written']
            output = item.file['structures']['box'][0,:,:]
            output = np.repeat(output[np.newaxis,:,:], n_structures, axis=0)
        else:
            n_structures = len(structure_indices)
            output = item.file['structures']['box'][0,:,:]
            output = np.repeat(output[np.newaxis,:,:], n_structures, axis=0)
    else:
        if is_all(structure_indices):
            output = item.file['structures']['box'][:,:,:]
        else:
            output = item.file['structures']['box'][structure_indices,:,:]

    output = puw.quantity(output, item.file.attrs['length_unit'], standardized=True)

    return output

@digest(form=form)
def get_time_from_system(item, structure_indices='all'):

    if item.file['structures'].attrs['constant_time_step']:
        init_time = item.file['structures']['time'][0]
        time_step = item.file['structures'].attrs['time_step']
        if is_all(structure_indices):
            n_structures = item.file['structures'].attrs['n_structures_written']
            output = init_time + time_step*np_arange(n_structures)
        else:
            output = init_time + time_step*structure_indices
    else:
        if is_all(structure_indices):
            output = item.file['structures']['time'][:]
        else:
            output = item.file['structures']['time'][structure_indices]

    output = puw.quantity(output, item.file.attrs['time_unit'], standardized=True)

    return output

@digest(form=form)
def get_structure_id_from_system(item, structure_indices='all'):

    if item.file['structures'].attrs['constant_id_step']:
        init_id = item.file['structures']['id'][0]
        id_step = item.file['structures'].attrs['id_step']
        if is_all(structure_indices):
            n_structures = item.file['structures'].attrs['n_structures_written']
            output = init_id + id_step*np_arange(n_structures)
        else:
            output = init_id + id_step*structure_indices
    else:
        if is_all(structure_indices):
            output = item.file['structures']['id'][:]
        else:
            output = item.file['structures']['id'][structure_indices]

    return output

@digest(form=form)
def get_kinetic_energy_from_system(item, structure_indices='all'):

    if is_all(structure_indices):
        output = item.file['structures']['kinetic_energy'][:]
    else:
        output = item.file['structures']['kinetic_energy'][structure_indices]

    output = puw.quantity(output, item.file.attrs['energy_unit'], standardized=True)

    return output

@digest(form=form)
def get_potential_energy_from_system(item, structure_indices='all'):

    if is_all(structure_indices):
        output = item.file['structures']['potential_energy'][:]
    else:
        output = item.file['structures']['potential_energy'][structure_indices]

    output = puw.quantity(output, item.file.attrs['energy_unit'], standardized=True)

    return output

@digest(form=form)
def get_temperature_from_system(item, structure_indices='all'):

    constant_R = puw.get_constant('R')

    if item.file['structures'].attrs['temperature_from_kinetic_energy']:

        kinetic_energy = get_kinetic_energy_from_system(item, structure_indices=structure_indices)
        kinetic_energy = puw.convert(kinetic_energy, to_form='openmm.unit')
        output = 2 * kinetic_energy / (item.file['structures'].attrs['n_degrees_of_freedom'] * constant_R)
        output = puw.standardize(output)

    else:

        if is_all(structure_indices):
            output = item.file['structures']['temperature'][:]
        else:
            output = item.file['structures']['temperature'][structure_indices]

        output = puw.quantity(output, item.file.attrs['temperature_unit'], standardized=True)

    return output


## From bond

@digest(form=form)
def get_bond_order_from_bond(item, indices='all'):

    output = item.file['topology']['bonds']['order'][:].astype('str')

    if not is_all(indices):
        output = output[indices]

    return output

@digest(form=form)
def get_bond_type_from_bond(item, indices='all'):

    output = item.file['topology']['bonds']['type'][:].astype('str')

    if not is_all(indices):
        output = output[indices]

    return output

@digest(form=form)
def get_bonded_atoms_from_bond(item, indices='all'):

    tmp_out = None

    if is_all(indices):

        atom1_index = item.file['topology']['bonds']['atom1_index'][:].astype('int64')
        atom2_index = item.file['topology']['bonds']['atom2_index'][:].astype('int64')

    else:

        atom1_index = item.file['topology']['bonds']['atom1_index'][indices].astype('int64')
        atom2_index = item.file['topology']['bonds']['atomw_index'][indices].astype('int64')

    tmp_out = np.array([atom1_index, atom2_index])
    tmp_out = np.sort(tmp_out)

    return tmp_out


#######################################################################################
######### DO NOT TOUCH THE FOLLOWING LINES, JUST INCLUDE THEM AS THEY ARE #############
#######################################################################################

from os import path
this_folder = path.dirname(path.abspath(__file__))
common_get = path.join(this_folder, '../../_private/common_get.py')
execfile(common_get, globals(), locals())
del(path, this_folder, common_get)


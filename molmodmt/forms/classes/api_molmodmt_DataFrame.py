from os.path import basename as _basename
from molmodmt.utils.exceptions import *
from molmodmt.native import DataFrame

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
     DataFrame : form_name,
    'molmodmt.DataFrame': form_name
}

def to_molmodmt_Composition(item, atom_indices='all', frame_indices='all'):

    from molmodmt.native.io.composition.classes import from_molmodmt_DataFrame as molmodmt_DataFrame_to_molmodmt_Composition
    return molmodmt_DataFrame_to_molmodmt_Composition(item, atom_indices=atom_indices, frame_indices=frame_indices)

def extract_subsystem(item, atom_inices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        return item.iloc(atom_indices)

def duplicate(item):

    raise NotImplementedError

def select_with_MDTraj(item, selection):

    raise NotImplementedError

def select_with_MolModMT(item, selection):

    from molmodmt.native.selector import dataframe_select
    atom_indices = dataframe_select(item, selection)
    return atom_indices

###### Get

## Atom

def get_index_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_id_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_id_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_name_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_name_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_type_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_type_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['atom.index'].to_list()
    else:
        output_list = item.dataframe['atom.index'][indices].to_list()

    return output_list

def get_atom_id_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['atom.id'].to_list()
    else:
        output_list = item.dataframe['atom.id'][indices].to_list()

    return output_list

def get_atom_name_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['atom.name'].to_list()
    else:
        output_list = item.dataframe['atom.name'][indices].to_list()

    return output_list

def get_atom_type_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['atom.type'].to_list()
    else:
        output_list = item.dataframe['atom.type'][indices].to_list()

    return output_list

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['group.index'].to_list()
    else:
        output_list = item.dataframe['group.index'][indices].to_list()

    return output_list

def get_group_id_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['group.id'].to_list()
    else:
        output_list = item.dataframe['group.id'][indices].to_list()

    return output_list

def get_group_name_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['group.name'].to_list()
    else:
        output_list = item.dataframe['group.name'][indices].to_list()

    return output_list

def get_group_type_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['group.type'].to_list()
    else:
        output_list = item.dataframe['group.type'][indices].to_list()

    return output_list

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['component.index'].to_list()
    else:
        output_list = item.dataframe['component.index'][indices].to_list()

    return output_list

def get_component_id_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['component.id'].to_list()
    else:
        output_list = item.dataframe['component.id'][indices].to_list()

    return output_list

def get_component_name_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['component.name'].to_list()
    else:
        output_list = item.dataframe['component.name'][indices].to_list()

    return output_list

def get_component_type_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['component.type'].to_list()
    else:
        output_list = item.dataframe['component.type'][indices].to_list()

    return output_list

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['chain.index'].to_list()
    else:
        output_list = item.dataframe['chain.index'][indices].to_list()

    return output_list

def get_chain_id_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['chain.id'].to_list()
    else:
        output_list = item.dataframe['chain.id'][indices].to_list()

    return output_list

def get_chain_name_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['chain.name'].to_list()
    else:
        output_list = item.dataframe['chain.name'][indices].to_list()

    return output_list

def get_chain_type_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['chain.type'].to_list()
    else:
        output_list = item.dataframe['chain.type'][indices].to_list()

    return output_list

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['molecule.index'].to_list()
    else:
        output_list = item.dataframe['molecule.index'][indices].to_list()

    return output_list

def get_molecule_id_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['molecule.id'].to_list()
    else:
        output_list = item.dataframe['molecule.id'][indices].to_list()

    return output_list

def get_molecule_name_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['molecule.name'].to_list()
    else:
        output_list = item.dataframe['molecule.name'][indices].to_list()

    return output_list

def get_molecule_type_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['molecule.type'].to_list()
    else:
        output_list = item.dataframe['molecule.type'][indices].to_list()

    return output_list

def get_entity_index_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['entity.index'].to_list()
    else:
        output_list = item.dataframe['entity.index'][indices].to_list()

    return output_list

def get_entity_id_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['entity.id'].to_list()
    else:
        output_list = item.dataframe['entity.id'][indices].to_list()

    return output_list

def get_entity_name_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['entity.name'].to_list()
    else:
        output_list = item.dataframe['entity.name'][indices].to_list()

    return output_list

def get_entity_type_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['entity.type'].to_list()
    else:
        output_list = item.dataframe['entity.type'][indices].to_list()

    return output_list

def get_bioassembly_index_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['bioassembly.index'].to_list()
    else:
        output_list = item.dataframe['bioassembly.index'][indices].to_list()

    return output_list

def get_bioassembly_id_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['bioassembly.id'].to_list()
    else:
        output_list = item.dataframe['bioassembly.id'][indices].to_list()

    return output_list

def get_bioassembly_name_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['bioassembly.name'].to_list()
    else:
        output_list = item.dataframe['bioassembly.name'][indices].to_list()

    return output_list

def get_bioassembly_type_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['bioassembly.type'].to_list()
    else:
        output_list = item.dataframe['bioassembly.type'][indices].to_list()

    return output_list

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['bioassembly.type'].to_list()
    else:
        output_list = item.dataframe['bioassembly.type'][indices].to_list()

    return output_list

def get_n_aminoacids_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_nucleotides_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_waters_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_ions_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError


## group

## chain

## system

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_aminoacids_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_nucleotides_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_ions_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_waters_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_cosolutes_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_small_molecules_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_peptides_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_proteins_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_dnas_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_rnas_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_form_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_masses_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_bonds_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_graph_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecules_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError


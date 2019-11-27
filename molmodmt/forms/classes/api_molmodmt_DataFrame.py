from os.path import basename as _basename
from molmodmt.utils.exceptions import *
from molmodmt.native import DataFrame

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
     DataFrame : form_name,
    'molmodmt.DataFrame': form_name
}

def to_molmodmt_Composition(item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def extract_subsystem(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        return item.iloc(atom_indices)

def duplicate(item):

    raise NotImplementedError

def select_with_MDTraj(item, selection):

    raise NotImplementedError

def select_with_Pandas(item, selection):

    from molmodmt.native.selector import dataframe_select
    atom_indices = dataframe_select(item, selection)
    return atom_indices

###### Get

def get_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_id_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_name_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_element_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_name_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_id_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_name_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_id_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_aminoacids_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_nucleotides_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_waters_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_ions_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_bonded_atoms_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecules_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_type_from_atom(item, indices='all', frame_indices='all'):

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


#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt.tools.file_pdb.is_file_pdb import _checking_form

## From atom

def get_atom_id_from_atom(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_atom_id_from_atom as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_atom_name_from_atom(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_atom_name_from_atom as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_atom_type_from_atom(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_atom_type_from_atom as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_group_index_from_atom (item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_group_index_from_atom as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_component_index_from_atom (item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_component_index_from_atom as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_chain_index_from_atom (item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_chain_index_from_atom as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_molecule_index_from_atom (item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_molecule_index_from_atom as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_entity_index_from_atom (item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_entity_index_from_atom as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_inner_bonded_atoms_from_atom (item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_inner_bonded_atoms_from_atom as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_n_inner_bonds_from_atom (item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_n_inner_bonds_from_atom as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_coordinates_from_atom(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_coordinates_from_atom as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_frame_from_atom(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_frame_from_atom as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

## group

def get_group_id_from_group(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_group_id_from_group as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_group_name_from_group(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_group_name_from_group as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_group_type_from_group(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_group_type_from_group as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

## component

def get_component_id_from_component (item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_component_id_from_component as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_component_name_from_component (item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_component_name_from_component as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_component_type_from_component (item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_component_type_from_component as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

## molecule

def get_molecule_id_from_molecule (item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_molecule_id_from_molecule as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_molecule_name_from_molecule (item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_molecule_name_from_molecule as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_molecule_type_from_molecule (item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_molecule_type_from_molecule as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

## chain

def get_chain_id_from_chain (item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_chain_id_from_chain as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_chain_name_from_chain (item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_chain_name_from_chain as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_chain_type_from_chain (item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_chain_type_from_chain as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

## entity

def get_entity_id_from_entity (item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_entity_id_from_entity as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_entity_name_from_entity (item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_entity_name_from_entity as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_entity_type_from_entity (item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_entity_type_from_entity as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

## system

def get_n_atoms_from_system(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_n_atoms_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_n_groups_from_system(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_n_groups_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_n_components_from_system(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_n_components_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_n_chains_from_system(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_n_chains_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_n_molecules_from_system(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_n_molecules_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_n_entities_from_system(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_n_entities_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_n_bonds_from_system(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_n_bonds_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_coordinates_from_system(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_coordinates_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_box_from_system(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_box_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_box_shape_from_system(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_box_shape_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_box_lengths_from_system(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_box_lengths_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_box_angles_from_system(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_box_angles_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_box_volume_from_system(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_box_volume_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_time_from_system(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_time_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_step_from_system(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_step_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_n_structures_from_system(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_n_structures_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_bonded_atoms_from_system(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_bonded_atoms_from_system as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

## bond

def get_bond_order_from_bond(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_bond_order_from_bond as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_bond_type_from_bond(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_bond_type_from_bond as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

def get_atom_index_from_bond(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.file_pdb import to_openmm_PDBFile
    from molsysmt.tools.openmm_PDBFile import get_atom_index_from_bond as aux_get

    tmp_item = to_openmm_PDBFile(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, check_form=False)

    return output

#######################################################################################
######### DO NOT TOUCH THE FOLLOWING LINES, JUST INCLUDE THEM AS THEY ARE #############
#######################################################################################

## From atom

def get_atom_index_from_atom(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    if indices is 'all':
        n_aux = get_n_atoms_from_system(item, check_form=False)
        output = np.arange(n_aux, dtype=int)
    else:
        output = np.array(indices, dtype=int)

    return output

def get_group_id_from_atom(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_group_index_from_atom(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_group_id_from_group(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_group_name_from_atom(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_group_index_from_atom(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_group_name_from_group(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_group_type_from_atom(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_group_index_from_atom(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_group_type_from_group(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_component_id_from_atom(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_component_index_from_atom(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_component_id_from_component(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_component_name_from_atom(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_component_index_from_atom(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_component_name_from_component(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_component_type_from_atom(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_component_index_from_atom(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_component_type_from_component(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_chain_id_from_atom(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_chain_index_from_atom(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_chain_name_from_atom(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_chain_index_from_atom(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_chain_type_from_atom(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_chain_index_from_atom(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_molecule_id_from_atom(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_molecule_index_from_atom(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_molecule_name_from_atom(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_molecule_index_from_atom(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_molecule_type_from_atom(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_molecule_index_from_atom(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_entity_id_from_atom(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_entity_index_from_atom(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_entity_name_from_atom(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_entity_index_from_atom(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_entity_type_from_atom(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_entity_index_from_atom(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    output = output.astype(object)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_n_atoms_from_atom(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    if indices is 'all':
        output = get_n_atoms_from_system(item, check_form=False)
    else:
        output = indices.shape[0]

    return output

def get_n_groups_from_atom(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    if indices is 'all':
        output = get_n_groups_from_system(item, check_form=False)
    else:
        output = get_group_index_from_atom(item, indices=indices, check_form=True)
        output = np.unique(output).shape[0]

    return output

def get_n_components_from_atom(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    if indices is 'all':
        output = get_n_components_from_system(item, check_form=False)
    else:
        output = get_component_index_from_atom(item, indices=indices, check_form=True)
        output = np.unique(output).shape[0]

    return output

def get_n_molecules_from_atom(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    if indices is 'all':
        output = get_n_molecules_from_system(item, check_form=False)
    else:
        output = get_molecule_index_from_atom(item, indices=indices, check_form=True)
        output = np.unique(output).shape[0]

    return output

def get_n_chains_from_atom(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    if indices is 'all':
        output = get_n_chains_from_system(item, check_form=False)
    else:
        output = get_chain_index_from_atom(item, indices=indices, check_form=True)
        output = np.unique(output).shape[0]

    return output

def get_n_entities_from_atom(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    if indices is 'all':
        output = get_n_entities_from_system(item, check_form=False)
    else:
        output = get_entity_index_from_atom(item, indices=indices, check_form=True)
        output = np.unique(output).shape[0]

    return output

def get_bonded_atoms_from_atom(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    output = None

    from networkx import Graph
    import numpy as np

    G = Graph()
    edges = get_atom_index_from_bond(item, check_form=False)
    G.add_edges_from(edges)

    if indices is 'all':

        indices = get_atom_index_from_atom(item, check_form=False)

    output = []

    for ii in indices:
        if ii in G:
            output.append(np.array([n for n in G[ii]]))
        else:
            output.append(np.array([]))

    output = np.array(output, dtype=object)

    del(Graph, G, edges)

    return output

def get_bond_index_from_atom(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    output = None

    from networkx import Graph
    import numpy as np

    G = Graph()
    edges = get_atom_index_from_bond(item, check_form=False)
    n_bonds = edges.shape[0]
    edge_indices = np.array([{'index':ii} for ii in range(n_bonds)]).reshape([n_bonds,1])
    G.add_edges_from(np.hstack([edges, edge_indices]))

    if indices is 'all':

        indices = get_atom_index_from_atom(item, check_form=False)

    output = []

    for ii in indices:
        if ii in G:
            output.append(np.array([n['index'] for n in G[ii].values()]))
        else:
            output.append(np.array([]))

    output = np.array(output, dtype=object)

    del(Graph, G, edges, edge_indices)

    return output

def get_n_bonds_from_atom(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    output = None

    from networkx import Graph
    import numpy as np

    G = Graph()
    edges = get_atom_index_from_bond(item, check_form=False)
    G.add_edges_from(edges)

    if indices is 'all':

        indices = get_atom_index_from_atom(item, check_form=False)

    output = []

    for ii in indices:
        if ii in G:
            output.append(len(G[ii]))
        else:
            output.append(0)

    output = np.array(output)

    del(Graph, G, edges)

    return output

def get_inner_bond_index_from_atom(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    raise NotImplementedError

    #output = None

    #if indices is 'all':
    #    output = get(item, target='bond', index=True)
    #else:
    #    edges = get(item, target='bond', atom_index=True)
    #    aux_list = list(indices)
    #    output = item.bonds_dataframe.query('atom1_index==@aux_list and atom2_index==@aux_list').index.to_numpy(dtype=int, copy=True)

    #return output

#def get_coordinates_from_atom(item, indices='all', structure_indices='all', check_form=True):
#
#    raise NotImplementedError

#def get_frame_from_atom(item, indices='all', structure_indices='all', check_form=True):
#
#    from molsysmt.basic import get
#
#    tmp_step, tmp_time, tmp_box = get(item, target='system', structure_indices=structure_indices, step=True, time=True, box=True)
#    tmp_coordinates = get(item, target='atom', indices=indices, structure_indices=structure_indices, coordinates=True)
#
#    return tmp_step, tmp_time, tmp_coordinates, tmp_box

#def get_n_structures_from_atom(item, indices='all', structure_indices='all', check_form=True):
#
#    from molsysmt.basic import get
#
#    return get(item, target='system', indices='all', structure_indices=structure_indices, n_structures=True)

## From group

def get_atom_index_from_group(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_atom_indices = get_atom_index_from_group(item, indices=indices, check_form=False)
    aux_indices = get_group_index_from_atom(item, check_form=False)
    aux_vals = get_atom_index_from_atom(item, check_form=False)

    output=[]

    for ii in aux_atom_indices:
        mask = (aux_indices==ii)
        output.append(np.unique(aux_vals[mask]))

    del(aux_atom_indices, aux_indices, aux_vals)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

def get_atom_id_from_group(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_atom_index_from_group(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_atom_name_from_group(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_atom_index_from_group(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_atom_type_from_group(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_atom_index_from_group(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_index_from_group(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    if indices is 'all':
        n_aux = get_n_groups_from_system(item, check_form=False)
        output = np.arange(n_aux, dtype=int)
    else:
        output = np.array(indices, dtype=int)

    return output

def get_component_index_from_group(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    atom_index_from_target = get_atom_index_from_group(item, indices=indices, check_form=False)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_component_index_from_atom(item, indices=first_atom_index_from_target, check_form=False)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

def get_component_id_from_group(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_component_index_from_group(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_component_id_from_component(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_component_name_from_group(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_component_index_from_group(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_component_name_from_component(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_component_type_from_group(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_component_index_from_group(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_component_type_from_component(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_chain_index_from_group(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    atom_index_from_target = get_atom_index_from_group(item, indices=indices, check_form=False)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_chain_index_from_atom(item, indices=first_atom_index_from_target, check_form=False)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

def get_chain_id_from_group(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_chain_index_from_group(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_chain_name_from_group(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_chain_index_from_group(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_chain_type_from_group(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_chain_index_from_group(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_molecule_index_from_group(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    atom_index_from_target = get_atom_index_from_group(item, indices=indices, check_form=False)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_molecule_index_from_atom(item, indices=first_atom_index_from_target, check_form=False)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

def get_molecule_id_from_group(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_molecule_index_from_group(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_molecule_name_from_group(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_molecule_index_from_group(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_molecule_type_from_group(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_molecule_index_from_group(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_entity_index_from_group(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    atom_index_from_target = get_atom_index_from_group(item, indices=indices, check_form=False)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_entity_index_from_atom(item, indices=first_atom_index_from_target, check_form=False)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

def get_entity_id_from_group(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_entity_index_from_group(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_entity_name_from_group(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_entity_index_from_group(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_entity_type_from_group(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_entity_index_from_group(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)
    return output

def get_n_atoms_from_group(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    output = get_atom_index_from_group(item, indices=indices, check_form=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

def get_n_groups_from_group(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    if indices is 'all':
        output = get_n_groups_from_system(item, check_form=False)
    else:
        output = indices.shape[0]

    return output

def get_n_components_from_group(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    if indices is 'all':
        return get_n_components_from_system(item, check_form=False)
    else:
        output = get_component_index_from_group(item, indices=indices, check_form=False)
        output = np.unique(output).shape[0]

    return output

def get_n_molecules_from_group(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.basic import get

    if indices is 'all':
        return get_n_molecules_from_system(item, check_form=False)
    else:
        output = get_molecule_index_from_group(item, indices=indices, check_form=False)
        output = np.unique(output).shape[0]

    return output

def get_n_chains_from_group(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.basic import get

    if indices is 'all':
        return get_n_chains_from_system(item, check_form=False)
    else:
        output = get_chain_index_from_group(item, indices=indices, check_form=False)
        output = np.unique(output).shape[0]

    return output

def get_n_entities_from_group(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.basic import get

    if indices is 'all':
        return get_n_entities_from_system(item, check_form=False)
    else:
        output = get_entity_index_from_group(item, indices=indices, check_form=False)
        output = np.unique(output).shape[0]

    return output


## From component

def get_atom_index_from_component(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_atom_indices = get_atom_index_from_component(item, indices=indices, check_form=False)
    aux_indices = get_component_index_from_atom(item, check_form=False)
    aux_vals = get_atom_index_from_atom(item, check_form=False)

    output=[]

    for ii in aux_atom_indices:
        mask = (aux_indices==ii)
        output.append(np.unique(aux_vals[mask]))

    del(aux_atom_indices, aux_indices, aux_vals)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

def get_atom_id_from_component(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_atom_index_from_component(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_atom_name_from_component(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_atom_index_from_component(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_atom_type_from_component(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_atom_index_from_component(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_index_from_component(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_atom_indices = get_atom_index_from_component(item, indices=indices, check_form=False)
    aux_indices = get_component_index_from_atom(item, check_form=False)
    aux_vals = get_group_index_from_atom(item, check_form=False)

    output=[]

    for ii in aux_atom_indices:
        mask = (aux_indices==ii)
        output.append(np.unique(aux_vals[mask]))

    del(aux_atom_indices, aux_indices, aux_vals)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

def get_group_id_from_component(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_group_index_from_component(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_id_from_group(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_name_from_component(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_group_index_from_component(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_name_from_group(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_type_from_component(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_group_index_from_component(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_type_from_group(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_component_index_from_component(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    if indices is 'all':
        n_aux = get_n_components_from_system(item, check_form=False)
        output = np.arange(n_aux, dtype=int)
    else:
        output = np.array(indices, dtype=int)

    return output

def get_chain_index_from_component(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    atom_index_from_target = get_atom_index_from_component(item, indices=indices, check_form=False)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_chain_index_from_atom(item, indices=first_atom_index_from_target, check_form=False)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

def get_chain_id_from_component(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_chain_index_from_component(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_chain_name_from_component(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_chain_index_from_component(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_chain_type_from_component(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_chain_index_from_component(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_molecule_index_from_component(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    atom_index_from_target = get_atom_index_from_component(item, indices=indices, check_form=False)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_molecule_index_from_atom(item, indices=first_atom_index_from_target, check_form=False)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

def get_molecule_id_from_component(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_molecule_index_from_component(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_molecule_name_from_component(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_molecule_index_from_component(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_molecule_type_from_component(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_molecule_index_from_component(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_entity_index_from_component(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    atom_index_from_target = get_atom_index_from_component(item, indices=indices, check_form=False)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_entity_index_from_atom(item, indices=first_atom_index_from_target, check_form=False)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

def get_entity_id_from_component(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_entity_index_from_component(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_entity_name_from_component(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_entity_index_from_component(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_entity_type_from_component(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_entity_index_from_component(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_n_atoms_from_component(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    output = get_atom_index_from_component(item, indices=indices, check_form=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

def get_n_groups_from_component(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    output = get_group_index_from_component(item, indices=indices, check_form=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

def get_n_components_from_component(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    if indices is 'all':
        output = get_n_components_from_system(item, check_form=False)
    else:
        output = indices.shape[0]

    return output

def get_n_molecules_from_component(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    if indices is 'all':
        output = get_n_molecules_from_system(item, check_form=False)
    else:
        output = get_molecule_index_from_component(item, indices=indices, check_form=True)
        output = np.unique(output).shape[0]

    return output

def get_n_chains_from_component(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    if indices is 'all':
        output = get_n_chains_from_system(item, check_form=False)
    else:
        output = get_chain_index_from_component(item, indices=indices, check_form=True)
        output = np.unique(output).shape[0]

    return output

def get_n_entities_from_component(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    if indices is 'all':
        output = get_n_entities_from_system(item, check_form=False)
    else:
        output = get_entity_index_from_component(item, indices=indices, check_form=True)
        output = np.unique(output).shape[0]

    return output

## molecule

def get_atom_index_from_molecule(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_atom_indices = get_atom_index_from_molecule(item, indices=indices, check_form=False)
    aux_indices = get_molecule_index_from_atom(item, check_form=False)
    aux_vals = get_atom_index_from_atom(item, check_form=False)

    output=[]

    for ii in aux_atom_indices:
        mask = (aux_indices==ii)
        output.append(np.unique(aux_vals[mask]))

    del(aux_atom_indices, aux_indices, aux_vals)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

def get_atom_id_from_molecule(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_atom_index_from_molecule(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_atom_name_from_molecule(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_atom_index_from_molecule(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_atom_type_from_molecule(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_atom_index_from_molecule(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_index_from_molecule(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_atom_indices = get_atom_index_from_molecule(item, indices=indices, check_form=False)
    aux_indices = get_molecule_index_from_atom(item, check_form=False)
    aux_vals = get_group_index_from_atom(item, check_form=False)

    output=[]

    for ii in aux_atom_indices:
        mask = (aux_indices==ii)
        output.append(np.unique(aux_vals[mask]))

    del(aux_atom_indices, aux_indices, aux_vals)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

def get_group_id_from_molecule(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_group_index_from_molecule(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_id_from_group(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_name_from_molecule(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_group_index_from_molecule(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_name_from_group(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_type_from_molecule(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_group_index_from_molecule(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_type_from_group(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_component_index_from_molecule(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_atom_indices = get_atom_index_from_molecule(item, indices=indices, check_form=False)
    aux_indices = get_molecule_index_from_atom(item, check_form=False)
    aux_vals = get_component_index_from_atom(item, check_form=False)

    output=[]

    for ii in aux_atom_indices:
        mask = (aux_indices==ii)
        output.append(np.unique(aux_vals[mask]))

    del(aux_atom_indices, aux_indices, aux_vals)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

def get_component_id_from_molecule(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_component_index_from_molecule(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_id_from_component(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_component_name_from_molecule(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_component_index_from_molecule(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_name_from_component(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_component_type_from_molecule(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_component_index_from_molecule(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_type_from_component(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_chain_index_from_molecule(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_atom_indices = get_atom_index_from_molecule(item, indices=indices, check_form=False)
    aux_indices = get_molecule_index_from_atom(item, check_form=False)
    aux_vals = get_chain_index_from_atom(item, check_form=False)

    output=[]

    for ii in aux_atom_indices:
        mask = (aux_indices==ii)
        output.append(np.unique(aux_vals[mask]))

    del(aux_atom_indices, aux_indices, aux_vals)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

def get_chain_id_from_molecule(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_chain_index_from_molecule(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_chain_name_from_molecule(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_chain_index_from_molecule(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_chain_type_from_molecule(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_chain_index_from_molecule(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_molecule_index_from_molecule(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    if indices is 'all':
        n_aux = get_n_molecules_from_system(item, check_form=False)
        output = np.arange(n_aux, dtype=int)
    else:
        output = np.array(indices, dtype=int)

    return output

def get_entity_index_from_molecule(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    atom_index_from_target = get_atom_index_from_molecule(item, indices=indices, check_form=False)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_entity_index_from_atom(item, indices=first_atom_index_from_target, check_form=False)

    del(atom_index_from_target, first_atom_index_from_target)

    return output

def get_entity_id_from_molecule(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_entity_index_from_molecule(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_entity_name_from_molecule(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_entity_index_from_molecule(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_entity_type_from_molecule(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_entity_index_from_molecule(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_n_atoms_from_molecule(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    output = get_atom_index_from_molecule(item, indices=indices, check_form=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

def get_n_groups_from_molecule(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    output = get_group_index_from_molecule(item, indices=indices, check_form=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

def get_n_components_from_molecule(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    output = get_component_index_from_molecule(item, indices=indices, check_form=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

def get_n_molecules_from_molecule(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    if indices is 'all':
        output = get_n_molecules_from_system(item, check_form=False)
    else:
        output = indices.shape[0]

    return output

def get_n_chains_from_molecule(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    output = get_chain_index_from_molecule(item, indices=indices, check_form=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

def get_n_entities_from_molecule(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    if indices is 'all':
        output = get_n_entities_from_system(item, check_form=False)
    else:
        output = get_entity_index_from_molecule(item, indices=indices, check_form=True)
        output = np.unique(output).shape[0]

    return output

## chain

def get_atom_index_from_chain(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_atom_indices = get_atom_index_from_chain(item, indices=indices, check_form=False)
    aux_indices = get_chain_index_from_atom(item, check_form=False)
    aux_vals = get_atom_index_from_atom(item, check_form=False)

    output=[]

    for ii in aux_atom_indices:
        mask = (aux_indices==ii)
        output.append(np.unique(aux_vals[mask]))

    del(aux_atom_indices, aux_indices, aux_vals)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

def get_atom_id_from_chain(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_atom_index_from_chain(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_atom_name_from_chain(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_atom_index_from_chain(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_atom_type_from_chain(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_atom_index_from_chain(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_index_from_chain(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_atom_indices = get_atom_index_from_chain(item, indices=indices, check_form=False)
    aux_indices = get_chain_index_from_atom(item, check_form=False)
    aux_vals = get_group_index_from_atom(item, check_form=False)

    output=[]

    for ii in aux_atom_indices:
        mask = (aux_indices==ii)
        output.append(np.unique(aux_vals[mask]))

    del(aux_atom_indices, aux_indices, aux_vals)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

def get_group_id_from_chain(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_group_index_from_chain(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_id_from_group(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_name_from_chain(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_group_index_from_chain(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_name_from_group(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_type_from_chain(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_group_index_from_chain(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_type_from_group(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_component_index_from_chain(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_atom_indices = get_atom_index_from_chain(item, indices=indices, check_form=False)
    aux_indices = get_chain_index_from_atom(item, check_form=False)
    aux_vals = get_component_index_from_atom(item, check_form=False)

    output=[]

    for ii in aux_atom_indices:
        mask = (aux_indices==ii)
        output.append(np.unique(aux_vals[mask]))

    del(aux_atom_indices, aux_indices, aux_vals)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

def get_component_id_from_chain(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_component_index_from_chain(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_id_from_component(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_component_name_from_chain(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_component_index_from_chain(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_name_from_component(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_component_type_from_chain(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_component_index_from_chain(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_type_from_component(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_chain_index_from_chain(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    if indices is 'all':
        n_aux = get_n_chains_from_system(item, check_form=False)
        output = np.arange(n_aux, dtype=int)
    else:
        output = np.array(indices, dtype=int)

    return output

def get_molecule_index_from_chain(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_atom_indices = get_atom_index_from_chain(item, indices=indices, check_form=False)
    aux_indices = get_chain_index_from_atom(item, check_form=False)
    aux_vals = get_molecule_index_from_atom(item, check_form=False)

    output=[]

    for ii in aux_atom_indices:
        mask = (aux_indices==ii)
        output.append(np.unique(aux_vals[mask]))

    del(aux_atom_indices, aux_indices, aux_vals)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

def get_molecule_id_from_chain(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_molecule_index_from_chain(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_molecule_name_from_chain(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_molecule_index_from_chain(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_molecule_type_from_chain(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_molecule_index_from_chain(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_entity_index_from_chain(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_atom_indices = get_atom_index_from_chain(item, indices=indices, check_form=False)
    aux_indices = get_chain_index_from_atom(item, check_form=False)
    aux_vals = get_entity_index_from_atom(item, check_form=False)

    output=[]

    for ii in aux_atom_indices:
        mask = (aux_indices==ii)
        output.append(np.unique(aux_vals[mask]))

    del(aux_atom_indices, aux_indices, aux_vals)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

def get_entity_id_from_chain(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_entity_index_from_chain(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_entity_name_from_chain(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_entity_index_from_chain(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_entity_type_from_chain(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_entity_index_from_chain(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_n_atoms_from_chain(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    output = get_atom_index_from_chain(item, indices=indices, check_form=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

def get_n_groups_from_chain(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    output = get_group_index_from_chain(item, indices=indices, check_form=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

def get_n_components_from_chain(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    output = get_component_index_from_chain(item, indices=indices, check_form=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

def get_n_molecules_from_chain(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    output = get_molecule_index_from_chain(item, indices=indices, check_form=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

def get_n_chains_from_chain(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    if indices is 'all':
        output = get_n_chains_from_system(item, check_form=False)
    else:
        output = indices.shape[0]

    return output

def get_n_entities_from_chain(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    if indices is 'all':
        output = get_n_entities_from_system(item, check_form=False)
    else:
        output = get_entity_index_from_chain(item, indices=indices, check_form=True)
        output = np.unique(output).shape[0]

    return output

## From entity

def get_atom_index_from_entity(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_atom_indices = get_atom_index_from_entity(item, indices=indices, check_form=False)
    aux_indices = get_entity_index_from_atom(item, check_form=False)
    aux_vals = get_atom_index_from_atom(item, check_form=False)

    output=[]

    for ii in aux_atom_indices:
        mask = (aux_indices==ii)
        output.append(np.unique(aux_vals[mask]))

    del(aux_atom_indices, aux_indices, aux_vals)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

def get_atom_id_from_entity(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_atom_index_from_entity(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_atom_name_from_entity(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_atom_index_from_entity(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_atom_type_from_entity(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_atom_index_from_entity(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_index_from_entity(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_atom_indices = get_atom_index_from_entity(item, indices=indices, check_form=False)
    aux_indices = get_entity_index_from_atom(item, check_form=False)
    aux_vals = get_group_index_from_atom(item, check_form=False)

    output=[]

    for ii in aux_atom_indices:
        mask = (aux_indices==ii)
        output.append(np.unique(aux_vals[mask]))

    del(aux_atom_indices, aux_indices, aux_vals)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

def get_group_id_from_entity(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_group_index_from_entity(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_id_from_group(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_name_from_entity(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_group_index_from_entity(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_name_from_group(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_group_type_from_entity(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_group_index_from_entity(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_group_type_from_group(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_component_index_from_entity(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_atom_indices = get_atom_index_from_entity(item, indices=indices, check_form=False)
    aux_indices = get_entity_index_from_atom(item, check_form=False)
    aux_vals = get_component_index_from_atom(item, check_form=False)

    output=[]

    for ii in aux_atom_indices:
        mask = (aux_indices==ii)
        output.append(np.unique(aux_vals[mask]))

    del(aux_atom_indices, aux_indices, aux_vals)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

def get_component_id_from_entity(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_component_index_from_entity(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_id_from_component(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_component_name_from_entity(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_component_index_from_entity(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_name_from_component(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_component_type_from_entity(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_component_index_from_entity(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_component_type_from_component(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_chain_index_from_entity(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_atom_indices = get_atom_index_from_entity(item, indices=indices, check_form=False)
    aux_indices = get_entity_index_from_atom(item, check_form=False)
    aux_vals = get_chain_index_from_atom(item, check_form=False)

    output=[]

    for ii in aux_atom_indices:
        mask = (aux_indices==ii)
        output.append(np.unique(aux_vals[mask]))

    del(aux_atom_indices, aux_indices, aux_vals)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

def get_chain_id_from_entity(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_chain_index_from_entity(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_chain_name_from_entity(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_chain_index_from_entity(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_chain_name_from_chain(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_chain_type_from_entity(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_chain_index_from_entity(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_molecule_index_from_entity(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_atom_indices = get_atom_index_from_entity(item, indices=indices, check_form=False)
    aux_indices = get_entity_index_from_atom(item, check_form=False)
    aux_vals = get_molecule_index_from_atom(item, check_form=False)

    output=[]

    for ii in aux_atom_indices:
        mask = (aux_indices==ii)
        output.append(np.unique(aux_vals[mask]))

    del(aux_atom_indices, aux_indices, aux_vals)

    if len(output)==1:
        output = np.array(output)
    else:
        output = np.array(output, dtype=object)

    return output

def get_molecule_id_from_entity(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_molecule_index_from_entity(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_molecule_name_from_entity(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_molecule_index_from_entity(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_molecule_type_from_entity(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_molecule_index_from_entity(item, indices=indices, check_form=False)

    if len(aux_indices)>0:
        aux_unique_indices = np.unique(np.concatenate(aux_indices))
        aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, check_form=False)
        aux_dict = dict(zip(aux_unique_indices, aux_vals))
        vv = np.vectorize(aux_dict.__getitem__)
        output = np.array([vv(ii) for ii in aux_indices], dtype=object)
        del(aux_unique_indices, aux_vals, aux_dict)
    else:
        output = np.array([], dtype=object)

    del(aux_indices)

    return output

def get_entity_index_from_entity(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    if indices is 'all':
        n_aux = get_n_entities_from_system(item, check_form=False)
        output = np.arange(n_aux, dtype=int)
    else:
        output = np.array(indices, dtype=int)

    return output

def get_n_atoms_from_entity(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    output = get_atom_index_from_entity(item, indices=indices, check_form=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

def get_n_groups_from_entity(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    output = get_group_index_from_entity(item, indices=indices, check_form=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

def get_n_components_from_entity(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    output = get_component_index_from_entity(item, indices=indices, check_form=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

def get_n_molecules_from_entity(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    output = get_molecule_index_from_entity(item, indices=indices, check_form=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

def get_n_chains_from_entity(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    output = get_chain_index_from_entity(item, indices=indices, check_form=False)
    output = [ii.shape[0] for ii in output]
    output = np.array(output)
    return output

def get_n_entities_from_entity(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    if indices is 'all':
        output = get_n_entities_from_system(item, check_form=False)
    else:
        output = indices.shape[0]

    return output

## system

#def get_bonded_atoms_from_system(item, indices='all', structure_indices='all', check_form=True):
#
#    raise NotImplementedError

#def get_n_atoms_from_system(item, indices='all', structure_indices='all', check_form=True):
#
#    raise NotImplementedError

#def get_n_groups_from_system(item, indices='all', structure_indices='all', check_form=True):
#
#    raise NotImplementedError

#def get_n_components_from_system(item, indices='all', structure_indices='all', check_form=True):
#
#    raise NotImplementedError

#def get_n_chains_from_system(item, indices='all', structure_indices='all', check_form=True):
#
#    raise NotImplementedError

#def get_n_molecules_from_system(item, indices='all', structure_indices='all', check_form=True):
#
#    raise NotImplementedError

#def get_n_entities_from_system(item, indices='all', structure_indices='all', check_form=True):
#
#    raise NotImplementedError

#def get_n_bonds_from_system(item, indices='all', structure_indices='all', check_form=True):
#
#    raise NotImplementedError

def get_n_aminoacids_from_system(item, indices='all', structure_indices='all', check_form=True):

    from molsysmt.basic import get

    group_types = get(item, target='group', indices='all', group_type=True)
    return (group_types=='aminoacid').sum()

def get_n_nucleotides_from_system(item, indices='all', structure_indices='all', check_form=True):

    from molsysmt.basic import get

    group_types = get(item, target='group', indices='all', group_type=True)
    return (group_types=='nucleotide').sum()

def get_n_ions_from_system(item, indices='all', structure_indices='all', check_form=True):

    from molsysmt.basic import get

    molecule_types = get(item, target='molecule', indices='all', molecule_type=True)
    return (molecule_types=='ion').sum()

def get_n_waters_from_system(item, indices='all', structure_indices='all', check_form=True):

    from molsysmt.basic import get

    molecule_types = get(item, target='molecule', indices='all', molecule_type=True, check_form=True)
    return (molecule_types=='water').sum()

def get_n_cosolutes_from_system(item, indices='all', structure_indices='all'):

    from molsysmt.basic import get

    molecule_types = get(item, target='molecule', indices='all', molecule_type=True, check_form=True)
    return (molecule_types=='cosolute').sum()

def get_n_small_molecules_from_system(item, indices='all', structure_indices='all', check_form=True):

    from molsysmt.basic import get

    molecule_types = get(item, target='molecule', indices='all', molecule_type=True)
    return (molecule_types=='small molecule').sum()

def get_n_peptides_from_system(item, indices='all', structure_indices='all', check_form=True):

    from molsysmt.basic import get

    molecule_types = get(item, target='molecule', indices='all', molecule_type=True)
    return (molecule_types=='peptide').sum()

def get_n_proteins_from_system(item, indices='all', structure_indices='all', check_form=True):

    from molsysmt.basic import get

    molecule_types = get(item, target='molecule', indices='all', molecule_type=True)
    return (molecule_types=='protein').sum()

def get_n_dnas_from_system(item, indices='all', structure_indices='all', check_form=True):

    from molsysmt.basic import get

    molecule_types = get(item, target='molecule', indices='all', molecule_type=True)
    return (molecule_types=='dna').sum()

def get_n_rnas_from_system(item, indices='all', structure_indices='all', check_form=True):

    from molsysmt.basic import get

    molecule_types = get(item, target='molecule', indices='all', molecule_type=True)
    return (molecule_types=='rna').sum()

def get_n_lipids_from_system(item, indices='all', structure_indices='all', check_form=True):

    from molsysmt.basic import get

    molecule_types = get(item, target='molecule', indices='all', molecule_type=True)
    return (molecule_types=='lipid').sum()

def get_coordinates_from_system(item, indices='all', structure_indices='all', check_form=True):

    from molsysmt.basic import get
    return get(item, target='atom', structure_indices=structure_indices)

#def get_box_from_system(item, indices='all', structure_indices='all', check_form=True):
#
#    raise NotImplementedError

#def get_box_shape_from_system(item, indices='all', structure_indices='all', check_form=True):
#
#    raise NotImplementedError

#def get_box_lengths_from_system(item, indices='all', structure_indices='all', check_form=True):
#
#    raise NotImplementedError

#def get_box_angles_from_system(item, indices='all', structure_indices='all', check_form=True):
#
#    raise NotImplementedError

#def get_time_from_system(item, indices='all', structure_indices='all', check_form=True):
#
#    raise NotImplementedError

#def get_step_from_system(item, indices='all', structure_indices='all', check_form=True):
#
#    raise NotImplementedError

def get_frame_from_system(item, indices='all', structure_indices='all', check_form=True):

    from molsysmt.basic import get
    return get(item, target='atom', structure_indices=structure_indices, frame=True)

#def get_n_structures_from_system(item, indices='all', structure_indices='all', check_form=True):
#
#    raise NotImplementedError

def get_bonded_atoms_from_system(item, indices='all', structure_indices='all', check_form=True):

    from molsysmt.basic import get
    return get(item, target='atoms', indices='all', bonded_atoms=True)

def get_bond_index_from_system(item, indices='all', structure_indices='all', check_form=True):

    from molsysmt.basic import get
    return get(item, target='atoms', indices='all', bond_index=True)

def get_inner_bonded_atoms_from_system(item, indices='all', structure_indices='all', check_form=True):

    from molsysmt.basic import get
    return get(item, target='bond', indices='all', atom_index=True)

def get_inner_bond_index_from_system(item, indices='all', structure_indices='all', check_form=True):

    from molsysmt.basic import get
    return get(item, target='bond', indices='all', bond_index=True)

## bond

def get_bond_index_from_bond(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    if indices is 'all':
        n_aux = get_n_bonds_from_system(item, check_form=False)
        output = np.arange(n_aux, dtype=int)
    else:
        output = np.array(indices, dtype=int)

    return output

#def get_bond_order_from_bond(item, indices='all', structure_indices='all', check_form=True):
#
#    return _aux_getter_attribute(item, 'order', 'bond', indices)
#
#def get_bond_type_from_bond(item, indices='all', structure_indices='all', check_form=True):
#
#    return _aux_getter_attribute(item, 'type', 'bond', indices)

#def get_bond_order_from_bond(item, indices='all', structure_indices='all', check_form=True):
#
#    raise NotImplementedError

#def get_bond_type_from_bond(item, indices='all', structure_indices='all', check_form=True):
#
#    raise NotImplementedError

#def get_atom_index_from_bond(item, indices='all', structure_indices='all', check_form=True):
#
#    raise NotImplementedError

def get_n_bonds_from_bond(item, indices='all', structure_indices='all', check_form=True):

    _checking_form(item, check_form)

    if indices is 'all':
        output = get_n_bonds_from_system(item, check_form=False)
    else:
        output = indices.shape[0]

    return output


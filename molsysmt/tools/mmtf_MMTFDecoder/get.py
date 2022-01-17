from molsysmt.tools.mmtf_MMTFDecoder.is_mmtf_MMTFDecoder import _checking_form

## Atom

def get_atom_id_from_atom(item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_atom_id_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

def get_atom_name_from_atom(item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_atom_name_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

def get_atom_type_from_atom(item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_atom_type_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

def get_group_index_from_atom (item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_group_index_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

def get_component_index_from_atom (item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_component_index_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

def get_chain_index_from_atom (item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_chain_index_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

def get_molecule_index_from_atom (item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_molecule_index_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

def get_entity_index_from_atom (item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_entity_index_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

def get_inner_bonded_atoms_from_atom (item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_inner_bonded_atoms_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

def get_n_inner_bonds_from_atom (item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_n_inner_bonds_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

def get_coordinates_from_atom(item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np
    from molsysmt import puw

    n_frames = get_n_frames_from_system(item, indices='all', frame_indices='all', check_form=False)
    n_atoms = get_n_atoms_from_system(item, indices='all', frame_indices='all', check_form=False)

    xyz = np.column_stack([item.x_coord_list, item.y_coord_list, item.z_coord_list])
    xyz = xyz.reshape([-1, item.num_atoms, 3])
    xyz = puw.quantity(xyz, 'angstroms')
    xyz = puw.standardize(xyz)

    if frame_indices is not 'all':
        xyz = xyz[frame_indices,:,:]

    if indices is not 'all':
        xyz = xyz[:,indices,:]

    return xyz

def get_frame_from_atom(item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    tmp_step = get_step_from_system(item, frame_indices=frame_indices, check_form=False)
    tmp_time = get_time_from_system(item, frame_indices=frame_indices, check_form=False)
    tmp_box = get_box_from_system(item, frame_indices=frame_indices, check_form=False)
    tmp_coordinates = get_coordinates_from_atom(item, indices=indices, frame_indices=frame_indices, check_form=False)

    return tmp_step, tmp_time, tmp_coordinates, tmp_box

## group

def get_group_id_from_group(item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_group_id_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

def get_group_name_from_group(item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_group_name_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

def get_group_type_from_group(item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_group_type_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

## component

def get_component_id_from_component (item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_component_id_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

def get_component_name_from_component (item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_component_name_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

def get_component_type_from_component (item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_component_type_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

## molecule

def get_molecule_id_from_molecule (item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_molecule_id_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

def get_molecule_name_from_molecule (item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_molecule_name_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

def get_molecule_type_from_molecule (item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_molecule_type_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

## chain

def get_chain_id_from_chain (item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_chain_id_from_chain as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

def get_chain_name_from_chain (item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_chain_name_from_chain as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

def get_chain_type_from_chain (item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_chain_type_from_chain as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

## entity

def get_entity_id_from_entity (item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_entity_id_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

def get_entity_name_from_entity (item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_entity_name_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

def get_entity_type_from_entity (item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_entity_type_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output


## system

def get_n_atoms_from_system(item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_n_atoms_from_system as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

def get_n_groups_from_system(item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_n_groups_from_system as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

def get_n_components_from_system(item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_n_components_from_system as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

def get_n_chains_from_system(item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_n_chains_from_system as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

def get_n_molecules_from_system(item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_n_molecules_from_system as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

def get_n_entities_from_system(item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_n_entities_from_system as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

def get_n_bonds_from_system(item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_n_bonds_from_system as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

def get_box_from_system(item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np
    from molsysmt import puw
    from molsysmt.pbc import box_vectors_from_box_lengths_and_angles

    n_frames = get_n_frames_from_system(item, indices='all', frame_indices='all', check_form=False)

    if item.unit_cell is not None:

        cell_lengths = np.empty([n_frames,3], dtype='float64')
        cell_angles = np.empty([n_frames,3], dtype='float64')
        for ii in range(3):
            cell_lengths[:,ii] = item.unit_cell[ii]
            cell_angles[:,ii] = item.unit_cell[ii+3]

        cell_lengths = puw.quantity(cell_lengths, 'angstroms')
        cell_angles = puw.quantity(cell_angles, 'degrees')

        box = box_vectors_from_box_lengths_and_angles(cell_lengths, cell_angles)
        box = puw.standardize(box)

    else:

        box = None

    if frame_indices is not 'all':
        if box is not None:
            box = box[frame_indices,:,:]

    return box

def get_box_shape_from_system(item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    raise NotImplementedError()

def get_box_lengths_from_system(item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    raise NotImplementedError()

def get_box_angles_from_system(item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    raise NotImplementedError()

def get_box_volume_from_system(item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    raise NotImplementedError()

def get_time_from_system(item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    return None

def get_step_from_system(item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    return None

def get_n_frames_from_system(item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    return item.num_models

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_bonded_atoms_from_system as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

## bond

def get_bond_order_from_bond(item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_bond_order_from_bond as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

def get_bond_type_from_bond(item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_bond_type_from_bond as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

def get_atom_index_from_bond(item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import get_atom_index_from_bond as aux_get

    tmp_item = to_molsysmt_Topology(item, check_form=False)
    output = aux_get(tmp_item, indices=indices, frame_indices=frame_indices, check_form=False)

    return output

#######################################################################################
######### DO NOT TOUCH THE FOLLOWING LINES, JUST INCLUDE THEM AS THEY ARE #############
#######################################################################################

## atom

def get_atom_index_from_atom(item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    if indices is 'all':
        n_aux = get_n_atoms_from_system(item, check_form=False)
        output = np.arange(n_aux, dtype=int)
    else:
        output = np.array(indices, dtype=int)

    return output

def get_group_id_from_atom (item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_group_index_from_atom(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_group_id_from_group(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_group_name_from_atom (item, indices='all', frame_indices='all', check_form=True):

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

def get_group_type_from_atom (item, indices='all', frame_indices='all', check_form=True):

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

def get_component_id_from_atom (item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_component_index_from_atom(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_component_id_from_component(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_component_name_from_atom (item, indices='all', frame_indices='all', check_form=True):

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

def get_component_type_from_atom (item, indices='all', frame_indices='all', check_form=True):

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

def get_chain_id_from_atom (item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_chain_index_from_atom(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_chain_name_from_atom (item, indices='all', frame_indices='all', check_form=True):

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

def get_chain_type_from_atom (item, indices='all', frame_indices='all', check_form=True):

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

def get_molecule_id_from_atom (item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_molecule_index_from_atom(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_molecule_name_from_atom (item, indices='all', frame_indices='all', check_form=True):

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

def get_molecule_type_from_atom (item, indices='all', frame_indices='all', check_form=True):

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

def get_entity_id_from_atom (item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    aux_indices = get_entity_index_from_atom(item, indices=indices, check_form=False)
    aux_unique_indices = np.unique(aux_indices)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, check_form=False)
    aux_dict = dict(zip(aux_unique_indices, aux_vals))
    output = np.vectorize(aux_dict.__getitem__)(aux_indices)
    del(aux_indices, aux_unique_indices, aux_vals, aux_dict)

    return output

def get_entity_name_from_atom (item, indices='all', frame_indices='all', check_form=True):

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

def get_entity_type_from_atom (item, indices='all', frame_indices='all', check_form=True):

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

def get_n_atoms_from_atom (item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    if indices is 'all':
        output = get_n_atoms_from_system(item, check_form=False)
    else:
        output = indices.shape[0]

    return output

def get_n_groups_from_atom (item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    if indices is 'all':
        output = get_n_groups_from_system(item, check_form=False)
    else:
        output = get_group_index_from_atom(item, indices=indices, check_form=True)
        output = np.unique(output).shape[0]

    return output

def get_n_components_from_atom (item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    if indices is 'all':
        output = get_n_components_from_system(item, check_form=False)
    else:
        output = get_component_index_from_atom(item, indices=indices, check_form=True)
        output = np.unique(output).shape[0]

    return output

def get_n_molecules_from_atom (item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    if indices is 'all':
        output = get_n_molecules_from_system(item, check_form=False)
    else:
        output = get_molecule_index_from_atom(item, indices=indices, check_form=True)
        output = np.unique(output).shape[0]

    return output

def get_n_chains_from_atom (item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    if indices is 'all':
        output = get_n_chains_from_system(item, check_form=False)
    else:
        output = get_chain_index_from_atom(item, indices=indices, check_form=True)
        output = np.unique(output).shape[0]

    return output

def get_n_entities_from_atom (item, indices='all', frame_indices='all', check_form=True):

    _checking_form(item, check_form)

    import numpy as np

    if indices is 'all':
        output = get_n_entities_from_system(item, check_form=False)
    else:
        output = get_entity_index_from_atom(item, indices=indices, check_form=True)
        output = np.unique(output).shape[0]

    return output

def get_bonded_atoms_from_atom (item, indices='all', frame_indices='all', check_form=True):

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

def get_bond_index_from_atom (item, indices='all', frame_indices='all', check_form=True):

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

def get_n_bonds_from_atom (item, indices='all', frame_indices='all', check_form=True):

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


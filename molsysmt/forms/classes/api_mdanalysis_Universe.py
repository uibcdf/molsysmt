from os.path import basename as _basename
from os import remove as _remove
from MDAnalysis import Universe as _mdanalysis_Universe
import numpy as np
import simtk.unit as unit

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _mdanalysis_Universe : form_name,
    'mdanalysis.Universe' : form_name
}

info=["",""]
with_topology=True
wih_coordinates=True
with_box=True
with_parameters=False

def to_NGLView(item, atom_indices='all', frame_indices='all',
               topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from nglview import show_mdtraj as _nglview_show_mdanalysis

    tmp_item = extract(item, atom_indices=atom_indices, frame_indices=frame_indices)

    return _nglview_show_mdanalysis(tmp_item)

def to_pdb(item, atom_indices='all', frame_indices='all', multiframe=False,
           topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    tmp_item = extract(item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item.atoms.write(output_filename, multiframe=multiframe)

def to_mdtraj_Trajectory (item, atom_indices='all', frame_indices='all', multiframe=False,
           topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt._private_tools.pdb import tmp_pdb_filename
    from molsysmt.forms.files.api_pdb import to_mdtraj_Trajectory as pdb_to_mdtraj_Trajectory

    tmp_item = extract(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_file = tmp_pdb_filename()
    to_pdb(tmp_item=item, output_filename=tmp_file, multiframe=multiframe)
    tmp_item=pdb_to_mdtraj_Trajectory(tmp_file)
    _remove(tmp_file)

    return tmp_item

def to_molsysmt_MolSys (item, atom_indices='all', frame_indices='all',
           topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.native.io.molsys.classes import from_mdanalysis_Universe as molsysmt_MolSys_from_mdanalysis_Universe
    return molsysmt_MolSys_from_mdanalysis_Universe(item, atom_indices=atom_indices, frame_indices=frame_indices)

def to_molsysmt_MolSys (item, atom_indices='all', frame_indices='all',
           topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.native.io.molsys.classes import from_mdanalysis_Universe as molsysmt_MolSys_from_mdanalysis_Universe
    return molsysmt_MolSys_from_mdanalysis_Universe(item, atom_indices=atom_indices, frame_indices=frame_indices)

def to_molsysmt_Topology (item, atom_indices='all', frame_indices='all',
           topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.native.io.topology.classes import from_mdanalysis_Universe as molsysmt_Topology_from_mdanalysis_Universe
    return molsysmt_Topology_from_mdanalysis_Universe(item, atom_indices=atom_indices, frame_indices=frame_indices)

def to_molsysmt_Trajectory (item, atom_indices='all', frame_indices='all',
           topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.native.io.trajectory.classes import from_mdanalysis_Universe as molsysmt_Trajectory_from_mdanalysis_Universe
    return molsysmt_Trajectory_from_mdanalysis_Universe(item, atom_indices=atom_indices, frame_indices=frame_indices)

def select_with_MDTraj(item, selection):

    tmp_form=to_mdtraj(item,multiframe=True)

    return tmp_form.topology.select(selection)

def select_with_MDAnalysis(item, selection):

    tmp_atomgroup=item.select_atoms(selection)
    tmp_sel = tmp_atomgroup.atoms.ids
    del(tmp_atomgroup)

    return tmp_sel

def select_with_MolSysMT(item, selection):

    raise NotImplementedError

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

###### Get

## atom

def get_index_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_id_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_id_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_name_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_name_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_type_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_type_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_id_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_name_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_type_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_id_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_name_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_type_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_name_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_id_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_type_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_name_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_id_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_type_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_id_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_name_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_type_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_id_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_name_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_type_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_atoms_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_groups_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_components_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_molecules_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_chains_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_entities_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_bonds_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_inner_bond_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_inner_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_inner_bonds_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    tmp_item=np.array(item.trajectory)*0.1*unit.nanometers

    if frame_indices is not 'all':
        tmp_item=item_item[frame_indices,:,:]
    if indices is not 'all':
        tmp_item=tmp_item[:,indices,:]

    return tmp_item

def get_frame_from_atom(item, indices='all', frame_indices='all'):

    tmp_step = get_step_from_system(item, frame_indices=frame_indices)
    tmp_time = get_time_from_system(item, frame_indices=frame_indices)
    tmp_coordinates = get_coordinates_from_atom(item, indices=indices, frame_indices=frame_indices)
    tmp_box = get_box_from_system(item, frame_indices=frame_indices)

    return tmp_step, tmp_time, tmp_coordinates, tmp_box

def get_n_frames_from_atom(item, indices='all', frame_indices='all'):

    if frame_indices is not 'all':
        return len(frame_indices)
    else:
        raise NotImplementedError

def get_form_from_atom(item, indices='all', frame_indices='all'):

    return form_name

## group

def get_index_from_group (item, indices='all', frame_indices='all'):

    return get_group_index_from_group (item, indices=indices, frame_indices=frame_indices)

def get_id_from_group (item, indices='all', frame_indices='all'):

    return get_group_id_from_group (item, indices=indices, frame_indices=frame_indices)

def get_name_from_group (item, indices='all', frame_indices='all'):

    return get_group_name_from_group (item, indices=indices, frame_indices=frame_indices)

def get_type_from_group (item, indices='all', frame_indices='all'):

    return get_group_type_from_group (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_id_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_name_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_type_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_index_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_id_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_name_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_type_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_name_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_index_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_id_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_type_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_name_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_index_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_id_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_type_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_index_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_id_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_name_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_type_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_index_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_id_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_name_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_type_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_atoms_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_groups_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_components_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_molecules_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_chains_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_entities_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_bonds_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

## component

def get_index_from_component (item, indices='all', frame_indices='all'):

    return get_component_index_from_component (item, indices=indices, frame_indices=frame_indices)

def get_id_from_component (item, indices='all', frame_indices='all'):

    return get_component_id_from_component (item, indices=indices, frame_indices=frame_indices)

def get_name_from_component (item, indices='all', frame_indices='all'):

    return get_component_name_from_component (item, indices=indices, frame_indices=frame_indices)

def get_type_from_component (item, indices='all', frame_indices='all'):

    return get_component_type_from_component (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_component(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_id_from_component(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_name_from_component(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_type_from_component(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_index_from_component(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_id_from_component(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_name_from_component(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_type_from_component(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_name_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_index_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_id_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_type_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_name_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_index_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_id_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_type_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_index_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_id_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_name_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_type_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_index_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_id_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_name_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_type_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_atoms_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_groups_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_components_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_molecules_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_chains_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_entities_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_bonds_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

## molecule

def get_index_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_index_from_molecule (item, indices=indices, frame_indices=frame_indices)

def get_id_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_id_from_molecule (item, indices=indices, frame_indices=frame_indices)

def get_name_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_name_from_molecule (item, indices=indices, frame_indices=frame_indices)

def get_type_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_type_from_molecule (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_molecule(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_id_from_molecule(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_name_from_molecule(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_type_from_molecule(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_index_from_molecule(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_id_from_molecule(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_name_from_molecule(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_type_from_molecule(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_name_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_index_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_id_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_type_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_name_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_index_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_id_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_type_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_index_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_id_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_name_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_type_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_index_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_id_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_name_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_type_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_atoms_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_groups_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_components_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_molecules_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_chains_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_entities_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_bonds_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

## chain

def get_index_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_index_from_chain (item, indices=indices, frame_indices=frame_indices)

def get_id_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_id_from_chain (item, indices=indices, frame_indices=frame_indices)

def get_name_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_name_from_chain (item, indices=indices, frame_indices=frame_indices)

def get_type_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_type_from_chain (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_chain(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_id_from_chain(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_name_from_chain(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_type_from_chain(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_index_from_chain(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_id_from_chain(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_name_from_chain(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_type_from_chain(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_name_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_index_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_id_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_type_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_name_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_index_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_id_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_type_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_index_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_id_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_name_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_type_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_index_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_id_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_name_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_type_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_atoms_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_groups_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_components_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_molecules_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_chains_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_entities_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_bonds_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

## entity

def get_index_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_index_from_entity (item, indices=indices, frame_indices=frame_indices)

def get_id_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_id_from_entity (item, indices=indices, frame_indices=frame_indices)

def get_name_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_name_from_entity (item, indices=indices, frame_indices=frame_indices)

def get_type_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_type_from_entity (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_id_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_name_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_type_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_index_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_id_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_name_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_type_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_name_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_index_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_id_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_type_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_name_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_index_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_id_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_type_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_index_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_id_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_name_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_type_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_index_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_id_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_name_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_entity_type_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_atoms_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_groups_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_components_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_molecules_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_chains_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_entities_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_bonds_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

## system

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

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

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

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

def get_mass_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_coordinates_from_system(item, indices='all', frame_indices='all'):

    tmp_item=np.array(item.trajectory)*0.1*unit.nanometers

    if frame_indices is not 'all':
        tmp_item=item_item[frame_indices,:,:]

    return tmp_item

def get_box_from_system(item, indices='all', frame_indices='all'):

    tmp_item = np.array([frame.triclinic_dimensions for frame in item.trajectory])*0.1*unit.nanometers

    if frame_indices is not 'all':
        tmp_item=item_item[frame_indices,:,:]

    return tmp_item

def get_box_shape_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_lengths_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_angles_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_time_from_system(item, indices='all', frame_indices='all'):

    tmp_item = np.array([frame.time for frame in item.trajectory])*unit.picoseconds

    if frame_indices is not 'all':
        tmp_item=item_item[frame_indices]

    return tmp_item

def get_step_from_system(item, indices='all', frame_indices='all'):

    if frame_indices is 'all':
        output = np.arange(get_n_frames_from_system(item))
    else:
        output = frame_indices
    return output

def get_frame_from_system(item, indices='all', frame_indices='all'):

    tmp_step = get_step_from_system(item, frame_indices=frame_indices)
    tmp_time = get_time_from_system(item, frame_indices=frame_indices)
    tmp_coordinates = get_coordinates_from_system(item, frame_indices=frame_indices)
    tmp_box = get_box_from_system(item, frame_indices=frame_indices)

    return tmp_step, tmp_time, tmp_coordinates, tmp_box

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    if frame_indices is 'all':
        output=item.trajectory.n_frames
    else:
        output=frame_indices.shape[0]

    return output

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name


from os.path import basename as _basename
from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
from MDAnalysis import Universe as _mdanalysis_Universe
import numpy as np

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

def to_nglview_NGLView(item, atom_indices='all', frame_indices='all',
                       topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from nglview import show_mdtraj

    tmp_item = extract(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = show_mdtraj(tmp_item)

    return tmp_item

def to_pdb(item, atom_indices='all', frame_indices='all',
           topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None,
           output_filename=None, multiframe=False):

    tmp_item = extract(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.atoms.write(output_filename, multiframe=multiframe)

    return output_filename

def to_mdtraj_Trajectory (item, atom_indices='all', frame_indices='all',
           topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt._private_tools.pdb import tmp_pdb_filename
    from molsysmt.forms.files.api_pdb import to_mdtraj_Trajectory as pdb_to_mdtraj_Trajectory
    from os import remove

    tmp_item = extract(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_file = tmp_pdb_filename()
    to_pdb(tmp_item=item, output_filename=tmp_file)
    tmp_item=pdb_to_mdtraj_Trajectory(tmp_file)
    remove(tmp_file)

    return tmp_item

def to_molsysmt_MolSys (item, atom_indices='all', frame_indices='all',
           topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.native.io.molsys.classes import from_mdanalysis_Universe as molsysmt_MolSys_from_mdanalysis_Universe
    return molsysmt_MolSys_from_mdanalysis_Universe(item, atom_indices=atom_indices, frame_indices=frame_indices,
                                topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None)

def to_molsysmt_MolSys (item, atom_indices='all', frame_indices='all',
           topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.native.io.molsys.classes import from_mdanalysis_Universe as molsysmt_MolSys_from_mdanalysis_Universe
    return molsysmt_MolSys_from_mdanalysis_Universe(item, atom_indices=atom_indices, frame_indices=frame_indices,
                                topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None)

def to_molsysmt_Topology (item, atom_indices='all', frame_indices='all',
           topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.native.io.topology.classes import from_mdanalysis_Universe as molsysmt_Topology_from_mdanalysis_Universe
    return molsysmt_Topology_from_mdanalysis_Universe(item, atom_indices=atom_indices, frame_indices=frame_indices,
                                topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None)

def to_molsysmt_Trajectory (item, atom_indices='all', frame_indices='all',
           topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.native.io.trajectory.classes import from_mdanalysis_Universe as molsysmt_Trajectory_from_mdanalysis_Universe
    return molsysmt_Trajectory_from_mdanalysis_Universe(item, atom_indices=atom_indices, frame_indices=frame_indices,
                                topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None)

def select_with_Amber(item, selection):

    raise NotImplementedError

def select_with_MDAnalysis(item, selection):

    tmp_atomgroup=item.select_atoms(selection)
    tmp_sel = tmp_atomgroup.atoms.ids
    del(tmp_atomgroup)

    return tmp_sel

def select_with_MDTraj(item, selection):

    tmp_form=to_mdtraj(item,multiframe=True)

    return tmp_form.topology.select(selection)

def select_with_MolSysMT(item, selection):

    raise NotImplementedError

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

def merge(list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def concatenate(list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def add(item, list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def append(item, list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def select_with_MolSysMT(item, selection):

    raise NotImplementedError

###### Get

## atom

def get_atom_id_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_name_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_type_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import get_component_index_from_atom as _get
    return _get(item, indices=indices)

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.elements.molecule import get_molecule_index_from_atom as _get
    return _get(item, indices=indices)

def get_entity_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.elements.entity import get_entity_index_from_atom as _get
    return _get(item, indices=indices)

def get_inner_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_inner_bonds_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_inner_bonds_from_system (item)
    else:
        raise NotImplementedError

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    tmp_item=np.array(item.trajectory)*0.1*unit.nanometers

    if frame_indices is not 'all':
        tmp_item=item_item[frame_indices,:,:]
    if indices is not 'all':
        tmp_item=tmp_item[:,indices,:]

    return tmp_item

## group

def get_group_id_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_name_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_group_type_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## component

def get_component_id_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import get_component_id_from_component as get
    return get(item, indices)

def get_component_name_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import get_component_name_from_component as get
    return get(item, indices)

def get_component_type_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import get_component_type_from_component as get
    return get(item, indices)

## molecule

def get_molecule_id_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.elements.molecule import get_molecule_id_from_molecule as get
    return get(item, indices)

def get_molecule_name_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.elements.molecule import get_molecule_name_from_molecule as get
    return get(item, indices)

def get_molecule_type_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.elements.molecule import get_molecule_type_from_molecule as get
    return get(item, indices)

## chain

def get_chain_id_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_name_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_type_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

## entity

def get_entity_id_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.elements.entity import get_entity_id_from_molecule as get
    return get(item, indices)

def get_entity_name_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.elements.entity import get_entity_name_from_molecule as get
    return get(item, indices)

def get_entity_type_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.elements.entity import get_entity_type_from_molecule as get
    return get(item, indices)

## system

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import get_n_components_from_system as get
    return get(item, indices)

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.elements.molecule import get_n_molecules_from_system as get
    return get(item, indices)

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.elements.entity import get_n_entities_from_system as get
    return get(item, indices)

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

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

def get_box_volume_from_system(item, indices='all', frame_indices='all'):

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

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    if frame_indices is 'all':
        output=item.trajectory.n_frames
    else:
        output=frame_indices.shape[0]

    return output

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

def get_has_topology_from_system(item, indices='all', frame_indices='all'):

    return with_topology

def get_has_parameters_from_system(item, indices='all', frame_indices='all'):

    return with_parameters

def get_has_coordinates_from_system(item, indices='all', frame_indices='all'):

    return with_coordinates

def get_has_box_from_system(item, indices='all', frame_indices='all'):

    output = False

    if with_box:
        tmp_box = get_box_from_system(item, indices=indices, frame_indices=frame_indices)
        if tmp_box[0] is not None:
            output = True

    return output

def get_has_bonds_from_system(item, indices='all', frame_indices='all'):

    output = False

    if with_topology:
        if get_n_bonds_from_system(item, indices=indices, frame_indices=frame_indices):
            output = True

    return output

## bond

def get_bond_order_from_bond(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_bond_type_from_bond(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_atom_index_from_bond(item, indices='all', frame_indices='all'):

    raise NotImplementedError

###### Set

def set_box_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError

def set_coordinates_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError



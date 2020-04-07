from os.path import basename as _basename
from molsysmt.utils.exceptions import *
from molsysmt import MolSys as _molsysmt_MolSys

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _molsysmt_MolSys : form_name,
    'molsysmt.MolSys': form_name
}

info=["",""]

def to_aminoacids3_seq(item, atom_indices='all', frame_indices='all'):

    from .api_mdtraj_Topology import to_aminoacids3_seq as mdtraj_Topology_to_aminoacids3_seq

    tmp_item = to_mdtraj_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = mdtraj_Topology_to_aminoacids3_seq(tmp_item)
    return tmp_item

def to_aminoacids1_seq(item, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.seqs.api_aminoacids3 import to_aminoacids1_seq as aminoacids3_seq_to_aminoacids1_seq
    tmp_item = to_aminoacids3_seq(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = aminoacids3_seq_to_aminoacids1_seq(tmp_item)
    return tmp_item

def to_biopython_Seq(item, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.seqs.api_aminoacids1 import to_biopython_Seq as aminoacids1_to_biopython_Seq
    tmp_item = to_aminoacids1_seq(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = aminoacids1_to_biopython_Seq(tmp_item)
    return tmp_item

def to_biopython_SeqRecord(item, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.seqs.api_aminoacids1 import to_biopython_SeqRecord as aminoacids1_to_biopython_SeqRecord
    tmp_item = to_aminoacids1_seq(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = aminoacids1_to_biopython_SeqRecord(tmp_item)
    return tmp_item

def to_mdtraj_Trajectory(item, atom_indices='all', frame_indices='all'):

    from simtk import unit as _unit
    from mdtraj.core.trajectory import Trajectory as mdtraj_Trajectory

    tmp_item_topology = to_mdtraj_Topology(item, atom_indices=atom_indices)
    tmp_box_lengths = get_box_lengths_from_system(item, frame_indices=frame_indices)
    tmp_box_lengths = tmp_box_lengths.in_units_of(_unit.nanometers)._value
    tmp_box_angles = get_box_angles_from_system(item, frame_indices=frame_indices)
    tmp_box_angles = tmp_box_angles.in_units_of(_unit.degrees)._value
    tmp_coordinates = get_coordinates_from_atom(item, indices=atom_indices, frame_indices=frame_indices)
    tmp_coordinates = tmp_coordinates.in_units_of(_unit.nanometers)._value
    tmp_time = get_coordinates_from_system(item, frame_indices=frame_indices)
    tmp_time = tmp_time.in_units_of(_unit.picoseconds)._value
    tmp_item = mdtraj_Trajectory(tmp_coordinates,tmp_item_topology, tmp_time,
            unitcell_lengths=tmp_box_lengths, unitcell_angles=tmp_box_angles)

    return tmp_item

def to_mdtraj_Topology(item, atom_indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import to_mdtraj_Topology as molsysmt_Composition_to_mdtraj_Topology
    return molsysmt_Composition_to_mdtraj_Topology(item.composition, atom_indices=atom_indices,
                                                frame_indices=frame_indices)

def to_pdb(item, output_file_path=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.files import to_pdb as molsysmt_MolSys_to_pdb
    return molsysmt_MolSys_to_pdb(item, output_file_path=output_file_path, selection=atom_indices,
            frame_indices=frame_indices)

def select_with_MDTraj(item, selection):

    from .api_molsysmt_Composition import select_with_MDTraj as select_Composition_with_MDTraj
    return select_Composition_with_MDTraj(item.composition, selection)

def select_with_MolSysMT(item, selection):

    from .api_molsysmt_Composition import select_with_MolSysMT as select_Composition_with_MolSysMT
    return select_Composition_with_MolSysMT(item.composition, selection)

def extract_subsystem(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def to_nglview(item, atom_indices='all', frame_indices='all'):

    from .api_mdtraj_Trajectory import to_nglview as mdtraj_to_nglview

    tmp_item = to_mdtraj_Trajectory(item, atom_indices=atom_indices, frame_indices=frame_indices)

    return mdtraj_to_nglview(tmp_item)

def duplicate(item):

    return tmp_item.duplicate()

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

    from .api_molsysmt_Composition import get_atom_index_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_atom(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_atom_id_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_atom(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_atom_name_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_atom(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_atom_type_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_group_index_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_group_id_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_group_id_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_group_name_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_group_name_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_group_type_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_group_type_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_component_name_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_component_name_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_component_index_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_component_id_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_component_id_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_component_type_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_component_type_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_chain_name_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_chain_index_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_chain_id_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_chain_type_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_molecule_index_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_molecule_id_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_molecule_name_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_molecule_type_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_entity_index_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_entity_id_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_entity_name_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_entity_type_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_bonded_atoms_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_atoms_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_groups_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_components_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_components_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_molecules_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_chains_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_entities_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_bonds_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_mass_from_atom(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_mass_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_charge_from_atom(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_charge_from_atom as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Trajectory import get_coordinates_from_atom as _get
    return _get(item.trajectory, indices=indices, frame_indices=frame_indices)

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

    from .api_molsysmt_Composition import get_atom_index_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_group(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_atom_id_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_group(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_atom_name_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_group(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_atom_type_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_group_index_from_group(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_group_index_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_group_id_from_group(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_group_id_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_group_name_from_group(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_group_name_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_group_type_from_group(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_group_type_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_component_name_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_component_name_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_component_index_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_component_index_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_component_id_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_component_id_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_component_type_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_component_type_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_chain_name_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_chain_index_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_chain_id_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_chain_type_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_molecule_index_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_molecule_id_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_molecule_name_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_molecule_type_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_entity_index_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_entity_id_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_entity_name_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_entity_type_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_atoms_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_groups_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_components_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_components_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_molecules_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_chains_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_entities_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_bonds_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_mass_from_group(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_mass_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_charge_from_group(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_charge_from_group as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_group(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Trajectory import get_coordinates_from_group as _get
    return _get(item.trajectory, indices=indices, frame_indices=frame_indices)

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

    from .api_molsysmt_Composition import get_atom_index_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_component(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_atom_id_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_component(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_atom_name_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_component(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_atom_type_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_group_index_from_component(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_group_index_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_group_id_from_component(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_group_id_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_group_name_from_component(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_group_name_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_group_type_from_component(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_group_type_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_component_name_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_component_name_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_component_index_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_component_index_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_component_id_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_component_id_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_component_type_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_component_type_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_chain_name_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_chain_index_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_chain_id_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_chain_type_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_molecule_index_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_molecule_id_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_molecule_name_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_molecule_type_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_entity_index_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_entity_id_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_entity_name_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_entity_type_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_atoms_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_groups_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_components_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_components_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_molecules_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_chains_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_entities_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_bonds_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_mass_from_component(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_mass_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_charge_from_component(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_charge_from_component as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_component(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Trajectory import get_coordinates_from_component as _get
    return _get(item.trajectory, indices=indices, frame_indices=frame_indices)


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

    from .api_molsysmt_Composition import get_atom_index_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_molecule(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_atom_id_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_molecule(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_atom_name_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_molecule(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_atom_type_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_group_index_from_molecule(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_group_index_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_group_id_from_molecule(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_group_id_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_group_name_from_molecule(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_group_name_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_group_type_from_molecule(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_group_type_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_component_name_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_component_name_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_component_index_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_component_index_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_component_id_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_component_id_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_component_type_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_component_type_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_chain_name_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_chain_index_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_chain_id_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_chain_type_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_molecule_index_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_molecule_id_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_molecule_name_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_molecule_type_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_entity_index_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_entity_id_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_entity_name_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_entity_type_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_atoms_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_groups_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_components_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_components_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_molecules_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_chains_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_entities_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_bonds_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_mass_from_molecule(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_mass_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_charge_from_molecule(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_charge_from_molecule as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_molecule(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Trajectory import get_coordinates_from_molecule as _get
    return _get(item.trajectory, indices=indices, frame_indices=frame_indices)


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

    from .api_molsysmt_Composition import get_atom_index_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_chain(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_atom_id_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_chain(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_atom_name_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_chain(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_atom_type_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_group_index_from_chain(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_group_index_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_group_id_from_chain(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_group_id_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_group_name_from_chain(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_group_name_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_group_type_from_chain(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_group_type_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_component_name_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_component_name_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_component_index_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_component_index_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_component_id_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_component_id_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_component_type_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_component_type_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_chain_name_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_chain_index_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_chain_id_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_chain_type_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_molecule_index_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_molecule_id_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_molecule_name_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_molecule_type_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_entity_index_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_entity_id_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_entity_name_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_entity_type_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_atoms_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_groups_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_components_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_components_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_molecules_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_chains_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_entities_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_bonds_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_mass_from_chain(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_mass_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_charge_from_chain(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_charge_from_chain as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_chain(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Trajectory import get_coordinates_from_chain as _get
    return _get(item.trajectory, indices=indices, frame_indices=frame_indices)

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

    from .api_molsysmt_Composition import get_atom_index_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_entity(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_atom_id_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_entity(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_atom_name_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_entity(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_atom_type_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_group_index_from_entity(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_group_index_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_group_id_from_entity(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_group_id_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_group_name_from_entity(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_group_name_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_group_type_from_entity(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_group_type_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_component_name_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_component_name_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_component_index_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_component_index_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_component_id_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_component_id_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_component_type_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_component_type_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_chain_name_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_chain_index_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_chain_id_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_chain_type_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_molecule_index_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_molecule_id_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_molecule_name_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_molecule_type_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_entity_index_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_entity_id_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_entity_name_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_entity_type_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_atoms_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_groups_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_components_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_components_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_molecules_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_chains_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_entities_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_bonds_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_mass_from_entity(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_mass_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_charge_from_entity(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_charge_from_entity as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_entity(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Trajectory import get_coordinates_from_entity as _get
    return _get(item.trajectory, indices=indices, frame_indices=frame_indices)


## system

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_bonded_atoms_from_system as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_atoms_from_system as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_groups_from_system as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_components_from_system as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_chains_from_system as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_molecules_from_system as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_entities_from_system as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_bonds_from_system as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_aminoacids_from_system (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_aminoacids_from_system as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_nucleotides_from_system (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_nucleotides_from_system as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_ions_from_system (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_ions_from_system as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_waters_from_system (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_waters_from_system as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_cosolutes_from_system (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_cosolutes_from_system as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_small_molecules_from_system (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_small_molecules_from_system as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_peptides_from_system (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_peptides_from_system as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_proteins_from_system (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_proteins_from_system as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_dnas_from_system (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_dnas_from_system as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_n_rnas_from_system (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_n_dnas_from_system as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_mass_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_mass_from_system as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_charge_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Composition import get_mass_from_system as _get
    return _get(item.composition, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Trajectory import get_coordinates_from_system as _get
    return _get(item.trajectory, indices=indices, frame_indices=frame_indices)

def get_box_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Trajectory import get_box_from_system as _get
    return _get(item.trajectory, indices=indices, frame_indices=frame_indices)

def get_box_shape_from_system(item, indices='all', frame_indices='all'):

    return item.trajectory.box_shape

def get_box_lengths_from_system(item, indices='all', frame_indices='all'):

    tmp_box_lengths = item.trajectory.get_box_lengths()
    tmp_box_lengths = tmp_box_lengths[frame_indices,:]
    return tmp_box_lengths

def get_box_angles_from_system(item, indices='all', frame_indices='all'):

    tmp_box_angles = item.trajectory.get_box_angles()
    tmp_box_angles = tmp_box_angles[frame_indices,:]
    return tmp_box_angles

def get_time_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Trajectory import get_time_from_system as _get
    return _get(item.trajectory, indices=indices, frame_indices=frame_indices)

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Trajectory import get_n_frames_from_system as _get
    return _get(item.trajectory, indices=indices, frame_indices=frame_indices)

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

###### Set

def set_box_to_system(item, indices='all', frame_indices='all', value=None):

    item.trajectory.box = value
    pass

def set_coordinates_to_system(item, indices='all', frame_indices='all', value=None):

    item.trajectory.coordinates = value
    pass


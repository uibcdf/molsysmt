from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np
from mdtraj.core.trajectory import Trajectory as _mdtraj_Trajectory
import importlib
import sys
from molsysmt import puw
from molsysmt.native.molecular_system import molecular_system_components

form_name='mdtraj.Trajectory'

is_form={
    _mdtraj_Trajectory:form_name,
    'mdtraj.Trajectory':form_name
    }

info=["",""]

has = molecular_system_components.copy()
for ii in ['elements', 'bonds', 'coordinates', 'box']:
    has[ii]=True

def to_string_aminoacids3(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mdtraj_Topology import to_string_aminoacids3 as mdtraj_Topology_to_string_aminoacids3

    tmp_item, tmp_molecular_system = to_mdtraj_Topology(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = mdtraj_Topology_to_string_aminoacids3(tmp_item, molecular_system=tmp_molecular_system)

    return tmp_item, tmp_molecular_system

def to_string_aminoacids1(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mdtraj_Topology import to_string_aminoacids1 as mdtraj_Topology_to_string_aminoacids1

    tmp_item, tmp_molecular_system = to_mdtraj_Topology(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = mdtraj_Topology_to_string_aminoacids1(tmp_item, molecular_system=tmp_molecular_system)

    return tmp_item, tmp_molecular_system

def to_biopython_Seq(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.strings.api_string_aminoacids1 import to_biopython_Seq as string_aminoacids1_to_biopython_Seq

    tmp_item, tmp_molecular_system = to_string_aminoacids1(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = string_aminoacids1_to_biopython_Seq(tmp_item, molecular_system=tmp_molecular_system)

    return tmp_item, tmp_molecular_system

def to_biopython_SeqRecord(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.strings.api_string_aminoacids1 import to_biopython_SeqRecord as string_aminoacids1_to_biopython_SeqRecord

    tmp_item, tmp_molecular_system = to_string_aminoacids1(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = string_aminoacids1_to_biopython_SeqRecord(tmp_item, molecular_system=tmp_molecular_system)

    return tmp_item, tmp_molecular_system

def to_molsysmt_MolSys(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.classes import from_mdtraj_Trajectory as mdtraj_Trajectory_to_molsysmt_MolSys

    tmp_item, tmp_molecular_system = mdtraj_Trajectory_to_molsysmt_MolSys(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_molsysmt_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.trajectory.classes import from_mdtraj_Trajectory as mdtraj_Trajectory_to_molsysmt_Topology

    tmp_item, tmp_molecular_system = mdtraj_Trajectory_to_molsysmt_Topology(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_molsysmt_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.classes import from_mdtraj_Trajectory as mdtraj_Trajectory_to_molsysmt_Topology

    tmp_item, tmp_molecular_system = mdtraj_Trajectory_to_molsysmt_Topology(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_mdtraj_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mdtraj_Topology import to_mdtraj_Topology as mdtraj_Topology_to_mdtraj_Topology

    tmp_item=item.topology
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None
    tmp_item, tmp_molecular_system = mdtraj_Topology_to_mdtraj_Topology(tmp_item, molecular_system=tmp_molecular_system, atom_indices=atom_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_openmm_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mdtraj_Topology import to_openmm_Topology as mdtraj_Topology_to_openmm_Topology

    tmp_item, tmp_molecular_system = to_mdtraj_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = mdtraj_Topology_to_openmm_Topology(tmp_item, tmp_molecular_system)

    return tmp_item, tmp_molecular_system

def to_openmm_Modeller(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from openmm.app import Modeller
    from openmm.unit import nanometers

    topology, _ = to_openmm_Topology(item, molecular_system=None, atom_indices=atom_indices, frame_indices=frame_indices)
    positions = get_coordinates_from_atom(item, indices=atom_indices, frame_indices=frame_indices)
    positions = puw.convert(positions, to_form='openmm.unit')
    tmp_item = Modeller(topology, positions)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    else:
        tmp_molecular_system = None

    del(topology, positions)

    return tmp_item, tmp_molecular_system

def to_parmed_Structure(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import to_parmed_Structure as openmm_Topology_to_parmed_Structure

    tmp_item, tmp_molecular_system = to_openmm_Topology(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = openmm_Topology_to_parmed_Structure(tmp_item, tmp_molecular_system)

    return tmp_item, tmp_molecular_system

def to_pdbfixer_PDBFixer(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.files.api_pdb import to_pdbfixer_PDBFixer as pdb_to_pdbfixer_PDBFixer
    from molsysmt._private_tools.files_and_directories import tmp_filename
    from os import remove as remove

    tmp_file = tmp_filename(extension='pdb')
    tmp_item, tmp_molecular_system = to_pdb(item, molecular_system=molecular_system, output_filename=tmp_file, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = pdb_to_pdbfixer_PDBFixer(tmp_item, tmp_molecular_system)
    remove(tmp_file)

    return tmp_item, tmp_molecular_system

def to_file_pdb(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):

    tmp_item, tmp_molecular_system = to_mdtraj_Trajectory(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)
    tmp_item.save_pdb(output_filename)
    tmp_item = output_filename
    if tmp_molecular_system is not None:
        tmp_molecular_system = tmp_molecular_system.combine_with_items(tmp_item)

    return tmp_item, tmp_molecular_system

def to_file_xtc(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):

    tmp_item, tmp_molecular_system = to_mdtraj_Trajectory(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)
    item.save_xtc(output_filename)
    tmp_item = output_filename
    if tmp_molecular_system is not None:
        tmp_molecular_system = tmp_molecular_system.combine_with_items(tmp_item)

    return tmp_item, tmp_molecular_system

def to_nglview_NGLWidget(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from nglview import show_mdtraj as show_mdtraj

    tmp_item, tmp_molecular_system = to_mdtraj_Trajectory(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)
    tmp_item = show_mdtraj(tmp_item)
    if tmp_molecular_system is not None:
        tmp_molecular_system = tmp_molecular_system.combine_with_items(tmp_item)

    return tmp_item, tmp_molecular_system

def to_mdtraj_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all', copy_if_all=True):

    tmp_molecular_system = None

    if (atom_indices is 'all') and (frame_indices is 'all'):
        if copy_if_all:
            tmp_item = extract_item(item)
            if molecular_system is not None:
                tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
        else:
            tmp_item = item
            if molecular_system is not None:
                tmp_molecular_system = molecular_system
    else:
        tmp_item = extract_item(item, atom_indices=atom_indices, frame_indices=frame_indices)
        if molecular_system is not None:
            tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def extract_item(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        tmp_item = item.copy()
    else:
        tmp_item = item
        if atom_indices is not 'all':
            tmp_item = tmp_item.atom_slice(atom_indices)
        if frame_indices is not 'all':
            tmp_item = tmp_item.slice(frame_indices)

    return tmp_item

def add(item, from_item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

##### Get

def aux_get(item, indices='all', frame_indices='all'):

    tmp_item, _ = to_mdtraj_Topology(item)
    method_name = sys._getframe(1).f_code.co_name
    module = importlib.import_module('molsysmt.forms.classes.api_mdtraj_Topology')
    _get = getattr(module, method_name)
    output = _get(tmp_item, indices=indices, frame_indices=frame_indices)

    return output

## atom

def get_atom_id_from_atom(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_atom(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_atom(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_atom (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_inner_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_inner_bonds_from_atom (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    tmp_item=item.xyz

    if frame_indices is not 'all':
        tmp_item=tmp_item[frame_indices,:,:]
    if indices is not 'all':
        tmp_item=tmp_item[:,indices,:]

    return tmp_item*puw.unit('nanometer')

## group

def get_group_id_from_group(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_group_name_from_group(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_group_type_from_group(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

## component

def get_component_id_from_component (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_component_name_from_component (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_component_type_from_component (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

## molecule

def get_molecule_id_from_molecule (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_molecule (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_molecule (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

## chain

def get_chain_id_from_chain (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_chain (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_chain (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

## entity

def get_entity_id_from_entity (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_entity (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_entity (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

## system

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_box_from_system(item, indices='all', frame_indices='all'):

    output = None

    if item.unitcell_vectors is not None:

        output = item.unitcell_vectors * puw.unit('nanometers')
        output = puw.standardize(output)

    return output

def get_box_shape_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_lengths_from_system(item, indices='all', frame_indices='all'):

    output = None

    if item.unitcell_lengths is not None:

        output = item.unitcell_vectors * puw.unit('nanometers')
        output = puw.standardize(output)

    return output

def get_box_angles_from_system(item, indices='all', frame_indices='all'):

    output = None

    if item.unitcell_angles is not None:

        output = item.unitcell_vectors * puw.unit('degrees')
        output = puw.standardize(output)

    return output

def get_box_volume_from_system(item, indices='all', frame_indices='all'):

    output = None

    if item.unitcell_volumes is not None:

        output = item.unitcell_vectors * puw.unit('nanometers **3')
        output = puw.standardize(output)

    return output

def get_time_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_step_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

## bond

def get_bond_order_from_bond(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_bond_type_from_bond(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_bond(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

###### Set

def set_box_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError

def set_coordinates_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError




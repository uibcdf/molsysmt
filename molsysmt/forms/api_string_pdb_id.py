import importlib
import numpy as np
import urllib
import sys
from shutil import move
from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
from molsysmt.native.molecular_system import molecular_system_components

form_name='string:pdb_id'

is_form = {
    'string:pdb_id': form_name,
    }

info=["",""]

has = molecular_system_components.copy()
for ii in ['elements', 'coordinates', 'box', 'bonds']:
    has[ii]=True

def to_file_pdb(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):

    from molsysmt.tools.file_pdb import download as download_pdb
    from molsysmt.forms.api_file_pdb import to_file_pdb as file_pdb_to_file_pdb

    tmp_item = item.split(':')[-1]
    download_pdb(tmp_item, output_filename)
    tmp_item = output_filename
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None
    tmp_item, tmp_molecular_system = file_pdb_to_file_pdb(tmp_item, tmp_molecular_system, output_filename=output_filename, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_file_mmtf(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):

    from mmtf import fetch
    from molsysmt.forms.api_mmtf_MMTFDecoder import to_file_mmtf as MMTFDecoder_to_file_mmtf

    tmp_item, tmp_molecular_system = to_mmtf_MMTFDecoder(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = MMTFDecoder_to_file_mmtf(tmp_item, molecular_system=tmp_molecular_system, output_filename=output_filename)

    return tmp_item, tmp_molecular_system

def to_file_msmpk(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):

    from molsysmt.forms.api_molsysmt_MolSys import to_file_msmpk as molsysmt_MolSys_to_file_msmpk

    tmp_item, tmp_molecular_system = to_molsysmt_MolSys(item, molecular_system=molecular_system,
            atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = molsysmt_MolSys_to_file_msmpk(tmp_item,
            molecular_system=tmp_molecular_system, output_filename=output_filename)

    return tmp_item, tmp_molecular_system

def to_file_fasta(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):

    from molsysmt.forms.api_file_fasta import to_file_fasta as file_fasta_to_file_fasta

    tmp_item = item.split(':')[-1]
    url = 'https://www.rcsb.org/pdb/download/downloadFastaFiles.do?structureIdList='+tmp_item+'&compressionType=uncompressed'
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    fasta_txt = response.read().decode('utf-8')
    with open(output_filename,'w') as f:
        f.write(fasta_txt)
    f.close()
    tmp_item = output_filename
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None
    tmp_item, tmp_molecular_system= file_fasta_to_file_fasta(tmp_item, molecular_system=tmp_molecular_items, atom_indices=atom_indices,
            frame_indices=frame_indices, output_filename=output_filename, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_mmtf_MMTFDecoder(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from mmtf import fetch
    from molsysmt.forms.api_mmtf_MMTFDecoder import to_mmtf_MMTFDecoder as mmtf_MMTFDecoder_to_mmtf_MMTFDecoder

    tmp_item = item.split(':')[-1]
    tmp_item = fetch(tmp_item)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None
    tmp_item, tmp_molecular_system = mmtf_MMTFDecoder_to_mmtf_MMTFDecoder(tmp_item, tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_molsysmt_MolSys(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys import from_string_pdb_id as string_pdb_id_to_molsysmt_MolSys

    tmp_item, tmp_molecular_system = string_pdb_id_to_molsysmt_MolSys(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_molsysmt_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology import from_string_pdb_id as string_pdb_id_to_molsysmt_Topology

    tmp_item, tmp_molecular_system = string_pdb_id_to_molsysmt_Topology(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_molsysmt_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.trajectory import from_string_pdb_id as string_pdb_id_to_molsysmt_Trajectory

    tmp_item, tmp_molecular_system = string_pdb_id_to_molsysmt_Trajectory(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_mdtraj_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.files_and_directories import temp_filename
    from molsysmt.forms.api_file_pdb import to_mdtraj_Trajectory as file_pdb_to_mdtraj_Trajectory
    from os import remove

    temp_filename = temp_filename(extension='pdb')
    tmp_item, tmp_molecular_system = to_file_pdb(item, molecular_system=molecular_system, output_filename=temp_filename)
    tmp_item, tmp_molecular_system = file_pdb_to_mdtraj_Trajectory(tmp_item, molecular_system=tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(temp_filename)

    return tmp_item, tmp_molecular_system

def to_mdtraj_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.files_and_directories import temp_filename
    from molsysmt.forms.api_file_pdb import to_mdtraj_Topology as file_pdb_to_mdtraj_Topology
    from os import remove

    temp_filename = temp_filename(extension='pdb')
    tmp_item, tmp_molecular_system = to_file_pdb(item, molecular_system, output_filename=temp_filename)
    tmp_item, tmp_molecular_system = file_pdb_to_mdtraj_Topology(tmp_item, tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(temp_filename)

    return tmp_item, tmp_molecular_system

def to_parmed_Structure(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.files_and_directories import temp_filename
    from molsysmt.forms.api_file_pdb import to_parmed_Structure as file_pdb_to_parmed_Structure
    from os import remove

    temp_filename = temp_filename(extension='pdb')
    tmp_item, tmp_molecular_system = to_file_pdb(item, molecular_system=molecular_system, output_filename=temp_filename)
    tmp_item, tmp_molecular_system = file_pdb_to_parmed_Structure(tmp_item, molecular_system=tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(temp_filename)

    return tmp_item, tmp_molecular_system

def to_pdbfixer_PDBFixer(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.files_and_directories import temp_filename
    from molsysmt.forms.api_file_pdb import to_pdbfixer_PDBFixer as file_pdb_to_pdbfixer_PDBFixer
    from os import remove

    temp_filename = temp_filename(extension='pdb')
    tmp_item, tmp_molecular_system = to_file_pdb(item, molecular_system=molecular_system, output_filename=temp_filename)
    tmp_item, tmp_molecular_system = file_pdb_to_pdbfixer_PDBFixer(tmp_item, molecular_system=tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(temp_filename)

    return tmp_item, tmp_molecular_system

def to_openmm_Modeller(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.files_and_directories import temp_filename
    from molsysmt.forms.api_file_pdb import to_openmm_Modeller as file_pdb_to_openmm_Modeller
    from os import remove

    temp_filename = temp_filename(extension='pdb')
    tmp_item, tmp_molecular_system = to_file_pdb(item, molecular_system=molecular_system, output_filename=temp_filename)
    tmp_item, tmp_molecular_system = file_pdb_to_openmm_Modeller(tmp_item, molecular_system=tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(temp_filename)

    return tmp_item, tmp_molecular_system

def to_openmm_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.files_and_directories import temp_filename
    from molsysmt.forms.api_file_pdb import to_openmm_Topology as file_pdb_to_openmm_Topology
    from os import remove

    temp_filename = temp_filename(extension='pdb')
    tmp_item, tmp_molecular_system = to_file_pdb(item, molecular_system=molecular_system, output_filename=temp_filename)
    tmp_item, tmp_molecular_system = file_pdb_to_openmm_Topology(tmp_item, molecular_system=tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(temp_filename)

    return tmp_item, tmp_molecular_system

def to_openmm_PDBFile(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.files_and_directories import temp_filename
    from molsysmt.forms.api_file_pdb import to_openmm_PDBFile as pdb_to_openmm_PDBFile
    from os import remove

    temp_filename = temp_filename(extension='pdb')
    tmp_item, tmp_molecular_system = to_file_pdb(item, molecular_system=molecular_system, output_filename=temp_filename)
    tmp_item, tmp_molecular_system = pdb_to_openmm_PDBFile(tmp_item, molecular_system=tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(temp_file)

    return tmp_item, tmp_molecular_system

def to_mdanalysis_Universe(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.files_and_directories import temp_filename
    from molsysmt.forms.api_file_pdb import to_mdanalysis_Universe as file_pdb_mdanalysis_Universe
    from os import remove

    temp_filename = temp_filename(extension='pdb')
    tmp_item, tmp_molecular_system = to_file_pdb(item, molecular_system=molecular_system, output_filename=temp_filename)
    tmp_item, tmp_molecular_system = file_pdb_to_mdanalysis_Universe(tmp_item, molecular_system=tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(temp_filename)

    return tmp_item, tmp_molecular_system

def to_pytraj_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.files_and_directories import temp_filename
    from molsysmt.forms.api_file_pdb import to_pytraj_Trajectory as file_pdb_pytraj_Trajectory
    from os import remove

    temp_filename = temp_filename(extension='pdb')
    tmp_item, tmp_molecular_system = to_file_pdb(item, molecular_system=molecular_system, output_filename=temp_filename)
    tmp_item, tmp_molecular_system = file_pdb_to_pytraj_Trajectory(tmp_item, molecular_system=tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(temp_filename)

    return tmp_item, tmp_molecular_system

def to_nglview_NGLWidget(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.files_and_directories import temp_filename
    from nglview import show_file as nglview_show_file
    from os import remove

    temp_filename = temp_filename(extension='pdb')
    tmp_item, _ = to_file_pdb(item, molecular_system=molecular_system, output_filename=temp_filename, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = nglview_show_file(temp_filename)
    remove(temp_filename)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_string_pdb_id(item, molecular_system=None, atom_indices='all', frame_indices='all', copy_if_all=True):

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
        raise NotImplementedError()
    else:
        raise NotImplementedError()

    return tmp_item

def merge(item_1, item_2):

    raise NotImplementedError

def add(to_item, item):

    raise NotImplementedError

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError()

def concatenate_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

###### Get

def aux_get(item, indices='all', frame_indices='all'):

    from molsysmt.forms import forms

    method_name = sys._getframe(1).f_code.co_name

    if 'mmtf.MMTFDecoder' in forms:

        tmp_item, _ = to_mmtf_MMTFDecoder(item)
        module = importlib.import_module('molsysmt.forms.api_mmtf_MMTFDecoder')
        _get = getattr(module, method_name)
        output = _get(tmp_item, indices=indices, frame_indices=frame_indices)

    elif 'openmm.PDBFile' in forms:

        tmp_item, _ = to_openmm_PDBFile(item)
        module = importlib.import_module('molsysmt.forms.api_openmm_PDBFile')
        _get = getattr(module, method_name)
        output = _get(tmp_item, indices=indices, frame_indices=frame_indices)

    elif 'pdbfixer.PDBFixer' in forms:

        tmp_item, _ = to_pdbfixer_PDBFixer(item)
        module = importlib.import_module('molsysmt.forms.api_pdbfixer_PDBFixer')
        _get = getattr(module, method_name)
        output = _get(tmp_item, indices=indices, frame_indices=frame_indices)

    elif 'mdtraj.PDBTrajectoryFile' in forms:

        tmp_item, _ = to_mdtraj_PDBTrajectoryFile(item)
        module = importlib.import_module('molsysmt.forms.api_mdtraj_PDBTrajectoryFile')
        _get = getattr(module, method_name)
        output = _get(tmp_item, indices=indices, frame_indices=frame_indices)

    elif 'molsysmt.Topology' in forms:

        tmp_item, _ = to_molsysmt_Topology(item)
        module = importlib.import_module('molsysmt.forms.api_molsysmt_Topology')
        _get = getattr(module, method_name)
        output = _get(tmp_item, indices=indices, frame_indices=frame_indices)


    else:

        raise NotImplementedError()

    return output

## atom

def get_atom_index_from_atom(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

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

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_frame_from_atom(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

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

def get_coordinates_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_box_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_box_shape_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_box_lengths_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_box_angles_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_box_volume_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_time_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_step_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

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

    raise NotImplementedError()

def set_coordinates_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError()


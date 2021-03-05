import importlib
import numpy as np
import urllib
import sys
from shutil import move
from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *

form_name='pdb:id'

is_form = {
    'pdb:id': form_name,
    'PDB:id': form_name
    }

info=["",""]
with_topology=True
with_coordinates=True
with_box=True
with_bonds=False
with_parameters=False

def to_pdb(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):

    from molsysmt._private_tools.pdb import download_pdb
    from molsysmt.forms.files.api_pdb import extract as extract_pdb

    tmp_item = item.split(':')[-1]
    download_pdb(tmp_item, output_filename)
    if atom_indices is not 'all' or frame_indices is not 'all':
        _ = extract_pdb(output_filename, output_filename=output_filename, atom_indices=atom_indices, frame_indices=frame_indices)

    return output_filename

def to_fasta(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):

    from molsysmt.forms.files.api_fasta import extract as extract_fasta

    tmp_item = item.split(':')[-1]
    url = 'https://www.rcsb.org/pdb/download/downloadFastaFiles.do?structureIdList='+tmp_item+'&compressionType=uncompressed'
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    fasta_txt = response.read().decode('utf-8')
    with open(output_filename,'w') as f:
        f.write(fasta_txt)
    f.close()
    tmp_item = extract_fasta(output_filename, atom_indices=atom_indices,
            frame_indices=frame_indices)
    if tmp_item!=output_filename:
        move(tmp_item, output_filename)

    return tmp_item

def to_mmtf(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):

    from .api_mmtf import to_mmtf as mmtf_to_mmtf_file

    tmp_item = 'mmtf:'+item.split(':')[-1]
    tmp_item = mmtf_to_mmtf_file(tmp_item, output_filename=output_filename, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_mmtf_MMTFDecoder(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from .api_mmtf import to_mmtf_MMTFDecoder as mmtf_to_mmtf_MMTFDecoder

    tmp_item = 'mmtf:'+item.split(':')[-1]
    tmp_item = mmtf_to_mmtf_MMTFDecoder(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_molsysmt_MolSys(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.files_and_directories import tmp_filename
    from molsysmt.native.io.molsys.files import from_pdb as pdb_to_molsysmt
    from os import remove

    tmp_filename = tmp_filename(extension='pdb')
    _ = to_pdb(item, output_filename=tmp_filename)
    tmp_item=pdb_to_molsysmt(tmp_filename, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(tmp_filename)

    return tmp_item

def to_mdtraj_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.files_and_directories import tmp_filename
    from molsysmt.forms.files.api_pdb import to_mdtraj_Trajectory as pdb_to_mdtraj_Trajectory
    from os import remove

    tmp_filename = tmp_filename(extension='pdb')
    _ = to_pdb(item, output_filename=tmp_filename)
    tmp_item=pdb_to_mdtraj_Trajectory(tmp_filename, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(tmp_filename)

    return tmp_item

def to_mdtraj_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.files_and_directories import tmp_filename
    from molsysmt.forms.files.api_pdb import to_mdtraj_Topology as pdb_to_mdtraj_Topology
    from os import remove

    tmp_filename = tmp_filename(extension='pdb')
    _ = to_pdb(item, output_filename=tmp_filename)
    tmp_item=pdb_to_mdtraj_Topology(tmp_filename, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(tmp_filename)

    return tmp_item

def to_parmed_Structure(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.files_and_directories import tmp_filename
    from molsysmt.forms.files.api_pdb import to_parmed_Structure as pdb_to_parmed_Structure
    from os import remove

    tmp_filename = tmp_filename(extension='pdb')
    _ = to_pdb(item, output_filename=tmp_filename)
    tmp_item=pdb_to_parmed_Structure(tmp_filename, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(tmp_filename)

    return tmp_item

def to_pdbfixer_PDBFixer(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.files_and_directories import tmp_filename
    from molsysmt.forms.files.api_pdb import to_pdbfixer_PDBFixer as pdb_to_pdbfixer_PDBFixer
    from os import remove

    tmp_filename = tmp_filename(extension='pdb')
    to_pdb(item, output_filename=tmp_filename)
    tmp_item=pdb_to_pdbfixer_PDBFixer(tmp_filename, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(tmp_filename)

    return tmp_item

def to_openmm_Modeller(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.files_and_directories import tmp_filename
    from molsysmt.forms.files.api_pdb import to_openmm_Modeller as pdb_to_openmm_Modeller
    from os import remove

    tmp_filename = tmp_filename(extension='pdb')
    _ = to_pdb(item, output_filename=tmp_filename)
    tmp_item=pdb_to_openmm_Modeller(tmp_filename, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(tmp_filename)

    return tmp_item

def to_openmm_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.files_and_directories import tmp_filename
    from molsysmt.forms.files.api_pdb import to_openmm_Topology as pdb_to_openmm_Topology
    from os import remove

    tmp_filename = tmp_filename(extension='pdb')
    to_pdb(item, output_filename=tmp_filename)
    tmp_item=pdb_to_openmm_Topology(tmp_filename, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(tmp_filename)

    return tmp_item

def to_openmm_PDBFile(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.files_and_directories import tmp_filename
    from molsysmt.forms.files.api_pdb import to_openmm_PDBFile as pdb_to_openmm_PDBFile
    from os import remove

    tmp_filename = tmp_filename(extension='pdb')
    _ = to_pdb(item, output_filename=tmp_filename)
    tmp_item=pdb_to_openmm_PDBFile(tmp_filename, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(tmp_file)

    return tmp_item

def to_yank_Topography(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.files_and_directories import tmp_filename
    from molsysmt.forms.files.api_pdb import to_yank_Topography as pdb_to_yank_Topography
    from os import remove

    tmp_filename = tmp_filename(extension='pdb')
    _ = to_pdb(item, output_filename=tmp_filename)
    tmp_item=pdb_to_yank_Topography(tmp_filename, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(tmp_filename)

    return tmp_item

def to_mdanalysis_Universe(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.files_and_directories import tmp_filename
    from molsysmt.forms.files.api_pdb import to_mdanalysis_Universe as pdb_mdanalysis_Universe
    from os import remove

    tmp_filename = tmp_filename(extension='pdb')
    _ = to_pdb(item, output_filename=tmp_filename)
    tmp_item=pdb_to_mdanalysis_Universe(tmp_filename, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(tmp_filename)

    return tmp_item

def to_pytraj_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.files_and_directories import tmp_filename
    from molsysmt.forms.files.api_pdb import to_pytraj_Trajectory as pdb_pytraj_Trajectory
    from os import remove

    tmp_filename = tmp_filename(extension='pdb')
    _ = to_pdb(item, output_filename=tmp_filename)
    tmp_item=pdb_to_pytraj_Trajectory(tmp_filename, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(tmp_filename)

    return tmp_item

def view_with_NGLView(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.files_and_directories import tmp_filename
    from nglview import show_file as nglview_show_file
    from os import remove

    tmp_filename = tmp_filename(extension='pdb')
    _ = to_pdb(item, output_filename=tmp_filename, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = nglview_show_file(tmp_filename)
    remove(tmp_filename)

    return tmp_item

def select_with_MDTraj(item, selection):

    tmp_form=to_mdtraj(item)
    tmp_sel=tmp_form.topology.select(selection)
    del(tmp_form)
    return tmp_sel

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

def merge(list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def concatenate_frames(list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def add(item, list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def append_frames(item, list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError


###### Get

def aux_get(item, indices='all', frame_indices='all'):

    from molsysmt.forms import forms

    if 'openmm.PDBFile' in forms:

        tmp_item = to_openmm_PDBFile(item)
        method_name = sys._getframe(1).f_code.co_name
        module = importlib.import_module('molsysmt.forms.classes.api_openmm_PDBFile')
        _get = getattr(module, method_name)
        output = _get(tmp_item, indices=indices, frame_indices=frame_indices)

    elif 'pdbfixer.PDBFixer' in forms:

        tmp_item = to_pdbfixer_PDBFixer(item)
        method_name = sys._getframe(1).f_code.co_name
        module = importlib.import_module('molsysmt.forms.classes.api_pdbfixer_PDBFixer')
        _get = getattr(module, method_name)
        output = _get(tmp_item, indices=indices, frame_indices=frame_indices)

    elif 'mdtraj.PDBTrajectoryFile' in forms:

        tmp_item = to_mdtraj_PDBTrajectoryFile(item)
        method_name = sys._getframe(1).f_code.co_name
        module = importlib.import_module('molsysmt.forms.classes.api_mdtraj_PDBTrajectoryFile')
        _get = getattr(module, method_name)
        output = _get(tmp_item, indices=indices, frame_indices=frame_indices)

    else:

        raise NotImplementedError

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

def get_has_topology_from_system(item, indices='all', frame_indices='all'):

    return with_topology

def get_has_parameters_from_system(item, indices='all', frame_indices='all'):

    return with_parameters

def get_has_coordinates_from_system(item, indices='all', frame_indices='all'):

    return with_coordinates

def get_has_box_from_system(item, indices='all', frame_indices='all'):

    return with_box

def get_has_bonds_from_system(item, indices='all', frame_indices='all'):

    return with_bonds

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


from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np
import urllib as _urllib
import json as _json

form_name='pdb:id'

is_form = {
    'pdb:id': form_name,
    'PDB:id': form_name
    }

info=["",""]
with_topology=True
with_trajectory=True
with_coordinates=True
with_box=True
with_bonds=False
with_parameters=False

def to_pdb(item, molecular_system, atom_indices='all', frame_indices='all', output_filename=None):

    from molsysmt._private_tools.miscellanea import download_pdb as download_pdb
    from molsysmt.forms.files.api_pdb import extract as extract_pdb
    from shutil import move

    tmp_item = item.split(':')[-1]
    download_pdb(tmp_item, output_filename)
    if atom_indices is not 'all' or frame_indices is not 'all':
        _ = extract_pdb(output_filename, output_filename=output_filename, atom_indices=atom_indices, frame_indices=frame_indices)

    return output_filename

def to_fasta(item, molecular_system, atom_indices='all', frame_indices='all', output_filename=None):

    from shutil import move
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

def to_mmtf(item, molecular_system, atom_indices='all', frame_indices='all', output_filename=None):

    from .api_mmtf import to_mmtf as mmtf_to_mmtf_file

    tmp_item = 'mmtf:'+item.split(':')[-1]
    tmp_item = mmtf_to_mmtf_file(tmp_item, output_filename=output_filename, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_mmtf_MMTFDecoder(item, molecular_system, atom_indices='all', frame_indices='all'):

    from .api_mmtf import to_mmtf_MMTFDecoder as mmtf_to_mmtf_MMTFDecoder

    tmp_item = 'mmtf:'+item.split(':')[-1]
    tmp_item = mmtf_to_mmtf_MMTFDecoder(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.pdb import tmp_pdb_filename
    from molsysmt.native.io.molsys.files import from_pdb as pdb_to_molsysmt
    from os import remove

    tmp_file = tmp_pdb_filename()
    to_pdb(item, output_filename=tmp_file)
    tmp_item=pdb_to_molsysmt(tmp_file, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(tmp_file)

    return tmp_item

def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.pdb import tmp_pdb_filename
    from molsysmt.forms.files.api_pdb import to_mdtraj_Trajectory as pdb_to_mdtraj_Trajectory
    from os import remove

    tmp_file = tmp_pdb_filename()
    to_pdb(item, output_filename=tmp_file)
    tmp_item=pdb_to_mdtraj_Trajectory(tmp_file, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(tmp_file)

    return tmp_item

def to_mdtraj_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.pdb import tmp_pdb_filename
    from molsysmt.forms.files.api_pdb import to_mdtraj_Topology as pdb_to_mdtraj_Topology
    from os import remove

    tmp_file = tmp_pdb_filename()
    to_pdb(item, output_filename=tmp_file)
    tmp_item=pdb_to_mdtraj_Topology(tmp_file, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(tmp_file)

    return tmp_item

def to_parmed_Structure(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.pdb import tmp_pdb_filename
    from molsysmt.forms.files.api_pdb import to_parmed_Structure as pdb_to_parmed_Structure
    from os import remove

    tmp_file = tmp_pdb_filename()
    to_pdb(item, output_filename=tmp_file)
    tmp_item=pdb_to_parmed_Structure(tmp_file, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(tmp_file)

    return tmp_item

def to_pdbfixer_PDBFixer(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.pdb import tmp_pdb_filename
    from molsysmt.forms.files.api_pdb import to_pdbfixer_PDBFixer as pdb_to_pdbfixer_PDBFixer
    from os import remove

    tmp_file = tmp_pdb_filename()
    to_pdb(item, output_filename=tmp_file)
    tmp_item=pdb_to_pdbfixer_PDBFixer(tmp_file, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(tmp_file)

    return tmp_item

def to_openmm_Modeller(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.pdb import tmp_pdb_filename
    from molsysmt.forms.files.api_pdb import to_openmm_Modeller as pdb_to_openmm_Modeller
    from os import remove

    tmp_file = tmp_pdb_filename()
    to_pdb(item, output_filename=tmp_file)
    tmp_item=pdb_to_openmm_Modeller(tmp_file, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(tmp_file)

    return tmp_item

def to_openmm_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.pdb import tmp_pdb_filename
    from molsysmt.forms.files.api_pdb import to_openmm_Topology as pdb_to_openmm_Topology
    from os import remove

    tmp_file = tmp_pdb_filename()
    to_pdb(item, output_filename=tmp_file)
    tmp_item=pdb_to_openmm_Topology(tmp_file, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(tmp_file)

    return tmp_item

def to_openmm_PDBFile(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.pdb import tmp_pdb_filename
    from molsysmt.forms.files.api_pdb import to_openmm_PDBFile as pdb_to_openmm_PDBFile
    from os import remove

    tmp_file = tmp_pdb_filename()
    to_pdb(item, output_filename=tmp_file)
    tmp_item=pdb_to_openmm_PDBFile(tmp_file, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(tmp_file)

    return tmp_item

def to_yank_Topography(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.pdb import tmp_pdb_filename
    from molsysmt.forms.files.api_pdb import to_yank_Topography as pdb_to_yank_Topography
    from os import remove

    tmp_file = tmp_pdb_filename()
    to_pdb(item, output_filename=tmp_file)
    tmp_item=pdb_to_yank_Topography(tmp_file, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(tmp_file)

    return tmp_item

def to_mdanalysis_Universe(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.pdb import tmp_pdb_filename
    from molsysmt.forms.files.api_pdb import to_mdanalysis_Universe as pdb_mdanalysis_Universe
    from os import remove

    tmp_file = tmp_pdb_filename()
    to_pdb(item, output_filename=tmp_file)
    tmp_item=pdb_to_mdanalysis_Universe(tmp_file, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(tmp_file)

    return tmp_item

def to_pytraj_Trajectory(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.pdb import tmp_pdb_filename
    from molsysmt.forms.files.api_pdb import to_pytraj_Trajectory as pdb_pytraj_Trajectory
    from os import remove

    tmp_file = tmp_pdb_filename()
    to_pdb(item, output_filename=tmp_file)
    tmp_item=pdb_to_pytraj_Trajectory(tmp_file, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(tmp_file)

    return tmp_item

def view_with_NGLView(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.pdb import tmp_pdb_filename
    from nglview import show_file as nglview_show_file
    from os import remove

    tmp_file = tmp_pdb_filename()
    to_pdb(item, output_filename=tmp_file, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = nglview_show_file(tmp_file)
    remove(tmp_file)

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

def concatenate(list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def add(item, list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def append(item, list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

###### Get

def get_index_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_id_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_id_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_name_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_name_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_type_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_type_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_index_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_id_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_name_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_type_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_index_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_id_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_id_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_name_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_name_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_type_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_type_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_name_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_name_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_index_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_id_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_id_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_type_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_type_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_name_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_index_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_id_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_type_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_index_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_id_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_name_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_type_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_index_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_id_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_name_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_type_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_bonded_atoms_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_atoms_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_groups_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_components_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_molecules_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_chains_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_entities_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_bonds_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_mass_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_mass_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_charge_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_charge_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_frames_from_atom(item, indices='all', frame_indices='all'):

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

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_index_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_id_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_name_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_type_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_index_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_index_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_id_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_id_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_name_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_name_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_type_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_type_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_name_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_name_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_index_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_index_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_id_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_id_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_type_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_type_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_name_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_index_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_id_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_type_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_index_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_id_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_name_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_type_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_index_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_id_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_name_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_type_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_atoms_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_groups_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_components_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_molecules_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_chains_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_entities_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_bonds_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_mass_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_mass_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_charge_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_charge_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_group(item, indices='all', frame_indices='all'):

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

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_index_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_id_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_name_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_type_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_index_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_index_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_id_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_id_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_name_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_name_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_type_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_type_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_name_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_name_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_index_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_index_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_id_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_id_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_type_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_type_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_name_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_index_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_id_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_type_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_index_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_id_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_name_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_type_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_index_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_id_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_name_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_type_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_atoms_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_groups_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_components_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_molecules_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_chains_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_entities_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_bonds_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_mass_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_mass_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_charge_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_charge_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_component(item, indices='all', frame_indices='all'):

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

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_index_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_id_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_name_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_type_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_index_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_index_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_id_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_id_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_name_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_name_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_type_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_type_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_name_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_name_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_index_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_index_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_id_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_id_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_type_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_type_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_name_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_index_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_id_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_type_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_index_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_id_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_name_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_type_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_index_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_id_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_name_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_type_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_atoms_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_groups_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_components_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_molecules_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_chains_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_entities_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_bonds_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_mass_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_mass_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_charge_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_charge_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_molecule(item, indices='all', frame_indices='all'):

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

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_index_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_id_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_name_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_type_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_index_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_index_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_id_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_id_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_name_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_name_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_type_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_type_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_name_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_name_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_index_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_index_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_id_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_id_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_type_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_type_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_name_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_index_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_id_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_type_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_index_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_id_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_name_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_type_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_index_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_id_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_name_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_type_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_atoms_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_groups_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_components_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_molecules_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_chains_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_entities_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_bonds_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_mass_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_mass_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_charge_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_charge_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_chain(item, indices='all', frame_indices='all'):

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

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_index_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_id_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_name_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_type_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_index_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_index_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_id_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_id_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_name_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_name_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_type_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_type_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_name_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_name_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_index_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_index_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_id_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_id_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_type_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_type_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_name_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_index_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_id_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_type_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_index_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_id_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_name_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_type_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_index_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_id_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_name_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_type_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_atoms_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_groups_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_components_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_molecules_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_chains_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_entities_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_bonds_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_mass_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_mass_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_charge_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_charge_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## system

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_bonded_atoms_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_atoms_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_groups_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_components_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_chains_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_molecules_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_entities_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_bonds_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_aminoacids_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_aminoacids_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_nucleotides_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_nucleotides_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_ions_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_ions_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_waters_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_waters_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_cosolutes_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_cosolutes_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_small_molecules_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_small_molecules_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_peptides_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_peptides_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_proteins_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_proteins_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_dnas_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_dnas_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_rnas_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_rnas_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_mass_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_mass_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_charge_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_charge_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_shape_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_lengths_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_angles_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_time_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name


from os.path import basename as _basename
import urllib as _urllib
import json as _json

form_name=_basename(__file__).split('.')[0][4:]+':id'

is_form = {
    'pdb:id': form_name,
    'PDB:id': form_name
    }

def to_pdb(item, output_file_path=None, atom_indices='all', frame_indices='all'):

    from molmodmt.utils.miscellanea import download_pdb as download_pdb
    from molmodmt.forms.files.api_pdb import extract_subsystem as extract_pdb
    from shutil import move
    tmp_item = item.split(':')[-1]
    download_pdb(tmp_item, output_file_path)
    tmp_item = extract_pdb(output_file_path, atom_indices=atom_indices, frame_indices=frame_indices)
    if tmp_item!=output_file_path:
        move(tmp_item, output_file_path)
    pass

def to_fasta(item, output_file_path=None, atom_indices='all', frame_indices='all'):

    from shutil import move
    from molmodmt.forms.files.api_fasta import extract_subsystem as extract_fasta
    tmp_item = item.split(':')[-1]
    url = 'https://www.rcsb.org/pdb/download/downloadFastaFiles.do?structureIdList='+tmp_item+'&compressionType=uncompressed'
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    fasta_txt = response.read().decode('utf-8')
    with open(output_file_path,'w') as f:
        f.write(fasta_txt)
    f.close()
    tmp_item = extract_fasta(output_file_path, atom_indices=atom_indices,
            frame_indices=frame_indices)
    if tmp_item!=output_file_path:
        move(tmp_item, output_file_path)
    pass

def to_mmtf(item, output_file_path=None, atom_indices='all', frame_indices='all'):

    from mmtf import fetch
    from molmodmt.forms.classes.api_mmtf_MMTFDecoder import to_mmtf as MMTFDecoder_to_mmtf

    tmp_item = to_mmtf_MMTFDecoder(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return MMTFDecoder_to_mmtf(tmp_item, output_file_path=output_file_path)

def to_mmtf_MMTFDecoder(item, atom_indices='all', frame_indices='all'):

    from mmtf import fetch
    from molmodmt.forms.classes.api_mmtf_MMTFDecoder import extract_subsystem as extract_MMTFDecoder
    tmp_item = item.split(':')[-1]
    tmp_item = fetch(tmp_item)
    tmp_item = extract_MMTFDecoder(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_molmodmt_MolMod(item, atom_indices='all', frame_indices='all'):

    from molmodmt.utils.pdb import tmp_pdb_filename
    from molmodmt.native.io_molmod import from_pdb as pdb_to_molmodmt
    from os import remove
    tmp_file = tmp_pdb_filename()
    to_pdb(item, output_file_path=tmp_file)
    tmp_item=pdb_to_molmodmt(tmp_file, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(tmp_file)
    return tmp_item

def to_mdtraj_Trajectory(item, atom_indices='all', frame_indices='all'):

    from molmodmt.utils.pdb import tmp_pdb_filename
    from molmodmt.forms.files.api_pdb import to_mdtraj_Trajectory as pdb_to_mdtraj_Trajectory
    from os import remove
    tmp_file = tmp_pdb_filename()
    to_pdb(item, output_file_path=tmp_file)
    tmp_item=pdb_to_mdtraj_Trajectory(tmp_file, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(tmp_file)
    return tmp_item

def to_mdtraj_Topology(item, atom_indices='all', frame_indices='all'):

    from molmodmt.utils.pdb import tmp_pdb_filename
    from molmodmt.forms.files.api_pdb import to_mdtraj_Topology as pdb_to_mdtraj_Topology
    from os import remove
    tmp_file = tmp_pdb_filename()
    to_pdb(item, output_file_path=tmp_file)
    tmp_item=pdb_to_mdtraj_Topology(tmp_file, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(tmp_file)
    return tmp_item

def to_parmed_Structure(item, atom_indices='all', frame_indices='all'):

    from molmodmt.utils.pdb import tmp_pdb_filename
    from molmodmt.forms.files.api_pdb import to_parmed_Structure as pdb_to_parmed_Structure
    from os import remove
    tmp_file = tmp_pdb_filename()
    to_pdb(item, output_file_path=tmp_file)
    tmp_item=pdb_to_parmed_Structure(tmp_file, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(tmp_file)
    return tmp_item

def to_pdbfixer_PDBFixer(item, atom_indices='all', frame_indices='all'):

    from molmodmt.utils.pdb import tmp_pdb_filename
    from molmodmt.forms.files.api_pdb import to_pdbfixer_PDBFixer as pdb_to_pdbfixer_PDBFixer
    from os import remove
    tmp_file = tmp_pdb_filename()
    to_pdb(item, output_file_path=tmp_file)
    tmp_item=pdb_to_pdbfixer_PDBFixer(tmp_file, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(tmp_file)
    return tmp_item

def to_openmm_Modeller(item, atom_indices='all', frame_indices='all'):

    from molmodmt.utils.pdb import tmp_pdb_filename
    from molmodmt.forms.files.api_pdb import to_openmm_Modeller as pdb_to_openmm_Modeller
    from os import remove
    tmp_file = tmp_pdb_filename()
    to_pdb(item, output_file_path=tmp_file)
    tmp_item=pdb_to_openmm_Modeller(tmp_file, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(tmp_file)
    return tmp_item

def to_yank_Topography(item, atom_indices='all', frame_indices='all'):

    from molmodmt.utils.pdb import tmp_pdb_filename
    from molmodmt.forms.files.api_pdb import to_yank_Topography as pdb_to_yank_Topography
    from os import remove
    tmp_file = tmp_pdb_filename()
    to_pdb(item, output_file_path=tmp_file)
    tmp_item=pdb_to_yank_Topography(tmp_file, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(tmp_file)
    return tmp_item


def to_mdanalysis_Universe(item, atom_indices='all', frame_indices='all'):

    from molmodmt.utils.pdb import tmp_pdb_filename
    from molmodmt.forms.files.api_pdb import to_mdanalysis_Universe as pdb_mdanalysis_Universe
    from os import remove
    tmp_file = tmp_pdb_filename()
    to_pdb(item, output_file_path=tmp_file)
    tmp_item=pdb_to_mdanalysis_Universe(tmp_file, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(tmp_file)
    return tmp_item

def to_pytraj_Trajectory(item, atom_indices='all', frame_indices='all'):

    from molmodmt.utils.pdb import tmp_pdb_filename
    from molmodmt.forms.files.api_pdb import to_pytraj_Trajectory as pdb_pytraj_Trajectory
    from os import remove
    tmp_file = tmp_pdb_filename()
    to_pdb(item, output_file_path=tmp_file)
    tmp_item=pdb_to_pytraj_Trajectory(tmp_file, atom_indices=atom_indices, frame_indices=frame_indices)
    remove(tmp_file)
    return tmp_item

def to_nglview(item, atom_indices='all', frame_indices='all'):

    from molmodmt.utils.pdb import tmp_pdb_filename
    from nglview import show_file as nglview_show_file
    from os import remove
    tmp_file = tmp_pdb_filename()
    to_pdb(item, output_file_path=tmp_file, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = nglview_show_file(tmp_file)
    remove(tmp_file)
    return tmp_item

def select_with_MDTraj(item, selection):
    tmp_form=to_mdtraj(item)
    tmp_sel=tmp_form.topology.select(selection)
    del(tmp_form)
    return tmp_sel

def extract_subsystem(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def duplicate(item):

    raise NotImplementedError

###### Get

## system

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    tmp_item = to_mmtf_MMTFDecoder(item)
    return tmp_item.num_atoms

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    tmp_item = to_mmtf_MMTFDecoder(item)
    return tmp_item.num_models

def get_form_from_system(item, indices='all', frame_indices='all'):

    from molmodmt import get_form
    return get_form(item)


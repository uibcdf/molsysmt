from os.path import basename as _basename
import urllib as _urllib
import json as _json

form_name=_basename(__file__).split('.')[0][4:]+':id'

is_form = {
    'mmtf:id': form_name,
    'MMTF:id': form_name
    }

def to_pdb(item, output_file_path=None, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def to_fasta(item, output_file_path=None, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

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

    raise NotImplementedError

def to_mdtraj_Trajectory(item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def to_mdtraj_Topology(item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def to_parmed_Structure(item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def to_pdbfixer_PDBFixer(item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def to_openmm_Modeller(item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def to_mdanalysis_Universe(item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def to_pytraj_Trajectory(item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def to_nglview(item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def select_with_MDTraj(item, selection):

    raise NotImplementedError

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


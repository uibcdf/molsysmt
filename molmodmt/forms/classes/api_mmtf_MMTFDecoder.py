from os.path import basename as _basename
from mmtf import MMTFDecoder as _mmtf_MMTFDecoder

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _mmtf_MMTFDecoder : form_name,
    'mmtf.MMTFDecoder' : form_name
}

def to_mdtraj_Topology(item, indices=None, frame_indices=None):

    from mdtraj import load_topology as _mdtraj_load_topology

    return _mdtraj_load_topology(item)

def to_mdtraj_Trajectory(item, indices=None, frame_indices=None):

    pass

def to_mmtf(item, output_file_path=None, atom_indices=None, frame_indices=None):

    from mmtf.api.default_api import write_mmtf, MMTFDecoder

    return write_mmtf(output_file_path, item, MMTFDecoder.pass_data_on)

###### Get

## atom

## system

def get_n_atoms_from_system (item, indices=None, frame_indices=None):

    return item.num_atoms

def get_n_frames_from_system(item, indices=None, frame_indices=None):

    return item.num_models

def get_form_from_system(item, indices=None, frame_indices=None):

    from molmodmt import get_form
    return get_form(item)




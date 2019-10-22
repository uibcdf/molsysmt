from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'mmtf': form_name
    }


def to_mmtf_MMTFDecoder(item, filename=None, atom_indices=None, frame_indices=None):

    from mmtf import parse
    return parse(filename)

# System

def get_n_frames_from_system (item, indices=None, frame_indices=None):

    from mmtf import parse
    tmp_item=parse(filename)
    n_frames = tmp_item.num_models
    del(tmp_item)
    return n_frames

def get_n_atoms_from_system (item, indices=None, frame_indices=None):

    from mmtf import parse
    tmp_item=parse(filename)
    n_atoms = tmp_item.num_atoms
    del(tmp_item)
    return n_atoms

def get_form_from_system(item, indices=None, frame_indices=None):

    from molmodmt import _get_form
    return _get_form(item)


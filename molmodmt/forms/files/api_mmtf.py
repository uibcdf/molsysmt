from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'mmtf': form_name
    }


def extract_subsystem(item, atom_indices=None, frame_indices=None):

    if (atom_indices is None) and (frame_indices is None):
        return item
    else:
        raise NotImplementedError

def duplicate(item):

    raise NotImplementedError

def to_mmtf_MMTFDecoder(item, filename=None, atom_indices=None, frame_indices=None):

    from mmtf import parse
    return parse(filename)

##### Get

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

    from molmodmt import get_form
    return get_form(item)


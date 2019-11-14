from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'mmtf': form_name
    }


def extract_subsystem(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def duplicate(item):

    raise NotImplementedError

def to_mmtf_MMTFDecoder(item, atom_indices='all', frame_indices='all'):

    from molmodmt.forms.classes.api_mmtf_MMTFDecoder import extract_subsystem as extract_mmtf_MMTFDecoder
    from mmtf import parse
    tmp_item = parse(output_file_path)
    tmp_item = extract_mmtf_MMTFDecoder(tmp_item, atom_indices='all', frame_indices='all')
    return tmp_item

##### Get

# System

def get_n_frames_from_system (item, indices='all', frame_indices='all'):

    from mmtf import parse
    tmp_item=parse(filename)
    n_frames = tmp_item.num_models
    del(tmp_item)
    return n_frames

def get_n_atoms_from_system (item, indices='all', frame_indices='all'):

    from mmtf import parse
    tmp_item=parse(filename)
    n_atoms = tmp_item.num_atoms
    del(tmp_item)
    return n_atoms

def get_form_from_system(item, indices='all', frame_indices='all'):

    from molmodmt import get_form
    return get_form(item)


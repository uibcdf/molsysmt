from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'dcd': form_name,
    'DCD': form_name
    }

def to_mdtraj_Trajectory(item, topology=None, atom_indices=None, frame_indices=None):

    if not topology:
        raise ValueError('"topology" argument is required to convert a dcd file to mdtraj_Trajectory')

    from molmodmt import convert
    from mdtraj import load_dcd as mdtraj_load_dcd
    from molmodmt.forms.classes.api_mdtraj_Trajectory import extract_subsystem as extract_mdtraj_Trajectory
    tmp_topology = convert(topology, to_form='mdtraj.Topology')
    tmp_item = mdtraj_load_dcd(item, top=tmp_topology)
    tmp_item = extract_mdtraj_Trajectory(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_mdanalysis_Universe(item, topology=None, atom_indices=None, frame_indices=None):

    if not topology:
        raise ValueError('"topology" argument is required for dcd.to_mdtraj')

    raise NotImplementedError

def extract_subsystem(item, atom_indices=None, frame_indices=None):

    if (atom_indices is None) and (frame_indices is None):
        return item
    else:
        raise NotImplementedError

def duplicate(item):

    raise NotImplementedError

###### Get

## system

def get_form_from_system(item, indices=None, frame_indices=None):

    from molmodmt import get_form
    return get_form(item)


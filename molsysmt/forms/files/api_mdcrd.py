from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'mdcrd': form_name
    }

info=["",""]
with_topology=False
with_trajectory=True
with_coordinates=True
with_box=True

info = ["AMBER mdcrd file format","https://ambermd.org/FileFormats.php#trajectory"]

def to_molsysmt_MolSys(item, atom_indices='all', frame_indices='all',
                       topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.native.io.molsys.files import from_mdcrd as mdcrd_to_molsysmt_MolSys
    tmp_item = mdcrd_to_molsysmt_MolSys(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_molsysmt_Topology(item, atom_indices='all', frame_indices='all',
                         topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.native.io.topology.files import from_mdcrd as mdcrd_to_molsysmt_Topology
    tmp_item = mdcrd_to_molsysmt_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_molsysmt_DataFrame(item, atom_indices='all', frame_indices='all',
                          topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.native.io.dataframe.files import from_mdcrd as mdcrd_to_molsysmt_DataFrame
    tmp_item = mdcrd_to_molsysmt_DataFrame(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_molsysmt_Trajectory(item, atom_indices='all', frame_indices='all',
                           topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.native.io.trajectory.files import from_mdcrd as mdcrd_to_molsysmt_Trajectory
    tmp_item = mdcrd_to_molsysmt_Trajectory(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def view_with_NGLView(item, atom_indices='all', frame_indices='all',
               topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    return NotImplementedError

def select_with_MDTraj(item, selection):

    return NotImplementedError

def select_with_MDTraj(item, selection):

    return NotImplementedError

def select_with_MolSysMT(item, selection):

    return NotImplementedError

def copy(item):

    return NotImplementedError

def extract(item, atom_indices='all', frame_indices='all'):

    return NotImplementedError

###### Get

# System

def get_n_frames_from_system (item, indices='all', frame_indices='all'):

    return NotImplementedError

def get_n_atoms_from_system (item, indices='all', frame_indices='all'):

    return NotImplementedError

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name


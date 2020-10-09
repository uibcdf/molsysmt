from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'inpcrd': form_name
    }

info=["",""]
with_topology=False
with_trajectory=True

info = ["AMBER ASCII restart/inpcrd file format","https://ambermd.org/FileFormats.php#trajectory"]

def to_inpcrd(item, output_filepath=None, trajectory_item=None, atom_indices='all', frame_indices='all'):

    if frame_indices=='all':
        from shutil import copyfile
        copyfile(item, output_filepath)
    else:
        raise NotImplementedError("Not implemented yet")

def to_molsysmt_MolSys(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.files import from_inpcrd as inpcrd_to_molsysmt_MolSys
    tmp_item = inpcrd_to_molsysmt_MolSys(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_molsysmt_Topology(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.files import from_inpcrd as inpcrd_to_molsysmt_Topology
    tmp_item = inpcrd_to_molsysmt_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_molsysmt_DataFrame(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.dataframe.files import from_inpcrd as inpcrd_to_molsysmt_DataFrame
    tmp_item = inpcrd_to_molsysmt_DataFrame(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_molsysmt_Trajectory(item, topology=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.trajectory.files import from_inpcrd as inpcrd_to_molsysmt_Trajectory
    tmp_item = inpcrd_to_molsysmt_Trajectory(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_parmed_Structure(item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def to_mdanalysis_Universe(item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def to_mdtraj_Topology(item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def to_mdtraj_Trajectory(item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def to_mdtraj_AmberRestartFile(item, atom_indices='all', frame_indices='all'):
    from mdtraj.formats import AmberRestartFile
    return AmberRestartFile(item)

def to_openmm_AmberInpcrdFile(item, atom_indices='all', frame_indices='all'):

    from simtk.openmm.app import AmberInpcrdFile
    return AmberInpcrdFile(item)

def to_openmm_Topology(item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def to_openmm_Modeller(item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def to_nglview(item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def to_yank_Topography(item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def select_with_MDTraj(item, selection):

    raise NotImplementedError

def select_with_MolSysMT(item, selection):

    raise NotImplementedError

def copy(item, output_filepath=None):

    from shutil import copy as copy_file
    from molsysmt.utils.files_and_directories import tmp_filename
    if output_filepath is None:
        output_filepath = tmp_filename(extension='inpcrd')
    copy_file(item, output_filepath)
    return output_filepath

def extract(item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

###### Get

# Atom

def get_coordinates_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mdtraj_AmberRestartFile import get_coordinates_from_atom as _get
    tmp_item = to_mdtraj_AmberRestartFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mdtraj_AmberRestartFile import get_n_atoms_from_atom as _get
    tmp_item = to_mdtraj_AmberRestartFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_form_from_atom(item, indices='all', frame_indices='all'):

    return get_form_from_system(item)

# System

def get_coordinates_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mdtraj_AmberRestartFile import get_coordinates_from_system as _get
    tmp_item = to_mdtraj_AmberRestartFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_frames_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mdtraj_AmberRestartFile import get_n_frames_from_system as _get
    tmp_item = to_mdtraj_AmberRestartFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_system (item, indices='all', frame_indices='all'):

    return get_n_atoms_from_atom(item)

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name


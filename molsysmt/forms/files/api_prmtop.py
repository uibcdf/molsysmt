from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'prmtop': form_name,
    'parm7': form_name
    }

info = ["AMBER  parameter/topology file format","https://ambermd.org/FileFormats.php#topology"]
with_topology=True
with_trajectory=False

def to_molsysmt_MolSys(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.files import from_prmtop as prmtop_to_molsysmt_MolSys
    tmp_item = prmtop_to_molsysmt_MolSys(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_molsysmt_Topology(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.files import from_prmtop as prmtop_to_molsysmt_Topology
    tmp_item = prmtop_to_molsysmt_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_molsysmt_DataFrame(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.dataframe.files import from_prmtop as prmtop_to_molsysmt_DataFrame
    tmp_item = prmtop_to_molsysmt_DataFrame(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_molsysmt_Trajectory(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.trajectory.files import from_prmtop as prmtop_to_molsysmt_Trajectory
    tmp_item = prmtop_to_molsysmt_Trajectory(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_parmed_Structure(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def to_mdanalysis_Universe(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def to_mdtraj_Topology(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from mdtraj import load_prmtop as prmtop_to_mdtraj_Topology
    return prmtop_to_mdtraj_Topology

def to_openmm_AmberPrmtopFile(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from simtk.openmm.app import AmberPrmtopFile
    return AmberPrmtopFile(item)

def to_openmm_Topology(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def to_openmm_Modeller(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def to_nglview(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def to_yank_Topography(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def select_with_MDTraj(item, selection):

    raise NotImplementedError

def select_with_MolSysMT(item, selection):

    raise NotImplementedError

def copy(item):

    raise NotImplementedError

def extract(item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

###### Get

def get_n_atoms_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mdtraj_Topology import get_n_atoms_from_system as _get
    tmp_item = to_mdtraj_Topology(item)
    return _get(temp_item, indices=indices, frame_indices=frame_indices)

def get_form_from_atom(item, indices='all', frame_indices='all'):

    return get_form_from_system(item)

# System

def get_n_frames_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mdtraj_Topology import get_n_frames_from_system as _get
    tmp_item = to_mdtraj_Topology(item)
    return _get(temp_item, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_system (item, indices='all', frame_indices='all'):

    return get_n_atoms_from_atom(item)

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name


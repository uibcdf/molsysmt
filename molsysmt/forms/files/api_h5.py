from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np

form_name='h5'

is_form = {
    'h5': form_name,
    'hdf5': form_name
    }

info=["",""]
with_topology=True
with_trajectory=True
with_coordinates=True
with_box=True
with_bonds=True
with_parameters=False

def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', frame_indices='all'):

    from mdtraj import load_hdf5 as mdtraj_load_hdf5

    tmp_item = mdtraj_load_hdf5(item)

    return tmp_item

def to_mdtraj_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

    tmp_item_aux = to_mdtraj_HDF5TrajectoryFile(item, molecular_system, atom_indices='all', frame_indices='all')
    tmp_item = tmp_item_aux.topology
    tmp_item_aux.close()
    del(tmp_item_aux)

    return tmp_item

def to_mdtraj_HDF5TrajectoryFile(item, molecular_system, atom_indices='all', frame_indices='all'):

    from mdtraj.formats import HDF5TrajectoryFile

    tmp_item = HDF5TrajectoryFile(item)

    return tmp_item

def to_openmm_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

    tmp_item = to_mdtraj_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = tmp_item.to_openmm()

    return tmp_item

def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.files import from_h5 as h5_to_molsysmt_MolSys

    tmp_item = h5_to_molsysmt_MolSys(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.files import from_h5 as h5_to_molsysmt_Topology

    tmp_item = h5_to_molsysmt_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_molsysmt_Trajectory(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.trajectory.files import from_h5 as h5_to_molsysmt_Trajectory

    tmp_item = h5_to_molsysmt_Trajectory(item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_pdb(item, molecular_system, atom_indices='all', frame_indices='all', output_filename=None):

    from molsysmt.forms.classes.api_molsysmt_MolSys import to_pdb as molsysmt_MolSys_to_pdb

    tmp_item = to_molsysmt_MolSys(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = molsysmt_MolSys_to_pdb(tmp_item, output_filename=output_filename)

    return tmp_item

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item, output_filename=None):

    from shutil import copyfile

    er=copyfile(item, output_filename)
    pass

def view_with_NGLView(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_MolSys import to_NGLView as molsysmt_MolSys_to_NGLView

    tmp_item = to_molsysmt_MolSys(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = molsysmt_MolSys_to_NGLView(tmp_item)

    return tmp_item

def merge(list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def concatenate(list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def add(item, list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def append(item, list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

#### Get

def get_frames_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt import get
    tmp_item = to_mdtraj_HDF5TrajectoryFile(item)
    xyz, time, step, box = get(tmp_item, target='atom', indices=indices,
                               frame_indices=frame_indices, frames=True)
    tmp_item.close()
    del(tmp_item, get)
    return xyz, time, step, box

# System

def get_frames_from_system (item, indices='all', frame_indices='all'):

    from molsysmt import get
    tmp_item = to_mdtraj_HDF5TrajectoryFile(item)
    xyz, time, step, box = get(tmp_item, target='system',
            frame_indices=frame_indices, frames=True)
    tmp_item.close()
    del(tmp_item, get)
    return xyz, time, step, box

def get_n_frames_from_system (item, indices='all', frame_indices='all'):

    from molsysmt import get
    tmp_item = to_mdtraj_HDF5TrajectoryFile(item)
    n_frames = get(tmp_item, target='system',  n_frames=True)
    tmp_item.close()
    del(tmp_item, get)
    return n_frames

def get_n_atoms_from_system (item, indices='all', frame_indices='all'):

    from molsysmt import get
    tmp_item = to_mdtraj_HDF5TrajectoryFile(item)
    n_atoms = get(tmp_item, target='system',  n_atoms=True)
    tmp_item.close()
    del(tmp_item, get)
    return n_atoms

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name


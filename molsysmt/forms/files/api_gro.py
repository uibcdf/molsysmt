from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np

form_name='gro'

is_form = {
    }

info = ["Gromacs gro file format","http://manual.gromacs.org/documentation/2018/user-guide/file-formats.html#gro"]

with_topology=True
with_coordinates=True
with_box=True
with_bonds=False
with_parameters=False

def to_molsysmt_MolSys(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.files import from_gro as gro_to_molsysmt_MolSys

    tmp_item = gro_to_molsysmt_MolSys(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.files import from_gro as gro_to_molsysmt_Topology

    tmp_item = gro_to_molsysmt_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_molsysmt_DataFrame(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.dataframe.files import from_gro as gro_to_molsysmt_DataFrame

    tmp_item = gro_to_molsysmt_DataFrame(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_molsysmt_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.trajectory.files import from_gro as gro_to_molsysmt_Trajectory

    tmp_item = gro_to_molsysmt_Trajectory(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_parmed_Structure(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from parmed import load_file as parmed_file_loader
    from molsysmt.forms.classes.api_parmed_Structure import extract as extract_parmed

    tmp_item = parmed_file_loader(item)
    tmp_item = extract_parmed(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_mdanalysis_Universe(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from MDAnalysis import Universe as mdanalysis_Universe
    from molsysmt.forms.classes.api_mdtraj_Universe import extract as extract_universe

    tmp_item = mdanalysis_Universe(item)
    tmp_item = extract_universe(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_mdtraj_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from mdtraj import load_topology as mdtraj_load_topology
    from molsysmt.forms.classes.api_mdtraj_Topology import extract as extract_mdtraj_topology

    tmp_item = mdtraj_load_topology(item)
    tmp_item = extract_mdtraj_topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_mdtraj_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from mdtraj import load_gro as mdtraj_gro_loader
    from molsysmt.forms.classes.api_mdtraj_Trajectory import extract as extract_mdtraj_trajectory

    tmp_item = mdtraj_gro_loader(item)
    tmp_item = extract_mdtraj_trajectory(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_mdtraj_GroTrajectoryFile(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from mdtraj.formats import GroTrajectoryFile

    tmp_item = GroTrajectoryFile(item)

    return tmp_item

def to_mol2(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):

    from parmed import load_file as parmed_file_loader
    from molsysmt.forms.classes.api_parmed_Structure import extract as extract_parmed

    tmp_item = parmed_file_loader(item)
    tmp_item = extract_parmed(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item.save(output_filename)

def to_openmm_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_parmed_Structure import to_openmm_Topology as parmed_Structure_to_openmm_Topology

    tmp_item = to_parmed_Structure(item)
    tmp_item = parmed_Structure_to_openmm_Topology(tmp_item)

    return tmp_item

def to_openmm_Modeller(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from simtk.openmm.app.modeller import Modeller
    from molsysmt.forms.classes.api_openmm_Modeller import extract as extract_modeller

    tmp_item = to_parmed_Structure(item)
    tmp_item = Modeller(tmp_item.topology, tmp_item.positions)
    tmp_item = extract_modeller(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_openmm_GromacsGroFile(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from simtk.openmm.app import GromacsGroFile
    from molsysmt.forms.classes.api_openmm_GromacsGroFile import extract as extract_openmm_GromacsGroFile

    tmp_item = GromacsGroFile(item)
    tmp_item = extract_openmm_GromacsGroFile(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_nglview_NGLView(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    tmp_item = view_with_NGLView(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def view_with_NGLView(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_MolSys import to_NGLView as molsysmt_MolSys_to_NGLView

    tmp_item = to_molsysmt_MolSys(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = molsysmt_MolSys_view_with_NGLView(tmp_item)

    return tmp_item

def select_with_MDTraj(item, selection):

    from mdtraj import load_topology as _dtraj_load_topology
    tmp_item = mdtraj_load_topology(item)
    tmp_sel = tmp_item.select(selection)
    del(tmp_item)
    return tmp_sel

def copy(item):

    raise NotImplementedError

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def merge(list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def concatenate(list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def add(item, list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def append(item, list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

###### Get

# System

def get_n_frames_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_GromacsGroFile import get_n_frames_from_system as _get
    tmp_item = to_openmm_GromacsGroFile(item)
    return _get(tmp_item)

def get_n_atoms_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_GromacsGroFile import get_n_atoms_from_system as _get
    tmp_item = to_openmm_GromacsGroFile(item)
    return _get(tmp_item)

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

def get_has_topology_from_system(item, indices='all', frame_indices='all'):

    return with_topology

def get_has_parameters_from_system(item, indices='all', frame_indices='all'):

    return with_parameters

def get_has_coordinates_from_system(item, indices='all', frame_indices='all'):

    return with_coordinates

def get_has_box_from_system(item, indices='all', frame_indices='all'):

    return with_box

def get_has_bonds_from_system(item, indices='all', frame_indices='all'):

    return with_bonds


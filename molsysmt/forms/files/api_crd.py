from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np

form_name='crd'

is_form = {
    }

info=["",""]
with_topology=False
with_trajectory=True
with_coordinates=True
with_box=True
with_bonds=False
with_parameters=False


info = ["CHARMM card (CRD) file format with coordinates.","https://www.charmmtutorial.org/index.php/CHARMM:The_Basics#CHARMM_data_structures"]

def to_crd(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):

    if frame_indices=='all':
        from shutil import copyfile
        copyfile(item, output_filename)
    else:
        raise NotImplementedError("Not implemented yet")

def to_molsysmt_MolSys(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.files import from_crd as crd_to_molsysmt_MolSys

    tmp_item = crd_to_molsysmt_MolSys(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.files import from_crd as crd_to_molsysmt_Topology

    tmp_item = crd_to_molsysmt_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_molsysmt_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.trajectory.files import from_crd as crd_to_molsysmt_Trajectory

    tmp_item = crd_to_molsysmt_Trajectory(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_mdanalysis_Universe(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mdanalysis_Universe import extract as extract_mdanalysis_Universe
    from MDAnalysis import Universe

    tmp_item = Universe(item)
    tmp_item = extract_mdanalysis_Universe(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_mdanalysis_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from MDAnalysis.topology import CRDParser

    tmp_item = CRDParser.CRDParser(item)
    tmp_item = tmp_item.parse()

    return tmp_item

def to_mdanalysis_topology_CRDParser(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from MDAnalysis.topology import CRDParser

    tmp_item = CRDParser(item)

    return tmp_item

def to_mdanalysis_coordinates_CRDReader(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from MDAnalysis.coordinates.CRD import CRDReader

    tmp_item = CRDReader(item)

    return tmp_item

def to_mdtraj_AmberRestartFile(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from mdtraj.formats import AmberRestartFile

    tmp_item = AmberRestartFile(item)

    return tmp_item

def to_openmm_AmberInpcrdFile(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from simtk.openmm.app import AmberInpcrdFile

    tmp_item = AmberInpcrdFile(item)

    return tmp_item

def view_with_NGLView(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def select_with_MDTraj(item, selection):

    raise NotImplementedError

def select_with_MDAnalysis(item, selection):

    raise NotImplementedError

def select_with_MolSysMT(item, selection):

    raise NotImplementedError

def copy(item, output_filename=None):

    from shutil import copy as copy_file
    from molsysmt._private_tools.files_and_directories import tmp_filename
    if output_filename is None:
        output_filename = tmp_filename(extension='inpcrd')
    copy_file(item, output_filename)
    return output_filename

def extract(item, atom_indices='all', frame_indices='all'):

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


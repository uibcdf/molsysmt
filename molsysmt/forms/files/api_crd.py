from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np
from molsysmt.molecular_system import molecular_system_components

form_name='crd'

is_form = {
    }

info=["",""]

has = molecular_system_components.copy()
for ii in ['coordinates', 'box']:
    has[ii]=True

info = ["CHARMM card (CRD) file format with coordinates.","https://www.charmmtutorial.org/index.php/CHARMM:The_Basics#CHARMM_data_structures"]

def to_crd(item, molecular_system, atom_indices='all', frame_indices='all', output_filename=None, copy_if_all=False):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        if copy_if_all:
            tmp_item = extract_item(item)
            tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
        else:
            tmp_item = item
            tmp_molecular_system = molecular_system
    else:
        tmp_item = extract_item(item, atom_indices=atom_indices, frame_indices=frame_indices)
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def extract_item(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):

        from shutil import copy as copy_file
        from molsysmt._private_tools.files_and_directories import tmp_filename
        if output_filename is None:
            output_filename = tmp_filename(extension='inpcrd')
        copy_file(item, output_filename)
        tmp_item = output_filename

    else:

        raise NotImplementedError()

    return tmp_item

def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.files import from_crd as crd_to_molsysmt_MolSys

    tmp_item, tmp_molecular_system = crd_to_molsysmt_MolSys(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.files import from_crd as crd_to_molsysmt_Topology

    tmp_item, tmp_molecular_system = crd_to_molsysmt_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_molsysmt_Trajectory(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.trajectory.files import from_crd as crd_to_molsysmt_Trajectory

    tmp_item, tmp_molecular_system = crd_to_molsysmt_Trajectory(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_mdanalysis_Universe(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mdanalysis_Universe import to_mdanalysis_Universe as mdanalysis_Universe_to_mdanalysis_Universe
    from MDAnalysis import Universe

    tmp_item = Universe(item)
    tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    tmp_item, tmp_molecular_system = mdanalysis_Universe_to_mdanalysis_Universe(tmp_item, tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_mdanalysis_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mdanalysis_Topology import to_mdanalysis_Topology as mdanalysis_Topology_to_mdanalysis_Topology
    from MDAnalysis.topology import CRDParser

    tmp_item = CRDParser.CRDParser(item)
    tmp_item = tmp_item.parse()
    tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    tmp_item, tmp_molecular_system = mdanalysis_Topology_to_mdanalysis_Topology(tmp_item, tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_mdanalysis_topology_CRDParser(item, molecular_system, atom_indices='all', frame_indices='all'):

    from MDAnalysis.topology import CRDParser

    tmp_item = CRDParser(item)
    tmp_molecular_system = molecular_system.combine_with_items(tmp_item)

    return tmp_item, tmp_molecular_system

def to_mdanalysis_coordinates_CRDReader(item, molecular_system, atom_indices='all', frame_indices='all'):

    from MDAnalysis.coordinates.CRD import CRDReader

    tmp_item = CRDReader(item)
    tmp_molecular_system = molecular_system.combine_with_items(tmp_item)

    return tmp_item, tmp_molecular_system

def to_mdtraj_AmberRestartFile(item, molecular_system, atom_indices='all', frame_indices='all'):

    from mdtraj.formats import AmberRestartFile

    tmp_item = AmberRestartFile(item)
    tmp_molecular_system = molecular_system.combine_with_items(tmp_item)

    return tmp_item, tmp_molecular_system

def to_openmm_AmberInpcrdFile(item, molecular_system, atom_indices='all', frame_indices='all'):

    from simtk.openmm.app import AmberInpcrdFile

    tmp_item = AmberInpcrdFile(item)
    tmp_molecular_system = molecular_system.combine_with_items(tmp_item)

    return tmp_item, tmp_molecular_system

def select_with_MDTraj(item, selection):

    raise NotImplementedError

def select_with_MDAnalysis(item, selection):

    raise NotImplementedError

def select_with_MolSysMT(item, selection):

    raise NotImplementedError

def add(item, from_item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def append_frames(item, step=None, time=None, coordinates=None, box=None):

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


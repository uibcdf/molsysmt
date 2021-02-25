from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np

form_name='prmtop'

is_form = {
    'prmtop': form_name,
    'parm7': form_name
    }

info = ["AMBER  parameter/topology file format","https://ambermd.org/FileFormats.php#topology"]
with_topology=True
with_trajectory=True
with_coordinates=False
with_box=False
with_bonds=True
with_parameters=True

def to_prmtop(item, molecular_system, atom_indices='all', frame_indices='all', output_filename=None):

    if atom_indices=='all':
        from shutil import copyfile
        copyfile(item, output_filename)
    else:
        raise NotImplementedError("Not implemented yet")

def to_pdb(item, molecular_system, atom_indices='all', frame_indices='all', output_filename=None):

    from molsysmt.forms.classes.api_openmm_Modeller import to_pdb as openmm_Modeller_to_pdb

    tmp_item = to_openmm_Modeller(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = openmm_Modeller_to_pdb(tmp_item, output_filename=output_filename)

    return tmp_item

def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.files import from_prmtop as prmtop_to_molsysmt_MolSys

    tmp_item = prmtop_to_molsysmt_MolSys(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.files import from_prmtop as prmtop_to_molsysmt_Topology

    tmp_item = prmtop_to_molsysmt_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_molsysmt_DataFrame(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.dataframe.files import from_prmtop as prmtop_to_molsysmt_DataFrame

    tmp_item = prmtop_to_molsysmt_DataFrame(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_molsysmt_Trajectory(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.trajectory.files import from_prmtop as prmtop_to_molsysmt_Trajectory

    tmp_item = prmtop_to_molsysmt_Trajectory(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_mdtraj_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

    from mdtraj import load_prmtop as prmtop_to_mdtraj_Topology

    tmp_item = prmtop_to_mdtraj_Topology(item)

    return tmp_item

def to_openmm_AmberPrmtopFile(item, molecular_system, atom_indices='all', frame_indices='all'):

    from simtk.openmm.app import AmberPrmtopFile

    tmp_item = AmberPrmtopFile(item)

    return tmp_item

def to_openmm_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_AmberPrmtopFile import to_openmm_Topology as openmm_AmberPrmtopFile_to_openmm_Topology

    tmp_item = to_openmm_AmberPrmtopFile(item, molecular_system)
    tmp_item = openmm_AmberPrmtopFile_to_openmm_Topology(tmp_item, atom_indices=atom_indices)

    return tmp_item

def to_openmm_Modeller(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import to_openmm_Modeller as openmm_Topology_to_openmm_Modeller

    tmp_item = to_openmm_Topology(item, molecular_system)
    tmp_item = openmm_Topology_to_openmm_Modeller(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', frame_indices='all'):

    tmp_item = view_with_NGLView(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def view_with_NGLView(item, atom_indices='all', frame_indices='all',
               topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.forms.classes.api_molsysmt_MolSys import to_NGLView as molsysmt_MolSys_to_NGLView

    tmp_item = to_molsysmt_MolSys(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = molsysmt_MolSys_view_with_NGLView(tmp_item)

    return tmp_item

def select_with_MDTraj(item, selection):

    raise NotImplementedError

def select_with_MolSysMT(item, selection):

    from molsysmt.forms.classes.api_molsysmt_DataFrame import select_with_MolSysMT as select_molsysmt_DataFrame_with_MolSysMT
    tmp_item = to_molsysmt_DataFrame(item)
    atom_indices=select_molsysmt_DataFrame_with_MolSysMT(tmp_item, selection)
    return atom_indices

def copy(item, output_filename=None):

    from shutil import copy as copy_file
    from molsysmt._private_tools.files_and_directories import tmp_filename
    if output_filename is None:
        output_filename = tmp_filename(extension='prmtop')
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

def get_has_topology_from_system(item, indices='all', frame_indices='all'):

    return with_topology

def get_has_parameters_from_system(item, indices='all', frame_indices='all'):

    return with_parameters

def get_has_coordinates_from_system(item, indices='all', frame_indices='all'):

    return with_coordinates

def get_has_box_from_system(item, indices='all', frame_indices='all'):

    tmp_box = get_box_from_system(item, indices=indices, frame_indices=frame_indices)
    if tmp_box[0] is not None:
        return True
    else:
        return False

def get_has_bonds_from_system(item, indices='all', frame_indices='all'):

    if get_n_bonds_from_system(item, indices=indices, frame_indices=frame_indices):
        return True
    else:
        return False

def get_is_solvated_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError


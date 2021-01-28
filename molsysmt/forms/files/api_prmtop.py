from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'prmtop': form_name,
    'parm7': form_name
    }

info = ["AMBER  parameter/topology file format","https://ambermd.org/FileFormats.php#topology"]
with_topology=True
with_coordinates=False
with_box=False
with_parameters=True

def to_prmtop(item, atom_indices='all', frame_indices='all',
              topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None,
              output_filename=None):

    if atom_indices=='all':
        from shutil import copyfile
        copyfile(item, output_filename)
    else:
        raise NotImplementedError("Not implemented yet")

def to_pdb(item, atom_indices='all', frame_indices='all',
           topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None,
           output_filename=None):

    from molsysmt.forms.classes.api_openmm_Modeller import to_pdb as openmm_Modeller_to_pdb
    tmp_item = to_openmm_Modeller(item, trajectory_item=trajectory_item, atom_indices=atom_indices,
                                 frame_indices=frame_indices)

    return openmm_Modeller_to_pdb(tmp_item, output_filename=output_filename)

def to_molsysmt_MolSys(item, atom_indices='all', frame_indices='all',
                       topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.native.io.molsys.files import from_prmtop as prmtop_to_molsysmt_MolSys
    tmp_item = prmtop_to_molsysmt_MolSys(item, trajectory_item=trajectory_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_molsysmt_Topology(item, atom_indices='all', frame_indices='all',
                         topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.native.io.topology.files import from_prmtop as prmtop_to_molsysmt_Topology
    tmp_item = prmtop_to_molsysmt_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_molsysmt_DataFrame(item, atom_indices='all', frame_indices='all',
                          topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.native.io.dataframe.files import from_prmtop as prmtop_to_molsysmt_DataFrame
    tmp_item = prmtop_to_molsysmt_DataFrame(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_molsysmt_Trajectory(item, atom_indices='all', frame_indices='all',
                          topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.native.io.trajectory.files import from_prmtop as prmtop_to_molsysmt_Trajectory
    tmp_item = prmtop_to_molsysmt_Trajectory(item, trajectory_item=trajectory_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_mdtraj_Topology(item, atom_indices='all', frame_indices='all',
                       topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):


    from mdtraj import load_prmtop as prmtop_to_mdtraj_Topology
    return prmtop_to_mdtraj_Topology

def to_openmm_AmberPrmtopFile(item, atom_indices='all', frame_indices='all',
                              topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from simtk.openmm.app import AmberPrmtopFile
    return AmberPrmtopFile(item)

def to_openmm_Topology(item, atom_indices='all', frame_indices='all',
                       topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.forms.classes.api_openmm_AmberPrmtopFile import to_openmm_Topology as openmm_AmberPrmtopFile_to_openmm_Topology
    tmp_item = to_openmm_AmberPrmtopFile(item)
    tmp_item = openmm_AmberPrmtopFile_to_openmm_Topology(tmp_item, atom_indices=atom_indices)
    return tmp_item

def to_openmm_Modeller(item, atom_indices='all', frame_indices='all',
                       topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.forms.classes.api_openmm_Topology import to_openmm_Modeller as openmm_Topology_to_openmm_Modeller
    tmp_item = to_openmm_Topology(item)
    tmp_item = openmm_Topology_to_openmm_Modeller(tmp_item, trajectory_item=trajectory_item,
                                                  atom_indices=atom_indices,
                                                  frame_indices=frame_indices)
    return tmp_item

def to_nglview_NGLWidget(item, atom_indices='all', frame_indices='all',
                         topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    return to_NGLView(item, topology_item=topology_item, trajectory_item=trajectory_item, atom_indices=atom_indices, frame_indices=frame_indices)

def to_NGLView(item, atom_indices='all', frame_indices='all',
               topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.forms.classes.api_molsysmt_MolSys import to_NGLView as molsysmt_MolSys_to_NGLView

    tmp_item = to_molsysmt_MolSys(item, trajectory_item=trajectory_item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = molsysmt_MolSys_to_NGLView(tmp_item)

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


from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np
from molsysmt.molecular_system import molecular_system_components

form_name='gro'

is_form = {
    'gro' : form_name,
}

info = ["Gromacs gro file format","http://manual.gromacs.org/documentation/2018/user-guide/file-formats.html#gro"]

has = molecular_system_components.copy()
for ii in ['elements', 'coordinates', 'box']:
    has[ii]=True

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

def to_nglview_NGLWidget(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_MolSys import to_nglview_NGLWidget as molsysmt_MolSys_to_nglview_NGLWidget

    tmp_item = to_molsysmt_MolSys(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = molsysmt_MolSys_to_nglview_NGLWidget(tmp_item)

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

def add(item, from_item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

###### Get

def aux_get_top(item, indices='all', frame_indices='all'):

    from molsysmt.forms import forms

    if 'mdtraj.Topology' in forms:

        tmp_item = to_mdtraj_Topology(item)
        method_name = sys._getframe(1).f_code.co_name
        module = importlib.import_module('molsysmt.forms.classes.api_mdtraj_Topology')
        _get = getattr(module, method_name)
        output = _get(tmp_item, indices=indices, frame_indices=frame_indices)

    else:

        raise NotImplementedError

    return output

def aux_get_coors(item, indices='all', frame_indices='all'):

    from molsysmt.forms import forms

    if 'openmm.GromacsGroFile' in forms:

        tmp_item = to_openmm_GromacsGroFilee(item)
        method_name = sys._getframe(1).f_code.co_name
        module = importlib.import_module('molsysmt.forms.classes.api_openmm_GromacsGroFile')
        _get = getattr(module, method_name)
        output = _get(tmp_item, indices=indices, frame_indices=frame_indices)

    elif 'mdtraj.GroTrajectoryFile' in forms:

        tmp_item = to_mdtraj_Topology(item)
        method_name = sys._getframe(1).f_code.co_name
        module = importlib.import_module('molsysmt.forms.classes.api_mdtraj_Topology')
        _get = getattr(module, method_name)
        output = _get(tmp_item, indices=indices, frame_indices=frame_indices)

    else:

        raise NotImplementedError

    return output


## atom

def get_atom_index_from_atom(item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_atom(item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_atom(item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_atom(item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_atom (item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

def get_inner_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

def get_n_inner_bonds_from_atom (item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    return aux_get_coors(item, indices=indices, frame_indices=frame_indices)

def get_frame_from_atom(item, indices='all', frame_indices='all'):

    return aux_get_coors(item, indices=indices, frame_indices=frame_indices)

## group

def get_group_id_from_group(item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

def get_group_name_from_group(item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

def get_group_type_from_group(item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

## component

def get_component_id_from_component (item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

def get_component_name_from_component (item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

def get_component_type_from_component (item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

## molecule

def get_molecule_id_from_molecule (item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_molecule (item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_molecule (item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

## chain

def get_chain_id_from_chain (item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_chain (item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_chain (item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

## entity

def get_entity_id_from_entity (item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_entity (item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_entity (item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

## system

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_system(item, indices='all', frame_indices='all'):

    return aux_get_coors(item, indices=indices, frame_indices=frame_indices)

def get_box_from_system(item, indices='all', frame_indices='all'):

    return aux_get_coors(item, indices=indices, frame_indices=frame_indices)

def get_box_shape_from_system(item, indices='all', frame_indices='all'):

    return aux_get_coors(item, indices=indices, frame_indices=frame_indices)

def get_box_lengths_from_system(item, indices='all', frame_indices='all'):

    return aux_get_coors(item, indices=indices, frame_indices=frame_indices)

def get_box_angles_from_system(item, indices='all', frame_indices='all'):

    return aux_get_coors(item, indices=indices, frame_indices=frame_indices)

def get_box_volume_from_system(item, indices='all', frame_indices='all'):

    return aux_get_coors(item, indices=indices, frame_indices=frame_indices)

def get_time_from_system(item, indices='all', frame_indices='all'):

    return aux_get_coors(item, indices=indices, frame_indices=frame_indices)

def get_step_from_system(item, indices='all', frame_indices='all'):

    return aux_get_coors(item, indices=indices, frame_indices=frame_indices)

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    return aux_get_coors(item, indices=indices, frame_indices=frame_indices)

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

## bond

def get_bond_order_from_bond(item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

def get_bond_type_from_bond(item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_bond(item, indices='all', frame_indices='all'):

    return aux_get_top(item, indices=indices, frame_indices=frame_indices)

###### Set

def set_box_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError

def set_coordinates_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError


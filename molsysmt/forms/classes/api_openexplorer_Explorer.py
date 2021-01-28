from os.path import basename as _basename
from molsysmt._private_tools.exceptions import *
import simtk.unit as unit
from molsysmt.forms.common_gets import *
import numpy as np
from openexplorer import Explorer as _openexplorer_Explorer

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _openexplorer_Explorer : form_name
}

info=["",""]
with_topology=True
with_coordinates=True
with_box=True
with_parameters=True

## Methods

def to_openmm_Topology(item, atom_indices='all', frame_indices='all',
           topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from .api_openmm_Topology import extract as extract_openmm_Topology
    tmp_item = item.topology
    tmp_item = extract_openmm_Topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return item.topology

def to_openmm_Context(item, atom_indices='all', frame_indices='all',
           topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    return item.context

def to_molsysmt_Topology(item, atom_indices='all', frame_indices='all',
           topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.native.io.topology.classes import from_openexplorer_Explorer as molsysmt_Topology_from_openexplorer_Explorer
    return molsysmt_Topology_from_openexplorer_Explorer(item, atom_indices=atom_indices)

def to_molsysmt_Trajectory(item, atom_indices='all', frame_indices='all',
           topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.native.io.trajectory.classes import from_openexplorer_Explorer as molsysmt_Trajectory_from_openexplorer_Explorer
    return molsysmt_Trajectory_from_openexplorer_Explorer(item, atom_indices=atom_indices)

def to_molsysmt_MolSys(item, atom_indices='all', frame_indices='all',
           topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.native.io.molsys.classes import from_openexplorer_Explorer as molsysmt_System_from_openexplorer_Explorer
    return molsysmt_System_from_openexplorer_Explorer(item, atom_indices=atom_indices)

def to_pdb(item, atom_indices='all', frame_indices='all',
           topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None,
           output_filename=None):

    from io import StringIO
    from simtk.openmm.app import PDBFile
    #from simtk.openmm.version import short_version
    from molsysmt import __version__ as msm_version
    from simtk.openmm import Platform # the openmm version is taken from this module (see: simtk/openmm/app/pdbfile.py)

    tmp_io = StringIO()
    positions = get_coordinates_from_system(item)[0]
    PDBFile.writeFile(item.topology, positions, tmp_io, keepIds=True)
    openmm_version = Platform.getOpenMMVersion()
    filedata = filedata.replace('WITH OPENMM '+openmm_version, 'WITH OPENMM '+openmm_version+' BY MOLSYSMT '+msm_version)
    tmp_io.close()
    del(tmp_io)

    if output_filename=='.pdb':
        return filedata
    else:
        with open(output_filename, 'w') as file:
            file.write(filedata)
        pass

def to_NGLView(item, atom_indices='all', frame_indices='all',
               topology_item=None, trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.forms.classes.api_molsysmt_MolSys import to_NGLView as molsysmt_MolSys_to_NGLView
    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return molsysmt_MolSys_to_NGLView(item)

def extract(item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def copy(item):

    return item.replicate()

def select_with_MDTraj(item, selection):

    raise NotImplementedError

def select_with_MolSysMT(item, selection):

    from .api_molsysmt_Topology import select_with_MolSysMT as select_molsysmt_Topology_with_MolSysMT
    tmp_item = to_molsysmt_Topology(item)
    return select_molsysmt_Topology_with_MolSysMT(tmp_item, selection)

def merge_two_items(item1, item2):

    raise NotImplementedError

##### Get

def get_atom_id_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_id_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_name_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_type_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_index_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_index_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_index_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_index_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_index_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_inner_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_inner_bonded_atoms_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_inner_bonds_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_inner_bonds_from_atom as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Context import get_coordinates_from_atom as _get
    tmp_item = to_openmm_Context(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

## group

def get_group_id_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_id_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_name_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_name_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_type_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_group_type_from_group as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

## component

def get_component_name_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_name_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_id_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_id_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_type_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_component_type_from_component as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

## molecule

def get_molecule_id_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_id_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_name_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_molecule_type_from_molecule as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

## chain

def get_chain_name_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_name_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_id_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_chain_type_from_chain as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

## entity

def get_entity_id_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_id_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_name_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_entity_type_from_entity as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

## system

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_atoms_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_groups_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_components_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_chains_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_molecules_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_entities_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_n_bonds_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Context import get_coordinates_from_system as _get
    tmp_item = to_openmm_Context(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_box_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Context import get_box_from_system as _get
    tmp_item = to_openmm_Context(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_box_shape_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Context import get_box_shape_from_system as _get
    tmp_item = to_openmm_Context(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_box_lengths_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Context import get_box_lengths_from_system as _get
    tmp_item = to_openmm_Context(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_box_angles_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Context import get_box_angles_from_system as _get
    tmp_item = to_openmm_Context(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_time_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Context import get_time_from_system as _get
    tmp_item = to_openmm_Context(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_step_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Context import get_step_from_system as _get
    tmp_item = to_openmm_Context(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    if frame_indices is 'all':

        return 1

    else:

        output = frame_indices.shape[0]
        if output>1:
            raise ValueError('The molecular system has a single frame')
        return output

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_bonded_atoms_from_system as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

def get_has_topology_from_system(item, indices='all', frame_indices='all'):

    return with_topology

def get_has_parameters_from_system(item, indices='all', frame_indices='all'):

    return with_parameters

def get_has_coordinates_from_system(item, indices='all', frame_indices='all'):

    return with_coordinates

def get_has_box_from_system(item, indices='all', frame_indices='all'):

    output = False

    if with_box:
        tmp_box = get_box_from_system(item, indices=indices, frame_indices=frame_indices)
        if tmp_box[0] is not None:
            output = True

    return output

def get_has_bonds_from_system(item, indices='all', frame_indices='all'):

    output = False

    if with_topology:
        if get_n_bonds_from_system(item, indices=indices, frame_indices=frame_indices):
            output = True

    return output

## bond

def get_bond_order_from_bond(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_bond_order_from_bond as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_bond_type_from_bond(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_bond_type_from_bond as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_bond(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import get_atom_index_from_bond as _get
    tmp_item = to_openmm_Topology(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

##### Set

def set_box_to_system(item, indices='all', frame_indices='all', value=None):

    from molsysmt.forms.classes.api_openmm_Context import set_box_to_system as _set
    return _set(item.context, indices=indices, frame_indices=frame_indices, value=value)

def set_coordinates_to_system(item, indices='all', frame_indices='all', value=None):

    from molsysmt.forms.classes.api_openmm_Context import set_coordinates_to_system as _set
    return _set(item.context, indices=indices, frame_indices=frame_indices, value=value)


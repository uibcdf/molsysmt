from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np
from pdbfixer.pdbfixer import PDBFixer as _pdbfixer_PDBFixer
from molsysmt import puw
import sys
import importlib
from molsysmt.native.molecular_system import molecular_system_components

form_name='pdbfixer.PDBFixer'

is_form={
    _pdbfixer_PDBFixer : form_name
}

info=["",""]

has = molecular_system_components.copy()
for ii in ['elements', 'coordinates', 'box', 'bonds']:
    has[ii]=True

## Methods

def to_string_aminoacids3(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    tmp_item, _ = to_openm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = ''.join([ r.name for r in tmp_item.groups() ])
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_wit_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_string_aminoacids1(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.strings.api_string_aminoacids3 import to_string_aminoacids1 as string_aminoacids3_to_string_aminoacids1

    tmp_item, _ = to_string_aminoacids3(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, _ = string_aminoacids3_to_string_aminoacids1(tmp_item)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_wit_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_biopython_Seq(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.strings.api_string_aminoacids1 import to_biopython_Seq as string_aminoacids1_to_biopython_Seq

    tmp_item, _ = to_string_aminoacids1(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, _ = string_aminoacids1_to_biopython_Seq(tmp_item)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_biopython_SeqRecord(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.strings.api_string_aminoacids1 import to_biopython_SeqRecord as string_aminoacids1_to_biopython_SeqRecord

    tmp_item, _ = to_string_aminoacids1(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, _ = string_aminoacids1_to_biopython_SeqRecord(tmp_item)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_mdtraj_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from mdtraj.core.topology import Topology as mdtraj_Topology

    tmp_item, _ = to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = mdtraj_Topology.from_openmm(tmp_item)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_mdtraj_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from openmm.unit import nanometers
    from mdtraj.core.trajectory import Trajectory as mdtraj_Trajectory

    tmp_topology, _ = to_mdtraj_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, frame_indices=frame_indices)
    coordinates = coordinates.in_units_of(nanometers)._value
    tmp_item = mdtraj_Trajectory(coordinates, tmp_topology)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_openmm_Modeller(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from openmm.app import Modeller as openmm_Modeller

    tmp_topology, _ = to_openmm_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, frame_indices=frame_indices)
    tmp_item = openmm_Modeller(tmp_topology, coordinates)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_openmm_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import to_openmm_Topology as openmm_Topology_to_openmm_Topology

    tmp_item = item.topology
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None
    tmp_item, tmp_molecular_system = openmm_Topology_to_openmm_Topology(tmp_item,
                                                                        tmp_molecular_system,
                                                                        atom_indices=atom_indices,
                                                                        frame_indices=frame_indices,
                                                                        copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_molsysmt_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.classes import from_pdbfixer_PDBFixer as pdbfixer_PDBFixer_to_molsysmt_Topology

    tmp_item, tmp_molecular_system = pdbfixer_PDBFixer_to_molsysmt_Topology(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_molsysmt_MolSys(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.classes import from_pdbfixer_PDBFixer as pdbfixer_PDBFixer_to_molsysmt_MolSys

    tmp_item, tmp_molecular_system = pdbfixer_PDBFixer_to_molsysmt_MolSys(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_parmed_Structure(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import to_parmed_Structure as openmm_Topology_to_parmed_Structure

    tmp_item, tmp_molecular_system = to_openmm_Topology(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = openmm_Topology_to_parmed_Structure(tmp_item,
            molecular_system=tmp_molecular_system)

    return tmp_item, tmp_molecular_system

def to_file_pdb(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):

    from io import StringIO
    from openmm.app import PDBFile
    from openmm.version import short_version
    from molsysmt import __version__ as msm_version
    from openmm import Platform # the openmm version is taken from this module (see: openmm/app/pdbfile.py)

    tmp_io = StringIO()
    PDBFile.writeFile(item.topology, item.positions, tmp_io, keepIds=True)
    filedata = tmp_io.getvalue()
    openmm_version = Platform.getOpenMMVersion()
    filedata = filedata.replace('WITH OPENMM '+openmm_version, 'WITH OPENMM '+openmm_version+' BY MOLSYSMT '+msm_version)
    tmp_io.close()
    del(tmp_io)

    with open(output_filename, 'w') as file:
        file.write(filedata)
    tmp_item = output_filename

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_nglview_NGLWidget(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from .api_mdtraj_Trajectory import to_nglview_NGLWidget as mdtraj_trajectory_to_nglview_NGLWidget

    tmp_item, tmp_molecular_system = to_mdtraj_Trajectory(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = mdtraj_Trajectory_nglview_NGLWidget(tmp_item,
            molecular_system=tmp_molecular_system)

    return tmp_item, tmp_molecular_system

def to_pdbfixer_PDBFixer(item, molecular_system=None, atom_indices='all', frame_indices='all', copy_if_all=True):

    tmp_molecular_system = None

    if (atom_indices is 'all') and (frame_indices is 'all'):

        if copy_if_all:

            tmp_item = extract_item(item, atom_indices=atom_indices, frame_indices=frame_indices)
            if molecular_system is not None:
                tmp_molecular_system = molecular_system.combine_with_items(tmp_item)

        else:

            tmp_item = item
            if molecular_system is not None:
                tmp_molecular_system = molecular_system

    else:

        tmp_item = extract_item(item, atom_indices=atom_indices, frame_indices=frame_indices)
        if molecular_system is not None:
            tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def extract_item(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):

        from copy import copy
        tmp_item = copy(item)

    else:
        tmp_item, _ = to_openmm_Modeller(item, atom_indices=atom_indices, frame_indices=frame_indices)
        tmp_item, _ = openmm_Modeller_to_pdbfixer_PDBFixer(tmp_item)

    return tmp_item

def add(item, from_item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

##### Get

def aux_get(item, indices='all', frame_indices='all'):

    from molsysmt.forms import forms

    method_name = sys._getframe(1).f_code.co_name

    if 'openmm.Topology' in forms:

        tmp_item, _ = to_openmm_Topology(item)
        module = importlib.import_module('molsysmt.forms.classes.api_openmm_Topology')
        _get = getattr(module, method_name)
        output = _get(tmp_item, indices=indices, frame_indices=frame_indices)

    else:

        raise NotImplementedError

    return output

## Atom

def get_atom_id_from_atom(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_atom(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_atom(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_atom (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_inner_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_inner_bonds_from_atom (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    unit = puw.get_unit(item.positions)
    coordinates = np.array(puw.get_value(item.positions))
    coordinates = coordinates.reshape(1, coordinates.shape[0], coordinates.shape[1])

    if frame_indices is not 'all':
        coordinates = coordinates[frame_indices,:,:]

    if indices is not 'all':
        coordinates = coordinates[:,indices,:]

    coordinates = coordinates * unit
    coordinates = puw.standardize(coordinates)

    return coordinates

def get_frame_from_atom(item, indices='all', frame_indices='all'):

    coordinates = get_coordinates_from_atom(item, indices=indices, frame_indices=frame_indices)
    box = get_box_from_system(item, frame_indices=frame_indices)
    step = get_step_from_system(item, frame_indices=frame_indices)
    time = get_time_from_system(item, frame_indices=frame_indices)

    return step, time, coordinates, box

## group

def get_group_id_from_group(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_group_name_from_group(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_group_type_from_group(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

## component

def get_component_id_from_component (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_component_name_from_component (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_component_type_from_component (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

## molecule

def get_molecule_id_from_molecule (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_molecule (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_molecule (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

## chain

def get_chain_id_from_chain (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_chain (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_chain (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

## entity

def get_entity_id_from_entity (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_entity (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_entity (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

## system

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_box_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_box_shape_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_box_lengths_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_box_angles_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_box_volume_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_time_from_system(item, indices='all', frame_indices='all'):

    return None

def get_step_from_system(item, indices='all', frame_indices='all'):

    return None

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    output = None

    if frame_indices is 'all':

        return 1

    else:

        output = frame_indices.shape[0]
        if output>1:
            raise ValueError('The molecular system has a single frame')
        return output

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

## bond

def get_bond_order_from_bond(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_bond_type_from_bond(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_bond(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

###### Set

def set_box_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError

def set_coordinates_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError

def set_name_to_group(item, indices='all', frame_indices='all', value=None):
    for group in tmp_item.topology.groups():
        if group.index in indices:
            name = value[np.where(indices == group.index)[0][0]]
            group.name = name
    for bond in tmp_item.topology.bonds():
        for ii in [0,1]:
            if bond[ii].group.index in set_indices:
                name = kwargs[option][np.where(array_indices == bond[ii].group.index)[0][0]]
                bond[ii].group.name = name


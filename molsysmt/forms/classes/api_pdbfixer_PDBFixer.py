from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np
from pdbfixer.pdbfixer import PDBFixer as _pdbfixer_PDBFixer
from molsysmt import puw
import sys
import importlib
from molsysmt.molecular_system import molecular_system_components

form_name='pdbfixer.PDBFixer'

is_form={
    _pdbfixer_PDBFixer : form_name
}

info=["",""]

has = molecular_system_components.copy()
for ii in ['elements', 'coordinates', 'box', 'bonds']:
    has[ii]=True

## Methods

def to_aminoacids3_seq(item, molecular_system, atom_indices='all', frame_indices='all'):

    tmp_item, tmp_molecular_system = to_openm_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = ''.join([ r.name for r in tmp_item.groups() ])

    return tmp_item, tmp_molecular_system

def to_aminoacids1_seq(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.seqs.api_aminoacids3_seq import to_aminoacids1_seq as aminoacids3_to_aminoacids1

    tmp_item, tmp_molecular_system = to_aminoacids3_seq(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = aminoacids3_to_aminoacids1(tmp_item)

    return tmp_item, tmp_molecular_system

def to_biopython_Seq(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.seqs.api_aminoacids1_seq import to_biopython_Seq as aminoacids1_to_biopython_Seq

    tmp_item, _ = to_aminoacids1_seq(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = aminoacids1_to_biopython_Seq(tmp_item)

    tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_biopython_SeqRecord(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.seqs.api_aminoacids1_seq import to_biopython_SeqRecord as aminoacids1_to_biopython_SeqRecord

    tmp_item, _ = to_aminoacids1_seq(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = aminoacids1_to_biopython_SeqRecord(tmp_item)

    tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_mdtraj_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

    from mdtraj.core.topology import Topology as mdtraj_Topology

    tmp_item, _ = to_openmm_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = mdtraj_Topology.from_openmm(tmp_item)

    tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', frame_indices='all'):

    from simtk.unit import nanometers
    from mdtraj.core.trajectory import Trajectory as mdtraj_Trajectory

    tmp_topology, _ = to_mdtraj_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, frame_indices=frame_indices)
    coordinates = coordinates.in_units_of(nanometers)._value
    tmp_item = mdtraj_Trajectory(coordinates, tmp_topology)

    tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_openmm_Modeller(item, molecular_system, atom_indices='all', frame_indices='all'):

    from simtk.openmm.app import Modeller as openmm_Modeller

    tmp_topology, _ = to_openmm_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, frame_indices=frame_indices)
    tmp_item = openmm_Modeller(tmp_topology, coordinates)

    tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_openmm_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import to_openmm_Topology as openmm_Topology_to_openmm_Topology

    tmp_item = item.topology
    tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    tmp_item, tmp_molecular_system = openmm_Topology_to_openmm_Topology(tmp_item, tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, copy=False)

    return tmp_item, tmp_molecular_system

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.classes import from_pdbfixer_PDBFixer as pdbfixer_PDBFixer_to_molsysmt_Topology

    tmp_item, tmp_molecular_system = pdbfixer_PDBFixer_to_molsysmt_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.classes import from_pdbfixer_PDBFixer as pdbfixer_PDBFixer_to_molsysmt_MolSys

    tmp_item, tmp_molecular_system = pdbfixer_PDBFixer_to_molsysmt_MolSys(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_parmed_Structure(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import to_parmed_Structure as openmm_Topology_to_parmed_Structure

    tmp_item, tmp_molecular_system = to_openmm_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = openmm_Topology_to_parmed_Structure(tmp_item, tmp_molecular_system)

    return tmp_item, tmp_molecular_system

def to_pdb(item, molecular_system, atom_indices='all', frame_indices='all', output_filename=None):

    from io import StringIO
    from simtk.openmm.app import PDBFile
    from simtk.openmm.version import short_version
    from molsysmt import __version__ as msm_version
    from simtk.openmm import Platform # the openmm version is taken from this module (see: simtk/openmm/app/pdbfile.py)

    tmp_io = StringIO()
    PDBFile.writeFile(item.topology, item.positions, tmp_io, keepIds=True)
    filedata = tmp_io.getvalue()
    openmm_version = Platform.getOpenMMVersion()
    filedata = filedata.replace('WITH OPENMM '+openmm_version, 'WITH OPENMM '+openmm_version+' BY MOLSYSMT '+msm_version)
    tmp_io.close()
    del(tmp_io)

    if output_filename=='.pdb':
        tmp_item = filedata
    else:
        with open(output_filename, 'w') as file:
            file.write(filedata)
        tmp_item = output_filename

    tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', frame_indices='all'):

    from .api_mdtraj_Trajectory import to_nglview_NGLWidget as mdtraj_trajectory_to_nglview_NGLWidget

    tmp_item, tmp_molecular_system = to_mdtraj_Trajectory(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = mdtraj_Trajectory_nglview_NGLWidget(tmp_item, tmp_molecular_system)

    return tmp_item, tmp_molecular_system

def to_pdbfixer_PDBFixer(item, molecular_system, atom_indices='all', frame_indices='all', copy=True):

    if (atom_indices is 'all') and (frame_indices is 'all'):

        if copy:
        patata
        from os import remove
        from molsysmt.forms.files.api_pdb import to_pdbfixer_PDBFixer as pdb_to_pdbfixer_PDBFixer
        from molsysmt._private_tools.pdb import tmp_pdb_filename
        tmp_file = tmp_pdb_filename()
        to_pdb(item, output_filename=tmp_file)
        tmp_item = pdb_to_pdbfixer_PDBFixer(tmp_file)
        remove(tmp_file)

    else:
        from simtk.openmm.app import Modeller as openmm_Modeller
        from .api_openmm_Topology import to_openmm_Topology as openmm_Topology_to_openmm_Topology
        from .api_openmm_Modeller import to_pdbfixer_PDBFixer as openmm_Modeller_to_pdbfixer_PDBFixer
        tmp_topology = item.topology
        if atom_indices is not 'all':
            tmp_topology = openmm_Topology_to_openmm_Topology(tmp_topology, molecular_system=molecular_system, atom_indices=atom_indices)
        coordinates = get_coordinates_from_atom(item, indices=atom_indices, frame_indices=frame_indices)
        tmp_item = openmm_Modeller(tmp_topology, coordinates)
        tmp_item = openmm_Modeller_to_pdbfixer_PDBFixer(tmp_item)
        return tmp_item

def select_with_MDTraj(item, selection):

    tmp_item = to_mdtraj_Topology(item, selection='all', syntaxis='MDTraj')
    return tmp_item.select(selection)

def select_with_MolSysMT(item, selection):

    from .api_molsysmt_Topology import select_with_MolSysMT as select_molsysmt_Topology_with_MolSysMT
    tmp_item = to_molsysmt_Topology(item)
    return select_molsysmt_Topology_with_MolSysMT(tmp_item, selection)

def add(item, from_item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

##### Get

def aux_get(item, indices='all', frame_indices='all'):

    from molsysmt.forms import forms

    if 'openmm.Topology' in forms:

        tmp_item = to_openmm_Topology(item)
        method_name = sys._getframe(1).f_code.co_name
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


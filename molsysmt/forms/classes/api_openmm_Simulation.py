from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np
from simtk.openmm.app import Simulation as _openmm_Simulation
from molsysmt.molecular_system import molecular_system_components

form_name='openmm.Simulation'

is_form={
    _openmm_Simulation : form_name,
}

info=["",""]

has = molecular_system_components.copy()
for ii in ['elements', 'bonds', 'ff_parameters', 'mm_parameters', 'simulation']:
    has[ii]=True

def to_molsysmt_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.classes import from_openmm_Simulation as openmm_Simulation_to_molsysmt_Topology

    tmp_item, tmp_molecular_system = openmm_Simulation_to_molsysmt_Topology(item,
            molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_molsysmt_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.trajectory.classes import from_openmm_Simulation as openmm_Simulation_to_molsysmt_Trajectory

    tmp_item, tmp_molecular_system = openmm_Simulation_to_molsysmt_Trajectory(item,
            molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_molsysmt_MolSys(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.classes import from_openmm_Simulation as openmm_Simulation_to_molsysmt_MolSys

    tmp_item, tmp_molecular_system = openmm_Simulation_to_molsysmt_MolSys(item,
            molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_openmm_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import openmm_Topology_to_openmm_Topology

    tmp_item = item.topology
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None
    tmp_item, tmp_molecular_system = openmm_Topology_to_openmm_Topology(tmp_item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, copy_with_all=False)

    return tmp_item, tmp_molecular_system

def to_openmm_Modeller(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from simtk.openmm.app import Modeller

    topology, _ = to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    positions = get_coordinates_from_atom(item, indices=atom_indices, frame_indices=frame_indices)
    tmp_item = Modeller(topology, positions)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_openmm_Context(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    tmp_item = item.context
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_pdbfixer_PDBFixer(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.files_and_directories import tmp_filename
    from molsysmt.forms.files.api_file_pdb import to_pdbfixer_PDBFixer as file_pdb_to_pdbfixer_PDBFixer
    from os import remove

    tmp_file = tmp_filename(extension='pdb')
    tmp_item, tmp_molecular_system = to_file_pdb(item, molecular_system=molecular_system, output_filename=tmp_file, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = file_pdb_to_pdbfixer_PDBFixer(tmp_file, molecular_system=tmp_molecular_system)
    remove(tmp_pdbfile)

    return tmp_item, tmp_molecular_system

def to_file_pdb(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):

    from molsysmt.forms.classes.api_openmm_Topology import to_file_pdb as openmm_Topology_to_file_pdb

    topology, _ = to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, frame_indices=frame_indices)
    box = get_box_from_system(item, frame_indices=frame_indices)
    topology.setPeriodicBoxVectors(box)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items([topology, coordinates])
    else:
        tmp_molecular_system = None
    tmp_item, tmp_molecular_system = openmm_Topology_to_file_pdb(topology, molecular_system=tmp_molecular_system, output_filename=output_filename)

    return tmp_item, tmp_molecular_system

def to_openmm_Simulation(item, molecular_system=None, atom_indices='all', frame_indices='all', copy_if_all=True):

    tmp_molecular_system = None

    if (atom_indices is 'all') and (frame_indices is 'all'):
        if copy_if_all:
            tmp_item = extract_item(item)
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
        raise NotImplementedError()
    else:
        raise NotImplementedError()

    return tmp_item

def add(item, from_item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

###### Get

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    state = item.context.getState(getPositions=True)
    coordinates = state.getPositions(asNumpy=True)
    if indices is not 'all':
        coordinates = coordinates[indices,:]
    return coordinates

## system

def get_coordinates_from_system(item, indices='all', frame_indices='all'):

    state = item.context.getState(getPositions=True)
    coordinates = state.getPositions(asNumpy=True)
    return coordinates

def get_box_from_system(item, indices='all', frame_indices='all'):

    state = item.context.getState()
    box = state.getPeriodicBoxVectors()
    return box


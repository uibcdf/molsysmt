from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np
from simtk.openmm.app.modeller import Modeller as _openmm_Modeller
from molsysmt import puw
import sys
import importlib
from molsysmt.molecular_system import molecular_system_components

form_name='openmm.Modeller'

is_form={
    _openmm_Modeller : form_name,
}

info=["",""]

has = molecular_system_components.copy()
for ii in ['elements', 'bonds', 'coordinates', 'box']:
    has[ii]=True

def to_mdtraj_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt import extract as _extract
    import simtk.unit as _unit
    from mdtraj.core.trajectory import Trajectory as _mdtraj_Trajectory

    tmp_topology = to_mdtraj_Topology(item)
    tmp_item = _mdtraj_Trajectory(item.positions/_unit.nanometers, tmp_topology)
    tmp_item = _extract(tmp_item, selection=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_mdtraj_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import to_mdtraj_Topology as _to_mdtraj_Topology

    tmp_item = to_openmm_Topology(item)
    tmp_item = _to_mdtraj_Topology(tmp_item, selection=selection, syntaxis=syntaxis)

    return tmp_item

def to_openmm_System(item, molecular_system=None, atom_indices='all', frame_indices='all',
                     forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff='1.0 nm', constraints=None,
                     rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                     flexible_constraints=False):

    from molsysmt.forms.classes.api_openmm_Topology import to_openmm_System as openmm_Topology_to_openmm_System

    tmp_item = to_openmm_Topology(item, molecular_system, atom_indices=atom_indices)
    tmp_item = openmm_Topology_to_openmm_System(tmp_item, molecular_system, atom_indices='all', forcefield=forcefield,
                                                non_bonded_method=non_bonded_method, non_bonded_cutoff=non_bonded_cutoff,
                                                constraints=constraints, rigid_water=rigid_water, remove_cm_motion=remove_cm_motion,
                                                hydrogen_mass=hydrogen_mass, switch_distance=switch_distance,
                                                flexible_constraints=flexible_constraints, **kwargs)

    return tmp_item

def to_openmm_Simulation(item, molecular_system=None, atom_indices='all', frame_indices='all',
                         forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff='1.0 nm', constraints=None,
                         rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                         flexible_constraints=False, integrator='Langevin', temperature='300.0 K',
                         collisions_rate='1.0 1/ps', integration_timestep='2.0 fs', platform='CUDA'):

    from molsysmt.forms.classes.api_openmm_Topology import to_openmm_Simulation as openmm_Topology_to_openmm_Simulation
    from molsysmt.multitool import get

    tmp_item = to_openmm_Topology(item, molecular_system, atom_indices=atom_indices)

    if trajectory_item is None:
        positions = get(item, target='atom', indices=atom_indices, frame_indices=frame_indices, coordinates=True)
    else:
        positions = get(trajectory_item, target='atom', indices=atom_indices, frame_indices=frame_indices, coordinates=True)

    tmp_item = openmm_Topology_to_openmm_Simulation(tmp_item, molecular_system, atom_indices='all', forcefield=forcefield,
                                                non_bonded_method=non_bonded_method, non_bonded_cutoff=non_bonded_cutoff,
                                                constraints=constraints, rigid_water=rigid_water, remove_cm_motion=remove_cm_motion,
                                                hydrogen_mass=hydrogen_mass, switch_distance=switch_distance,
                                                flexible_constraints=flexible_constraints, integrator=integrator, temperature=temperature,
                                                collisions_rate=collisions_rate, platform=platform, **kwargs)

    return tmp_item

def to_openmm_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from .api_openmm_Topology import extract as extract_openmm_Topology

    tmp_item = item.getTopology()
    tmp_item = extract_openmm_Topology(tmp_item, atom_indices=atom_indices)

    return tmp_item

def to_pdbfixer_PDBFixer(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from io import StringIO
    from pdbfixer.pdbfixer import PDBFixer

    tmp_item = to_pdb(item, output_filename='.pdb', atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = StringIO(tmp_item)
    tmp_item = PDBFixer(pdbfile=tmp_item)

    return tmp_item

def to_molsysmt_MolSys(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.classes import from_openmm_Modeller as MolSys_from_openmm_Modeller
    return MolSys_from_openmm_Modeller(item, atom_indices=atom_indices)

def to_pdb(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename = None):

    from io import StringIO
    from simtk.openmm.app import PDBFile
    #from simtk.openmm.version import short_version
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
        return filedata
    else:
        with open(output_filename, 'w') as file:
            file.write(filedata)
        pass

def to_nglview_NGLWidget(item, atom_indices='all', frame_indices='all'):

    from .api_molsysmt_MolSys import to_nglview_NGLWidget as molsysmt_MolSys_to_nglview_NGLWidget
    tmp_item = to_molsysmt_MolSys(item)
    tmp_item = molsysmt_MolSys_to_nglview_NGLWidget(tmp_item)
    return tmp_item

def select_with_MDTraj(item, selection):

    tmp_item = to_mdtraj_Topology(item)
    return tmp_item.select(selection)

def copy(item):

    from simtk.openmm.app import Modeller as _Modeller

    tmp_item = _Modeller(item.topology, item.positions)
    return tmp_item

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:

        from api_openmm_Topology import extract_atom_indices as _extract_topology

        tmp_item = copy(item)
        tmp_item.topology = _extract_topology(item.topology, atom_indices)
        tmp_item.positions = get_coordinates_from_atom(item, atom_indices)

        return tmp_item

def add(item, from_item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

###### Get

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

def get_coordinates_from_atom (item, indices='all', frame_indices='all'):

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

def get_frame_from_atom (item, indices='all', frame_indices='all'):

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

def get_time_from_system(item, indices='all', frame_indices='all'):

    return None

def get_step_from_system(item, indices='all', frame_indices='all'):

    return None

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    if frame_indices is 'all':

        return 1

    else:

        output = frame_indices.shape[0]
        if output>1:
            raise ValueError('The molecular system has a single frame')
        return output

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

###### Set

def set_box_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError

def set_coordinates_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError


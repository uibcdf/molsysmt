from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np
import importlib
import sys
from molsysmt.native.molecular_system import molecular_system_components
from molsysmt._private_tools.files_and_directories import tmp_filename
#import io

form_name='string:pdb'

is_form = {
        'string:pdb': form_name
    }

info = ["Protein Data Bank file format","https://www.rcsb.org/pdb/static.do?p=file_formats/pdb/index.html"]

has = molecular_system_components.copy()
for ii in ['elements', 'bonds', 'coordinates', 'box']:
    has[ii]=True

def to_molsysmt_MolSys(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.strings import from_string_pdb as string_pdb_to_molsysmt_MolSys

    tmp_item, tmp_molecular_system = string_pdb_to_molsysmt_MolSys(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_molsysmt_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.strings import from_string_pdb as string_pdb_to_molsysmt_Topology

    tmp_item, tmp_molecular_system = string_pdb_to_molsysmt_Topology(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_molsysmt_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.trajectory.strings import from_string_pdb as string_pdb_to_molsysmt_Trajectory

    tmp_item, tmp_molecular_system = string_pdb_to_molsysmt_Trajectory(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_parmed_Structure(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from parmed import load_file as parmed_file_loader
    from molsysmt.forms.classes.api_parmed_Structure import to_parmed_Structure as parmed_Structure_to_parmed_Structure

    tmp_item, tmp_molecular_system = to_file_pdb(item, molecular_system)
    tmp_item = parmed_file_loader(tmp_item)
    if tmp_molecular_system is not None:
        tmp_molecular_system = tmp_molecular_system.combine_with_items(tmp_item)
    tmp_item, tmp_molecular_system = parmed_Structure_to_parmed_Structure(tmp_item, tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_mdanalysis_Universe(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from MDAnalysis import Universe as mdanalysis_Universe
    from molsysmt.forms.classes.api_mdanalysis_Universe import to_mdanalysis_Universe as mdanalysis_Universe_to_mdanalysis_Universe

    tmp_item, tmp_molecular_system = to_file_pdb(item, molecular_system=molecular_system)
    tmp_item = mdanalysis_Universe(tmp_item)
    if tmp_molecular_system is not None:
        tmp_molecular_system = tmp_molecular_system.combine_with_items(tmp_item)
    tmp_item, tmp_molecular_system = mdanalysis_Universe_to_mdanalysis_Universe(tmp_item,
            molecular_system=tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_mdanalysis_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mdanalysis_topology_PDBParser import to_mdanalysis_Topology as mdanalysis_topology_PDBParser_to_mdanalysis_Topology

    tmp_item, tmp_molecular_system = to_mdanalysis_topology_PDBParser(item, molecular_system=molecular_system)
    tmp_item, tmp_molecular_system = mdanalysis_topology_PDBParser_to_mdanalysis_Topology(tmp_item, molecular_system=tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_mdanalysis_topology_PDBParser(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from MDAnalysis.topology import PDBParser

    tmp_item = PDBParser.PDBParser(item)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_mdtraj_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from mdtraj import load_topology as mdtraj_load_topology
    from molsysmt.forms.classes.api_mdtraj_Topology import to_mdtraj_Topology as mdtraj_Topology_to_mdtraj_Topology

    tmp_item, tmp_molecular_system = to_file_pdb(item, molecular_system=molecular_system)
    tmp_item = mdtraj_load_topology(tmp_item)
    if tmp_molecular_system is not None:
        tmp_molecular_system = tmp_molecular_system.combine_with_items(tmp_item)
    tmp_item, tmp_molecular_system = mdtraj_Topology_to_mdtraj_Topology(tmp_item, molecular_system=tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_mdtraj_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from mdtraj import load_pdb as mdtraj_pdb_loader
    from molsysmt.forms.classes.api_mdtraj_Trajectory import to_mdtraj_Trajectory as mdtraj_Trajectory_to_mdtraj_Trajectory

    tmp_item, tmp_molecular_system = to_file_pdb(item, molecular_system=molecular_system)
    tmp_item = mdtraj_pdb_loader(tmp_item)
    if tmp_molecular_system is not None:
        tmp_molecular_system = tmp_molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None
    tmp_item, tmp_molecular_system = mdtraj_Trajectory_to_mdtraj_Trajectory(tmp_item,
            molecular_system=tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_mdtraj_PDBTrajectoryFile(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from mdtraj.formats.pdb import PDBTrajectoryFile

    tmp_item, tmp_molecular_system = to_file_pdb(item, molecular_system=molecular_system)
    tmp_item = PDBTrajectoryFile(tmp_item)
    if tmp_molecular_system is not None:
        tmp_molecular_system = tmp_molecular_system.combine_with_items(tmp_item)

    return tmp_item, tmp_molecular_system

def to_file_mol2(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):

    from parmed import load_file as parmed_file_loader
    from molsysmt.forms.classes.api_parmed_Structure import to_parmed_Structure as parmed_Structure_to_parmed_Structure

    tmp_item, tmp_molecular_system = to_file_pdb(item, molecular_system=molecular_system)
    tmp_item = parmed_file_loader(tmp_item)
    if tmp_molecular_system is not None:
        tmp_molecular_system = tmp_molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None
    tmp_item, tmp_molecular_system = parmed_Structure_to_parmed_Structure(tmp_item,
            molecular_system=tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)
    tmp_item.save(output_filename)
    tmp_item = output_filename
    if tmp_molecular_system is not None:
        tmp_molecular_system = tmp_molecular_system.combine_with_items(tmp_item)

    return tmp_item, tmp_molecular_system

def to_openmm_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from openmm.app.pdbfile import PDBFile
    from molsysmt.forms.classes.api_openmm_PDBFile import to_openmm_Topology as openmm_PDBFile_to_openmm_Topology

    tmp_item, tmp_molecular_system = to_openmm_PDBFile(item, molecular_system=molecular_system)
    tmp_item, tmp_molecular_system = openmm_PDBFile_to_openmm_Topology(tmp_item, molecular_system=tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_openmm_Modeller(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from openmm.app.pdbfile import PDBFile
    from openmm.app.modeller import Modeller
    from molsysmt.forms.classes.api_openmm_Modeller import to_openmm_Modeller as openmm_Modeller_to_openmm_Modeller

    tmp_item = PDBFile(item)
    tmp_item = Modeller(tmp_item.topology, tmp_item.positions)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None
    tmp_item, tmp_molecular_system = openmm_Modeller_to_openmm_Modeller(tmp_item, tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_openmm_System(item, molecular_system=None, atom_indices='all', frame_indices='all',
                     forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff='1.0 nm', constraints=None,
                     rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                     flexible_constraints=False):

    from molsysmt.forms.classes.api_openmm_Modeller import to_openmm_System as openmm_Modeller_to_openmm_System

    tmp_item, tmp_molecular_system = to_openmm_Modeller(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = openmm_Modeller_to_openmm_System(tmp_item, molecular_system=tmp_molecular_system, forcefield=forcefield,
                                                non_bonded_method=non_bonded_method,
                                                non_bonded_cutoff=non_bonded_cutoff,
                                                constraints=constraints, rigid_water=rigid_water,
                                                remove_cm_motion=remove_cm_motion,
                                                hydrogen_mass=hydrogen_mass,
                                                switch_distance=switch_distance,
                                                flexible_constraints=flexible_constraints, **kwargs)

    return tmp_item, tmp_molecular_system

def to_openmm_Simulation(item, molecular_system=None, atom_indices='all', frame_indices='all',
                         forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff=None, constraints=None,
                         rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                         flexible_constraints=False, integrator='Langevin', temperature='300.0 K',
                         collisions_rate='1.0 1/ps', integration_timestep='2.0 fs', platform='CUDA'):

    from molsysmt.forms.classes.api_openmm_Modeller import to_openmm_Simulation as openmm_Modeller_to_openmm_Simulation

    tmp_item, tmp_molecular_system = to_openmm_Modeller(item, molecular_system=None, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = openmm_Modeller_to_openmm_Simulation(tmp_item, molecular_system=tmp_molecular_system, forcefield=forcefield, non_bonded_method=non_bonded_method,
                                                    non_bonded_cutoff=non_bonded_cutoff, constraints=constraints, rigid_water=rigid_water,
                                                    remove_cm_motion=remove_cm_motion, hydrogen_mass=hydrogen_mass,
                                                    switch_distance=switch_distance, flexible_constraints=flexible_constraints,
                                                    integrator=integrator, temperature=temperature,
                                                    collisions_rate=collisions_rate, integration_timestep=integration_timestep,
                                                    platform=platform, **kwargs)

    return tmp_item, tmp_molecular_system

def to_openmm_PDBFile(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from io import StringIO
    from openmm.app.pdbfile import PDBFile
    from molsysmt.forms.classes.api_openmm_PDBFile import to_openmm_PDBFile as openmm_PDBFile_to_openmm_PDBFile

    tmp_item = StringIO(item)
    tmp_item = PDBFile(tmp_item)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None
    tmp_item, tmp_molecular_system = openmm_PDBFile_to_openmm_PDBFile(tmp_item, tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_pdbfixer_PDBFixer(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from io import StringIO
    from pdbfixer.pdbfixer import PDBFixer
    from molsysmt.forms.classes.api_pdbfixer_PDBFixer import to_pdbfixer_PDBFixer as pdbfixer_PDBFixer_to_pdbfixer_PDBFixer

    tmp_item = StringIO(item)
    tmp_item = PDBFixer(pdbfile=tmp_item)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None
    tmp_item, tmp_molecular_system = pdbfixer_PDBFixer_to_pdbfixer_PDBFixer(tmp_item, tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_pytraj_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from pytraj import load as pytraj_load
    from molsysmt.forms.classes.api_pytraj_Trajectory import to_pytraj_Trajectory as pytraj_Trajectory_to_pytraj_Trajectory

    tmp_item, tmp_molecular_system = to_file_pdb(item, molecular_system=molecular_system)
    tmp_item = pytraj_load(tmp_item)
    if tmp_molecular_system is not None:
        tmp_molecular_system = tmp_molecular_system.combine_with_items(tmp_item)
    tmp_item, tmp_molecular_system = pytraj_Trajectory_to_pytraj_Trajectory(tmp_item,
            molecular_system=tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_pytraj_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from pytraj import load_topology as pytraj_load_topology
    from molsysmt.forms.classes.api_pytraj_Topology import to_pytraj_Topology as pytraj_Topology_to_pytraj_Topology

    tmp_item, tmp_molecular_system = to_file_pdb(item, molecular_system=molecular_system)
    tmp_item = pytraj_load_topology(tmp_item)
    if tmp_molecular_system is not None:
        tmp_molecular_system = tmp_molecular_system.combine_with_items(tmp_item)
    tmp_item, tmp_molecular_system = pytraj_Topology_to_pytraj_Topology(tmp_item, molecular_system=tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_nglview_NGLWidget(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from nglview import show_text
    from os import remove

    tmp_item, tmp_molecular_system = to_string_pdb(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)
    tmp_item = show_text(tmp_item)
    if molecular_system is not None:
        tmp_molecular_system = tmp_molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_file_pdb(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):

    if output_filename is None:
        output_filename = tmp_filename(extension='pdb')

    tmp_item, tmp_molecular_system = to_string_pdb(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)

    with open(output_filename, 'w') as fff:
        fff.write(tmp_item)

    tmp_item = output_filename
    if tmp_molecular_system is not None:
        tmp_molecular_system = tmp_molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_string_pdb(item, molecular_system=None, atom_indices='all', frame_indices='all', copy_if_all=True):

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

        from copy import copy
        tmp_item = copy(item)
        del(copy)

    else:

        from molsysmt.forms.classes.api_molsysmt_MolSys import to_string_pdb as molsysmt_MolSys_to_string_pdb
        tmp_item, _ = to_molsysmt_MolSys(item, atom_indices=atom_indices, frame_indices=frame_indices)
        tmp_item, _ = molsysmt_MolSys_to_string_pdb(tmp_item, output_filename=output_filename)

    return tmp_item

def merge(item_1, item_2):

    raise NotImplementedError

def add(to_item, item):

    raise NotImplementedError

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

def concatenate_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

###### Get

def aux_get_top(item, indices='all', frame_indices='all'):

    from molsysmt.forms import forms

    method_name = sys._getframe(1).f_code.co_name

    if 'openmm.PDBFile' in forms:

        tmp_item, _ = to_openmm_PDBFile(item)
        module = importlib.import_module('molsysmt.forms.classes.api_openmm_PDBFile')
        _get = getattr(module, method_name)
        output = _get(tmp_item, indices=indices, frame_indices=frame_indices)

    elif 'pdbfixer.PDBFixer' in forms:

        tmp_item, _ = to_pdbfixer_PDBFixer(item)
        module = importlib.import_module('molsysmt.forms.classes.api_pdbfixer_PDBFixer')
        _get = getattr(module, method_name)
        output = _get(tmp_item, indices=indices, frame_indices=frame_indices)

    elif 'mdtraj.Topology' in forms:

        tmp_item, _ = to_mdtraj_Topology(item)
        module = importlib.import_module('molsysmt.forms.classes.api_mdtraj_PDBTopology')
        _get = getattr(module, method_name)
        output = _get(tmp_item, indices=indices, frame_indices=frame_indices)

    else:

        raise NotImplementedError

    return output

def aux_get_coors(item, indices='all', frame_indices='all'):

    from molsysmt.forms import forms

    method_name = sys._getframe(1).f_code.co_name

    if 'openmm.PDBFile' in forms:

        tmp_item, _ = to_openmm_PDBFile(item)
        module = importlib.import_module('molsysmt.forms.classes.api_openmm_PDBFile')
        _get = getattr(module, method_name)
        output = _get(tmp_item, indices=indices, frame_indices=frame_indices)

    elif 'pdbfixer.PDBFixer' in forms:

        tmp_item, _ = to_pdbfixer_PDBFixer(item)
        module = importlib.import_module('molsysmt.forms.classes.api_pdbfixer_PDBFixer')
        _get = getattr(module, method_name)
        output = _get(tmp_item, indices=indices, frame_indices=frame_indices)

    elif 'mdtraj.PDBTrajectoryFile' in forms:

        tmp_item = to_mdtraj_PDBTrajectoryFile(item)
        module = importlib.import_module('molsysmt.forms.classes.api_mdtraj_PDBTrajectoryFile')
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


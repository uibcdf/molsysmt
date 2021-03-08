from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np
import importlib
import sys


form_name='pdb'

is_form = {
    'pdb': form_name
    }

info = ["Protein Data Bank file format","https://www.rcsb.org/pdb/static.do?p=file_formats/pdb/index.html"]
with_topology=True
with_coordinates=True
with_box=True
with_bonds=True
with_parameters=False

def to_molsysmt_MolSys(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.files import from_pdb as pdb_to_molsysmt_MolSys

    tmp_item = pdb_to_molsysmt_MolSys(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.files import from_pdb as pdb_to_molsysmt_Topology

    tmp_item = pdb_to_molsysmt_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_molsysmt_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.trajectory.files import from_pdb as pdb_to_molsysmt_Trajectory

    tmp_item = pdb_to_molsysmt_Trajectory(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_parmed_Structure(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from parmed import load_file as parmed_file_loader
    from molsysmt.forms.classes.api_parmed_Structure import extract as extract_parmed

    tmp_item = parmed_file_loader(item)
    tmp_item = extract_parmed(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_mdanalysis_Universe(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from MDAnalysis import Universe as mdanalysis_Universe
    from molsysmt.forms.classes.api_mdanalysis_Universe import extract as extract_universe

    tmp_item = mdanalysis_Universe(item)
    tmp_item = extract_universe(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_mdanalysis_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mdanalysis_topology_PDBParser import to_mdanalysis_Topology as mdanalysis_topology_PDBParser_to_mdanalysis_Topology

    tmp_item = to_mdanalysis_topology_PDBParser(item, molecular_system)
    tmp_item = mdanalysis_topology_PDBParser_to_mdanalysis_Topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_mdanalysis_topology_PDBParser(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from MDAnalysis.topology import PDBParser

    tmp_item = PDBParser.PDBParser(item)

    return tmp_item

def to_mdtraj_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from mdtraj import load_topology as mdtraj_load_topology
    from molsysmt.forms.classes.api_mdtraj_Topology import extract as extract_mdtraj_topology

    tmp_item = mdtraj_load_topology(item)
    tmp_item = extract_mdtraj_topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_mdtraj_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from mdtraj import load_pdb as mdtraj_pdb_loader
    from molsysmt.forms.classes.api_mdtraj_Trajectory import extract as extract_mdtraj_trajectory

    tmp_item = mdtraj_pdb_loader(item)
    tmp_item = extract_mdtraj_trajectory(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_mdtraj_PDBTrajectoryFile(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from mdtraj.formats.pdb import PDBTrajectoryFile

    tmp_item = PDBTrajectoryFile(item)

    return tmp_item

def to_mol2(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):

    from parmed import load_file as parmed_file_loader
    from molsysmt.forms.classes.api_parmed_Structure import extract as extract_parmed

    tmp_item = parmed_file_loader(item)
    tmp_item = extract_parmed(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item.save(output_filename)

def to_openmm_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from simtk.openmm.app.pdbfile import PDBFile
    from molsysmt.forms.classes.api_openmm_PDBFile import to_openmm_Topology as openmm_PDBFile_to_openmm_Topology

    tmp_item = to_openmm_PDBFile(item)
    tmp_item = openmm_PDBFile_to_openmm_Topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_openmm_Modeller(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from simtk.openmm.app.pdbfile import PDBFile
    from simtk.openmm.app.modeller import Modeller
    from molsysmt.forms.classes.api_openmm_Modeller import extract as extract_modeller

    tmp_item = PDBFile(item)
    tmp_item = Modeller(tmp_item.topology, tmp_item.positions)
    tmp_item = extract_modeller(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_openmm_System(item, molecular_system=None, atom_indices='all', frame_indices='all',
                     forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff='1.0 nm', constraints=None,
                     rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                     flexible_constraints=False):

    from molsysmt.forms.classes.api_openmm_Modeller import to_openmm_System as openmm_Modeller_to_openmm_System

    tmp_item = to_openmm_Modeller(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = openmm_Modeller_to_openmm_System(tmp_item, forcefield=forcefield,
                                                non_bonded_method=non_bonded_method,
                                                non_bonded_cutoff=non_bonded_cutoff,
                                                constraints=constraints, rigid_water=rigid_water,
                                                remove_cm_motion=remove_cm_motion,
                                                hydrogen_mass=hydrogen_mass,
                                                switch_distance=switch_distance,
                                                flexible_constraints=flexible_constraints, **kwargs)

    return tmp_item

def to_openmm_Simulation(item, molecular_system=None, atom_indices='all', frame_indices='all',
                         forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff=None, constraints=None,
                         rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                         flexible_constraints=False, integrator='Langevin', temperature='300.0 K',
                         collisions_rate='1.0 1/ps', integration_timestep='2.0 fs', platform='CUDA'):

    from molsysmt.forms.classes.api_openmm_Modeller import to_openmm_Simulation as openmm_Modeller_to_openmm_Simulation

    tmp_item = to_openmm_Modeller(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = openmm_Modeller_to_openmm_Simulation(tmp_item, forcefield=forcefield, non_bonded_method=non_bonded_method,
                                                    non_bonded_cutoff=non_bonded_cutoff, constraints=constraints, rigid_water=rigid_water,
                                                    remove_cm_motion=remove_cm_motion, hydrogen_mass=hydrogen_mass,
                                                    switch_distance=switch_distance, flexible_constraints=flexible_constraints,
                                                    integrator=integrator, temperature=temperature,
                                                    collisions_rate=collisions_rate, integration_timestep=integration_timestep,
                                                    platform=platform, **kwargs)

    return tmp_item

def to_openmm_PDBFile(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from simtk.openmm.app.pdbfile import PDBFile
    from molsysmt.forms.classes.api_openmm_PDBFile import extract as extract_pdbfile

    tmp_item = PDBFile(item)
    tmp_item = extract_pdbfile(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_pdbfixer_PDBFixer(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from pdbfixer.pdbfixer import PDBFixer
    from molsysmt.forms.classes.api_pdbfixer_PDBFixer import extract as extract_pdbfixer_PDBFixer

    tmp_item = PDBFixer(item)
    tmp_item = extract_pdbfixer_PDBFixer(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_pytraj_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from pytraj import load as pytraj_load
    from molsysmt.forms.classes.api_pytraj_Trajectory import extract as extract_pytraj_Trajectory

    tmp_item = pytraj_load(item)
    tmp_item = extract_pytraj_Trajectory(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_pytraj_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from pytraj import load_topology as pytraj_load_topology
    from molsysmt.forms.classes.api_pytraj_Topology import extract as extract_pytraj_Topology

    tmp_item = pytraj_load_topology(item)
    tmp_item = extract_pytraj_Topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_nglview_NGLWidget(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from nglview import show_file as _nglview_show_file
    from os import remove

    tmp_file = extract(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = _nglview_show_file(tmp_file)
    remove(tmp_file)

    return tmp_item

def to_yank_Topography(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import to_yank_Topography as openmm_to_yank_Topography

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = openmm_to_yank_Topography(tmp_item)

    return tmp_item

def select_with_MDTraj(item, selection):

    from mdtraj import load_topology as _dtraj_load_topology
    tmp_item = mdtraj_load_topology(item)
    tmp_sel = tmp_item.select(selection)
    del(tmp_item)
    return tmp_sel

def select_with_MolSysMT(item, selection):

    from molsysmt.forms.classes.api_openmm_PDBFile import select_with_MolSysMT as select_openmm_PDBFile_with_MolSysMT
    tmp_item = to_openmm_PDBFile(item)
    return select_openmm_PDBFile_with_MolSysMT(tmp_item, selection)

def copy(item, output_filename=None):

    from shutil import copy as copy_file
    from molsysmt._private_tools.files_and_directories import tmp_filename
    if output_filename is None:
        output_filename = tmp_filename(extension='pdb')
    copy_file(item, output_filename)
    return output_filename

def extract(item, output_filename=None, atom_indices='all', frame_indices='all'):

    if atom_indices is 'all' and frame_indices is 'all':

        return copy(item, output_filename=output_filename)

    else:

        from molsysmt.forms.classes.api_molsysmt_MolSys import to_pdb as molsysmt_MolSys_to_pdb
        tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices, frame_indices=frame_indices)
        return molsysmt_MolSys_to_pdb(tmp_item, output_filename=output_filename)

def add(item, from_item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

###### Get

def aux_get_top(item, indices='all', frame_indices='all'):

    from molsysmt.forms import forms

    if 'openmm.PDBFile' in forms:

        tmp_item = to_openmm_PDBFile(item)
        method_name = sys._getframe(1).f_code.co_name
        module = importlib.import_module('molsysmt.forms.classes.api_openmm_PDBFile')
        _get = getattr(module, method_name)
        output = _get(tmp_item, indices=indices, frame_indices=frame_indices)

    elif 'pdbfixer.PDBFixer' in forms:

        tmp_item = to_pdbfixer_PDBFixer(item)
        method_name = sys._getframe(1).f_code.co_name
        module = importlib.import_module('molsysmt.forms.classes.api_pdbfixer_PDBFixer')
        _get = getattr(module, method_name)
        output = _get(tmp_item, indices=indices, frame_indices=frame_indices)

    elif 'mdtraj.Topology' in forms:

        tmp_item = to_mdtraj_Topology(item)
        method_name = sys._getframe(1).f_code.co_name
        module = importlib.import_module('molsysmt.forms.classes.api_mdtraj_PDBTopology')
        _get = getattr(module, method_name)
        output = _get(tmp_item, indices=indices, frame_indices=frame_indices)

    else:

        raise NotImplementedError

    return output

def aux_get_coors(item, indices='all', frame_indices='all'):

    from molsysmt.forms import forms

    if 'openmm.PDBFile' in forms:

        tmp_item = to_openmm_PDBFile(item)
        method_name = sys._getframe(1).f_code.co_name
        module = importlib.import_module('molsysmt.forms.classes.api_openmm_PDBFile')
        _get = getattr(module, method_name)
        output = _get(tmp_item, indices=indices, frame_indices=frame_indices)

    elif 'pdbfixer.PDBFixer' in forms:

        tmp_item = to_pdbfixer_PDBFixer(item)
        method_name = sys._getframe(1).f_code.co_name
        module = importlib.import_module('molsysmt.forms.classes.api_pdbfixer_PDBFixer')
        _get = getattr(module, method_name)
        output = _get(tmp_item, indices=indices, frame_indices=frame_indices)

    elif 'mdtraj.PDBTrajectoryFile' in forms:

        tmp_item = to_mdtraj_PDBTrajectoryFile(item)
        method_name = sys._getframe(1).f_code.co_name
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

def get_has_topology_from_system(item, indices='all', frame_indices='all'):

    return with_topology

def get_has_parameters_from_system(item, indices='all', frame_indices='all'):

    return with_parameters

def get_has_coordinates_from_system(item, indices='all', frame_indices='all'):

    return with_coordinates

def get_has_box_from_system(item, indices='all', frame_indices='all'):

    return with_box

def get_has_bonds_from_system(item, indices='all', frame_indices='all'):

    return with_bonds

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


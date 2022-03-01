from molsysmt._private_tools.exceptions import *

from molsysmt.tools.file_pdb.is_file_pdb import is_file_pdb as is_form
from molsysmt.tools.file_pdb.extract import extract
from molsysmt.tools.file_pdb.add import add
from molsysmt.tools.file_pdb.merge import merge
from molsysmt.tools.file_pdb.append_frames import append_frames
from molsysmt.tools.file_pdb.concatenate_frames import concatenate_frames
from molsysmt.tools.file_pdb.get import *
from molsysmt.tools.file_pdb.set import *

form_name='file:pdb'
form_type='file'
form_info=["Protein Data Bank file format","https://www.rcsb.org/pdb/static.do?p=file_formats/pdb/index.html"]

form_elements = {
    'atoms' : True,
    'bonds' : True,
    'groups' : True,
    'component' : False,
    'molecule' : True,
    'chain' : True,
    'entity' : True,
        }

form_attributes = {
    'atom_id' : True,
    'atom_name' : True,
    'atom_type' : True,

    'bond_id' : True,
    'bond_name' : True,
    'bond_type' : True,

    'group_id' : True,
    'group_name' : True,
    'group_type' : True,

    'component_id' : False,
    'component_name' : False,
    'component_type' : False,

    'molecule_id' : True,
    'molecule_name' : True,
    'molecule_type' : True,

    'chain_id' : True,
    'chain_name' : True,
    'chain_type' : True,

    'entity_id' : True,
    'entity_name' : True,
    'entity_type' : True,

    'coordinates' : True,
    'velocities' : False,
    'box' : True,
    'time' : False,
    'step' : False,

    'forcefield' : False,
    'temperature' : False,
    'pressure' : False,
    'integrator' : False,
    'damping' : False,
}


from molsysmt._private_tools.exceptions import *
from molsysmt.api_forms.common_gets import *
import numpy as np
import importlib
import sys
from molsysmt.native.molecular_system import molecular_system_components
from molsysmt._private_tools.files_and_directories import temp_filename


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.file_pdb import to_molsysmt_MolSys as file_pdb_to_molsysmt_MolSys

    tmp_item = file_pdb_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices, check_form=False)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.file_pdb import to_molsysmt_Topology as file_pdb_to_molsysmt_Topology

    tmp_item = file_pdb_to_molsysmt_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check_form=False)

    return tmp_item

def to_molsysmt_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.file_pdb import to_molsysmt_Trajectory as file_pdb_to_molsysmt_Trajectory

    tmp_item = file_pdb_to_molsysmt_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices, check_form=False)

    return tmp_item

def to_parmed_Structure(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.file_pdb import to_parmed_Structure as file_pdb_to_parmed_Structure

    tmp_item = file_pdb_to_parmed_Structure(item, atom_indices=atom_indices, structure_indices=structure_indices, check_form=False)

    return tmp_item

def to_mdanalysis_Universe(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.file_pdb import to_mdanalysis_Universe as file_pdb_to_mdanalysis_Universe

    tmp_item = file_pdb_to_mdanalysis_Universe(item, atom_indices=atom_indices, structure_indices=structure_indices, check_form=False)

    return tmp_item, tmp_molecular_system

def to_mdanalysis_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.file_pdb import to_mdanalysis_Topology as file_pdb_to_mdanalysis_Topology

    tmp_item = file_pdb_to_mdanalysis_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check_form=False)

    return tmp_item

def to_mdanalysis_topology_PDBParser(item, molecular_system, atom_indices='all', structure_indices='all'):

    from MDAnalysis.topology import PDBParser

    tmp_item = PDBParser.PDBParser(item)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from mdtraj import load_topology as mdtraj_load_topology
    from molsysmt.api_forms.api_mdtraj_Topology import to_mdtraj_Topology as mdtraj_Topology_to_mdtraj_Topology

    tmp_item = mdtraj_load_topology(item)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None
    tmp_item, tmp_molecular_system = mdtraj_Topology_to_mdtraj_Topology(tmp_item, molecular_system=tmp_molecular_system, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):

    from mdtraj import load_pdb as mdtraj_pdb_loader
    from molsysmt.api_forms.api_mdtraj_Trajectory import to_mdtraj_Trajectory as mdtraj_Trajectory_to_mdtraj_Trajectory

    tmp_item = mdtraj_pdb_loader(item)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None
    tmp_item, tmp_molecular_system = mdtraj_Trajectory_to_mdtraj_Trajectory(tmp_item, tmp_molecular_system, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_mdtraj_PDBTrajectoryFile(item, molecular_system, atom_indices='all', structure_indices='all'):

    from mdtraj.formats.pdb import PDBTrajectoryFile

    tmp_item = PDBTrajectoryFile(item)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_file_mol2(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):

    from parmed import load_file as parmed_file_loader
    from molsysmt.api_forms.api_parmed_Structure import to_parmed_Structure as parmed_Structure_to_parmed_Structure

    tmp_item = parmed_file_loader(item)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None
    tmp_item, tmp_molecular_system = parmed_Structure_to_parmed_Structure(tmp_item, tmp_molecular_system, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False)
    tmp_item.save(output_filename)
    tmp_item = output_filename
    if tmp_molecular_system is not None:
        tmp_molecular_system = tmp_molecular_system.combine_with_items(tmp_item)

    return tmp_item, tmp_molecular_system

def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from openmm.app.pdbfile import PDBFile
    from molsysmt.api_forms.api_openmm_PDBFile import to_openmm_Topology as openmm_PDBFile_to_openmm_Topology

    tmp_item, tmp_molecular_system = to_openmm_PDBFile(item, molecular_system=molecular_system)
    tmp_item, tmp_molecular_system = openmm_PDBFile_to_openmm_Topology(tmp_item, molecular_system=tmp_molecular_system, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item, tmp_molecular_system

def to_openmm_Modeller(item, molecular_system, atom_indices='all', structure_indices='all'):

    from openmm.app.pdbfile import PDBFile
    from openmm.app.modeller import Modeller
    from molsysmt.api_forms.api_openmm_Modeller import to_openmm_Modeller as openmm_Modeller_to_openmm_Modeller

    tmp_item = PDBFile(item)
    tmp_item = Modeller(tmp_item.topology, tmp_item.positions)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None
    tmp_item, tmp_molecular_system = openmm_Modeller_to_openmm_Modeller(tmp_item, molecular_system=tmp_molecular_system, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_openmm_System(item, molecular_system, atom_indices='all', structure_indices='all',
                     forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff='1.0 nm', constraints=None,
                     rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                     flexible_constraints=False):

    from molsysmt.api_forms.api_openmm_Modeller import to_openmm_System as openmm_Modeller_to_openmm_System

    tmp_item, tmp_molecular_system = to_openmm_Modeller(item, molecular_system=molecular_system, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item, tmp_molecular_system = openmm_Modeller_to_openmm_System(tmp_item, molecular_system=tmp_molecular_system, forcefield=forcefield,
                                                non_bonded_method=non_bonded_method,
                                                non_bonded_cutoff=non_bonded_cutoff,
                                                constraints=constraints, rigid_water=rigid_water,
                                                remove_cm_motion=remove_cm_motion,
                                                hydrogen_mass=hydrogen_mass,
                                                switch_distance=switch_distance,
                                                flexible_constraints=flexible_constraints, **kwargs)

    return tmp_item, tmp_molecular_system

def to_openmm_Simulation(item, molecular_system, atom_indices='all', structure_indices='all',
                         forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff=None, constraints=None,
                         rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                         flexible_constraints=False, integrator='Langevin', temperature='300.0 K',
                         collisions_rate='1.0 1/ps', integration_timestep='2.0 fs', platform='CUDA'):

    from molsysmt.api_forms.api_openmm_Modeller import to_openmm_Simulation as openmm_Modeller_to_openmm_Simulation

    tmp_item, tmp_molecular_system = to_openmm_Modeller(item, molecular_system=molecular_system, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item, tmp_molecular_system = openmm_Modeller_to_openmm_Simulation(tmp_item,
            molecular_system=tmp_molecular_system, forcefield=forcefield, non_bonded_method=non_bonded_method,
                                                    non_bonded_cutoff=non_bonded_cutoff, constraints=constraints, rigid_water=rigid_water,
                                                    remove_cm_motion=remove_cm_motion, hydrogen_mass=hydrogen_mass,
                                                    switch_distance=switch_distance, flexible_constraints=flexible_constraints,
                                                    integrator=integrator, temperature=temperature,
                                                    collisions_rate=collisions_rate, integration_timestep=integration_timestep,
                                                    platform=platform, **kwargs)

    return tmp_item, tmp_molecular_system

def to_openmm_PDBFile(item, molecular_system, atom_indices='all', structure_indices='all'):

    from openmm.app.pdbfile import PDBFile
    from molsysmt.api_forms.api_openmm_PDBFile import to_openmm_PDBFile as openmm_PDBFile_to_openmm_PDBFile

    tmp_item = PDBFile(item)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None
    tmp_item, tmp_molecular_system = openmm_PDBFile_to_openmm_PDBFile(tmp_item, molecular_system=tmp_molecular_system, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_pdbfixer_PDBFixer(item, molecular_system, atom_indices='all', structure_indices='all'):

    from pdbfixer.pdbfixer import PDBFixer
    from molsysmt.api_forms.api_pdbfixer_PDBFixer import to_pdbfixer_PDBFixer as pdbfixer_PDBFixer_to_pdbfixer_PDBFixer

    tmp_item = PDBFixer(item)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None
    tmp_item, tmp_molecular_system = pdbfixer_PDBFixer_to_pdbfixer_PDBFixer(tmp_item,
            molecular_system=tmp_molecular_system, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_pytraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):

    from pytraj import load as pytraj_load
    from molsysmt.api_forms.api_pytraj_Trajectory import to_pytraj_Trajectory as pytraj_Trajectory_to_pytraj_Trajectory

    tmp_item = pytraj_load(item)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None
    tmp_item, tmp_molecular_system = pytraj_Trajectory_to_pytraj_Trajectory(tmp_item,
            molecular_system=tmp_molecular_system, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_pytraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from pytraj import load_topology as pytraj_load_topology
    from molsysmt.api_forms.api_pytraj_Topology import to_pytraj_Topology as pytraj_Topology_to_pytraj_Topology

    tmp_item = pytraj_load_topology(item)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None
    tmp_item, tmp_molecular_system = pytraj_Topology_to_pytraj_Topology(tmp_item, molecular_system=tmp_molecular_system, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):

    from nglview import show_file
    from os import remove

    tmp_molecular_system = None

    if (atom_indices is not 'all') or (structure_indices is not 'all'):
        temp_file = to_pdb(item, atom_indices=atom_indices, structure_indices=structure_indices)
        tmp_item = show_file(temp_file)
        if molecular_system is not None:
            tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)
        remove(temp_file)
    else:
        tmp_item = show_file(item)
        if molecular_system is not None:
            tmp_molecular_system = molecular_system.combine_with_items(tmp_item)

    return tmp_item, tmp_molecular_system

def to_string_pdb_text(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.api_forms.api_string_pdb_text import to_string_pdb_text as string_pdb_text_to_string_pdb_text

    fff = open(item, 'r')
    tmp_item = fff.read()
    fff.close()

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None

    tmp_item, tmp_molecular_system = string_pdb_text_to_string_pdb_text(tmp_item, molecular_system=tmp_molecular_system, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item, tmp_molecular_system


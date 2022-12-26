from molsysmt.form.file_pdb.is_file_pdb import is_file_pdb as is_form
from molsysmt.form.file_pdb.extract import extract
from molsysmt.form.file_pdb.add import add
from molsysmt.form.file_pdb.append_structures import append_structures
from molsysmt.form.file_pdb.get import *
from molsysmt.form.file_pdb.set import *
from molsysmt.form.file_pdb.iterators import StructuresIterator, TopologyIterator
from .form_attributes import form_attributes

form_name = 'file:pdb'
form_type = 'file'
form_info = ["Protein Data Bank file format", "https://www.rcsb.org/pdb/static.do?p=file_formats/pdb/index.html"]

form_attributes = form_attributes()
form_attributes['atom_index'] = True
form_attributes['atom_id'] = True
form_attributes['atom_name'] = True
form_attributes['atom_type'] = True
form_attributes['bond_index'] = True
form_attributes['bond_id'] = True
form_attributes['bond_name'] = True
form_attributes['bond_type'] = True
form_attributes['bond_order'] = True
form_attributes['group_index'] = True
form_attributes['group_id'] = True
form_attributes['group_name'] = True
form_attributes['group_type'] = True
form_attributes['component_index'] = True
form_attributes['molecule_index'] = True
form_attributes['molecule_id'] = True
form_attributes['molecule_name'] = True
form_attributes['molecule_type'] = True
form_attributes['chain_index'] = True
form_attributes['chain_id'] = True
form_attributes['chain_name'] = True
form_attributes['chain_type'] = True
form_attributes['box'] = True
form_attributes['forcefield_parameters'] = True


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_pdb import to_molsysmt_MolSys as file_pdb_to_molsysmt_MolSys

    return file_pdb_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices, digest=False)


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_pdb import to_molsysmt_Topology as file_pdb_to_molsysmt_Topology

    return file_pdb_to_molsysmt_Topology(item, atom_indices=atom_indices, digest=False)


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_pdb import to_molsysmt_Structures as file_pdb_to_molsysmt_Structures

    return file_pdb_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices, digest=False)


def to_parmed_Structure(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_pdb import to_parmed_Structure as file_pdb_to_parmed_Structure

    return file_pdb_to_parmed_Structure(item, atom_indices=atom_indices, structure_indices=structure_indices, digest=False)


def to_mdanalysis_Universe(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_pdb import to_mdanalysis_Universe as file_pdb_to_mdanalysis_Universe

    return file_pdb_to_mdanalysis_Universe(item, atom_indices=atom_indices, structure_indices=structure_indices, digest=False)


def to_mdanalysis_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_pdb import to_mdanalysis_Topology as file_pdb_to_mdanalysis_Topology

    return file_pdb_to_mdanalysis_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, digest=False)


def to_mdanalysis_topology_PDBParser(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_pdb import to_mdanalysis_topology_PDBParser as file_pdb_to_mdanalysis_topology_PDBParser

    return file_pdb_to_mdanalysis_topology_PDBParser(item, atom_indices=atom_indices, digest=False)


def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_pdb import to_mdtraj_Topology as file_pdb_to_mdtraj_Topology

    return file_pdb_to_mdtraj_Topology(item, atom_indices=atom_indices, digest=False)


def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_pdb import to_mdtraj_Trajectory as file_pdb_to_mdtraj_Trajectory

    return file_pdb_to_mdtraj_Trajectory(item, atom_indices=atom_indices,
                                         structure_indices=structure_indices, digest=False)


def to_mdtraj_PDBTrajectoryFile(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_pdb import to_mdtraj_PDBTrajectoryFile as file_pdb_to_mdtraj_PDBTrajectoryFile

    return file_pdb_to_mdtraj_PDBTrajectoryFile(item, atom_indices=atom_indices, digest=False)


def to_file_mol2(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):
    from molsysmt.form.file_pdb import to_file_mol2 as file_pdb_to_file_mol2

    return file_pdb_to_file_mol2(item, atom_indices=atom_indices,
                                 structure_indices=structure_indices, output_filename=output_filename, digest=False)


def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_pdb import to_openmm_Topology as file_pdb_to_openmm_Topology

    return file_pdb_to_openmm_Topology(item, atom_indices=atom_indices, digest=False)


def to_openmm_Modeller(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_pdb import to_openmm_Modeller as file_pdb_to_openmm_Modeller

    return file_pdb_to_openmm_Modeller(item, atom_indices=atom_indices,
                                       structure_indices=structure_indices, digest=False)


def to_openmm_System(item, molecular_system, atom_indices='all', structure_indices='all',
                     forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff='1.0 nm', constraints=None,
                     rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                     flexible_constraints=False):
    from molsysmt.form.file_pdb import to_openmm_System as file_pdb_to_openmm_System

    return file_pdb_to_openmm_System(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                     forcefield=forcefield, non_bonded_method=non_bonded_method,
                                     non_bonded_cutoff=non_bonded_cutoff, constraints=constraints,
                                     rigid_water=rigid_water, remove_cm_motion=remove_cm_motion,
                                     hydrogen_mass=hydrogen_mass, switch_distance=switch_distance,
                                     flexible_constraints=flexible_constraints, digest=False)


def to_openmm_Simulation(item, molecular_system, atom_indices='all', structure_indices='all',
                         forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff=None, constraints=None,
                         rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                         flexible_constraints=False, integrator='Langevin', temperature='300.0 K',
                         collisions_rate='1.0 1/ps', integration_timestep='2.0 fs', platform='CUDA'):
    from molsysmt.form.file_pdb import to_openmm_Simulation as file_pdb_to_openmm_Simulation

    return file_pdb_to_openmm_Simulation(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                         forcefield=forcefield, non_bonded_method=non_bonded_method,
                                         non_bonded_cutoff=non_bonded_cutoff, constraints=constraints,
                                         rigid_water=rigid_water, remove_cm_motion=remove_cm_motion,
                                         hydrogen_mass=hydrogen_mass, switch_distance=switch_distance,
                                         flexible_constraints=flexible_constraints, integrator=integrator,
                                         temperature=temperature, collisions_rate=collisions_rate,
                                         integration_timestep=integration_timestep, platform=platform, digest=False)


def to_openmm_PDBFile(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_pdb import to_openmm_PDBFile as file_pdb_to_openmm_PDBFile

    return file_pdb_to_openmm_PDBFile(item, atom_indices=atom_indices, structure_indices=structure_indices, digest=False)


def to_pdbfixer_PDBFixer(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_pdb import to_pdbfixer_PDBFixer as file_pdb_to_pdbfixer_PDBFixer

    return file_pdb_to_pdbfixer_PDBFixer(item, atom_indices=atom_indices, structure_indices=structure_indices, digest=False)


def to_pytraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_pdb import to_pytraj_Trajectory as file_pdb_to_pytraj_Trajectory

    return file_pdb_to_pytraj_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices, digest=False)


def to_pytraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_pdb import to_pytraj_Topology as file_pdb_to_pytraj_Topology

    return file_pdb_to_pytraj_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, digest=False)


def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_pdb import to_nglview_NGLWidget as file_pdb_to_nglview_NGLWidget

    return file_pdb_to_nglview_NGLWidget(item, atom_indices=atom_indices, structure_indices=structure_indices, digest=False)


def to_string_pdb_text(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_pdb import to_string_pdb_text as file_pdb_to_string_pdb_text

    return file_pdb_to_string_pdb_text(item, atom_indices=atom_indices, structure_indices=structure_indices, digest=False)

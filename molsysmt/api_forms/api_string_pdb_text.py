from molsysmt._private.exceptions import *
from molsysmt.item.string_pdb_text.is_string_pdb_text import is_string_pdb_text as is_form
from molsysmt.item.string_pdb_text.extract import extract
from molsysmt.item.string_pdb_text.add import add
from molsysmt.item.string_pdb_text.append_structures import append_structures
from molsysmt.item.string_pdb_text.get import *
from molsysmt.item.string_pdb_text.set import *
from .form_attributes import form_attributes

form_name = 'string:pdb_text'
form_type = 'string'
form_info = ["Protein Data Bank file format",
             "https://www.rcsb.org/pdb/static.do?p=file_formats/pdb/index.html"]

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
form_attributes['coordinates'] = True
form_attributes['box'] = True


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.string_pdb_text import to_molsysmt_MolSys as string_pdb_text_to_molsysmt_MolSys

    return string_pdb_text_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                              check=False)


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.string_pdb_text import to_molsysmt_Topology as string_pdb_text_to_molsysmt_Topology

    return string_pdb_text_to_molsysmt_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                                check=False)


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.string_pdb_text import to_molsysmt_Structures as string_pdb_text_to_molsysmt_Structures

    return string_pdb_text_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                                  check=False)


def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.string_pdb_text import to_mdtraj_Topology as string_pdb_text_to_mdtraj_Topology

    return string_pdb_text_to_mdtraj_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                              check=False)


def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.string_pdb_text import to_mdtraj_Trajectory as string_pdb_text_to_mdtraj_Trajectory

    return string_pdb_text_to_mdtraj_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                                check=False)


def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.string_pdb_text import to_openmm_Topology as string_pdb_text_to_openmm_Topology

    return string_pdb_text_to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                              check=False)


def to_openmm_Modeller(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.string_pdb_text import to_openmm_Topology as string_pdb_text_to_openmm_Topology

    return string_pdb_text_to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                              check=False)


def to_openmm_System(item, molecular_system, atom_indices='all', structure_indices='all',
                     forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff='1.0 nm', constraints=None,
                     rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                     flexible_constraints=False):
    from molsysmt.item.string_pdb_text import to_openmm_System as string_pdb_text_to_openmm_System

    return string_pdb_text_to_openmm_System(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                            check=False)


def to_openmm_Simulation(item, molecular_system, atom_indices='all', structure_indices='all',
                         forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff=None, constraints=None,
                         rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                         flexible_constraints=False, integrator='Langevin', temperature='300.0 K',
                         collisions_rate='1.0 1/ps', integration_timestep='2.0 fs', platform='CUDA'):
    from molsysmt.item.string_pdb_text import to_openmm_System as string_pdb_text_to_openmm_System

    return string_pdb_text_to_openmm_Simulation(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                                check=False)


def to_openmm_PDBFile(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.string_pdb_text import to_openmm_PDBFile as string_pdb_text_to_openmm_PDBFile

    return string_pdb_text_to_openmm_PDBFile(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                             check=False)


def to_pdbfixer_PDBFixer(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.string_pdb_text import to_pdbfixer_PDBFixer as string_pdb_text_to_pdbfixer_PDBFixer

    return string_pdb_text_to_pdbfixer_PDBFixer(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                                check=False)


def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.string_pdb_text import to_nglview_NGLWidget as string_pdb_text_to_nglview_NGLWidget

    return string_pdb_text_to_nglview_NGLWidget(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                                check=False)


def to_file_pdb(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):
    from molsysmt.item.string_pdb_text import to_file_pdb as string_pdb_text_to_file_pdb

    return string_pdb_text_to_file_pdb(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                       output_filename=output_filename, check=False)

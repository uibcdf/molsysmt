from molsysmt.form.openmm_Simulation.is_openmm_Simulation import is_openmm_Simulation as is_form
from molsysmt.form.openmm_Simulation.extract import extract
from molsysmt.form.openmm_Simulation.add import add
from molsysmt.form.openmm_Simulation.append_structures import append_structures
from molsysmt.form.openmm_Simulation.get import *
from molsysmt.form.openmm_Simulation.set import *
from molsysmt.form.openmm_Simulation.iterators import StructuresIterator, TopologyIterator
from .form_attributes import form_attributes

form_name = 'openmm.Simulation'
form_type = 'class'
form_info = ["", ""]

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
form_attributes['component_id'] = True
form_attributes['component_name'] = True
form_attributes['component_type'] = True
form_attributes['molecule_index'] = True
form_attributes['molecule_id'] = True
form_attributes['molecule_name'] = True
form_attributes['molecule_type'] = True
form_attributes['chain_index'] = True
form_attributes['chain_id'] = True
form_attributes['chain_name'] = True
form_attributes['chain_type'] = True
form_attributes['entity_index'] = True
form_attributes['entity_id'] = True
form_attributes['entity_name'] = True
form_attributes['entity_type'] = True
form_attributes['coordinates'] = True
form_attributes['velocities'] = True
form_attributes['box'] = True
form_attributes['time'] = True
form_attributes['step'] = True
form_attributes['forcefield'] = True
form_attributes['temperature'] = True
form_attributes['pressure'] = True
form_attributes['integrator'] = True
form_attributes['damping'] = True


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_Simulation import to_molsysmt_Topology as openmm_Simulation_to_molsysmt_Topology

    return openmm_Simulation_to_molsysmt_Topology(item, atom_indices=atom_indices)


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_Simulation import to_molsysmt_Structures as openmm_Simulation_to_molsysmt_Structures

    return openmm_Simulation_to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                    structure_indices=structure_indices)


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_Simulation import to_molsysmt_MolSys as openmm_Simulation_to_molsysmt_MolSys

    return openmm_Simulation_to_molsysmt_MolSys(item, atom_indices=atom_indices,
                                                structure_indices=structure_indices)


def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_Simulation import to_openmm_Topology as openmm_Simulation_to_openmm_Topology

    return openmm_Simulation_to_openmm_Topology(item, atom_indices=atom_indices)


def to_openmm_Modeller(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_Simulation import to_openmm_Modeller as openmm_Simulation_to_openmm_Modeller

    return openmm_Simulation_to_openmm_Modeller(item, atom_indices=atom_indices,
                                                structure_indices=structure_indices)


def to_openmm_Context(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_Simulation import to_openmm_Context as openmm_Simulation_to_openmm_Context

    return openmm_Simulation_to_openmm_Context(item, atom_indices=atom_indices,
                                               structure_indices=structure_indices)


def to_pdbfixer_PDBFixer(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_Simulation import to_pdbfixer_PDBFixer as openmm_Simulation_to_pdbfixer_PDBFixer

    return openmm_Simulation_to_pdbfixer_PDBFixer(item, atom_indices=atom_indices,
                                                  structure_indices=structure_indices)


def to_file_pdb(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):
    from molsysmt.form.openmm_Simulation import to_file_pdb as openmm_Simulation_to_file_pdb

    return openmm_Simulation_to_file_pdb(item, atom_indices=atom_indices,
                                         structure_indices=structure_indices, output_filename=output_filename)

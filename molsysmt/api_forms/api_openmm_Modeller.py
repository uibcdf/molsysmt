from molsysmt.item.openmm_Modeller.is_openmm_Modeller import is_openmm_Modeller as is_form
from molsysmt.item.openmm_Modeller.extract import extract
from molsysmt.item.openmm_Modeller.add import add
from molsysmt.item.openmm_Modeller.append_structures import append_structures
from molsysmt.item.openmm_Modeller.get import *
from molsysmt.item.openmm_Modeller.set import *
from .form_attributes import form_attributes

form_name = 'openmm.Modeller'
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
form_attributes['box'] = True


def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.openmm_Modeller import to_mdtraj_Trajectory as openmm_Modeller_to_mdtraj_Trajectory

    return openmm_Modeller_to_mdtraj_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.openmm_Modeller import to_mdtraj_Topology as openmm_Modeller_to_mdtraj_Topology

    return openmm_Modeller_to_mdtraj_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_openmm_System(item, molecular_system, atom_indices='all', structure_indices='all',
                     forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff='1.0 nm', constraints=None,
                     rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                     flexible_constraints=False):
    from molsysmt.item.openmm_Modeller import to_openmm_System as openmm_Modeller_to_openmm_System

    return openmm_Modeller_to_openmm_System(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                            forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff='1.0 nm',
                                            constraints=None,
                                            rigid_water=True, remove_cm_motion=True, hydrogen_mass=None,
                                            switch_distance=None,
                                            flexible_constraints=False)


def to_openmm_Simulation(item, molecular_system, atom_indices='all', structure_indices='all',
                         forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff='1.0 nm', constraints=None,
                         rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                         flexible_constraints=False, integrator='Langevin', temperature='300.0 K',
                         collisions_rate='1.0 1/ps', integration_timestep='2.0 fs', platform='CUDA'):
    from molsysmt.item.openmm_Modeller import to_openmm_Simulation as openmm_Modeller_to_openmm_Simulation

    return openmm_Modeller_to_openmm_Simulation(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                                forcefield=None, non_bonded_method='no_cutoff',
                                                non_bonded_cutoff='1.0 nm', constraints=None,
                                                rigid_water=True, remove_cm_motion=True, hydrogen_mass=None,
                                                switch_distance=None,
                                                flexible_constraints=False, integrator='Langevin',
                                                temperature='300.0 K',
                                                collisions_rate='1.0 1/ps', integration_timestep='2.0 fs',
                                                platform='CUDA')


def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.openmm_Modeller import to_openmm_Topology as openmm_Modeller_to_openmm_Topology

    return openmm_Modeller_to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_pdbfixer_PDBFixer(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.openmm_Modeller import to_pdbfixer_PDBFixer as openmm_Modeller_to_pdbfixer_PDBFixer

    return openmm_Modeller_to_pdbfixer_PDBFixer(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.openmm_Modeller import to_molsysmt_MolSys as openmm_Modeller_to_molsysmt_MolSys

    return openmm_Modeller_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_file_pdb(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):
    from molsysmt.item.openmm_Modeller import to_file_pdb as openmm_Modeller_to_file_pdb

    return openmm_Modeller_to_file_pdb(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                       output_filename=output_filename)


def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.item.openmm_Modeller import to_nglview_NGLWidget as openmm_Modeller_to_nglview_NGLWidget

    return openmm_Modeller_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices)

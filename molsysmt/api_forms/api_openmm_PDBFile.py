from molsysmt.form.openmm_PDBFile.is_openmm_PDBFile import is_openmm_PDBFile as is_form
from molsysmt.form.openmm_PDBFile.extract import extract
from molsysmt.form.openmm_PDBFile.add import add
from molsysmt.form.openmm_PDBFile.append_structures import append_structures
from molsysmt.form.openmm_PDBFile.get import *
from molsysmt.form.openmm_PDBFile.set import *
from .form_attributes import form_attributes

form_name = 'openmm.PDBFile'
form_type = 'class'
form_info = ["", ""]

form_attributes = form_attributes()
form_attributes['atom_index'] = True
form_attributes['atom_id'] = True
form_attributes['atom_name'] = True
form_attributes['atom_type'] = True
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
form_attributes['time'] = True
form_attributes['step'] = True


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_PDBFile import to_molsysmt_Topology as openmm_PDBFile_to_molsysmt_Topology

    return openmm_PDBFile_to_molsysmt_Topology(item, atom_indices=atom_indices)


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_PDBFile import to_molsysmt_Structures as openmm_PDBFile_to_molsysmt_Structures

    return openmm_PDBFile_to_molsysmt_Structures(item, atom_indices=atom_indices)


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_PDBFile import to_molsysmt_MolSys as openmm_PDBFile_to_molsysmt_MolSys

    return openmm_PDBFile_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_PDBFile import to_mdtraj_Trajectory as openmm_PDBFile_to_mdtraj_Trajectory

    return openmm_PDBFile_to_molsysmt_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_PDBFile import to_mdtraj_Topology as openmm_PDBFile_to_mdtraj_Topology

    return openmm_PDBFile_to_mdtraj_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_Topology import to_openmm_Topology as openmm_PDBFile_to_mdtraj_Topology

    return openmm_PDBFile_to_mdtraj_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_PDBFile import to_nglview_NGLWidget as openmm_PDBFile_to_nglview_NGLWidget

    return openmm_PDBFile_to_nglview_NGLWidget(item, atom_indices=atom_indices, structure_indices=structure_indices)

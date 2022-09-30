from molsysmt.form.file_mol2.is_file_mol2 import is_file_mol2 as is_form
from molsysmt.form.file_mol2.extract import extract
from molsysmt.form.file_mol2.add import add
from molsysmt.form.file_mol2.append_structures import append_structures
from molsysmt.form.file_mol2.get import *
from molsysmt.form.file_mol2.set import *
from .form_attributes import form_attributes

form_name = 'file:mol2'
form_type = 'file'
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
    from molsysmt.form.file_mol2 import to_molsysmt_MolSys as file_mol2_to_molsysmt_MolSys

    return file_mol2_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_mol2 import to_molsysmt_Topology as file_mol2_to_molsysmt_Topology

    return file_mol2_to_molsysmt_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_mol2 import to_molsysmt_Structures as file_mol2_to_molsysmt_Structures

    return file_mol2_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_parmed_Structure(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_mol2 import to_parmed_Structure as file_mol2_to_parmed_Structure

    return file_mol2_to_parmed_Structure(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_mol2 import to_mdtraj_Trajectory as file_mol2_to_mdtraj_Trajectory

    return file_mol2_to_mdtraj_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_mol2 import to_mdtraj_Topology as file_mol2_to_mdtraj_Topology

    return file_mol2_to_mdtraj_Topology(item, atom_indices=atom_indices)


def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_mol2 import to_openmm_Topology as file_mol2_to_openmm_Topology

    return file_mol2_to_openmm_Topology(item, atom_indices=atom_indices)


def to_openmm_Modeller(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_mol2 import to_openmm_Modeller as file_mol2_to_openmm_Modeller

    return file_mol2_to_openmm_Modeller(item, atom_indices=atom_indices,
                                        structure_indices=structure_indices)


def to_file_pdb(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):
    from molsysmt.form.file_mol2 import to_file_pdb as file_mol2_to_file_pdb

    return file_mol2_to_file_pdb(item, atom_indices=atom_indices,
                                 structure_indices=structure_indices, output_filename=output_filename)


def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_mol2 import to_nglview_NGLWidget as file_mol2_to_nglview_NGLWidget

    return file_mol2_to_nglview_NGLWidget(item, atom_indices=atom_indices,
                                          structure_indices=structure_indices)

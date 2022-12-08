import numpy as np
from molsysmt.form.pytraj_Trajectory.is_pytraj_Trajectory import is_pytraj_Trajectory as is_form
from molsysmt.form.pytraj_Trajectory.extract import extract
from molsysmt.form.pytraj_Trajectory.add import add
from molsysmt.form.pytraj_Trajectory.append_structures import append_structures
from molsysmt.form.pytraj_Trajectory.get import *
from molsysmt.form.pytraj_Trajectory.set import *
from molsysmt.form.pytraj_Trajectory.iterators import StructuresIterator, TopologyIterator
from .form_attributes import form_attributes

form_name = 'pytraj.Trajectory'
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


def to_pytraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pytraj_Trajectory import to_pytraj_Topology as pytraj_Trajectory_to_pytraj_Topology

    return pytraj_Trajectory_to_pytraj_Topology(item, atom_indices=atom_indices)


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pytraj_Trajectory import to_molsysmt_MolSys as pytraj_Trajectory_to_molsysmt_MolSys

    return pytraj_Trajectory_to_molsysmt_MolSys(item, atom_indices=atom_indices,
                                                structure_indices=structure_indices)


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pytraj_Trajectory import to_molsysmt_Topology as pytraj_Trajectory_to_molsysmt_Topology

    return pytraj_Trajectory_to_molsysmt_Topology(item, atom_indices=atom_indices)


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pytraj_Trajectory import to_molsysmt_Structures as pytraj_Trajectory_to_molsysmt_Structures

    return pytraj_Trajectory_to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                    structure_indices=structure_indices)


def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pytraj_Trajectory import to_nglview_NGLWidget as pytraj_Trajectory_to_nglview_NGLWidget

    return pytraj_Trajectory_to_nglview_NGLWidget(item, atom_indices=atom_indices,
                                                  structure_indices=structure_indices)


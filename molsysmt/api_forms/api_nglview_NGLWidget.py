from molsysmt.form.nglview_NGLWidget.is_nglview_NGLWidget import is_nglview_NGLWidget as is_form
from molsysmt.form.nglview_NGLWidget.extract import extract
from molsysmt.form.nglview_NGLWidget.add import add
from molsysmt.form.nglview_NGLWidget.append_structures import append_structures
from molsysmt.form.nglview_NGLWidget.get import *
from molsysmt.form.nglview_NGLWidget.set import *
from molsysmt.form.nglview_NGLWidget.iterators import StructuresIterator, TopologyIterator
from .form_attributes import form_attributes

form_name = 'nglview.NGLWidget'
form_type = 'class'
form_info = ["NGLView visualization native object", "http://nglviewer.org/nglview/latest/_modules/nglview/widget.html"]

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
form_attributes['entity_index'] = True
form_attributes['entity_id'] = True
form_attributes['entity_name'] = True
form_attributes['entity_type'] = True
form_attributes['coordinates'] = True
form_attributes['box'] = True


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.nglview_NGLWidget import to_molsysmt_Topology as nglview_NGLWidget_to_molsysmt_Topology

    return nglview_NGLWidget_to_molsysmt_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.nglview_NGLWidget import to_molsysmt_Structures as nglview_NGLWidget_to_molsysmt_Structures

    return nglview_NGLWidget_to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                    structure_indices=structure_indices)


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.nglview_NGLWidget import to_molsysmt_MolSys as nglview_NGLWidget_to_molsysmt_MolSys

    return nglview_NGLWidget_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_openmm_Topology(item, molecular_system=None, atom_indices='all', structure_indices='all'):
    from molsysmt.form.nglview_NGLWidget import to_openmm_Topology as nglview_NGLWidget_to_openmm_Topology

    return nglview_NGLWidget_to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_string_pdb_text(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.nglview_NGLWidget import to_string_pdb_text as nglview_NGLWidget_to_string_pdb_text

    return nglview_NGLWidget_to_string_pdb_text(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_string_aminoacids1(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.nglview_NGLWidget import to_string_aminoacids1 as nglview_NGLWidget_to_aminoacids1

    return nglview_NGLWidget_to_aminoacids1(item, atom_indices=atom_indices)


def to_string_aminoacids3(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.nglview_NGLWidget import to_string_aminoacids3 as nglview_NGLWidget_to_aminoacids3

    return nglview_NGLWidget_to_aminoacids3(item, atom_indices=atom_indices)

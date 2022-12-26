from molsysmt.form.file_msmpk.is_file_msmpk import is_file_msmpk as is_form
from molsysmt.form.file_msmpk.extract import extract
from molsysmt.form.file_msmpk.add import add
from molsysmt.form.file_msmpk.append_structures import append_structures
from molsysmt.form.file_msmpk.get import *
from molsysmt.form.file_msmpk.set import *
from molsysmt.form.file_msmpk.iterators import StructuresIterator, TopologyIterator
from .form_attributes import form_attributes

form_name = 'file:msmpk'
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
form_attributes['structure_id'] = True


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_msmpk import to_molsysmt_MolSys as file_msmpk_to_molsysmt_MolSys

    return file_msmpk_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices, digest=False)


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_msmpk import to_molsysmt_Topology as file_msmpk_to_molsysmt_Topology

    return file_msmpk_to_molsysmt_Topology(item, atom_indices=atom_indices, digest=False)


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_msmpk import to_molsysmt_Structures as file_msmpk_to_molsysmt_Structures

    return file_msmpk_to_molsysmt_Structures(item, atom_indices=atom_indices, digest=False)


def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_msmpk import to_nglview_NGLWidget as file_msmpk_to_nglview_NGLWidget

    return file_msmpk_to_nglview_NGLWidget(item, atom_indices=atom_indices,
                                           structure_indices=structure_indices, digest=False)

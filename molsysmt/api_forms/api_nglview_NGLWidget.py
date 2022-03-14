from molsysmt._private_tools.exceptions import *

from molsysmt.tools.nglview_NGLWidget.is_nglview_NGLWidget import is_nglview_NGLWidget as is_form
from molsysmt.tools.nglview_NGLWidget.extract import extract
from molsysmt.tools.nglview_NGLWidget.add import add
from molsysmt.tools.nglview_NGLWidget.merge import merge
from molsysmt.tools.nglview_NGLWidget.append_structures import append_structures
from molsysmt.tools.nglview_NGLWidget.concatenate_structures import concatenate_structures
from molsysmt.tools.nglview_NGLWidget.get import *
from molsysmt.tools.nglview_NGLWidget.set import *

form_name='nglview.NGLWidget'
form_type='class'
form_info=["NGLView visualization native object","http://nglviewer.org/nglview/latest/_modules/nglview/widget.html"]

form_attributes = {

    'atom_index' : True,
    'atom_id' : True,
    'atom_name' : True,
    'atom_type' : True,

    'bond_index' : True,
    'bond_id' : True,
    'bond_name' : True,
    'bond_type' : True,

    'group_index' : True,
    'group_id' : True,
    'group_name' : True,
    'group_type' : True,

    'component_index' : True,
    'component_id' : False,
    'component_name' : False,
    'component_type' : False,

    'molecule_index' : True,
    'molecule_id' : True,
    'molecule_name' : True,
    'molecule_type' : True,

    'chain_index' : True,
    'chain_id' : True,
    'chain_name' : True,
    'chain_type' : True,

    'entity_index' : False,
    'entity_id' : False,
    'entity_name' : False,
    'entity_type' : False,

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

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.nglview_NGLWidget import to_molsysmt_Topology as nglview_NGLWidget_to_molsysmt_Topology

    tmp_item = nglview_NGLWidget_to_molsysmt_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.nglview_NGLWidget import to_molsysmt_Structures as nglview_NGLWidget_to_molsysmt_Structures

    tmp_item = nglview_NGLWidget_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.nglview_NGLWidget import to_molsysmt_Structures as nglview_NGLWidget_to_molsysmt_Structures

    tmp_item = nglview_NGLWidget_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_openmm_Topology(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.nglview_NGLWidget import to_openmm_Topology as nglview_NGLWidget_to_openmm_Topology

    tmp_item = nglview_NGLWidget_to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_string_pdb_text(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.nglview_NGLWidget import to_string_pdb_text as nglview_NGLWidget_to_string_pdb_text

    tmp_item = nglview_NGLWidget_to_string_pdb_text(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_string_aminoacids1(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.nglview_NGLWidget import to_string_aminoacids1 as nglview_NGLWidget_to_aminoacids1

    tmp_item = nglview_NGLWidget_to_aminoacids1(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_string_aminoacids3(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.nglview_NGLWidget import to_string_aminoacids3 as nglview_NGLWidget_to_aminoacids3

    tmp_item = nglview_NGLWidget_to_aminoacids3(item, atom_indices=atom_indices, check=False)

    return tmp_item



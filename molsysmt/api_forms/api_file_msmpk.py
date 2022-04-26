from molsysmt._private.exceptions import *

from molsysmt.form.file_msmpk.is_file_msmpk import is_file_msmpk as is_form
from molsysmt.form.file_msmpk.extract import extract
from molsysmt.form.file_msmpk.add import add
from molsysmt.form.file_msmpk.append_structures import append_structures
from molsysmt.form.file_msmpk.get import *
from molsysmt.form.file_msmpk.set import *

form_name='file:msmpk'
form_type='file'
form_info=["",""]

form_attributes = {

    'atom_index' : True,
    'atom_id' : True,
    'atom_name' : True,
    'atom_type' : True,

    'bond_index' : True,
    'bond_id' : True,
    'bond_name' : True,
    'bond_type' : True,
    'bond_order' : True,

    'group_index' : True,
    'group_id' : True,
    'group_name' : True,
    'group_type' : True,

    'component_index' : True,
    'component_id' : True,
    'component_name' : True,
    'component_type' : True,

    'molecule_index' : True,
    'molecule_id' : True,
    'molecule_name' : True,
    'molecule_type' : True,

    'chain_index' : True,
    'chain_id' : True,
    'chain_name' : True,
    'chain_type' : True,

    'entity_index' : True,
    'entity_id' : True,
    'entity_name' : True,
    'entity_type' : True,

    'coordinates' : True,
    'velocities' : True,
    'box' : True,
    'time' : True,
    'step' : True,

    'forcefield_parameters' : False,

    'forcefield' : False,
    'temperature' : False,
    'pressure' : False,
    'integrator' : False,
    'damping' : False,
}


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_msmpk import to_molsysmt_MolSys as file_msmpk_to_molsysmt_MolSys

    tmp_item = file_msmpk_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_msmpk import to_molsysmt_Topology as file_msmpk_to_molsysmt_Topology

    tmp_item = file_msmpk_to_molsysmt_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_msmpk import to_molsysmt_Structures as file_msmpk_to_molsysmt_Structures

    tmp_item = file_msmpk_to_molsysmt_Structures(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_msmpk import to_nglview_NGLWidget as file_msmpk_to_nglview_NGLWidget

    tmp_item = file_msmpk_to_molsysmt_nglview_NGLWidget(item, atom_indices=atom_indices,
            structure_indices=structure_indices, check=False)

    return tmp_item


from molsysmt._private.exceptions import *

from molsysmt.item.file_xyznpy.is_file_xyznpy import is_file_xyznpy as is_form
from molsysmt.item.file_xyznpy.extract import extract
from molsysmt.item.file_xyznpy.add import add
from molsysmt.item.file_xyznpy.append_structures import append_structures
from molsysmt.item.file_xyznpy.get import *
from molsysmt.item.file_xyznpy.set import *

form_name='file:xyznpy'
form_type='file'
form_info = ["XYZ file format like saved with Numpy",""]


form_attributes = {

    'atom_index' : False,
    'atom_id' : False,
    'atom_name' : False,
    'atom_type' : False,

    'bond_index' : False,
    'bond_id' : False,
    'bond_name' : False,
    'bond_type' : False,
    'bond_order' : False,

    'group_index' : False,
    'group_id' : False,
    'group_name' : False,
    'group_type' : False,

    'component_index' : False,
    'component_id' : False,
    'component_name' : False,
    'component_type' : False,

    'molecule_index' : False,
    'molecule_id' : False,
    'molecule_name' : False,
    'molecule_type' : False,

    'chain_index' : False,
    'chain_id' : False,
    'chain_name' : False,
    'chain_type' : False,

    'entity_index' : False,
    'entity_id' : False,
    'entity_name' : False,
    'entity_type' : False,

    'coordinates' : True,
    'velocities' : False,
    'box' : False,
    'time' : False,
    'step' : False,

    'forcefield' : False,
    'temperature' : False,
    'pressure' : False,
    'integrator' : False,
    'damping' : False,
}


def to_XYZ(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.file_xyznpy import to_XYZ as file_xyznpy_to_XYZ

    tmp_item = XYZ_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item



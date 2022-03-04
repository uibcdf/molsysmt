from molsysmt._private_tools.exceptions import *

from molsysmt.tools.molsysmt_Structures.is_molsysmt_Structures import is_molsysmt_Structures as is_form
from molsysmt.tools.molsysmt_Structures.extract import extract
from molsysmt.tools.molsysmt_Structures.add import add
from molsysmt.tools.molsysmt_Structures.merge import merge
from molsysmt.tools.molsysmt_Structures.append_structures import append_structures
from molsysmt.tools.molsysmt_Structures.concatenate_structures import concatenate_structures
from molsysmt.tools.molsysmt_Structures.get import *
from molsysmt.tools.molsysmt_Structures.set import *

form_name='molsysmt.Structures'
form_type='class'
form_info=["",""]

form_attributes = {

    'atom_index' : False,
    'atom_id' : False,
    'atom_name' : False,
    'atom_type' : False,

    'bond_index' : False,
    'bond_id' : False,
    'bond_name' : False,
    'bond_type' : False,

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
    'box' : True,
    'time' : True,
    'step' : True,

    'forcefield' : False,
    'temperature' : False,
    'pressure' : False,
    'integrator' : False,
    'damping' : False,
}


# Methods

def to_molsysmt_TrajectoryDict(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.molsysmt_Structures import to_molsysmt_TrajectoryDict as molsysmt_Structures_to_molsysmt_TrajectoryDict

    tmp_item = molsysmt_Structures_to_molsysmt_TrajectoryDict(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_XYZ(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.molsysmt_Structures import to_XYZ as molsysmt_Structures_to_XYZ

    tmp_item = molsysmt_Structures_to_XYZ(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item



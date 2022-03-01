from molsysmt._private_tools.exceptions import *

from molsysmt.tools.molsysmt_StructuresCollection.is_molsysmt_StructuresCollection import is_molsysmt_StructuresCollection as is_form
from molsysmt.tools.molsysmt_StructuresCollection.extract import extract
from molsysmt.tools.molsysmt_StructuresCollection.add import add
from molsysmt.tools.molsysmt_StructuresCollection.merge import merge
from molsysmt.tools.molsysmt_StructuresCollection.append_frames import append_frames
from molsysmt.tools.molsysmt_StructuresCollection.concatenate_frames import concatenate_frames
from molsysmt.tools.molsysmt_StructuresCollection.get import *
from molsysmt.tools.molsysmt_StructuresCollection.set import *

form_name='molsysmt.StructuresCollection'
form_type='class'
form_info=["",""]

form_elements = {
    'atoms' : False,
    'bonds' : False,
    'groups' : False,
    'component' : False,
    'molecule' : False,
    'chain' : False,
    'entity' : False,
        }

form_attributes = {

    'atom_id' : False,
    'atom_name' : False,
    'atom_type' : False,

    'bond_id' : False,
    'bond_name' : False,
    'bond_type' : False,

    'group_id' : False,
    'group_name' : False,
    'group_type' : False,

    'component_id' : False,
    'component_name' : False,
    'component_type' : False,

    'molecule_id' : False,
    'molecule_name' : False,
    'molecule_type' : False,

    'chain_id' : False,
    'chain_name' : False,
    'chain_type' : False,

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

    from molsysmt.tools.molsysmt_StructuresCollection import to_molsysmt_TrajectoryDict as molsysmt_StructuresCollection_to_molsysmt_TrajectoryDict

    tmp_item = molsysmt_StructuresCollection_to_molsysmt_TrajectoryDict(item, atom_indices=atom_indices, structure_indices=structure_indices, check_form=False)

    return tmp_item

def to_XYZ(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.molsysmt_StructuresCollection import to_XYZ as molsysmt_StructuresCollection_to_XYZ

    tmp_item = molsysmt_StructuresCollection_to_XYZ(item, atom_indices=atom_indices, structure_indices=structure_indices, check_form=False)

    return tmp_item



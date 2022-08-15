from molsysmt.item.molsysmt_TrajectoryDict.is_molsysmt_TrajectoryDict import is_molsysmt_TrajectoryDict as is_form
from molsysmt.item.molsysmt_TrajectoryDict.extract import extract
from molsysmt.item.molsysmt_TrajectoryDict.add import add
from molsysmt.item.molsysmt_TrajectoryDict.append_structures import append_structures
from molsysmt.item.molsysmt_TrajectoryDict.get import *
from molsysmt.item.molsysmt_TrajectoryDict.set import *

form_name='molsysmt.TrajectoryDict'
form_type='class'
form_info = ["",""]

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
    'box' : True,
    'time' : True,
    'step' : True,

    'forcefield' : False,
    'temperature' : False,
    'pressure' : False,
    'integrator' : False,
    'damping' : False,
}


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.molsysmt_TrajectoryDict import to_molsysmt_Structures as TrajectoryDict_to_molsysmt_Structures

    tmp_item = TrajectoryDict_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

def to_file_trjpk(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.item.molsysmt_TrajectoryDict import to_file_trjpk as TrajectoryDict_to_file_trjpk

    tmp_item = TrajectoryDict_to_file_trjpk(item, atom_indices=atom_indices,
            structure_indices=structure_indices, output_filename=output_filename)

    return tmp_item


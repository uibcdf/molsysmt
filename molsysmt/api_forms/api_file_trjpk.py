from molsysmt.form.file_trjpk.is_file_trjpk import is_file_trjpk as is_form
from molsysmt.form.file_trjpk.extract import extract
from molsysmt.form.file_trjpk.add import add
from molsysmt.form.file_trjpk.append_structures import append_structures
from molsysmt.form.file_trjpk.get import *
from molsysmt.form.file_trjpk.set import *

form_name='file:trjpk'
form_type='file'
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


def to_molsysmt_TrajectoryDict(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_trjpk import to_molsysmt_TrajectoryDict as file_trjpk_to_molsysmt_TrajectoryDict

    tmp_item = file_trjpk_to_molsysmt_TrajectoryDict(item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item


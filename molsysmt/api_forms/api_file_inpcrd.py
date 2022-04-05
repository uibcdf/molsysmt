from molsysmt._private.exceptions import *

from molsysmt.form.file_inpcrd.is_file_inpcrd import is_file_inpcrd as is_form
from molsysmt.form.file_inpcrd.extract import extract
from molsysmt.form.file_inpcrd.add import add
from molsysmt.form.file_inpcrd.merge import merge
from molsysmt.form.file_inpcrd.append_structures import append_structures
from molsysmt.form.file_inpcrd.concatenate_structures import concatenate_structures
from molsysmt.form.file_inpcrd.get import *
from molsysmt.form.file_inpcrd.set import *

form_name='file:inpcrd'
form_type='file'
info = ["AMBER ASCII restart/inpcrd file format","https://ambermd.org/FileFormats.php#trajectory"]

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
    'time' : False,
    'step' : False,

    'forcefield' : False,
    'temperature' : False,
    'pressure' : False,
    'integrator' : False,
    'damping' : False,
}


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_inpcrd import to_molsysmt_Structures as file_inpcrd_to_molsysmt_Structures

    tmp_item = file_inpcrd_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_mdtraj_AmberRestartFile(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_inpcrd import to_mdtraj_AmberRestartFile as file_inpcrd_to_mdtraj_AmberRestartFile

    tmp_item = file_inpcrd_to_mdtraj_AmberRestartFile(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_openmm_AmberInpcrdFile(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_inpcrd import to_openmm_AmberInpcrdFile as file_inpcrd_to_openmm_AmberInpcrdFile

    tmp_item = file_inpcrd_to_openmm_AmberInpcrdFile(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item



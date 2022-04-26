from molsysmt._private.exceptions import *

from molsysmt.form.openmm_GromacsGroFile.is_openmm_GromacsGroFile import is_openmm_GromacsGroFile as is_form
from molsysmt.form.openmm_GromacsGroFile.extract import extract
from molsysmt.form.openmm_GromacsGroFile.add import add
from molsysmt.form.openmm_GromacsGroFile.append_structures import append_structures
from molsysmt.form.openmm_GromacsGroFile.get import *
from molsysmt.form.openmm_GromacsGroFile.set import *

form_name='openmm.GromacsGroFile'
form_type='class'
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

    'component_index' : False,
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

    'forcefield_parameters' : False,

    'forcefield' : False,
    'temperature' : False,
    'pressure' : False,
    'integrator' : False,
    'damping' : False,
}

def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_GromacsGroFile import to_openmm_Topology as openmm_GromacsGroFile_to_openmm_Topology

    tmp_item = openmm_GromacsGroFile_to_openmm_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_openmm_Modeller(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_GromacsGroFile import to_openmm_Modeller as openmm_GromacsGroFile_to_openmm_Modeller

    tmp_item = openmm_GromacsGroFile_to_openmm_Modeller(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_GromacsGroFile import to_molsysmt_MolSys as openmm_GromacsGroFile_to_molsysmt_MolSys

    tmp_item = openmm_GromacsGroFile_to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_GromacsGroFile import to_molsysmt_Topology as openmm_GromacsGroFile_to_molsysmt_Topology

    tmp_item = openmm_GromacsGroFile_to_molsysmt_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.openmm_GromacsGroFile import to_molsysmt_Structures as openmm_GromacsGroFile_to_molsysmt_Structures

    tmp_item = openmm_GromacsGroFile_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item


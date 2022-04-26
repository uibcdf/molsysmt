from molsysmt._private.exceptions import *

from molsysmt.form.openmm_AmberPrmtopFile.is_openmm_AmberPrmtopFile import is_openmm_AmberPrmtopFile as is_form
from molsysmt.form.openmm_AmberPrmtopFile.extract import extract
from molsysmt.form.openmm_AmberPrmtopFile.add import add
from molsysmt.form.openmm_AmberPrmtopFile.append_structures import append_structures
from molsysmt.form.openmm_AmberPrmtopFile.get import *
from molsysmt.form.openmm_AmberPrmtopFile.set import *

form_name='openmm.AmberPrmtopFile'
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

    'coordinates' : False,
    'velocities' : False,
    'box' : True,
    'time' : False,
    'step' : False,

    'forcefield_parameters' : True,

    'forcefield' : False,
    'temperature' : False,
    'pressure' : False,
    'integrator' : False,
    'damping' : False,
}


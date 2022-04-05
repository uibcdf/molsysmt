from molsysmt._private.exceptions import *

from molsysmt.form.openmm_AmberInpcrdFile.is_file_inpcrd import is_file_inpcrd as is_form
from molsysmt.form.openmm_AmberInpcrdFile.extract import extract
from molsysmt.form.openmm_AmberInpcrdFile.add import add
from molsysmt.form.openmm_AmberInpcrdFile.merge import merge
from molsysmt.form.openmm_AmberInpcrdFile.append_structures import append_structures
from molsysmt.form.openmm_AmberInpcrdFile.concatenate_structures import concatenate_structures
from molsysmt.form.openmm_AmberInpcrdFile.get import *
from molsysmt.form.openmm_AmberInpcrdFile.set import *

form_name='openmm.AmberInpcrdFile'
form_type='class'
info = []

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


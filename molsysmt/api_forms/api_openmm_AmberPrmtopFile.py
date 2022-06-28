from molsysmt._private.exceptions import *
from molsysmt.item.openmm_AmberPrmtopFile.is_openmm_AmberPrmtopFile import is_openmm_AmberPrmtopFile as is_form
from molsysmt.item.openmm_AmberPrmtopFile.extract import extract
from molsysmt.item.openmm_AmberPrmtopFile.add import add
from molsysmt.item.openmm_AmberPrmtopFile.append_structures import append_structures
from molsysmt.item.openmm_AmberPrmtopFile.get import *
from molsysmt.item.openmm_AmberPrmtopFile.set import *
from .form_attributes import form_attributes

form_name = 'openmm.AmberPrmtopFile'
form_type = 'class'
form_info = ["", ""]

form_attributes = form_attributes()
form_attributes['atom_index'] = True
form_attributes['atom_id'] = True
form_attributes['atom_name'] = True
form_attributes['atom_type'] = True
form_attributes['bond_index'] = True
form_attributes['bond_id'] = True
form_attributes['bond_name'] = True
form_attributes['bond_type'] = True
form_attributes['bond_order'] = True
form_attributes['group_index'] = True
form_attributes['group_id'] = True
form_attributes['group_name'] = True
form_attributes['group_type'] = True
form_attributes['component_index'] = True
form_attributes['molecule_index'] = True
form_attributes['molecule_id'] = True
form_attributes['molecule_name'] = True
form_attributes['molecule_type'] = True
form_attributes['chain_index'] = True
form_attributes['chain_id'] = True
form_attributes['chain_name'] = True
form_attributes['chain_type'] = True
form_attributes['box'] = True
form_attributes['forcefield_parameters'] = True

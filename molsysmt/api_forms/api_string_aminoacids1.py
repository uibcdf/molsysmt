from molsysmt._private_tools.exceptions import *

from molsysmt.tools.string_aminoacids1.is_string_aminoacids1 import is_string_aminoacids1 as is_form
from molsysmt.tools.string_aminoacids1.extract import extract
from molsysmt.tools.string_aminoacids1.add import add
from molsysmt.tools.string_aminoacids1.merge import merge
from molsysmt.tools.string_aminoacids1.append_structures import append_structures
from molsysmt.tools.string_aminoacids1.concatenate_structures import concatenate_structures
from molsysmt.tools.string_aminoacids1.get import *
from molsysmt.tools.string_aminoacids1.set import *

form_name='string:aminoacids1'
form_type='string'
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

    'group_index' : True,
    'group_id' : False,
    'group_name' : True,
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

    'coordinates' : False,
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


### Corresponde al formato IUPAC extended protein que aparece en Biopython

def to_string_aminoacids3(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.string_aminoacids1 import to_string_aminoacids3 as string_aminoacids1_to_string_aminoacids3

    tmp_item = string_aminoacids1_to_string_aminoacids3(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_biopython_Seq(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.string_aminoacids1 import to_biopython_Seq as string_aminoacids1_to_biopython_Seq

    tmp_item = string_aminoacids1_to_biopython_Seq(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_biopython_SeqRecord(item, molecular_system=None, atom_indices='all', structure_indices='all', id=None, name=None, description=None):

    from molsysmt.tools.string_aminoacids1 import to_biopython_SeqRecord as string_aminoacids1_to_biopython_SeqRecord

    tmp_item = string_aminoacids1_to_biopython_SeqRecord(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item



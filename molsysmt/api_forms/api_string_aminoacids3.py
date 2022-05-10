from molsysmt._private.exceptions import *

from molsysmt.item.string_aminoacids3.is_string_aminoacids3 import is_string_aminoacids3 as is_form
from molsysmt.item.string_aminoacids3.extract import extract
from molsysmt.item.string_aminoacids3.add import add
from molsysmt.item.string_aminoacids3.append_structures import append_structures
from molsysmt.item.string_aminoacids3.get import *
from molsysmt.item.string_aminoacids3.set import *

form_name='string:aminoacids3'
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
    'bond_order' : False,

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

def to_string_aminoacids1(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.item.string_aminoacids3 import to_string_aminoacids1 as string_aminoacids3_to_string_aminoacids1

    tmp_item = string_aminoacids3_to_string_aminoacids1(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_biopython_Seq(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.string_aminoacids3 import to_biopython_Seq as string_aminoacids3_to_biopython_Seq

    tmp_item = string_aminoacids3_to_biopython_Seq(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_biopython_SeqRecord(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.item.string_aminoacids3 import to_biopython_SeqRecord as string_aminoacids3_to_biopython_SeqRecord

    tmp_item = string_aminoacids3_to_biopython_SeqRecord(item, atom_indices=atom_indices, check=False)

    return tmp_item



from molsysmt._private.exceptions import *

from molsysmt.form.biopython_Seq.is_biopython_Seq import is_biopython_Seq as is_form
from molsysmt.form.biopython_Seq.extract import extract
from molsysmt.form.biopython_Seq.add import add
from molsysmt.form.biopython_Seq.merge import merge
from molsysmt.form.biopython_Seq.append_structures import append_structures
from molsysmt.form.biopython_Seq.concatenate_structures import concatenate_structures
from molsysmt.form.biopython_Seq.get import *
from molsysmt.form.biopython_Seq.set import *

form_name='biopython.Seq'
form_type='class'
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


def to_biopython_SeqRecord(item, molecular_system, atom_indices='all', structure_indices='all',
                           id=None, name=None, description=None):

    from molsysmt.form.biopython_Seq import to_biopython_SeqRecord as biopython_Seq_to_biopython_SeqRecord

    tmp_item = biopython_Seq_to_biopython_SeqRecord(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_file_fasta(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.form.biopython_Seq import to_file_fasta as biopython_Seq_to_file_fasta

    tmp_item = biopython_Seq_to_file_fasta(item, atom_indices=atom_indices,
                                           structure_indices=structure_indices,
                                           output_filename=output_filename, check=False)

    return tmp_item


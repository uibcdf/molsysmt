from molsysmt.item.biopython_Seq.is_biopython_Seq import is_biopython_Seq as is_form
from molsysmt.item.biopython_Seq.extract import extract
from molsysmt.item.biopython_Seq.add import add
from molsysmt.item.biopython_Seq.append_structures import append_structures
from molsysmt.item.biopython_Seq.get import *
from molsysmt.item.biopython_Seq.set import *
from .form_attributes import form_attributes

form_name = 'biopython.Seq'
form_type = 'class'
form_info = ["", ""]

form_attributes = form_attributes()
form_attributes['group_index'] = True
form_attributes['group_name'] = True


def to_biopython_SeqRecord(item, molecular_system, atom_indices='all', structure_indices='all',
                           id=None, name=None, description=None):

    from molsysmt.item.biopython_Seq import to_biopython_SeqRecord as biopython_Seq_to_biopython_SeqRecord

    return biopython_Seq_to_biopython_SeqRecord(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_file_fasta(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.item.biopython_Seq import to_file_fasta as biopython_Seq_to_file_fasta

    return biopython_Seq_to_file_fasta(item, atom_indices=atom_indices,
                                           structure_indices=structure_indices,
                                           output_filename=output_filename)

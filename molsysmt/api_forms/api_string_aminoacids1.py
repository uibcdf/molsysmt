from molsysmt.form.string_aminoacids1.is_string_aminoacids1 import is_string_aminoacids1 as is_form
from molsysmt.form.string_aminoacids1.extract import extract
from molsysmt.form.string_aminoacids1.add import add
from molsysmt.form.string_aminoacids1.append_structures import append_structures
from molsysmt.form.string_aminoacids1.get import *
from molsysmt.form.string_aminoacids1.set import *
from molsysmt.form.string_aminoacids1.iterators import StructuresIterator, TopologyIterator
from .form_attributes import form_attributes

form_name = 'string:aminoacids1'
form_type = 'string'
form_info = ["", ""]

form_attributes = form_attributes()
form_attributes['group_index'] = True
form_attributes['group_name'] = True


# Corresponde al formato IUPAC extended protein que aparece en Biopython
def to_string_aminoacids3(item, molecular_system=None, atom_indices='all', structure_indices='all'):
    from molsysmt.form.string_aminoacids1 import to_string_aminoacids3 as string_aminoacids1_to_string_aminoacids3

    return string_aminoacids1_to_string_aminoacids3(item)


def to_biopython_Seq(item, molecular_system=None, atom_indices='all', structure_indices='all'):
    from molsysmt.form.string_aminoacids1 import to_biopython_Seq as string_aminoacids1_to_biopython_Seq

    return string_aminoacids1_to_biopython_Seq(item)


def to_biopython_SeqRecord(item, molecular_system=None, atom_indices='all', structure_indices='all', id=None, name=None,
                           description=None):
    from molsysmt.form.string_aminoacids1 import to_biopython_SeqRecord as string_aminoacids1_to_biopython_SeqRecord

    return string_aminoacids1_to_biopython_SeqRecord(item)

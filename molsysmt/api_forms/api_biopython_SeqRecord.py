from molsysmt.form.biopython_SeqRecord.is_biopython_SeqRecord import is_biopython_SeqRecord as is_form
from molsysmt.form.biopython_SeqRecord.extract import extract
from molsysmt.form.biopython_SeqRecord.add import add
from molsysmt.form.biopython_SeqRecord.append_structures import append_structures
from molsysmt.form.biopython_SeqRecord.get import *
from molsysmt.form.biopython_SeqRecord.set import *
from .form_attributes import form_attributes

form_name = 'biopython.SeqRecord'
form_type = 'class'
form_info = ["", ""]

form_attributes = form_attributes()
form_attributes['group_index'] = True
form_attributes['group_name'] = True



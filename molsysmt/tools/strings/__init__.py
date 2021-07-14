from .is_string_pdb import is_string_pdb
from .is_string_pdbid import is_string_pdbid
from .is_string_aminoacids3 import is_string_aminoacids3
from .is_string_aminoacids1 import is_string_aminoacids1

def guess_form_from_string(string):

    output = None

    if is_string_pdb(string):
        output = 'string:pdb'
    elif is_string_pdbid(string):
        output = 'string:pdbid'
    elif is_string_aminoacids3(string):
        output = 'string:aminoacids3'
    elif is_string_aminoacids1(string):
        output = 'string:aminoacids1'

    return output


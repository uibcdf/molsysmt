def guess_form_from_string(string):

    from molsysmt.tools.string.pdb import string_is_pdb
    from molsysmt.tools.string.pdbid import string_is_pdbid
    from molsysmt.tools.string.aminoacids3 import string_is_aminoacids3
    from molsysmt.tools.string.aminoacids1 import string_is_aminoacids1

    output = None

    if string_is_pdb(string):
        output = 'string:pdb'
    elif string_is_pdbid(string):
        output = 'string:pdbid'
    elif string_is_aminoacids3(string):
        output = 'string:aminoacids3'
    elif string_is_aminoacids1(string):
        output = 'string:aminoacids1'

    return output



def is_form(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'molsysmt.native.pdb_file_handler.PDBFileHandler')

    return output


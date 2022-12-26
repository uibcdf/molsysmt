from molsysmt._private.digestion import digest

@digest(form='string:pdb_id')
def to_string_pdb_text(item, atom_indices='all', structure_indices='all', digest=True):

    from . import to_file_pdb
    from ..string_pdb_text import extract as extract_string_pdb_text
    from os import remove

    tmp_item = to_file_pdb(item)

    tmp_file = tmp_item
    fff = open(tmp_item, 'r')
    tmp_item = fff.read()
    fff.close()
    remove(tmp_file)

    tmp_item = extract_string_pdb_text(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
            copy_if_all=False, digest=False)

    return tmp_item


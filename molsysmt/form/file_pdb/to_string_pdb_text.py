from molsysmt._private.digestion import digest

@digest(form='file:pdb')
def to_string_pdb_text(item, atom_indices='all', structure_indices='all'):

    from ..string_pdb_text import extract as extract_string_pdb_text

    fff = open(item, 'r')
    tmp_item = fff.read()
    fff.close()

    tmp_item = extract_string_pdb_text(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, copy_if_all=False)

    return tmp_item

def _to_string_pdb_text(item, atom_indices='all', structure_indices='all'):

    return to_string_pdb_text(item, atom_indices=atom_indices, structure_indices=structure_indices)


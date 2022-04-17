from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def to_string_pdb_text(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        digest_item(item, 'file:pdb')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from ..string_pdb_text import extract as extract_string_pdb_text

    fff = open(item, 'r')
    tmp_item = fff.read()
    fff.close()

    tmp_item = extract_string_pdb_text(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, copy_if_all=False, check=False)

    return tmp_item


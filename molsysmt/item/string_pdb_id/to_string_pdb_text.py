from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def to_string_pdb_text(item, atom_indices='all', structure_indices='all'):

    if check:

        digest_item(item, 'string:pdb_id')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from ..file_pdb import download as download_file_pdb
    from ..string_pdb_text import extract as extract_string_pdb_text
    from os import remove

    tmp_item = download_file_pdb(item.replace('pdb_id:', ''), output_filename)

    tmp_file = tmp_item
    fff = open(tmp_item, 'r')
    tmp_item = fff.read()
    fff.close()
    remove(tmp_file)

    tmp_item = extract_string_pdb_text(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
            copy_if_all=False)

    return tmp_item


from molsysmt._private.digestion import digest

@digest(form='string:pdb_text')
def to_file_pdb(item, atom_indices='all', structure_indices='all', output_filename=None,
        digest=True):

    from . import extract
    from molsysmt._private.files_and_directories import temp_filename

    if output_filename is None:
        output_filename = temp_filename(extension='pdb')

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices,
            copy_if_all=False, digest=False)

    with open(output_filename, 'w') as fff:
        fff.write(tmp_item)

    tmp_item = output_filename

    return tmp_item


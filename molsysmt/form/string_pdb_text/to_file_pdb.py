from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:pdb_text')
def to_file_pdb(item, atom_indices='all', structure_indices='all', output_filename=None, 
        skip_digestion=False):
    """
    Converting from string:pdb_text to file.pdb.

    Parameters
    ----------
    item : string:pdb_text
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file.pdb
        Converted molecular system representation.
    """

    from . import extract
    from molsysmt._private.files_and_directories import temp_filename

    if output_filename is None:
        output_filename = temp_filename(extension='pdb')

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices,
            copy_if_all=False, skip_digestion=True)

    with open(output_filename, 'w') as fff:
        fff.write(tmp_item)

    tmp_item = output_filename

    return tmp_item


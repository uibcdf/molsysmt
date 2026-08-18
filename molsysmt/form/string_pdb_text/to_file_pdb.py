from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:pdb_text')
def to_file_pdb(item, atom_indices='all', structure_indices='all', output_filename=None, 
        skip_digestion=False):
    """
    Converting from string:pdb_text to file:pdb.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    output_filename : str or pathlib.Path, default=None
        Output file path for serialization.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:pdb
        Resulting object in file:pdb form.


    .. versionadded:: 1.0.0
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


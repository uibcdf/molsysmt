from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:pdb_id')
def to_file_bcif_gz(item, atom_indices='all', structure_indices='all', output_filename=None, skip_digestion=False):
    """
    Converting from string:pdb_id to file:bcif_gz.

    Parameters
    ----------
    item : string:pdb_id
        Source item in string:pdb_id form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    output_filename : str or pathlib.Path
        Output file path for serialization.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:bcif_gz
        Resulting object in file:bcif_gz form.

    .. versionadded:: 1.0.0
    """

    from ..file_bcif_gz import download
    from ..file_bcif_gz.extract import extract

    tmp_item = download(item, output_filename=output_filename)
    tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
            output_filename=tmp_item, copy_if_all=False, skip_digestion=True)

    return tmp_item

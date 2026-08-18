from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:pdb_id')
def to_file_bcif(item, atom_indices='all', structure_indices='all', output_filename=None, skip_digestion=False):
    """
    Converting from string:pdb_id to file:bcif.

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
    file:bcif
        Resulting object in file:bcif form.

    .. versionadded:: 1.0.0
    """

    from ..file_bcif import download
    from ..file_bcif.extract import extract

    from molsysmt.form.string_pdb_id import _extract_pdb_id
    tmp_item = download(_extract_pdb_id(item), output_filename)
    tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
            output_filename=tmp_item, copy_if_all=False, skip_digestion=True)

    return tmp_item

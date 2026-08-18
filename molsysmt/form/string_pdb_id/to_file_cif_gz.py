from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:pdb_id')
def to_file_cif_gz(item, atom_indices='all', structure_indices='all', output_filename=None, skip_digestion=False):
    """
    Converting from string:pdb_id to file:cif_gz.


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
    file:cif_gz
        Resulting object in file:cif_gz form.


    .. versionadded:: 1.0.0
    """

    from ..file_cif_gz import download
    from ..file_cif_gz.extract import extract

    from molsysmt.form.string_pdb_id import _extract_pdb_id
    tmp_item = download(_extract_pdb_id(item), output_filename)
    tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
            output_filename=tmp_item, copy_if_all=False, skip_digestion=True)

    return tmp_item

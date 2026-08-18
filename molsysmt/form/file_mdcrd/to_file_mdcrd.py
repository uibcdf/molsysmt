from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:mdcrd')
def to_file_mdcrd(item, atom_indices='all', structure_indices='all', output_filename=None, skip_digestion=False):
    """
    Converting from file:mdcrd to file:mdcrd.

    Parameters
    ----------
    item : file:mdcrd
        Source item in file:mdcrd form.
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
    file:mdcrd
        Resulting object in file:mdcrd form.

    .. versionadded:: 1.0.0
    """

    from .extract import extract

    return extract(item, atom_indices=atom_indices, structure_indices=structure_indices,
                   output_filename=output_filename, skip_digestion=True)

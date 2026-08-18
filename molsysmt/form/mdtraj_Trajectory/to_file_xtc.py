from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.Trajectory')
def to_file_xtc(item, atom_indices='all', structure_indices='all', output_filename=None, skip_digestion=False):
    """
    Converting from mdtraj.Trajectory to file:xtc.

    Parameters
    ----------
    item : mdtraj.Trajectory
        Source item in mdtraj.Trajectory form.
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
    file:xtc
        Resulting object in file:xtc form.

    .. versionadded:: 1.0.0
    """

    from . import extract

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices,
            copy_if_all=False, skip_digestion=True)

    tmp_item.save_xtc(output_filename)
    tmp_item = output_filename

    return tmp_item


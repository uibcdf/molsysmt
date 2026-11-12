from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:h5")
def to_file_h5(
    item,
    atom_indices="all",
    structure_indices="all",
    output_name=None,
    copy_if_all=True,
    skip_digestion=False,
    *,
    output_filename=None,
):
    """
    Converting from file:h5 to file:h5.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    output_name : str or pathlib.Path, default=None
        Legacy destination alias. Prefer output_filename; do not provide both.
    output_filename : str or pathlib.Path, default=None
        Canonical destination. Whole-file requests can create an independent
        temporary copy; selected HDF5 serialization requires a distinct path.
    copy_if_all : object, default=True
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:h5
        Resulting object in file:h5 form.


    Raises
    ------
    ArgumentConflictError
        If both destination spellings are supplied.


    .. versionadded:: 1.0.0
    """

    from molsysmt._private.files_and_directories import resolve_output_filename

    output_filename = resolve_output_filename(
        output_filename, output_name, caller="molsysmt.form.file_h5.to_file_h5"
    )

    from .extract import extract

    return extract(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        output_filename=output_filename,
        copy_if_all=copy_if_all,
        skip_digestion=True,
    )

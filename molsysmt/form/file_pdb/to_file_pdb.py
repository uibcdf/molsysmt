from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:pdb")
def to_file_pdb(
    item,
    atom_indices="all",
    structure_indices="all",
    output_filename=None,
    copy_if_all=True,
    skip_digestion=False,
    *,
    output_name=None,
):
    """
    Converting from file:pdb to file:pdb.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    output_filename : str or pathlib.Path, default=None
        Destination PDB path, required when making a copy.
    copy_if_all : object, default=True
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    output_name : str or pathlib.Path, default=None
        Legacy alias for output_filename. Supply only one destination argument.

    Returns
    -------
    file:pdb
        Resulting object in file:pdb form.


    Examples
    --------
    >>> import molsysmt as msm
    >>> from pathlib import Path
    >>> from tempfile import TemporaryDirectory
    >>> source = msm.systems["T4 lysozyme L99A"]["181l.pdb"]
    >>> with TemporaryDirectory() as directory:
    ...     output = to_file_pdb(source, output_filename=f"{directory}/copy.pdb")
    ...     assert Path(output).read_bytes() == Path(source).read_bytes()

    .. versionadded:: 1.0.0
    """

    from .extract import extract

    if output_name is not None:
        if output_filename is not None:
            from molsysmt._private.smonitor import ArgumentError

            raise ArgumentError(
                "output_name",
                value=output_name,
                message="Supply only output_filename or its output_name alias.",
            )
        output_filename = output_name

    return extract(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        output_filename=output_filename,
        copy_if_all=copy_if_all,
        skip_digestion=True,
    )

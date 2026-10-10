from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:trjpk")
def to_file_trjpk(
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
    Converting from file:trjpk to file:trjpk.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    output_name : object, default=None
        Legacy output filename alias. Prefer output_filename.
    copy_if_all : bool, default=True
        Retained for adapter compatibility. A distinct destination always
        copies the file; no destination retains the source path.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    output_filename : str or pathlib.Path, default=None
        Destination file path accepted by the public conversion dispatcher.
        Omit both output arguments to retain the source file.

    Returns
    -------
    file:trjpk
        Resulting object in file:trjpk form.


    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.systems['two LJ particles']['traj_two_lj_particles.trjpk']
    >>> to_file_trjpk(molsys, copy_if_all=False) == molsys
    True

    .. versionadded:: 1.0.0
    """

    from .extract import extract

    if output_filename is not None and output_name is not None:
        raise ValueError("Provide output_filename or output_name, not both.")
    if output_filename is None:
        output_filename = output_name

    return extract(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        output_filename=output_filename,
        copy_if_all=copy_if_all,
        skip_digestion=skip_digestion,
    )

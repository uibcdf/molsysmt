from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:xtc")
def extract(
    item,
    atom_indices="all",
    structure_indices="all",
    output_filename=None,
    copy_if_all=True,
    skip_digestion=False,
):
    """
    Copying a complete file:xtc while refusing unsupported file subsets.


    Parameters
    ----------
    item : molecular system
        Source coordinate file; its bytes are never modified.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    output_filename : str or pathlib.Path, default=None
        None creates a session-owned temporary for whole-file copying. An
        explicit destination must differ from the source.
    copy_if_all : bool, default=True
        False returns the source for all atoms/structures when no output is given.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:xtc
        Resulting object in file:xtc form.


    Raises
    ------
    ArgumentError
        If an explicit destination aliases the source or names a directory.
    NotImplementedMethodError
        If a subset is requested. Convert it to native structures or H5MSM instead.

    Examples
    --------
    >>> import filecmp
    >>> from pathlib import Path
    >>> from tempfile import TemporaryDirectory
    >>> import molsysmt as msm
    >>> source = msm.systems['nglview']['md_1u19.xtc']
    >>> with TemporaryDirectory() as folder:
    ...     target = extract(source, output_filename=Path(folder) / 'snapshot.xtc')
    ...     assert filecmp.cmp(source, target, shallow=False)

    .. admonition:: User guide

       See :ref:`Cookbook_Copying_Disk_Systems` for ownership and selected H5MSM output.

    .. versionadded:: 1.0.0
    """

    from .to_file_xtc import to_file_xtc

    return to_file_xtc(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        output_filename=output_filename,
        copy_if_all=copy_if_all,
        skip_digestion=True,
    )

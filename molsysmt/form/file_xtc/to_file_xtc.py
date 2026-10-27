from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:xtc")
def to_file_xtc(
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
    Converting from file:xtc to file:xtc.


    Parameters
    ----------
    item : molecular system
        Source coordinate file; its bytes are never modified.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    output_name : str or pathlib.Path, default=None
        Legacy destination alias; prefer output_filename. Do not supply both.
    output_filename : str or pathlib.Path, default=None
        None creates a session-owned temporary copy. An explicit destination
        is caller-owned and must differ from the source.
    copy_if_all : bool, default=True
        False returns the source only when both selections are all and no
        destination is given. An explicit destination always creates a copy.
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
        If an atom or structure subset is requested for file serialization.

    Notes
    -----
    Whole-file copies preserve every original byte and do not require MDTraj.
    Atom and structure selections are supported when converting to native
    structures or H5MSM; this file identity route supports whole-file copying.

    Examples
    --------
    >>> import filecmp
    >>> from pathlib import Path
    >>> from tempfile import TemporaryDirectory
    >>> import molsysmt as msm
    >>> source = msm.systems['nglview']['md_1u19.xtc']
    >>> with TemporaryDirectory() as folder:
    ...     target = to_file_xtc(source, output_filename=Path(folder) / 'snapshot.xtc')
    ...     assert filecmp.cmp(source, target, shallow=False)

    .. admonition:: User guide

       See :ref:`Cookbook_Copying_Disk_Systems` for ownership and selected H5MSM output.

    .. versionadded:: 1.0.0
    """

    from molsysmt._private.variables import is_all

    if output_name is not None:
        if output_filename is not None:
            from molsysmt._private.smonitor import ArgumentConflictError

            raise ArgumentConflictError(
                arg1="output_name",
                arg2="output_filename",
                reason="Provide only one destination; output_filename is preferred.",
                caller="molsysmt.form.file_xtc.to_file_xtc",
            )
        output_filename = output_name

    if is_all(atom_indices) and is_all(structure_indices):
        if output_filename is None and not copy_if_all:
            return item
        from .copy import copy

        return copy(item, output_filename=output_filename, skip_digestion=True)

    from molsysmt._private.smonitor import NotImplementedMethodError

    raise NotImplementedMethodError(
        caller="molsysmt.form.file_xtc.to_file_xtc",
        message="Subset file serialization is unsupported; convert the selection to molsysmt.Structures or H5MSM instead.",
    )

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:pdbqt")
def copy(item, output_filename=None, skip_digestion=False):
    """Copying a validated PDBQT source.

    Parameters
    ----------
    item : str or pathlib.Path
        PDBQT path containing one supported rigid receptor or ligand.
    output_filename : str or pathlib.Path, default=None
        None creates a private session-owned temporary. An explicit destination
        is caller-owned and must differ from the source.
    skip_digestion : bool, default=False
        Whether to skip argument digestion. Default is False.

    Returns
    -------
    str or pathlib.Path
        Validated copied contents, preserving the original payload.

    Raises
    ------
    ArgumentError
        If an explicit output_filename aliases the source or names a directory.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.files_and_directories import file_copy_destination

    from .to_file_pdbqt import to_file_pdbqt

    with file_copy_destination(
        item, output_filename, caller="molsysmt.form.file_pdbqt.copy"
    ) as destination:
        return to_file_pdbqt(item, output_filename=destination)

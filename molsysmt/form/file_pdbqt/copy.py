from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:pdbqt")
def copy(item, output_filename=None, skip_digestion=False):
    """Copying a validated PDBQT source.

    Parameters
    ----------
    item : str or pathlib.Path
        PDBQT path containing one supported rigid receptor or ligand.
    output_filename : str or pathlib.Path, default=None
        Destination path, required to copy a file.
    skip_digestion : bool, default=False
        Whether to skip argument digestion. Default is False.

    Returns
    -------
    str or pathlib.Path
        Validated copied contents, preserving the original payload.

    .. versionadded:: 1.0.0
    """
    from .to_file_pdbqt import to_file_pdbqt

    return to_file_pdbqt(item, output_filename=output_filename)

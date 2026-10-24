from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:sdf")
def copy(item, output_filename=None, skip_digestion=False):
    """Copying a single SDF record without changing its source bytes.

    Parameters
    ----------
    item : str or pathlib.Path
        Single-record SDF source file.
    output_filename : str or pathlib.Path, default=None
        None creates a private session-owned temporary. An explicit destination
        is caller-owned and must differ from the source.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    str or pathlib.Path
        Destination path, preserving source property blocks and syntax.

    Raises
    ------
    ArgumentError
        If an explicit output_filename aliases the source or names a directory.

    Notes
    -----
    Only the single-record envelope is checked. The source chemistry may be
    outside the native parser profile; copying does not certify chemical validity.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.files_and_directories import file_copy_destination

    from .to_file_sdf import to_file_sdf

    with file_copy_destination(
        item, output_filename, caller="molsysmt.form.file_sdf.copy"
    ) as destination:
        return to_file_sdf(item, output_filename=destination, skip_digestion=True)

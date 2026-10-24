from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:crd")
def copy(item, output_filename=None, progress_bar=False, skip_digestion=False):
    """
    Creating a copy of an item of form file:crd.


    Parameters
    ----------
    item : molecular system
        Argument item.
    output_filename : str or pathlib.Path, default=None
        None creates a private session-owned temporary. An explicit destination
        must differ from the source; existing distinct files may be overwritten.
    progress_bar : object, default=False
        Argument progress_bar.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:crd
        Resulting object in file:crd form.


    Raises
    ------
    ArgumentError
        If an explicit output_filename aliases the source or names a directory.

    .. versionadded:: 1.0.0
    """

    from molsysmt._private.files_and_directories import copy_file

    return copy_file(item, output_filename, caller="molsysmt.form.file_crd.copy")

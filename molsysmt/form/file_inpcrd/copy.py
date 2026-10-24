from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:inpcrd")
def copy(item, output_filename=None, skip_digestion=False):
    """
    Creating a copy of an item of form file:inpcrd.


    Parameters
    ----------
    item : molecular system
        Argument item.
    output_filename : str or pathlib.Path, default=None
        None creates a private session-owned temporary. An explicit destination
        must differ from the source; existing distinct files may be overwritten.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:inpcrd
        Resulting object in file:inpcrd form.


    Raises
    ------
    ArgumentError
        If an explicit output_filename aliases the source or names a directory.

    .. versionadded:: 1.0.0
    """

    from molsysmt._private.files_and_directories import copy_file

    return copy_file(item, output_filename, caller="molsysmt.form.file_inpcrd.copy")
